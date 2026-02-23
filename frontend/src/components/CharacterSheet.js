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
                    fetch(`http://localhost:5000/api/classes/${data.class.name}`)
                        .then(res => res.json())
                        .then(rules => setClassRules(rules))
                        .catch(err => console.error("Failed to load class rules:", err));
                }

                // Load layout from character data if it exists
                if (data.data?.layout) {
                    setLayout(data.data.layout);
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

    // --- Dynamic Feature Logic ---
    const availableFeatures = useMemo(() => {
        if (!classRules || !character) return [];

        const allFeatures = [];
        const currentLevel = character.level;

        // Add Class Features
        if (classRules.features) {
            Object.keys(classRules.features).forEach(lvl => {
                if (parseInt(lvl) <= currentLevel) {
                    allFeatures.push(...classRules.features[lvl]);
                }
            });
        }

        // Add Subclass Features
        const subclassId = character.class?.subclass;
        if (subclassId && classRules.subclasses?.[subclassId]?.features) {
            const scFeatures = classRules.subclasses[subclassId].features;
            Object.keys(scFeatures).forEach(lvl => {
                if (parseInt(lvl) <= currentLevel) {
                    allFeatures.push(...scFeatures[lvl]);
                }
            });
        }

        return allFeatures;
    }, [classRules, character]);

    const filteredFeatures = useMemo(() => {
        if (featureFilter === "All") return availableFeatures;

        return availableFeatures.filter(f => {
            const actionText = (f.details?.action || f.summary || "").toLowerCase();
            if (featureFilter === "Action") return actionText.includes("action") && !actionText.includes("bonus action");
            if (featureFilter === "Bonus Action") return actionText.includes("bonus action");
            if (featureFilter === "Reaction") return actionText.includes("reaction");
            if (featureFilter === "Passive") return !actionText.includes("action") && !actionText.includes("reaction");
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
            { i: "header", x: 0, y: 0, w: 12, h: 2, static: isLayoutLocked, minW: 12, maxW: 12, minH: 2, maxH: 4 },
            { i: "hp", x: 0, y: 2, w: 4, h: 3, static: isLayoutLocked, minW: 3, maxW: 6, minH: 2, maxH: 5 },
            { i: "abilities", x: 4, y: 2, w: 4, h: 6, static: isLayoutLocked, minW: 3, maxW: 6, minH: 5, maxH: 10 },
            { i: "saves", x: 8, y: 2, w: 4, h: 6, static: isLayoutLocked, minW: 3, maxW: 6, minH: 5, maxH: 10 },
            { i: "skills", x: 0, y: 5, w: 4, h: 10, static: isLayoutLocked, minW: 2, maxW: 6, minH: 4, maxH: 20 },
            { i: "features", x: 4, y: 8, w: 8, h: 10, static: isLayoutLocked, minW: 4, maxW: 12, minH: 4, maxH: 30 },
            { i: "inventory", x: 0, y: 15, w: 12, h: 6, static: isLayoutLocked, minW: 4, maxW: 12, minH: 3, maxH: 20 },
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
                            <span>{character.class.name}</span>
                            <span>{character.data.species}</span>
                            <span>{character.data.background}</span>
                        </div>
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
                            return (
                                <div key={skill.key} className="skill-row">
                                    <span
                                        className={`prof-toggle ${isProficient ? "is-prof" : ""}`}
                                        onClick={() => toggleSkillProficiency(skill.key)}
                                    ></span>
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
                            <div key={f.id} className={`feature-card ${expandedFeatures[f.id] ? "expanded" : "collapsed"}`}>
                                <div className="feature-title" onClick={() => toggleFeature(f.id)}>
                                    <span className="feature-name">{f.name}</span>
                                    <span className="feature-lvl">Lvl {f.level || "??"}</span>
                                </div>
                                {expandedFeatures[f.id] && (
                                    <div className="feature-body">
                                        <p className="feature-summary">{f.summary}</p>
                                        {f.details && <pre className="feature-details-raw">{JSON.stringify(f.details, null, 2)}</pre>}
                                    </div>
                                )}
                            </div>
                        ))}
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