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

    let usedStrForDamage = false;

    if (isRanged) {
        toHitMod = dexMod;
        damageMod = dexMod;
    } else if (isFinesse) {
        if (dexMod > strMod) {
            toHitMod = dexMod;
            damageMod = dexMod;
        } else {
            usedStrForDamage = true;
        }
    } else {
        usedStrForDamage = true;
    }

    // Special case: Unarmed Strike
    let damageDie = data.damage;
    if (name === "Unarmed Strike") {
        const hasMartialArts = features.some(f => f.id === "monk_martial_arts");
        if (hasMartialArts) {
            if (dexMod > strMod) {
                toHitMod = dexMod;
                damageMod = dexMod;
                usedStrForDamage = false;
            } else {
                usedStrForDamage = true;
            }
            // Martial arts die scales
            if (level >= 17) damageDie = "1d12";
            else if (level >= 11) damageDie = "1d10";
            else if (level >= 5) damageDie = "1d8";
            else damageDie = "1d6";
        } else {
            damageMod = Math.max(0, strMod);
            usedStrForDamage = true;
        }
    }

    // Check for Rage
    const activeFeatureIds = features.activeIds || [];
    const isCurrentlyRaging = activeFeatureIds.includes("barbarian_rage");
    let notes = data.properties.join(", ");

    if (isCurrentlyRaging && usedStrForDamage) {
        const rageBonus = level >= 16 ? 4 : (level >= 9 ? 3 : 2);
        damageMod += rageBonus;
        notes += (notes ? ", " : "") + `(+${rageBonus} Rage Damage)`;
    }

    return {
        name,
        reach,
        toHit: toHitMod + profBonus,
        damage: damageDie === "1" ? (1 + damageMod) : `${damageDie} ${damageMod >= 0 ? "+" : ""}${damageMod}`,
        type: data.type,
        notes,
        usedStrForDamage // Added for external checks if needed
    };
};

// --- Sub-Components ---

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

const CombatWidget = ({ character, inventory, features, profBonus, weaponRules, activeFeatures }) => {
    const [expandedAttack, setExpandedAttack] = useState(null);

    const attacks = useMemo(() => {
        const list = [];
        const featuresWithActive = [...features];
        featuresWithActive.activeIds = activeFeatures;

        // 1. Always add Unarmed Strike
        list.push(calculateAttack("Unarmed Strike", character.data.abilities, profBonus, featuresWithActive, character.level, weaponRules));

        // 2. Add weapons from inventory
        inventory.forEach(item => {
            if (weaponRules[item.name]) {
                list.push(calculateAttack(item.name, character.data.abilities, profBonus, featuresWithActive, character.level, weaponRules));
            }
        });
        return list;
    }, [character, inventory, features, profBonus, weaponRules, activeFeatures]);

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

const RichFeature = ({ feature, isExpanded, onToggle, level, isActive, onActivate, currentUses }) => {
    const maxUsesData = feature.details?.Uses;
    const maxUses = maxUsesData ? resolveScalingValue(maxUsesData, level) : null;
    const hasUses = maxUses !== null;

    return (
        <div className={`feature-card ${isExpanded ? "expanded" : "collapsed"} source-${feature.source || 'unknown'} ${isActive ? 'is-active' : ''}`}>
            <div className="feature-title" onClick={() => onToggle(feature.id)}>
                <div className="feature-title-left">
                    <span className="feature-name">{feature.name}</span>
                    <span className="feature-source-tag">{feature.source}</span>
                    {isActive && <span className="active-tag">ACTIVE</span>}
                </div>
                <div className="feature-title-right">
                    {hasUses && (
                        <span className="feature-uses">
                            Uses: {currentUses !== undefined ? currentUses : maxUses} / {maxUses}
                        </span>
                    )}
                    <span className="feature-lvl">
                        {feature.source === 'Class' || feature.source === 'Subclass' ? `Lvl ${feature.level}` : ''}
                    </span>
                </div>
            </div>
            {isExpanded && (
                <div className="feature-body">
                    {feature.id === "barbarian_rage" && (
                        <button
                            className={`activate-btn ${isActive ? 'active' : ''} ${(currentUses === 0 || (!isActive && currentUses === 0)) ? 'disabled' : ''}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                onActivate(feature.id, maxUses);
                            }}
                            disabled={!isActive && currentUses === 0}
                        >
                            {isActive ? "End Rage" : "Rage!"}
                        </button>
                    )}
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
    spellcasting: { minW: 6, maxW: 12, minH: 12, maxH: 30 },
};

const DEFAULT_LAYOUTS = {
    lg: [
        { i: "header", x: 0, y: 0, w: 12, h: 5, ...LAYOUT_CONSTRAINTS.header },
        { i: "hp", x: 0, y: 5, w: 4, h: 3, ...LAYOUT_CONSTRAINTS.hp },
        { i: "abilities", x: 4, y: 5, w: 4, h: 6, ...LAYOUT_CONSTRAINTS.abilities },
        { i: "saves", x: 8, y: 5, w: 4, h: 6, ...LAYOUT_CONSTRAINTS.saves },
        { i: "skills", x: 0, y: 8, w: 4, h: 12, ...LAYOUT_CONSTRAINTS.skills },
        { i: "species", x: 4, y: 11, w: 8, h: 8, ...LAYOUT_CONSTRAINTS.species },
        { i: "features", x: 4, y: 19, w: 8, h: 10, ...LAYOUT_CONSTRAINTS.features },
        { i: "combat", x: 4, y: 29, w: 8, h: 10, ...LAYOUT_CONSTRAINTS.combat },
        { i: "inventory", x: 0, y: 39, w: 12, h: 6, ...LAYOUT_CONSTRAINTS.inventory },
        { i: "spellcasting", x: 0, y: 45, w: 12, h: 12, ...LAYOUT_CONSTRAINTS.spellcasting },
    ],
    md: [
        { i: "header", x: 0, y: 0, w: 10, h: 5, ...LAYOUT_CONSTRAINTS.header },
        { i: "hp", x: 0, y: 5, w: 5, h: 3, ...LAYOUT_CONSTRAINTS.hp },
        { i: "abilities", x: 5, y: 5, w: 5, h: 6, ...LAYOUT_CONSTRAINTS.abilities },
        { i: "saves", x: 0, y: 8, w: 5, h: 6, ...LAYOUT_CONSTRAINTS.saves },
        { i: "skills", x: 5, y: 11, w: 5, h: 12, ...LAYOUT_CONSTRAINTS.skills },
        { i: "species", x: 0, y: 14, w: 10, h: 8, ...LAYOUT_CONSTRAINTS.species },
        { i: "features", x: 0, y: 22, w: 10, h: 10, ...LAYOUT_CONSTRAINTS.features },
        { i: "combat", x: 0, y: 32, w: 10, h: 10, ...LAYOUT_CONSTRAINTS.combat },
        { i: "inventory", x: 0, y: 42, w: 10, h: 6, ...LAYOUT_CONSTRAINTS.inventory },
        { i: "spellcasting", x: 0, y: 48, w: 10, h: 12, ...LAYOUT_CONSTRAINTS.spellcasting },
    ],
    sm: [
        { i: "header", x: 0, y: 0, w: 6, h: 6, ...LAYOUT_CONSTRAINTS.header },
        { i: "hp", x: 0, y: 6, w: 6, h: 3, ...LAYOUT_CONSTRAINTS.hp },
        { i: "abilities", x: 0, y: 9, w: 6, h: 8, ...LAYOUT_CONSTRAINTS.abilities },
        { i: "saves", x: 0, y: 17, w: 6, h: 8, ...LAYOUT_CONSTRAINTS.saves },
        { i: "skills", x: 0, y: 25, w: 6, h: 12, ...LAYOUT_CONSTRAINTS.skills },
        { i: "species", x: 0, y: 37, w: 6, h: 10, ...LAYOUT_CONSTRAINTS.species },
        { i: "features", x: 0, y: 47, w: 6, h: 10, ...LAYOUT_CONSTRAINTS.features },
        { i: "combat", x: 0, y: 57, w: 6, h: 10, ...LAYOUT_CONSTRAINTS.combat },
        { i: "inventory", x: 0, y: 67, w: 6, h: 8, ...LAYOUT_CONSTRAINTS.inventory },
        { i: "spellcasting", x: 0, y: 75, w: 6, h: 12, ...LAYOUT_CONSTRAINTS.spellcasting },
    ],
    xs: [
        { i: "header", x: 0, y: 0, w: 4, h: 6, ...LAYOUT_CONSTRAINTS.header },
        { i: "hp", x: 0, y: 6, w: 4, h: 4, ...LAYOUT_CONSTRAINTS.hp },
        { i: "abilities", x: 0, y: 10, w: 4, h: 10, ...LAYOUT_CONSTRAINTS.abilities },
        { i: "saves", x: 0, y: 20, w: 4, h: 10, ...LAYOUT_CONSTRAINTS.saves },
        { i: "skills", x: 0, y: 30, w: 4, h: 12, ...LAYOUT_CONSTRAINTS.skills },
        { i: "species", x: 0, y: 42, w: 4, h: 10, ...LAYOUT_CONSTRAINTS.species },
        { i: "features", x: 0, y: 52, w: 4, h: 10, ...LAYOUT_CONSTRAINTS.features },
        { i: "combat", x: 0, y: 62, w: 4, h: 10, ...LAYOUT_CONSTRAINTS.combat },
        { i: "inventory", x: 0, y: 72, w: 4, h: 8, ...LAYOUT_CONSTRAINTS.inventory },
        { i: "spellcasting", x: 0, y: 80, w: 4, h: 12, ...LAYOUT_CONSTRAINTS.spellcasting },
    ],
    xxs: [
        { i: "header", x: 0, y: 0, w: 2, h: 8, ...LAYOUT_CONSTRAINTS.header },
        { i: "hp", x: 0, y: 8, w: 2, h: 4, ...LAYOUT_CONSTRAINTS.hp },
        { i: "abilities", x: 0, y: 12, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.abilities },
        { i: "saves", x: 0, y: 24, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.saves },
        { i: "skills", x: 0, y: 36, w: 2, h: 15, ...LAYOUT_CONSTRAINTS.skills },
        { i: "species", x: 0, y: 51, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.species },
        { i: "features", x: 0, y: 63, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.features },
        { i: "combat", x: 0, y: 75, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.combat },
        { i: "inventory", x: 0, y: 87, w: 2, h: 10, ...LAYOUT_CONSTRAINTS.inventory },
        { i: "spellcasting", x: 0, y: 97, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.spellcasting },
    ],
};

const SpellcastingWidget = ({ 
    hasSpellcasting, 
    classRules, 
    spellSlotsRules, 
    character, 
    availableSpells, 
    isLayoutLocked, 
    currentProficiencyBonus, 
    onOpenOverlay 
}) => {
    if (!hasSpellcasting || !classRules?.spellcasting || !spellSlotsRules || !character) return null;

    const spellcasting = classRules.spellcasting;
    const ability = spellcasting.ability || "intelligence";
    const abilityScore = character.data.abilities[ability.toLowerCase()] || 10;
    const mod = calculateModifier(abilityScore);
    const saveDC = 8 + currentProficiencyBonus + mod;
    const attackBonus = currentProficiencyBonus + mod;

    const progression = spellcasting.progression;
    const progressionKey = progression === "pact" ? "pact_magic" : progression;
    const slotsTable = spellSlotsRules[progressionKey];
    let availableSlotsObj = {};
    if (slotsTable) {
        let maxSlotLevel = character.level;
        while (maxSlotLevel > 0 && !slotsTable[maxSlotLevel]) {
            maxSlotLevel--;
        }
        if (maxSlotLevel > 0) {
            availableSlotsObj = slotsTable[maxSlotLevel];
        }
    }

    const selectedSpells = character.data.spells || [];

    return (
        <div className="spellcasting-content">
            {!isLayoutLocked && <div className="widget-handle">⠿</div>}
            <div className="spellcasting-header">
                <h3>Spellcasting</h3>
                <button className="manage-spells-btn" onClick={onOpenOverlay}>
                    📖 Manage Spells
                </button>
            </div>

            <div className="spell-stats-row">
                <div className="spell-stat-box">
                    <span className="spell-stat-label">Ability</span>
                    <span className="spell-stat-val">{ability.slice(0, 3).toUpperCase()}</span>
                </div>
                <div className="spell-stat-box">
                    <span className="spell-stat-label">Save DC</span>
                    <span className="spell-stat-val">{saveDC}</span>
                </div>
                <div className="spell-stat-box">
                    <span className="spell-stat-label">Attack Bonus</span>
                    <span className="spell-stat-val">+{attackBonus}</span>
                </div>
            </div>

            <div className="spell-slots-row">
                {Object.keys(availableSlotsObj).map(level => (
                    <div key={level} className="spell-slot-box">
                        <span className="slot-lvl">Lv {level}</span>
                        <span className="slot-count">{availableSlotsObj[level]}</span>
                    </div>
                ))}
                {Object.keys(availableSlotsObj).length === 0 && <span className="no-slots-msg">No spell slots available yet.</span>}
            </div>

            <div className="prepared-spells-list scrollable">
                {["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"].map(level => {
                    const spellsAtLevel = availableSpells?.[level] || [];
                    const selectedAtLevel = spellsAtLevel.filter(s => selectedSpells.includes(s.name));

                    if (selectedAtLevel.length === 0) return null;

                    return (
                        <div key={level} className="spell-level-group">
                            <h4>{level === "0" ? "Cantrips" : `Level ${level}`}</h4>
                            {selectedAtLevel.map(spell => (
                                <div key={spell.name} className="prepared-spell-row">
                                    <span className="spell-name">{spell.name}</span>
                                    <span className="spell-school">{spell.school}</span>
                                </div>
                            ))}
                        </div>
                    );
                })}
                {selectedSpells.length === 0 && <div className="no-spells-note">No spells selected. Click 'Manage Spells' to choose.</div>}
            </div>
        </div>
    );
};

const SpellOverlay = ({ 
    show, 
    minimized, 
    onClose, 
    onMinimize, 
    onRestore, 
    availableSpells, 
    character, 
    classRules, 
    spellSlotsRules,
    onToggleSpell 
}) => {
    if (!show || !availableSpells) return null;

    const selectedSpells = character.data.spells || [];
    const spellcasting = classRules?.spellcasting;
    const progression = spellcasting?.progression;
    const progressionKey = progression === "pact" ? "pact_magic" : progression;
    const slotsTable = progressionKey ? spellSlotsRules?.[progressionKey] : null;

    let maxAvailableSlot = 0;
    if (slotsTable) {
        let clvl = character.level;
        while (clvl > 0 && !slotsTable[clvl]) clvl--;
        if (clvl > 0) {
            const slots = slotsTable[clvl];
            maxAvailableSlot = Math.max(...Object.keys(slots).map(Number));
        }
    }

    const hasCantrips = !!(availableSpells?.["0"]?.length);
    const hintText = hasCantrips
        ? `Filtering by your max available spell slot level (Cantrips to Level ${maxAvailableSlot}). Spells chosen are saved automatically.`
        : `Filtering by your max available spell slot level (Level 1 to Level ${maxAvailableSlot}). Spells chosen are saved automatically.`;

    if (minimized) {
        return (
            <div className="spell-overlay-minimized">
                <span className="overlay-minimized-title">📖 Manage Spells</span>
                <button className="overlay-eye-btn" title="Restore spell panel" onClick={onRestore}>👁</button>
                <button className="close-btn overlay-close-min" onClick={onClose}>✕</button>
            </div>
        );
    }

    return (
        <div className="spell-overlay">
            <div className="spell-overlay-content">
                <div className="overlay-header">
                    <h2>Select Spells</h2>
                    <div className="overlay-header-actions">
                        <button className="overlay-eye-btn" title="Minimize — keep panel open while viewing character sheet" onClick={onMinimize}>👁</button>
                        <button className="close-btn" onClick={onClose}>✕</button>
                    </div>
                </div>
                <p className="overlay-hint">{hintText}</p>
                <div className="spell-overlay-list">
                    {Object.keys(availableSpells).map(level => {
                        if (parseInt(level) > maxAvailableSlot && level !== "0") return null;
                        const spellsAtLevel = availableSpells[level];

                        return (
                            <div key={level} className="overlay-level-group">
                                <h3>{level === "0" ? "Cantrips" : `Level ${level}`}</h3>
                                <div className="spell-selection-grid">
                                    {spellsAtLevel.map(spell => {
                                        const isSelected = selectedSpells.includes(spell.name);
                                        return (
                                            <div
                                                key={spell.name}
                                                className={`spell-select-card ${isSelected ? 'selected' : ''}`}
                                                onClick={() => onToggleSpell(spell.name)}
                                            >
                                                <div className="spell-name">{spell.name}</div>
                                                <div className="spell-school">{spell.school}</div>
                                                {isSelected && <div className="spell-check">✓</div>}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
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
    const [featureUses, setFeatureUses] = useState({}); // ID -> current uses
    const [weaponRules, setWeaponRules] = useState({});
    const [armorRules, setArmorRules] = useState({});
    const [activeFeatures, setActiveFeatures] = useState([]); // Array of IDs
    const [spellSlotsRules, setSpellSlotsRules] = useState(null);
    const [availableSpells, setAvailableSpells] = useState(null);
    const [showSpellOverlay, setShowSpellOverlay] = useState(false);
    const [spellOverlayMinimized, setSpellOverlayMinimized] = useState(false);


    // Drag and Drop state for Inventory
    const [draggedItemIndex, setDraggedItemIndex] = useState(null);
    const [dragOverItemIndex, setDragOverItemIndex] = useState(null);

    // New HP related states
    const [currentHp, setCurrentHp] = useState(0);
    const [baseMaxHp, setBaseMaxHp] = useState(0);
    const [effectiveMaxHp, setEffectiveMaxHp] = useState(0);

    // Consolidated Loading Logic
    useEffect(() => {
        const loadAllData = async () => {
            try {
                
                // 1. Fetch Global Rules first (Optional but good to have ready)
                const [weaponRes, armorRes, spellSlotsRes] = await Promise.all([
                    fetch(`http://localhost:5000/api/rules/weapons`),
                    fetch(`http://localhost:5000/api/rules/armor`),
                    fetch(`http://localhost:5000/api/rules/spell_slots`)
                ]);

                const wRules = await weaponRes.json();
                const aRules = await armorRes.json();
                const sSlotsRules = await spellSlotsRes.json();

                setWeaponRules(wRules);
                setArmorRules(aRules);
                setSpellSlotsRules(sSlotsRules);

                // 2. Fetch Character Data
                const charRes = await fetch(`http://localhost:5000/api/characters/${id}`);
                if (!charRes.ok) {
                    if (charRes.status === 404) throw new Error("Character not found");
                    throw new Error("Failed to load character");
                }
                const data = await charRes.json();
                
                // Set immediate basic state
                setCharacter(data);
                setSkills(data.data.skillProficiencies || {});
                setGold(data.data.gold || 0);
                setXp(data.data.xp || 0);
                setTempXp(data.data.xp || 0);
                setActiveFeatures(data.data.activeFeatures || []);
                setFeatureUses(data.data.featureUses || {});

                // Initialize HP
                const initialBaseMaxHp = data.data.hp_max_base || 0;
                const initialMaxHpModifier = data.data.hp_modifier || 0;
                setBaseMaxHp(initialBaseMaxHp);
                setEffectiveMaxHp(initialBaseMaxHp + initialMaxHpModifier);
                setCurrentHp(data.data.hp_current || 0);

                // 3. Normalize Inventory (Needs wRules and aRules)
                const rawInventory = data.data.inventory || [];
                const normalizedInventory = rawInventory.map(item => {
                    let normalized = typeof item === 'string' ? { name: item, quantity: 1, category: "Other", equipped: false } : { equipped: false, ...item };
                    if (typeof item === 'string') {
                        const match = item.match(/^(\d+)\s+(.*)$/);
                        if (match) { normalized.quantity = parseInt(match[1]); normalized.name = match[2]; }
                    }
                    if (normalized.name.endsWith('s') && !wRules[normalized.name]) {
                        const singular = normalized.name.slice(0, -1);
                        if (wRules[singular]) { normalized.name = singular; normalized.category = "Weapon"; }
                    } else if (wRules[normalized.name]) { normalized.category = "Weapon"; }
                    if (aRules[normalized.name]) normalized.category = "Armor";
                    return normalized;
                });
                setInventoryItems(normalizedInventory);

                // 4. Fetch Specific Rules (Parallel)
                const rulePromises = [];
                if (data.class?.name) {
                    rulePromises.push(fetch(`http://localhost:5000/api/classes/${data.class.name.toLowerCase()}`).then(r => r.json()));
                    rulePromises.push(fetch(`http://localhost:5000/api/spells/${data.class.name.toLowerCase()}`).then(r => r.json()));
                }
                if (data.data?.species) {
                    rulePromises.push(fetch(`http://localhost:5000/api/species`).then(r => r.json()));
                }
                if (data.data?.background) {
                    rulePromises.push(fetch(`http://localhost:5000/api/backgrounds`).then(r => r.json()));
                }

                const ruleResults = await Promise.all(rulePromises);
                let resultIdx = 0;

                let resolvedClassRules = null;
                if (data.class?.name) {
                    resolvedClassRules = ruleResults[resultIdx++];
                    setClassRules(resolvedClassRules);
                    setAvailableSpells(ruleResults[resultIdx++]);
                }
                
                if (data.data?.species) {
                    const speciesList = ruleResults[resultIdx++];
                    const species = speciesList.find(s => s.name.toLowerCase() === data.data.species.toLowerCase());
                    if (species) setSpeciesRules(species);
                }

                if (data.data?.background) {
                    const bgList = ruleResults[resultIdx++];
                    const bg = bgList.find(b => b.name.toLowerCase() === data.data.background.toLowerCase());
                    if (bg) setBackgroundRules(bg);
                }

                // 5. Final Step: Layout Initialization
                // Now that we have all rules, checks like hasSpellcasting will be accurate
                if (data.data?.layout) {
                    const mergedLayout = { ...data.data.layout };
                    Object.keys(DEFAULT_LAYOUTS).forEach(bp => {
                        const defaultForBp = DEFAULT_LAYOUTS[bp];
                        const savedForBp = mergedLayout[bp] || [];
                        const savedKeys = new Set(savedForBp.map(item => item.i));
                        const updatedSaved = savedForBp.map(item => {
                            const constraints = LAYOUT_CONSTRAINTS[item.i];
                            if (constraints) {
                                const merged = { ...item, ...constraints };
                                if (constraints.minH && merged.h < constraints.minH) merged.h = constraints.minH;
                                if (constraints.minW && merged.w < constraints.minW) merged.w = constraints.minW;
                                return merged;
                            }
                            return item;
                        });
                        defaultForBp.forEach(defaultItem => {
                            if (!savedKeys.has(defaultItem.i)) updatedSaved.push(defaultItem);
                        });
                        mergedLayout[bp] = updatedSaved;
                    });
                    setLayout(mergedLayout);
                }

                setLoading(false);

            } catch (err) {
                console.error("Load failed:", err);
                setError(err.message);
                setLoading(false);
            }
        };

        loadAllData();
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

    const toggleFeatureActive = (featureId, maxUses) => {
        setActiveFeatures(prev => {
            let next;
            if (prev.includes(featureId)) {
                next = prev.filter(id => id !== featureId);
            } else {
                // Check if we have uses left
                const currentUses = featureUses[featureId] !== undefined ? featureUses[featureId] : maxUses;
                if (currentUses <= 0) return prev; // No uses left

                next = [...prev, featureId];
                // Consume use
                setFeatureUses(u => {
                    const newUses = { ...u, [featureId]: currentUses - 1 };
                    saveCharacter({ featureUses: newUses });
                    return newUses;
                });
            }
            saveCharacter({ activeFeatures: next });
            return next;
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

    const toggleEquip = (targetItem) => {
        setInventoryItems(prev => {
            const isShield = armorRules[targetItem.name]?.type === "Shield";

            const next = prev.map((item, idx) => {
                if (idx === targetItem.originalIndex) {
                    return { ...item, equipped: !item.equipped };
                }
                // Only allow one armor to be equipped at a time (excluding shields)
                if (!isShield && item.equipped && armorRules[item.name] && armorRules[item.name].type !== "Shield") {
                    return { ...item, equipped: false };
                }
                return item;
            });
            saveCharacter({ inventory: next });
            return next;
        });
    };

    const removeItem = (itemToRemove) => {
        if (itemToRemove.quantity > 1) {
            const removeOne = window.confirm(`This item has ${itemToRemove.quantity} copies. \n\nClick OK to remove JUST ONE copy, or CANCEL to remove the ENTIRE STACK.`);

            if (removeOne) {
                // Remove just one
                const newInventory = inventoryItems.map(item =>
                    item === itemToRemove ? { ...item, quantity: item.quantity - 1 } : item
                );
                setInventoryItems(newInventory);
                saveCharacter({ inventory: newInventory });
            } else {
                // Confirm total removal
                if (window.confirm(`Are you sure you want to remove ALL copies of ${itemToRemove.name}?`)) {
                    const newInventory = inventoryItems.filter(item => item !== itemToRemove);
                    setInventoryItems(newInventory);
                    saveCharacter({ inventory: newInventory });
                }
            }
        } else {
            if (window.confirm(`Are you sure you want to remove ${itemToRemove.name} from your inventory?`)) {
                const newInventory = inventoryItems.filter(item => item !== itemToRemove);
                setInventoryItems(newInventory);
                saveCharacter({ inventory: newInventory });
            }
        }
    };

    const groupedInventory = useMemo(() => inventoryItems.reduce((acc, item, originalIndex) => {
        let category = item.category || "Other";
        if (armorRules[item.name]) category = "Armor";
        else if (weaponRules[item.name]) category = "Weapon";

        const itemWithCat = { ...item, category, originalIndex };

        if (!acc[category]) acc[category] = [];
        acc[category].push(itemWithCat);
        return acc;
    }, { "All": inventoryItems.map((it, idx) => ({ ...it, originalIndex: idx })) }), [inventoryItems, armorRules, weaponRules]);

    const displayedItems = groupedInventory[inventoryFilter] || [];

    // --- Drag and Drop Handlers for Inventory ---
    const handleDragStart = (e, index) => {
        setDraggedItemIndex(index);
        e.dataTransfer.effectAllowed = "move";
        // Required for Firefox
        e.dataTransfer.setData("text/plain", index);

        // Add a class for visual feedback
        e.target.classList.add('dragging');
    };

    const handleDragOver = (e, index) => {
        e.preventDefault();
        if (draggedItemIndex === null || draggedItemIndex === index) return;
        setDragOverItemIndex(index);
    };

    const handleDrop = (e, index) => {
        e.preventDefault();
        if (draggedItemIndex === null) return;

        const newItems = [...inventoryItems];
        // We need to map the filtered indices back to the original indices if we filter, 
        // but the user wants to reorder the *list* he sees. 
        // For simplicity, if we are in "All" filter, it's direct.
        // If we are in a sub-category, it gets complex. 
        // User said: "reorder them however they want... just like the various windows"
        // Most premium sheets only allow reordering when in "All" view or they reorder within the category.

        const draggedItem = newItems[draggedItemIndex];
        newItems.splice(draggedItemIndex, 1);
        newItems.splice(index, 0, draggedItem);

        setInventoryItems(newItems);
        saveCharacter({ inventory: newItems });

        setDraggedItemIndex(null);
        setDragOverItemIndex(null);
    };

    const handleDragEnd = (e) => {
        e.target.classList.remove('dragging');
        setDraggedItemIndex(null);
        setDragOverItemIndex(null);
    };

    // --- Rich Rendering Components ---

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

    const ac = useMemo(() => {
        if (!character) return 10;

        const dexMod = calculateModifier(character.data.abilities.dexterity);
        const conMod = calculateModifier(character.data.abilities.constitution);

        let baseAC = 10;
        let dexBonus = dexMod;
        let shieldBonus = 0;

        const equippedArmor = inventoryItems.find(item => item.equipped && armorRules[item.name] && armorRules[item.name].type !== "Shield");
        const equippedShield = inventoryItems.find(item => item.equipped && armorRules[item.name] && armorRules[item.name].type === "Shield");

        if (equippedShield) {
            shieldBonus = armorRules[equippedShield.name]?.bonus || 2;
        }

        if (equippedArmor) {
            const rules = armorRules[equippedArmor.name];
            baseAC = rules.baseAC;
            if (rules.dexLimit !== null) {
                dexBonus = Math.min(dexMod, rules.dexLimit);
            }
        } else {
            // Unarmored
            const hasBarbarianUnarmored = availableFeatures.some(f => f.id === "barbarian_unarmored_defense");
            if (hasBarbarianUnarmored) {
                baseAC = 10;
                dexBonus = dexMod + conMod;
            } else {
                baseAC = 10;
                dexBonus = dexMod;
            }
        }

        return baseAC + dexBonus + shieldBonus;
    }, [character, inventoryItems, armorRules, availableFeatures]);


    // --- Dynamic Defenses Logic ---
    const defenses = useMemo(() => {
        const result = { resistances: [], immunities: [] };
        if (!availableFeatures) return result;

        availableFeatures.forEach(f => {
            // Check if feature is passive or active
            const isRage = f.id === "barbarian_rage";
            const isActive = activeFeatures.includes(f.id);

            // Rage resistances only apply when active
            if (isRage && !isActive) return;

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
    }, [availableFeatures, activeFeatures]);

    const filteredFeatures = useMemo(() => {
        // Only show Class, Subclass, and Background features in the general widget
        const generalFeatures = availableFeatures.filter(f => f.source !== 'Species');

        if (featureFilter === "All") return generalFeatures;

        return generalFeatures.filter(f => {
            // Priority 1: Explicit Action field in details
            const explicitAction = f.details?.Action || f.details?.action;
            if (explicitAction) {
                const lowerAction = explicitAction.toLowerCase();
                if (featureFilter === "Action") return lowerAction === "action";
                if (featureFilter === "Bonus Action") return lowerAction === "bonus action";
                if (featureFilter === "Reaction") return lowerAction === "reaction";
                if (featureFilter === "Passive") return lowerAction === "passive";
            }

            // Priority 2: Fallback to smart text matching for legacy data
            const actionText = (f.summary || f.description || "").toLowerCase();
            if (featureFilter === "Action") return actionText.includes("action") && !actionText.includes("bonus action");
            if (featureFilter === "Bonus Action") return actionText.includes("bonus action");
            if (featureFilter === "Reaction") return actionText.includes("reaction");
            if (featureFilter === "Passive") {
                return !actionText.includes("action") && !actionText.includes("reaction") && !actionText.includes("bonus action");
            }
            return true;
        });
    }, [availableFeatures, featureFilter]);

    const toggleFeature = (id) => {
        setExpandedFeatures(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const toggleSpellSelection = (name) => {
        const selectedSpells = character.data.spells || [];
        const current = [...selectedSpells];
        if (current.includes(name)) {
            // Remove
            const updated = current.filter(n => n !== name);
            saveCharacter({ spells: updated });
            setCharacter(prev => ({ ...prev, data: { ...prev.data, spells: updated } }));
        } else {
            // Add
            current.push(name);
            saveCharacter({ spells: current });
            setCharacter(prev => ({ ...prev, data: { ...prev.data, spells: current } }));
        }
    };

    const hasSpellcasting = useMemo(() => {
        return availableFeatures.some(f => f.name === "Spellcasting" || f.name === "Pact Magic");
    }, [availableFeatures]);

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
                layouts={layout || DEFAULT_LAYOUTS}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={30}
                margin={[40, 40]}
                compactType="vertical"
                preventCollision={false}
                isDraggable={!isLayoutLocked}
                isResizable={!isLayoutLocked}
                onLayoutChange={(current, all) => {
                    if (isLayoutLocked || loading) return;
                    setLayout(all);
                    saveCharacter({ layout: all });
                }}
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
                            <div className="ac-display" title="Armor Class">
                                <div className="ac-shield">
                                    <span className="ac-value">{ac}</span>
                                    <span className="ac-label">AC</span>
                                </div>
                            </div>
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
                            const hasAdvantage = key === "strength" && activeFeatures.includes("barbarian_rage");
                            return (
                                <div key={key} className={`ability-box ${hasAdvantage ? 'has-adv' : ''}`}>
                                    <span className="ability-name">{name.slice(0, 3).toUpperCase()}</span>
                                    <span className="ability-mod">{mod >= 0 ? "+" : ""}{mod}</span>
                                    <span className="ability-score">{score}</span>
                                    {hasAdvantage && <div className="adv-indicator" title="Advantage from Rage">✧ ADV</div>}
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
                            const hasAdvantage = key === "strength" && activeFeatures.includes("barbarian_rage");
                            return (
                                <div key={key} className={`save-row ${hasAdvantage ? 'has-adv' : ''}`}>
                                    <span className={`prof-dot ${isProficient ? "fill" : ""}`}></span>
                                    <span className="save-name">{name}</span>
                                    <span className="save-total">
                                        {total >= 0 ? "+" : ""}{total}
                                        {hasAdvantage && <span className="adv-note">Advantage</span>}
                                    </span>
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
                                isActive={activeFeatures.includes(f.id)}
                                onActivate={toggleFeatureActive}
                                currentUses={featureUses[f.id]}
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
                                    isActive={activeFeatures.includes(f.id)}
                                    onActivate={toggleFeatureActive}
                                    currentUses={featureUses[f.id]}
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
                            activeFeatures={activeFeatures}
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
                            <div
                                key={idx}
                                className={`inventory-row ${dragOverItemIndex === idx ? 'drag-over' : ''} ${draggedItemIndex === idx ? 'is-dragging' : ''}`}
                                draggable={inventoryFilter === "All"}
                                onDragStart={(e) => handleDragStart(e, idx)}
                                onDragOver={(e) => handleDragOver(e, idx)}
                                onDrop={(e) => handleDrop(e, idx)}
                                onDragEnd={handleDragEnd}
                            >
                                <div className="inv-item-info">
                                    <span className="drag-handle">⠿</span>
                                    <span className="item-name">{item.name}</span>
                                    {item.quantity > 1 && <span className="item-qty">x{item.quantity}</span>}
                                    <span className="item-cat-tag">{item.category}</span>
                                    {item.equipped && <span className="equipped-tag">E</span>}
                                </div>
                                <div className="inv-item-actions">
                                    {item.category === "Armor" && (
                                        <button
                                            className={`equip-btn ${item.equipped ? 'equipped' : ''}`}
                                            onClick={() => toggleEquip(item)}
                                        >
                                            {item.equipped ? "Unequip" : "Equip"}
                                        </button>
                                    )}
                                    <button className="del-btn" onClick={() => removeItem(item)}>✕</button>
                                </div>
                            </div>
                        ))}
                        {inventoryFilter !== "All" && (
                            <div className="inv-reorder-hint">
                                * Reordering is only available in the "All" view.
                            </div>
                        )}
                    </div>
                </div>
                {hasSpellcasting && (
                    <div key="spellcasting" className="widget card spellcasting-widget">
                        <SpellcastingWidget 
                            hasSpellcasting={hasSpellcasting}
                            classRules={classRules}
                            spellSlotsRules={spellSlotsRules}
                            character={character}
                            availableSpells={availableSpells}
                            isLayoutLocked={isLayoutLocked}
                            currentProficiencyBonus={currentProficiencyBonus}
                            onOpenOverlay={() => { setShowSpellOverlay(true); setSpellOverlayMinimized(false); }}
                        />
                    </div>
                )}
            </ResponsiveGridLayout>

            <SpellOverlay 
                show={showSpellOverlay}
                minimized={spellOverlayMinimized}
                onClose={() => setShowSpellOverlay(false)}
                onMinimize={() => setSpellOverlayMinimized(true)}
                onRestore={() => setSpellOverlayMinimized(false)}
                availableSpells={availableSpells}
                character={character}
                classRules={classRules}
                spellSlotsRules={spellSlotsRules}
                onToggleSpell={toggleSpellSelection}
            />



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