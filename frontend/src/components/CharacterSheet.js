import { useEffect, useState, useCallback, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Responsive, WidthProvider } from "react-grid-layout/legacy";

import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "../styles/CharacterSheet.css";

const ResponsiveGridLayout = WidthProvider(Responsive);

// Helper functions and constants
const calculateModifier = (score) => {
    return Math.floor((score - 10) / 2);
};

const proficiencyBonus = (level) => {
    if (level >= 17) return 6;
    if (level >= 13) return 5;
    if (level >= 9) return 4;
    if (level >= 5) return 3;
    return 2;
};

const XP_THRESHOLDS = {
    1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
    6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
    11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
    16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
};

// --- Helper Utilities ---

/**
 * Resolves a scaling value (like Rage Damage or Uses) based on character level.
 * Handles range strings like "1-8", "9-15", or "16-20".
 */
const resolveScalingValue = (scalingData, level) => {
    if (typeof scalingData !== 'object' || scalingData === null) return scalingData;

    for (const [range, value] of Object.entries(scalingData)) {
        // Handle "1-8" or single numbers
        const parts = range.split('-');
        if (parts.length === 2) {
            const min = parseInt(parts[0]);
            const max = parseInt(parts[1]);
            if (level >= min && level <= max) return value;
        } else if (parseInt(range) === level) {
            return value;
        }

        // Handle "17+" style (though usually it's "17-20" in this data)
        if (range.endsWith('+')) {
            const min = parseInt(range);
            if (level >= min) return value;
        }
    }
    return null; // Fallback if no range match
};

/**
 * Simple processor to handle **bold** or *bold* text in descriptions.
 * Returns an array of React elements/strings.
 */
const processRichText = (text) => {
    if (!text) return text;
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);
    return parts.map((part, i) => {
        if ((part.startsWith('**') && part.endsWith('**')) || (part.startsWith('*') && part.endsWith('*'))) {
            const clean = part.replace(/^\*\*?|\*\*?$/g, '');
            return <strong key={i}>{clean}</strong>;
        }
        return part;
    });
};


/**
 * Calculates attack statistics for a weapon or unarmed strike.
 */
const calculateAttack = (name, abilities, profBonus, features = [], level = 1, weaponRules = {}) => {
    const data = weaponRules[name] || { damage: "???", type: "Unknown", properties: [], reach: "5ft" };
    const strMod = calculateModifier(abilities.strength || 10);
    const dexMod = calculateModifier(abilities.dexterity || 10);

    let toHitMod = strMod;
    let damageMod = strMod;
    let reach = data.reach || data.range || "5ft";

    const isFinesse = data.properties.includes("Finesse");
    const isRanged = data.properties.includes("Ammunition") || data.properties.includes("Range");

    if (isRanged) {
        toHitMod = dexMod;
        damageMod = dexMod;
    } else if (isFinesse) {
        if (dexMod > strMod) {
            toHitMod = dexMod;
            damageMod = dexMod;
        }
    }

    // Special case: Unarmed Strike
    let damageDie = data.damage;
    if (name === "Unarmed Strike") {
        damageMod = Math.max(0, strMod); // Minimum 0 bonus to damage base
        // Check for Monk Martial Arts (simple example for future expansion)
        const hasMartialArts = features.some(f => f.id === "monk_martial_arts");
        if (hasMartialArts) {
            toHitMod = Math.max(strMod, dexMod);
            damageMod = Math.max(strMod, dexMod);
            // Martial arts die scales: 1-4: 1d6, 5-10: 1d8, 11-16: 1d10, 17-20: 1d12
            if (level >= 17) damageDie = "1d12";
            else if (level >= 11) damageDie = "1d10";
            else if (level >= 5) damageDie = "1d8";
            else damageDie = "1d6";
        }
    }

    // Check for Rage
    const isRaging = features.some(f => f.id === "barbarian_rage"); // Placeholder for "active" rage
    let notes = data.properties.join(", ");
    if (isRaging && !isRanged) {
        const rageBonus = level >= 16 ? 4 : (level >= 9 ? 3 : 2);
        damageMod += rageBonus;
        notes += ` (+${rageBonus} Rage Damage)`;
    }

    return {
        name,
        reach,
        toHit: toHitMod + profBonus,
        damage: damageDie === "1" ? (1 + damageMod) : `${damageDie} ${damageMod >= 0 ? "+" : ""}${damageMod}`,
        type: data.type,
        notes
    };
};

const LAYOUT_CONSTRAINTS = {
    header: { minW: 6, maxW: 12, minH: 4, maxH: 6 },
    hp: { minW: 3, maxW: 6, minH: 2, maxH: 5 },
    abilities: { minW: 3, maxW: 4, minH: 5, maxH: 7 },
    saves: { minW: 3, maxW: 6, minH: 5, maxH: 7 },
    skills: { minW: 2, maxW: 4, minH: 11, maxH: 11 },
    features: { minW: 4, maxW: 12, minH: 4, maxH: 20 },
    species: { minW: 4, maxW: 12, minH: 7, maxH: 9 },
    combat: { minW: 6, maxW: 12, minH: 5, maxH: 15 },
    inventory: { minW: 12, maxW: 12, minH: 3, maxH: 20 },
};


function CharacterSheet() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [character, setCharacter] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [skills, setSkills] = useState({}); // Renamed from skillProficiencies
    const [showMaxHpModifiers, setShowMaxHpModifiers] = useState(false); // Renamed from showModifierInput
    const [maxHpModifier, setMaxHpModifier] = useState(0); // Renamed from damageModInput
    const [inventoryItems, setInventoryItems] = useState([]); // Renamed from inventory
    const [gold, setGold] = useState(0);
    const [inventoryFilter, setInventoryFilter] = useState("All");
    const [classRules, setClassRules] = useState(null);
    const [layout, setLayout] = useState(null);
    const [isLayoutLocked, setIsLayoutLocked] = useState(true);
    const [expandedFeatures, setExpandedFeatures] = useState({});
    const [featureFilter, setFeatureFilter] = useState("All");
    const [xp, setXp] = useState(0);
    const [tempXp, setTempXp] = useState("");
    const [showXpEditor, setShowXpEditor] = useState(false);
    const [speciesRules, setSpeciesRules] = useState(null);
    const [backgroundRules, setBackgroundRules] = useState(null);
    const [weaponRules, setWeaponRules] = useState({});

    // New HP related states
    const [currentHp, setCurrentHp] = useState(0);
    const [baseMaxHp, setBaseMaxHp] = useState(0);
    const [effectiveMaxHp, setEffectiveMaxHp] = useState(0);

    useEffect(() => {
        fetch(`http://localhost:5000/api/characters/${id}`)
            .then(res => {
                if (!res.ok) {
                    if (res.status === 404) throw new Error("Character not found (it may have been deleted)");
                    throw new Error("Failed to load character data");
                }
                return res.json();
            })
            .then(data => {
                setCharacter(data);
                // Initialize state from fetched data (using backend snake_case keys if needed)
                setSkills(data.data.skillProficiencies || {}); // Use 'skills'
                setInventoryItems(data.data.inventory || []); // Use 'inventoryItems'
                setGold(data.data.gold || 0);
                setXp(data.data.xp || 0);
                setTempXp(data.data.xp || 0);

                // Initialize HP states
                const constitutionScore = data.data.abilities.constitution;
                calculateModifier(constitutionScore);

                const initialBaseMaxHp = data.data.hp_max_base || 0;
                const initialMaxHpModifier = data.data.hp_modifier || 0;
                const initialEffectiveMaxHp = initialBaseMaxHp + initialMaxHpModifier;

                setBaseMaxHp(initialBaseMaxHp);
                setEffectiveMaxHp(initialEffectiveMaxHp);
                setCurrentHp(data.data.hp_current || 0);

                setLoading(false);

                // Fetch class rules
                if (data.class?.name) {
                    fetch(`http://localhost:5000/api/classes/${data.class.name.toLowerCase()}`)
                        .then(res => res.json())
                        .then(rules => setClassRules(rules))
                        .catch(err => console.error("Failed to load class rules:", err));
                }

                if (data.data?.species) {
                    fetch(`http://localhost:5000/api/species`)
                        .then(res => res.json())
                        .then(allSpecies => {
                            const species = allSpecies.find(s => s.name.toLowerCase() === data.data.species.toLowerCase());
                            if (species) setSpeciesRules(species);
                        })
                        .catch(err => console.error("Failed to load species rules:", err));
                }

                if (data.data?.background) {
                    fetch(`http://localhost:5000/api/backgrounds`)
                        .then(res => res.json())
                        .then(allBackgrounds => {
                            const bg = allBackgrounds.find(b => b.name.toLowerCase() === data.data.background.toLowerCase());
                            if (bg) setBackgroundRules(bg);
                        })
                        .catch(err => console.error("Failed to load background rules:", err));
                }

                // Fetch weapon rules
                fetch(`http://localhost:5000/api/rules/weapons`)
                    .then(res => res.json())
                    .then(rules => setWeaponRules(rules))
                    .catch(err => console.error("Failed to load weapon rules:", err));

                // Load layout from character data if it exists
                if (data.data?.layout) {
                    // Force the latest constraints onto the loaded layout
                    const mergedLayout = { ...data.data.layout };
                    if (mergedLayout.lg) {
                        mergedLayout.lg = mergedLayout.lg.map(item => {
                            const constraints = LAYOUT_CONSTRAINTS[item.i];
                            if (constraints) {
                                return {
                                    ...item,
                                    ...constraints
                                };
                            }
                            return item;
                        });
                    }
                    setLayout(mergedLayout);
                }
            })
            .catch(err => {
                console.error("Failed to load character:", err);
                setError(err.message);
                setLoading(false);
            });
    }, [id]);

    // Effect to update effectiveMaxHp when baseMaxHp or maxHpModifier changes
    useEffect(() => {
        setEffectiveMaxHp(baseMaxHp + maxHpModifier);
    }, [baseMaxHp, maxHpModifier]);

    const saveCharacter = useCallback((updates) => {
        fetch(`http://localhost:5000/api/characters/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                data: updates
            })
        })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    console.error("Failed to save character updates");
                }
            })
            .catch(err => console.error("Error saving character:", err));
    }, [id]);

    // Effect to ensure currentHp doesn't exceed effectiveMaxHp
    useEffect(() => {
        if (loading) return;
        if (effectiveMaxHp > 0 && currentHp > effectiveMaxHp) {
            setCurrentHp(effectiveMaxHp);
            saveCharacter({ hp_current: effectiveMaxHp });
        }
    }, [currentHp, effectiveMaxHp, saveCharacter, loading]);


    useEffect(() => {
        if (showXpEditor) {
            setTempXp(xp.toString());
        }
    }, [showXpEditor, xp]);

    const handleLevelUp = () => {
        if (!character) return;
        const nextLevel = character.level + 1;
        const requiredXp = XP_THRESHOLDS[nextLevel] || 0;

        if (xp < requiredXp) {
            alert(`Not enough XP to level up to ${nextLevel}. Required: ${requiredXp}`);
            return;
        }

        fetch(`http://localhost:5000/api/characters/${id}/levelup`, {
            method: "POST"
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Update local state to reflect level up
                    setCharacter(prev => ({ ...prev, level: data.new_level }));
                    // Potentially re-fetch full data to update HP etc.
                    window.location.reload(); // Simplest way to refresh all rules and HP
                } else {
                    alert(data.error || "Level up failed");
                }
            })
            .catch(err => console.error("Error during level up:", err));
    };

    const handleLevelDown = () => {
        if (!character) return;
        if (!window.confirm("Are you sure you want to level down? This will reset your stats for the previous level.")) return;

        fetch(`http://localhost:5000/api/characters/${id}/leveldown`, {
            method: "POST"
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(data.error || "Level down failed");
                }
            })
            .catch(err => console.error("Error during level down:", err));
    };

    const handleXpAdjust = (amount) => {
        const currentThreshold = XP_THRESHOLDS[character.level] || 0;
        const nextThreshold = XP_THRESHOLDS[character.level + 1] || Infinity;
        const newXp = Math.max(currentThreshold, Math.min(nextThreshold, xp + amount));
        setXp(newXp);
        setTempXp(newXp.toString());
        saveCharacter({ xp: newXp });
    };

    const handleXpBlur = () => {
        let val = parseInt(tempXp) || 0;
        const currentThreshold = XP_THRESHOLDS[character.level] || 0;
        const nextThreshold = Math.min(999999, XP_THRESHOLDS[character.level + 1] || 999999);

        // If lower than threshold, reset to minimum
        if (val < currentThreshold) {
            val = currentThreshold;
        }
        // If higher than next level requirement (or 999,999), cap it
        if (val > nextThreshold) {
            val = nextThreshold;
        }

        setXp(val);
        setTempXp(val.toString());
        saveCharacter({ xp: val });
    };

    const ABILITY_SCORES = useMemo(() => [
        { name: "Strength", key: "strength" },
        { name: "Dexterity", key: "dexterity" },
        { name: "Constitution", key: "constitution" },
        { name: "Intelligence", key: "intelligence" },
        { name: "Wisdom", key: "wisdom" },
        { name: "Charisma", key: "charisma" },
    ], []);

    const SKILL_LIST = useMemo(() => [
        { name: "Acrobatics", key: "acrobatics", ability: "dexterity" },
        { name: "Animal Handling", key: "animal_handling", ability: "wisdom" },
        { name: "Arcana", key: "arcana", ability: "intelligence" },
        { name: "Athletics", key: "athletics", ability: "strength" },
        { name: "Deception", key: "deception", ability: "charisma" },
        { name: "History", key: "history", ability: "intelligence" },
        { name: "Insight", key: "insight", ability: "wisdom" },
        { name: "Intimidation", key: "intimidation", ability: "charisma" },
        { name: "Investigation", key: "investigation", ability: "intelligence" },
        { name: "Medicine", key: "medicine", ability: "wisdom" },
        { name: "Nature", key: "nature", ability: "intelligence" },
        { name: "Perception", key: "perception", ability: "wisdom" },
        { name: "Performance", key: "performance", ability: "charisma" },
        { name: "Persuasion", key: "persuasion", ability: "charisma" },
        { name: "Religion", key: "religion", ability: "intelligence" },
        { name: "Sleight Of Hand", key: "sleight_of_hand", ability: "dexterity" },
        { name: "Stealth", key: "stealth", ability: "dexterity" },
        { name: "Survival", key: "survival", ability: "wisdom" },
    ], []);

    const currentProficiencyBonus = useMemo(() => character ? proficiencyBonus(character.level) : 2, [character]);

    // Proactive: Get proficient saves from class rules if available
    const proficientSaves = useMemo(() => {
        if (classRules?.proficiencies?.saving_throws) {
            return classRules.proficiencies.saving_throws.map(s => s.toLowerCase());
        }
        return ["strength", "constitution"]; // Fallback
    }, [classRules]);

    const toggleSkillProficiency = (skillKey) => {
        setSkills(prev => {
            const newState = { ...prev, [skillKey]: !prev[skillKey] };
            saveCharacter({ skillProficiencies: newState });
            return newState;
        });
    };

    const updateCurrentHp = (value) => {
        let val = parseInt(value) || 0;
        val = Math.min(val, effectiveMaxHp);
        val = Math.max(0, val);
        setCurrentHp(val);
        saveCharacter({ hp_current: val });
    };

    const updateMaxHpModifier = (value) => {
        let val = parseInt(value) || 0;
        val = Math.max(-10, Math.min(10, val));
        setMaxHpModifier(val);
    };

    const applyMaxHpModifier = () => {
        saveCharacter({ hp_modifier: maxHpModifier });
    };

    const removeItem = (itemToRemove) => {
        const newInventory = inventoryItems.filter(item => item !== itemToRemove);
        setInventoryItems(newInventory);
        saveCharacter({ inventory: newInventory });
    };

    const groupedInventory = useMemo(() => inventoryItems.reduce((acc, item) => {
        const category = item.category || "Other";
        if (!acc[category]) acc[category] = [];
        acc[category].push(item);
        return acc;
    }, { "All": inventoryItems }), [inventoryItems]);

    const displayedItems = groupedInventory[inventoryFilter] || [];

    // --- Rich Rendering Components ---
    const ValueRenderer = ({ value, label, level }) => {
        if (value === null || value === undefined) return null;

        // 1. Detect and Resolve Scaling Dictionaries
        const isScaling = typeof value === 'object' && !Array.isArray(value) && Object.keys(value).some(k => k.match(/^\d+(-?\d+)?$/));
        if (isScaling) {
            const currentVal = resolveScalingValue(value, level);
            return <span className="resolved-scaling-value">{currentVal}</span>;
        }

        // 2. Custom Renderers for special categories
        const category = label?.toLowerCase() || "";
        const isBadgeCategory = ["resists", "resistances", "immunities", "advantages", "senses", "uses"].includes(category);

        if (isBadgeCategory) {
            const items = typeof value === 'string' ? value.split(', ') : (Array.isArray(value) ? value : [value]);
            return (
                <div className={`benefit-badges ${category}`}>
                    {items.map((item, idx) => (
                        <span key={idx} className="benefit-badge">{item}</span>
                    ))}
                </div>
            );
        }

        if (Array.isArray(value)) {
            return (
                <div className="value-list">
                    {value.map((item, idx) => (
                        <div key={idx} className="value-list-item">
                            {typeof item === 'object' ? <ValueRenderer value={item} level={level} /> : item}
                        </div>
                    ))}
                </div>
            );
        }

        if (typeof value === 'object') {
            // Check if it's an options list
            if (value.Options) {
                return (
                    <div className="options-list">
                        {value.Options.map((opt, idx) => (
                            <div key={idx} className="option-item">
                                <span className="option-name">{opt.name}</span>
                                <span className="option-desc">{opt.description}</span>
                            </div>
                        ))}
                    </div>
                );
            }

            // Regular key-value pairs
            return (
                <div className="detail-pairs">
                    {Object.entries(value).map(([l, val]) => (
                        <div key={l} className="detail-pair">
                            <span className="detail-label">{l}:</span>
                            <span className="detail-value">
                                <ValueRenderer value={val} label={l} level={level} />
                            </span>
                        </div>
                    ))}
                </div>
            );
        }

        return <span className="value-primitive">{processRichText(value)}</span>;
    };

    const AttackRow = ({ attack, onToggle, isExpanded }) => {
        return (
            <div className={`attack-row-wrapper ${isExpanded ? 'expanded' : ''}`}>
                <div className="attack-row" onClick={onToggle}>
                    <span className="attack-name">{attack.name}</span>
                    <span className="attack-reach">{attack.reach}</span>
                    <span className="attack-hit">+{attack.toHit}</span>
                    <span className="attack-damage">{attack.damage}</span>
                    <span className="attack-type-icon" title={attack.type}>{attack.type[0]}</span>
                </div>
                {isExpanded && (
                    <div className="attack-details-expanded">
                        <div className="attack-notes">{attack.notes}</div>
                    </div>
                )}
            </div>
        );
    };

    const CombatWidget = ({ character, inventory, features, profBonus, weaponRules }) => {
        const [expandedAttack, setExpandedAttack] = useState(null);

        const attacks = useMemo(() => {
            const list = [];
            // 1. Always add Unarmed Strike
            list.push(calculateAttack("Unarmed Strike", character.data.abilities, profBonus, features, character.level, weaponRules));

            // 2. Add weapons from inventory
            inventory.forEach(item => {
                if (weaponRules[item.name]) {
                    list.push(calculateAttack(item.name, character.data.abilities, profBonus, features, character.level, weaponRules));
                }
            });
            return list;
        }, [character, inventory, features, profBonus, weaponRules]);

        const combatActions = useMemo(() => {
            const grouped = { Action: [], "Bonus Action": [], Reaction: [] };
            features.forEach(f => {
                const actionText = (f.details?.Action || f.details?.action || f.summary || f.description || "").toLowerCase();
                if (actionText.includes("bonus action")) grouped["Bonus Action"].push(f);
                else if (actionText.includes("reaction")) grouped["Reaction"].push(f);
                else if (actionText.includes("action") && !actionText.includes("bonus action")) grouped["Action"].push(f);
            });
            return grouped;
        }, [features]);

        return (
            <div className="combat-actions-content">
                <section className="combat-section">
                    <h4>Attacks</h4>
                    <div className="attacks-table">
                        <div className="attack-header">
                            <span>Name</span>
                            <span>Reach</span>
                            <span>Hit</span>
                            <span>Damage</span>
                            <span></span>
                        </div>
                        {attacks.map((atk, idx) => (
                            <AttackRow
                                key={idx}
                                attack={atk}
                                isExpanded={expandedAttack === idx}
                                onToggle={() => setExpandedAttack(expandedAttack === idx ? null : idx)}
                            />
                        ))}
                    </div>
                </section>

                {Object.entries(combatActions).map(([type, list]) => (
                    list.length > 0 && (
                        <section key={type} className="combat-section">
                            <h4>{type}s</h4>
                            <div className="action-list-compact">
                                {list.map(f => (
                                    <div key={f.id} className="compact-action-item">
                                        <span className="action-name">{f.name}</span>
                                        <span className="action-summary-short">{f.summary}</span>
                                    </div>
                                ))}
                            </div>
                        </section>
                    )
                ))}
            </div>
        );
    };

    const RichFeature = ({ feature, isExpanded, onToggle, level }) => {
        return (
            <div className={`feature-card ${isExpanded ? "expanded" : "collapsed"} source-${feature.source || 'unknown'}`}>
                <div className="feature-title" onClick={() => onToggle(feature.id)}>
                    <div className="feature-title-left">
                        <span className="feature-name">{feature.name}</span>
                        <span className="feature-source-tag">{feature.source}</span>
                    </div>
                    <span className="feature-lvl">
                        {feature.source === 'Class' || feature.source === 'Subclass' ? `Lvl ${feature.level}` : ''}
                    </span>
                </div>
                {isExpanded && (
                    <div className="feature-body">
                        {feature.summary && <p className="feature-summary"><strong>Summary:</strong> {processRichText(feature.summary)}</p>}
                        {feature.description && (
                            <div className="feature-description">
                                {feature.description.split('\n').map((para, i) => (
                                    <p key={i}>{processRichText(para)}</p>
                                ))}
                            </div>
                        )}
                        {feature.details && (
                            <div className="feature-details">
                                <ValueRenderer value={feature.details} level={level} />
                            </div>
                        )}
                    </div>
                )}
            </div>
        );
    };

    // --- Dynamic Feature Logic ---
    const availableFeatures = useMemo(() => {
        if (!character) return [];

        const allFeatures = [];
        const currentLevel = character.level;

        // 1. Add Class Features
        if (classRules?.features) {
            Object.keys(classRules.features).forEach(lvl => {
                if (parseInt(lvl) <= currentLevel) {
                    allFeatures.push(...classRules.features[lvl].map(f => ({ ...f, source: 'Class', level: lvl })));
                }
            });
        }

        // 2. Add Subclass Features
        const subclassId = character.class?.subclass;
        if (subclassId && classRules?.subclasses?.[subclassId]?.features) {
            const scFeatures = classRules.subclasses[subclassId].features;
            Object.keys(scFeatures).forEach(lvl => {
                if (parseInt(lvl) <= currentLevel) {
                    allFeatures.push(...scFeatures[lvl].map(f => ({ ...f, source: 'Subclass', level: lvl })));
                }
            });
        }

        // 3. Add Species Features
        if (speciesRules?.features) {
            allFeatures.push(...speciesRules.features.map(f => ({ ...f, source: 'Species' })));
        } else if (speciesRules?.traits) { // Backward compatibility for un-migrated species
            allFeatures.push(...speciesRules.traits.map((t, idx) => ({
                id: `species_trait_${idx}`,
                name: t.split('.')[0],
                description: t,
                source: 'Species'
            })));
        }

        // 4. Add Background & Origin Feat
        if (backgroundRules) {
            const choices = character.data?.choices;
            const bgFeat = choices?.background_feat;
            const bgBonus = choices?.background_bonus;

            allFeatures.push({
                id: 'background_feature',
                name: `Background: ${backgroundRules.name}`,
                description: backgroundRules.description || "No description available.",
                source: 'Background',
                details: {
                    "Skills": backgroundRules.skills?.join(", "),
                    "Tools": backgroundRules.tools,
                    "Stat Bonuses": bgBonus ? (
                        bgBonus.mode === '2_1'
                            ? `+2 ${bgBonus.plus2}, +1 ${bgBonus.plus1}`
                            : `+1 to ${backgroundRules.ability_scores?.join(", ")}`
                    ) : "Included in Base Stats"
                }
            });

            if (bgFeat) {
                allFeatures.push({
                    id: 'background_origin_feat',
                    name: `Origin Feat: ${bgFeat.name}`,
                    description: bgFeat.effects?.join("\n\n") || "No effects listed.",
                    source: 'Background Feat'
                });
            } else if (backgroundRules.feat) {
                allFeatures.push({
                    id: 'background_origin_feat_placeholder',
                    name: `Origin Feat: ${backgroundRules.feat}`,
                    description: "Select feat effects in character creation for full details.",
                    source: 'Background Feat'
                });
            }
        }

        return allFeatures;
    }, [classRules, character, speciesRules, backgroundRules]);

    // --- Dynamic Defenses Logic ---
    const defenses = useMemo(() => {
        const result = { resistances: [], immunities: [] };
        if (!availableFeatures) return result;

        availableFeatures.forEach(f => {
            if (f.details?.Resistances) {
                const res = typeof f.details.Resistances === 'string'
                    ? f.details.Resistances.split(', ')
                    : f.details.Resistances;
                result.resistances = [...new Set([...result.resistances, ...res])];
            }
            if (f.details?.Immunities) {
                const imm = typeof f.details.Immunities === 'string'
                    ? f.details.Immunities.split(', ')
                    : f.details.Immunities;
                result.immunities = [...new Set([...result.immunities, ...imm])];
            }
        });
        return result;
    }, [availableFeatures]);

    const filteredFeatures = useMemo(() => {
        if (featureFilter === "All") return availableFeatures;

        return availableFeatures.filter(f => {
            const actionText = (f.details?.Action || f.details?.action || f.summary || f.description || "").toLowerCase();
            if (featureFilter === "Action") return actionText.includes("action") && !actionText.includes("bonus action");
            if (featureFilter === "Bonus Action") return actionText.includes("bonus action");
            if (featureFilter === "Reaction") return actionText.includes("reaction");
            if (featureFilter === "Passive") return !actionText.includes("action") && !actionText.includes("reaction") && !actionText.includes("bonus action");
            return true;
        });
    }, [availableFeatures, featureFilter]);

    const toggleFeature = (id) => {
        setExpandedFeatures(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const onLayoutChange = (currentLayout, allLayouts) => {
        if (isLayoutLocked || loading) return;
        setLayout(allLayouts);
        saveCharacter({ layout: allLayouts });
    };

    const defaultLayouts = {
        lg: [
            { i: "header", x: 0, y: 0, w: 12, h: 5, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.header },
            { i: "hp", x: 0, y: 5, w: 4, h: 3, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.hp },
            { i: "abilities", x: 4, y: 5, w: 4, h: 6, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.abilities },
            { i: "saves", x: 8, y: 5, w: 4, h: 6, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.saves },
            { i: "skills", x: 0, y: 8, w: 4, h: 12, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.skills },
            { i: "species", x: 4, y: 11, w: 8, h: 8, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.species },
            { i: "features", x: 4, y: 19, w: 8, h: 10, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.features },
            { i: "combat", x: 4, y: 29, w: 8, h: 10, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.combat },
            { i: "inventory", x: 0, y: 39, w: 12, h: 6, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.inventory },
        ]
    };

    if (loading) return <div className="loading-screen">Invoking the Character Sheet...</div>;

    if (error) {
        return (
            <div className="error-screen">
                <div className="error-card">
                    <h2>✧ Access Denied ✧</h2>
                    <p>{error}</p>
                    <button className="back-button" onClick={() => navigate("/")}>
                        Return to Characters Hub
                    </button>
                </div>
            </div>
        );
    }

    if (!character) return <div className="loading-screen">Character not found...</div>;

    return (
        <div className={`character-sheet-container premium-theme ${!isLayoutLocked ? "layout-unlocked" : ""}`}>
            <div className="sheet-top-bar">
                <button onClick={() => navigate("/")} className="back-button">Back to Hub</button>
                <button
                    onClick={() => setIsLayoutLocked(!isLayoutLocked)}
                    className={`lock-button ${isLayoutLocked ? "locked" : "unlocked"}`}
                >
                    {isLayoutLocked ? "🔒 Unlock Layout" : "🔓 Lock & Save Layout"}
                </button>
            </div>

            <ResponsiveGridLayout
                className="layout"
                layouts={layout || defaultLayouts}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={30}
                margin={[40, 40]}
                compactType="vertical"
                preventCollision={false}
                isDraggable={!isLayoutLocked}
                isResizable={!isLayoutLocked}
                onLayoutChange={onLayoutChange}
            >
                <div key="header" className="widget card header-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <div className="header-content">
                        <div className="header-main">
                            <div>
                                <h2>{character.name} <span className="level-badge">Lvl {character.level}</span></h2>
                                <div className="xp-bar-container" onClick={() => setShowXpEditor(true)} style={{ cursor: "pointer" }} title="Edit Experience">
                                    <span className="xp-text">XP: {xp} / {XP_THRESHOLDS[character.level + 1] || "MAX"}</span>
                                    {character.level < 20 && (
                                        <div className="xp-progress-bg">
                                            <div
                                                className="xp-progress-fill"
                                                style={{ width: `${Math.min(100, (xp / XP_THRESHOLDS[character.level + 1]) * 100)}%` }}
                                            ></div>
                                        </div>
                                    )}
                                </div>
                            </div>
                            {character.level < 20 && (
                                <button
                                    className={`levelup-button ${xp >= (XP_THRESHOLDS[character.level + 1] || 0) ? "available" : "locked"}`}
                                    onClick={handleLevelUp}
                                    disabled={xp < (XP_THRESHOLDS[character.level + 1] || 0)}
                                >
                                    {xp >= (XP_THRESHOLDS[character.level + 1] || 0) ? "✧ LEVEL UP ✧" : "Level Up"}
                                </button>
                            )}
                        </div>
                        <div className="header-details">
                            <span className="detail-pill class-pill">{character.class.name}</span>
                            <span className="detail-pill species-pill">
                                {character.data.species}
                                {character.data.species_variant ? ` (${character.data.species_variant})` : ""} |
                                {character.data.size || speciesRules?.size || "Medium"} |
                                {speciesRules?.speed || "30 ft."}
                            </span>
                            <span className="detail-pill background-pill">{character.data.background}</span>
                        </div>
                        {(defenses.resistances.length > 0 || defenses.immunities.length > 0) && (
                            <div className="header-defenses">
                                {defenses.resistances.length > 0 && (
                                    <div className="defense-group">
                                        <span className="defense-label">Resists:</span>
                                        <div className="defense-tags">
                                            {defenses.resistances.map(r => <span key={r} className="defense-tag">{r}</span>)}
                                        </div>
                                    </div>
                                )}
                                {defenses.immunities.length > 0 && (
                                    <div className="defense-group">
                                        <span className="defense-label">Immune:</span>
                                        <div className="defense-tags">
                                            {defenses.immunities.map(i => <span key={i} className="defense-tag immunity">{i}</span>)}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>

                <div key="hp" className="widget card hp-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <div className="hp-content">
                        <h3>Hit Points</h3>
                        <div className="hp-main">
                            <input
                                type="number"
                                value={currentHp}
                                onChange={(e) => updateCurrentHp(e.target.value)}
                                className="hp-current-input"
                            />
                            <span className="hp-sep">/</span>
                            <span className="hp-max" onClick={() => setShowMaxHpModifiers(!showMaxHpModifiers)}>
                                {effectiveMaxHp}
                            </span>
                        </div>
                        {showMaxHpModifiers && (
                            <div className="hp-mod-overlay">
                                <input type="number" value={maxHpModifier} onChange={(e) => updateMaxHpModifier(e.target.value)} />
                                <button onClick={applyMaxHpModifier}>Apply</button>
                                <button onClick={() => setShowMaxHpModifiers(false)}>✕</button>
                            </div>
                        )}
                    </div>
                </div>

                <div key="abilities" className="widget card abilities-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <h3>Abilities</h3>
                    <div className="ability-grid">
                        {ABILITY_SCORES.map(({ name, key }) => {
                            const score = character.data?.abilities?.[key] ?? 10;
                            const mod = calculateModifier(score);
                            return (
                                <div key={key} className="ability-box">
                                    <span className="ability-name">{name.slice(0, 3).toUpperCase()}</span>
                                    <span className="ability-mod">{mod >= 0 ? "+" : ""}{mod}</span>
                                    <span className="ability-score">{score}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div key="saves" className="widget card saves-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <h3>Saving Throws</h3>
                    <div className="saves-list">
                        {ABILITY_SCORES.map(({ name, key }) => {
                            const score = character.data?.abilities?.[key] ?? 10;
                            const base = calculateModifier(score);
                            const isProficient = proficientSaves.includes(key);
                            const total = base + (isProficient ? currentProficiencyBonus : 0);
                            return (
                                <div key={key} className="save-row">
                                    <span className={`prof-dot ${isProficient ? "fill" : ""}`}></span>
                                    <span className="save-name">{name}</span>
                                    <span className="save-total">{total >= 0 ? "+" : ""}{total}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div key="skills" className="widget card skills-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <h3>Skills</h3>
                    <div className="skills-container scrollable">
                        {SKILL_LIST.map(skill => {
                            const isProficient = skills[skill.key] ?? false;
                            const abilityScore = character.data.abilities[skill.ability];
                            const mod = calculateModifier(abilityScore);
                            const bonus = mod + (isProficient ? currentProficiencyBonus : 0);

                            // Check if this skill is from the background
                            const bgSkills = (character.data?.choices?.background_skills || []).map(s => s.toLowerCase().replace(/\s+/g, '_'));
                            const isFromBackground = bgSkills.includes(skill.key);

                            return (
                                <div key={skill.key} className={`skill-row ${isFromBackground ? 'is-locked' : ''}`} title={isFromBackground ? `Gained from background (${character.data.background})` : ""}>
                                    <span
                                        className={`prof-toggle ${isProficient ? "is-prof" : ""} ${isFromBackground ? "locked" : ""}`}
                                        onClick={() => !isFromBackground && toggleSkillProficiency(skill.key)}
                                    >
                                        {isFromBackground && <span className="lock-icon-tiny">🔒</span>}
                                    </span>
                                    <span className="skill-name">{skill.name}</span>
                                    <span className="skill-bonus">{bonus >= 0 ? "+" : ""}{bonus}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div key="features" className="widget card features-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <div className="features-header">
                        <h3>Features</h3>
                        <div className="feature-tabs">
                            {["All", "Action", "Bonus Action", "Reaction", "Passive"].map(t => (
                                <button
                                    key={t}
                                    onClick={() => setFeatureFilter(t)}
                                    className={featureFilter === t ? "active" : ""}
                                >
                                    {t}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="features-container scrollable">
                        {filteredFeatures.map(f => (
                            <RichFeature
                                key={f.id}
                                feature={f}
                                isExpanded={expandedFeatures[f.id]}
                                onToggle={toggleFeature}
                                level={character.level}
                            />
                        ))}
                    </div>
                </div>

                <div key="species" className="widget card species-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <h3>Species: {character.data.species}</h3>
                    <div className="species-info-content scrollable">
                        {speciesRules?.summary && <p className="species-lore-summary">{speciesRules.summary}</p>}
                        <div className="species-traits-list">
                            {availableFeatures.filter(f => f.source === 'Species').map(f => (
                                <RichFeature
                                    key={f.id}
                                    feature={f}
                                    isExpanded={expandedFeatures[f.id]}
                                    onToggle={toggleFeature}
                                    level={character.level}
                                />
                            ))}
                        </div>
                    </div>
                </div>

                <div key="combat" className="widget card combat-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <h3>Combat Actions</h3>
                    <div className="scrollable">
                        <CombatWidget
                            character={character}
                            inventory={inventoryItems}
                            features={availableFeatures}
                            profBonus={currentProficiencyBonus}
                            weaponRules={weaponRules}
                        />
                    </div>
                </div>

                <div key="inventory" className="widget card inventory-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <div className="inventory-header-row">
                        <h3>Inventory</h3>
                        <div className="gold-box">Gold: {gold} GP</div>
                        <div className="inv-tabs">
                            {Object.keys(groupedInventory).map(cat => (
                                <button
                                    key={cat}
                                    onClick={() => setInventoryFilter(cat)}
                                    className={inventoryFilter === cat ? "active" : ""}
                                >
                                    {cat}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="inventory-container scrollable">
                        {displayedItems.map((item, idx) => (
                            <div key={idx} className="inventory-row">
                                <span>{item.name} {item.quantity > 1 ? `x${item.quantity}` : ""}</span>
                                <button className="del-btn" onClick={() => removeItem(item)}>✕</button>
                            </div>
                        ))}
                    </div>
                </div>
            </ResponsiveGridLayout>

            {showXpEditor && (
                <div className="xp-editor-overlay" onClick={() => setShowXpEditor(false)}>
                    <div className="xp-editor-panel" onClick={e => e.stopPropagation()}>
                        <div className="xp-editor-header">
                            <h3>✧ Experience Editor ✧</h3>
                            <button className="close-btn" onClick={() => setShowXpEditor(false)}>×</button>
                        </div>

                        <div className="xp-editor-body">
                            <div className="xp-status">
                                <span>Current Level: <strong>{character.level}</strong></span>
                                <span>Current XP: <strong>{xp}</strong></span>
                            </div>

                            <div className="xp-controls">
                                <label>Adjust Experience</label>
                                <div className="xp-adjust-row">
                                    <button onClick={() => handleXpAdjust(-10)}>-10</button>
                                    <button onClick={() => handleXpAdjust(-1)}>-1</button>
                                    <input
                                        type="text"
                                        inputMode="numeric"
                                        pattern="[0-9]*"
                                        value={tempXp}
                                        onChange={(e) => {
                                            let rawVal = e.target.value.replace(/\D/g, "");
                                            if (rawVal.length > 6) rawVal = rawVal.slice(0, 6);
                                            // Handle multiple zeros or leading zeros during typing
                                            if (rawVal.length > 1 && rawVal.startsWith("0")) {
                                                rawVal = rawVal.replace(/^0+/, "") || "0";
                                            }
                                            setTempXp(rawVal);
                                        }}
                                        onBlur={handleXpBlur}
                                    />
                                    <button onClick={() => handleXpAdjust(1)}>+1</button>
                                    <button onClick={() => handleXpAdjust(10)}>+10</button>
                                </div>
                                <div className="xp-threshold-hint">
                                    Next Level: {XP_THRESHOLDS[character.level + 1] || "None"} XP
                                </div>
                            </div>

                            <div className="xp-actions">
                                <button
                                    className="action-btn levelup-btn"
                                    onClick={handleLevelUp}
                                    disabled={xp < (XP_THRESHOLDS[character.level + 1] || 0) || character.level >= 20}
                                >
                                    ✧ Level Up ✧
                                </button>
                                <button
                                    className="action-btn leveldown-btn"
                                    onClick={handleLevelDown}
                                    disabled={character.level <= 1 || xp !== (XP_THRESHOLDS[character.level] || 0)}
                                    title={xp !== (XP_THRESHOLDS[character.level] || 0) ? `Reset XP to ${XP_THRESHOLDS[character.level]} to Level Down` : ""}
                                >
                                    ⚠ Level Down
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CharacterSheet;