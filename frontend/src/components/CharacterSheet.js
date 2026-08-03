import { useEffect, useState, useCallback, useMemo } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { Responsive, WidthProvider } from "react-grid-layout/legacy";
import { useAuth } from "../context/AuthContext";
import { useNotification } from "../context/NotificationContext";

import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "../styles/CharacterSheet.css";
import "../styles/LevelUpPreview.css";
import RestOverlay from './RestOverlay';
import StatModifierOverlay from './StatModifierOverlay';
import LevelUpOverlay from "./LevelUpOverlay";
import NotesWidget from "./NotesWidget";
import BackToTop from "./common/BackToTop";
import API_BASE_URL from "../config";

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

    let bestValue = null;
    let highestLevelFound = -1;

    for (const [range, value] of Object.entries(scalingData)) {
        // Handle "1-8" range strings
        const parts = range.split('-');
        if (parts.length === 2) {
            const min = parseInt(parts[0]);
            const max = parseInt(parts[1]);
            if (level >= min && level <= max) return value;
        }

        // Handle "17+" style
        else if (range.endsWith('+')) {
            const min = parseInt(range);
            if (level >= min) {
                // For milestone style, we want the highest min that is <= level
                if (min > highestLevelFound) {
                    highestLevelFound = min;
                    bestValue = value;
                }
            }
        }

        // Handle single level milestones or specific levels
        else {
            const milestone = parseInt(range);
            if (!isNaN(milestone) && level >= milestone) {
                if (milestone > highestLevelFound) {
                    highestLevelFound = milestone;
                    bestValue = value;
                }
            }
        }
    }

    return bestValue;
};

const getChoiceLimitForFeature = (feature, level) => {
    if (!feature || !feature.details) return 1;
    const details = feature.details;

    // 1. Explicit choice limit
    if (details.choice?.choose) return details.choice.choose;

    // 2. Weapon Mastery Scaling (generic or class-specific)
    const wmScaling = details.weapons_mastered?.scaling || details.Scaling;
    if (wmScaling) {
        const val = resolveScalingValue(wmScaling, level);
        if (typeof val === 'number') return val;
        if (typeof val === 'string') {
            const match = val.match(/(\d+)/);
            if (match) return parseInt(match[1]);
        }
    }

    // 3. Simple numeric limits
    if (typeof details.masteries === 'number') return details.masteries;
    if (typeof details.number_to_choose === 'number') return details.number_to_choose;

    return 1;
};

/**
 * Checks if a feature or feat prerequisite is met by the character.
 * Handles strings like "Level 4+", "Strength 13+", and nested OR conditions.
 */
const checkPrerequisites = (prerequisite, character, level = 1, classRules = null) => {
    if (!prerequisite || !character) return null;

    const checkSingle = (req) => {
        if (typeof req !== 'string') return null;

        // 1. Level check
        const levelMatch = req.match(/Level\s+(\d+)/i);
        if (levelMatch) {
            const reqLevel = parseInt(levelMatch[1]);
            if (level < reqLevel) return req;
        }

        // 2. Ability score check
        const abilityMatch = req.match(/(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)\s+(\d+)/i);
        if (abilityMatch) {
            const ability = abilityMatch[1].toLowerCase();
            const reqScore = parseInt(abilityMatch[2]);
            const currentScore = character.data?.abilities?.[ability] || 10;
            if (currentScore < reqScore) return req;
        }

        // 3. Armor/Weapon Training check (Simplified)
        if (req.includes('Armor Training') || req.includes('Weapon Proficiency')) {
            // This would ideally check character.proficiencies, but simple string check for now
            // if (!character.data.proficiencies?.includes(req)) return req;
        }

        // 4. Spellcasting Feature
        if (req.includes('Spellcasting Feature') || req.includes('Pact Magic')) {
            const hasMagic = !!(classRules?.spellcasting || character.class?.spellcasting);
            if (!hasMagic) return req;
        }

        return null;
    };

    if (typeof prerequisite === 'string') return checkSingle(prerequisite);

    if (Array.isArray(prerequisite)) {
        // Find failed requirements
        const failed = [];
        for (const req of prerequisite) {
            if (Array.isArray(req)) {
                // Nested list is an OR condition
                const anyMet = req.some(r => !checkSingle(r));
                if (!anyMet) failed.push(`(${req.join(' or ')})`);
            } else {
                const error = checkSingle(req);
                if (error) failed.push(error);
            }
        }
        return failed.length > 0 ? failed.join(' and ') : null;
    }

    return null;
};

/**
 * Renders comparison details for Ability Score Improvements and warnings for unmet prerequisites.
 */
const PreviewChoiceDetails = ({ feature, choice, character, level }) => {
    if (!choice) return null;

    const choiceName = typeof choice === 'string' ? choice : (choice.name || choice.id);
    const result = [];

    // 0. Special Handling for "Feat" option in ASI list
    if (choiceName === 'Feat') {
        result.push(<div key="feat-inst" className="preview-choice-instruction">Select a specific feat from the choice menu.</div>);
    }


    // 1. ASI Comparison Display
    const abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"];
    if (abilities.includes(choiceName)) {
        const key = choiceName.toLowerCase();
        const currentScore = character.data?.abilities?.[key] || 10;
        const currentMod = Math.floor((currentScore - 10) / 2);

        // Typically ASI is +2 or two +1s. For simplicity in preview, assume +2 if chosen
        const newScore = currentScore + 2;
        const newMod = Math.floor((newScore - 10) / 2);

        result.push(
            <div key="asi" className="asi-preview-comparison">
                <span className="comparison-label">{choiceName}:</span>
                <span className="comparison-val">{currentScore} ({currentMod >= 0 ? '+' : ''}{currentMod})</span>
                <span className="comparison-arrow">→</span>
                <span className="comparison-val highlight">{newScore} ({newMod >= 0 ? '+' : ''}{newMod})</span>
            </div>
        );
    }

    // 2. Feat Prerequisite Checking
    if (typeof choice === 'object' && choice.prerequisite) {
        const warning = checkPrerequisites(choice.prerequisite, character, level);
        if (warning) {

            result.push(
                <div key="warning" className="prereq-warning-box">
                    <div className="warning-header">
                        <i className="fa-solid fa-circle-exclamation"></i>
                        <span>PREREQUISITE NOT MET</span>
                    </div>
                    <p>Normally, you would not be able to choose this because: <strong>{warning}</strong></p>
                </div>
            );
        }
    }

    return result.length > 0 ? <div className="preview-extra-info">{result}</div> : null;
};


/**
 * Simple processor to handle **bold** or *bold* text in descriptions.
 * Returns an array of React elements/strings.
 */
const processRichText = (text) => {
    if (typeof text !== 'string' || !text) return text;
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
    const rageActive = activeFeatureIds.includes("barbarian_rage");
    let notes = data.properties.join(", ");

    if (data.mastery && data.mastery.length > 0) {
        notes += (notes ? ", " : "") + `Mastery: ${data.mastery[0]}`;
    }

    if (rageActive && usedStrForDamage) {
        let rageBonus = 2;

        if (level >= 16) rageBonus = 4;
        else if (level >= 9) rageBonus = 3;
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

export const ValueRenderer = ({ value, level, themeRole, label }) => {
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

const CombatWidget = ({ character, inventory, features, profBonus, weaponRules, activeFeatures, viewOnly }) => {
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

const RichFeature = ({
    feature, isExpanded, onToggle, level, isActive, onActivate, currentUses,
    characterData, classRules, allClassRules, ruleOptions, featureChoices, onUpdateChoice, availableSpells,
    viewOnly, isAuthorized, featureNotes, setFeatureNotes
}) => {
    const maxUsesData = feature.details?.uses;
    const maxUses = maxUsesData ? resolveScalingValue(maxUsesData, level) : null;
    const hasUses = maxUses !== null;
    const isActivatable = feature.id === "barbarian_rage";

    const rawChoice = featureChoices?.[feature.id];
    const currentChoices = Array.isArray(rawChoice) ? rawChoice : (rawChoice ? [rawChoice] : []);
    const options = resolveOptionsForFeature(feature, characterData, classRules, allClassRules, ruleOptions, availableSpells);
    const flatOptions = Array.isArray(options)
        ? options
        : Object.values(options).flat();
    const hasOptions = flatOptions.length > 0;
    const choiceLimit = getChoiceLimitForFeature(feature, level);
    const hasChoices = hasOptions && choiceLimit > 0;

    // Resolve the chosen options details
    const chosenOptionsDetails = currentChoices.map(choice => {
        const found = flatOptions.find(o => (typeof o === 'string' ? o : (o.id || o.name)) === choice);
        return found ? (typeof found === 'string' ? { name: found } : found) : { name: choice };
    });

    return (
        <div className={`feature-card ${isExpanded ? "expanded" : "collapsed"} source-${feature.source || 'unknown'} ${isActive ? 'is-active' : ''}`}>
            <div className="feature-title" onClick={() => onToggle(feature.id)}>
                <div className="feature-title-left">
                    <span className="feature-name">{feature.name}</span>
                    {chosenOptionsDetails.map((opt, idx) => (
                        <span key={idx} className="feature-choice-badge">{opt.name}</span>
                    ))}
                    <span className="feature-source-tag">{feature.source}</span>
                    {isActive && <span className="active-tag">ACTIVE</span>}
                </div>
                <div className="feature-title-right">
                    {/* Allow Weapon Mastery choices even in View Mode for owners (Long Rest rule) */}
                    {((!viewOnly || (feature.id.includes('weapon_mastery') && isAuthorized)) && hasChoices) && (
                        <button
                            className={`feature-choice-btn ${feature.type === 'subclass_choice' && currentChoices.length > 0 ? 'locked' : ''}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                onUpdateChoice(feature, options);
                            }}
                        >
                            {feature.type === 'subclass_choice' && currentChoices.length > 0
                                ? 'Locked'
                                : (currentChoices.length > 0 ? (currentChoices.length < choiceLimit ? 'Complete' : 'Change') : 'Choose')}
                        </button>
                    )}
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
                    {!viewOnly && isActivatable && (
                        <button
                            className={`activate-btn ${isActive ? 'active' : ''} ${hasUses && currentUses === 0 ? 'disabled' : ''}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                onActivate(feature.id);
                            }}
                            disabled={!isActive && (currentUses ?? maxUses ?? 0) <= 0}
                            title={!isActive && (currentUses ?? 0) <= 0
                                ? "You have 0 uses for this feature. Check description to know how to gain them."
                                : ""}
                        >
                            {isActive ? "Deactive" : "Activate!"}
                        </button>
                    )}
                    {feature.summary && <p className="feature-summary"><strong>Summary:</strong> {processRichText(feature.summary)}</p>}
                    {feature.prerequisite && (() => {
                        const warning = checkPrerequisites(feature.prerequisite, characterData, level, classRules);
                        return (
                            <div className={`feat-prerequisite-line ${warning ? 'unmet' : 'met'}`}>
                                <span className="prereq-icon">{warning ? '⚠' : '✓'}</span>
                                <span className="prereq-text">
                                    Prerequisite: {Array.isArray(feature.prerequisite) ? feature.prerequisite.flat().join(', ') : feature.prerequisite}
                                </span>
                                {warning && (
                                    <span className="prereq-warning-inline"> — Not met: {warning}</span>
                                )}
                            </div>
                        );
                    })()}
                    {feature.effects && Array.isArray(feature.effects) && (
                        <div className="feat-effects-list">
                            {feature.effects.map((eff, i) => (
                                <p key={i} className="feat-effect-item">{processRichText(eff)}</p>
                            ))}
                        </div>
                    )}
                    {feature.description && (
                        <div className="feature-description">
                            {feature.description.split('\n').map((para, i) => (
                                <p key={i}>{processRichText(para)}</p>
                            ))}
                        </div>
                    )}
                    {chosenOptionsDetails.length > 0 && (
                        <div className="chosen-options-list">
                            {chosenOptionsDetails.map((opt, idx) => {
                                const subChoiceId = `${feature.id}_sub_${idx}`;
                                const rawSubChoice = featureChoices?.[subChoiceId];
                                const currentSubChoices = Array.isArray(rawSubChoice) ? rawSubChoice : (rawSubChoice ? [rawSubChoice] : []);
                                // Check if this option (feat) has its own choices
                                const hasSubChoices = !!opt.choice;
                                return (
                                    <div key={idx} className="chosen-option-block">
                                        <div className="chosen-option-header">
                                            <h4>Selected: {opt.name}</h4>
                                            {!viewOnly && hasSubChoices && (
                                                <button
                                                    className="feature-choice-btn sub-choice-btn"
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        // Create a virtual feature for the sub-choice overlay
                                                        const virtualFeature = {
                                                            ...feature,
                                                            id: subChoiceId,
                                                            name: `${opt.name} Choice`,
                                                            details: { choice: opt.choice }
                                                        };
                                                        onUpdateChoice(virtualFeature, opt.choice.options);
                                                    }}
                                                >
                                                    {currentSubChoices.length > 0 ? 'Change' : 'Choose'}
                                                </button>
                                            )}
                                        </div>
                                        {currentSubChoices.length > 0 && (
                                            <div className="sub-choice-badges">
                                                {currentSubChoices.map((c, i) => (
                                                    <span key={i} className="feature-choice-badge sub-badge">{c}</span>
                                                ))}
                                            </div>
                                        )}
                                        {opt.summary && (
                                            <p className="option-summary-line">
                                                {processRichText(opt.summary)}
                                            </p>
                                        )}
                                        {opt.description && (
                                            <div className="chosen-feat-description">
                                                {opt.description.split("\n").map((line, i) => (
                                                    <p key={i}>{processRichText(line)}</p>
                                                ))}
                                            </div>
                                        )}
                                        {opt.effects && Array.isArray(opt.effects) && (
                                            <div className="chosen-feat-effects">
                                                {opt.effects.map((effect, i) => (
                                                    <p key={i} className="chosen-feat-effect">
                                                        {processRichText(effect)}
                                                    </p>
                                                ))}
                                            </div>
                                        )}
                                        {opt.benefit && (
                                            <p>{processRichText(opt.benefit)}</p>
                                        )}
                                        {opt.details && (
                                            <div className="option-details">
                                                <ValueRenderer value={opt.details} level={level} />
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    )}

                    {feature.details && (
                        <div className="feature-details">
                            <ValueRenderer value={feature.details} level={level} themeRole="view_only" />
                        </div>
                    )}
                    <div className="feature-notes-section">
                        <label className="feature-notes-label">
                            Notes ({(featureNotes?.[feature.id] || "").replace(/\s/g, "").length}/1000)
                        </label>

                        <textarea
                            className="feature-notes-input"
                            value={featureNotes?.[feature.id] || ""}
                            maxLength={2000}
                            placeholder="Write personal notes for this feature..."
                            onChange={(e) => {
                                const value = e.target.value;

                                const nonSpaceCount = value.replace(/\s/g, "").length;

                                if (nonSpaceCount > 1000) return;

                                setFeatureNotes(prev => ({
                                    ...prev,
                                    [feature.id]: value
                                }));
                            }}
                        >
                        </textarea>
                    </div>
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
    spellcasting: { minW: 6, maxW: 12, minH: 12, maxH: 15 },
    notes: { minW: 2, maxW: 4, minH: 11, maxH: 11 },
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
        { i: "notes", x: 0, y: 20, w: 4, h: 12, ...LAYOUT_CONSTRAINTS.notes },
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
        { i: "notes", x: 5, y: 23, w: 5, h: 12, ...LAYOUT_CONSTRAINTS.notes },
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
        { i: "notes", x: 0, y: 37, w: 6, h: 12, ...LAYOUT_CONSTRAINTS.notes },
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
        { i: "notes", x: 0, y: 42, w: 4, h: 12, ...LAYOUT_CONSTRAINTS.notes },
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
        { i: "notes", x: 0, y: 51, w: 2, h: 15, ...LAYOUT_CONSTRAINTS.notes },
        { i: "inventory", x: 0, y: 87, w: 2, h: 10, ...LAYOUT_CONSTRAINTS.inventory },
        { i: "spellcasting", x: 0, y: 97, w: 2, h: 12, ...LAYOUT_CONSTRAINTS.spellcasting },
    ],
};

const resolveOptionsForFeature = (feature, characterData, classRules, allClassRules, ruleOptions, availableSpells, targetChoiceId = null) => {
    if (!feature) return [];

    // Handle sub-choices for a specific chosen option
    if (targetChoiceId) {
        // Find the choice object in ruleOptions (usually a feat)
        const allFeats = [...(ruleOptions.origin || []), ...(ruleOptions.general || []), ...(ruleOptions.fighting_style || []), ...(ruleOptions.epic_boon || [])];
        const chosenFeat = allFeats.find(f => (f.id || f.name) === targetChoiceId);
        if (chosenFeat && chosenFeat.choice) {
            return chosenFeat.choice.options || [];
        }
        return [];
    }

    const id = feature.id;
    const details = feature.details || {};

    // 1. Static Options from Details or details.choice
    // Note: Skip fast-path for subclasses so they can be prettified below
    if (details.choice?.options && !id.toLowerCase().includes('subclass')) return details.choice.options;
    if (details.expertise_choice_options) return details.expertise_choice_options;
    if (details.skills_affected) return details.skills_affected;

    // 2. Global Rule Options
    if (id.toLowerCase().includes('weapon_mastery')) {
        const weapons = ruleOptions.weapons || {};
        const masteries = ruleOptions.weapon_mastery || {};

        const weaponOptions = Object.entries(weapons)
            .filter(([_, data]) => data.mastery && (Array.isArray(data.mastery) ? data.mastery.length > 0 : true))
            .map(([name, data]) => {
                const masteryKey = Array.isArray(data.mastery) ? data.mastery[0] : data.mastery;
                const masteryData = masteries[masteryKey] || {};

                // Construct detailed description
                let desc = `**Stats:** ${data.damage || '1d4'} ${data.type || 'Physical'}. `;
                if (data.properties?.length > 0) desc += `${data.properties.join(', ')}. `;
                if (data.range) desc += `Range: ${data.range}. `;
                if (data.reach) desc += `Reach: ${data.reach}. `;

                desc += `\n\n**Mastery: ${masteryKey}**\n${masteryData.description || 'No description available.'}`;

                return {
                    id: name,
                    name: name,
                    description: desc
                };
            })
            .sort((a, b) => a.name.localeCompare(b.name));

        return weaponOptions;
    }
    if (id.includes('fighting_style')) return ruleOptions.fighting_style || [];
    if (id === 'sorcerer_metamagic') return Object.values(ruleOptions.metamagic || {});
    if (id === 'warlock_eldritch_invocations') return Object.values(ruleOptions.invocations || {});

    // 3. Subclasses
    if (feature.type === "subclass_choice" || id.includes("_subclass")) {
        // Use the rules for the class that owns this feature
        const ownerRules =
            allClassRules?.[feature.classId] || classRules;

        const subclasses = ownerRules?.subclasses || {};

        return Object.keys(subclasses).map(key => {
            let prettyName = subclasses[key].name || key;
            prettyName = prettyName.replace(/^Path Of The /i, '');
            prettyName = prettyName
                .split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');

            return {
                id: key,
                name: prettyName,
                description:
                    subclasses[key].description ||
                    subclasses[key].summary
            };
        });
    }

    // 4. Feats/Boons
    if ((id.includes('feat_or_asi') || id.includes('epic_boon')) && !id.startsWith('chosen_feat_')) {
        return {
            origin: ruleOptions.origin || [],
            general: ruleOptions.general || [],
            epic_boon: id.includes('epic_boon') ? (ruleOptions.epic_boon || []) : []
        };
    }

    // 5. Dynamic Lists (Expertise, Spells)
    // Map internal proficiency keys to display names
    const getProfName = (key) => key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

    // Character proficiencies (true/false map)
    const profMap = characterData.data?.skillProficiencies || {};
    const expertiseMap = characterData.data?.skillExpertise || {};

    const proficiencies = Object.keys(profMap).filter(k => profMap[k]);
    const expertise = Object.keys(expertiseMap).filter(k => expertiseMap[k]);

    if (id.includes('expertise') || id.includes('deft_explorer')) {
        const available = proficiencies.filter(p => !expertise.includes(p));
        return available.map(getProfName);
    }

    if (id.includes('mystic_arcanum')) {
        const level = id.split('_').pop();
        return (availableSpells?.[level] || []).map(s => s.name);
    }

    if (id === 'wizard_spell_mastery') {
        // Level 1 and 2 chosen spells
        // const selected = characterData.data?.spellSelection?.leaded || []; // Re-check selection path
        // For now, return a prompt if we can't find them easily
        return ["Level 1 and 2 chosen spells will appear here"];
    }

    return [];
};

const FeatureChoiceOverlay = ({ isOpen, onClose, feature, options, onSelect, currentChoice, level, character }) => {
    const [tempChoices, setTempChoices] = useState([]);
    const limit = getChoiceLimitForFeature(feature, level);
    const isMulti = limit > 1;

    const isSubclassChoice = feature?.type === 'subclass_choice';
    // Logic to check if choice is already made (locked)
    const isLocked = isSubclassChoice && currentChoice && currentChoice !== "";

    // Initialize temp choices from currentChoice
    useEffect(() => {
        if (isOpen) {
            const initial = Array.isArray(currentChoice) ? currentChoice : (currentChoice ? [currentChoice] : []);
            setTempChoices(initial);
        }
    }, [isOpen, currentChoice]);

    if (!isOpen || !feature) return null;
    const groupedOptions = !Array.isArray(options);

    const allowDuplicates = feature?.details?.choice?.allow_duplicates;

    const handleToggleOption = (optKey) => {
        if (isLocked) return; // Prevent interaction if locked

        if (isMulti) {
            if (allowDuplicates) return; // Handled by + / - buttons
            setTempChoices(prev => {
                if (prev.includes(optKey)) return prev.filter(k => k !== optKey);
                if (prev.length < limit) return [...prev, optKey];
                return prev;
            });
        } else {
            onSelect(feature.id, optKey);
            onClose();
        }
    };

    const handleAddDuplicate = (optKey, e) => {
        e?.stopPropagation();
        if (isLocked) return;
        if (tempChoices.length < limit) {
            setTempChoices(prev => [...prev, optKey]);
        }
    };

    const handleRemoveDuplicate = (optKey, e) => {
        e?.stopPropagation();
        if (isLocked) return;
        setTempChoices(prev => {
            const idx = prev.lastIndexOf(optKey);
            if (idx !== -1) {
                const arr = [...prev];
                arr.splice(idx, 1);
                return arr;
            }
            return prev;
        });
    };

    const handleSaveMulti = () => {
        if (isLocked) return;
        onSelect(feature.id, tempChoices);
        onClose();
    };

    const renderChoiceOption = (opt, idx) => {
        const optKey = typeof opt === 'string' ? opt : (opt.id || opt.name);
        const count = tempChoices.filter(k => k === optKey).length;
        const isSelected = count > 0;
        const optName = typeof opt === 'string' ? opt : opt.name;
        const prerequisiteWarning = opt.prerequisite
            ? checkPrerequisites(opt.prerequisite, character, level)
            : null;
        const prerequisiteBlocked = !!prerequisiteWarning;
        const optDescRaw = typeof opt === 'string'
            ? null
            : (opt.description || opt.summary || opt.benefit || (opt.effects && opt.effects.join(' ')));
        return (
            <div
                key={idx}
                className={`choice-option-card
                    ${isSelected ? 'selected' : ''}
                    ${isLocked ? 'locked' : ''}
                    ${prerequisiteBlocked ? 'disabled' : ''}
                `}
                onClick={() => !allowDuplicates && !prerequisiteBlocked && handleToggleOption(optKey)}
            >
                <div className="option-name">
                    {optName}
                </div>
                {opt.prerequisite && (
                    <div className="feat-prerequisite">
                        Need: {
                            Array.isArray(opt.prerequisite)
                                ? opt.prerequisite.join(" • ")
                                : opt.prerequisite
                        }
                    </div>
                )}
                {optDescRaw && (
                    <div className="option-desc">
                        {processRichText(optDescRaw)}
                    </div>
                )}
                {allowDuplicates ? (
                    <div className="duplicate-counter">
                        <button
                            className="dup-btn"
                            onClick={(e) => handleRemoveDuplicate(optKey, e)}
                            disabled={count === 0 || isLocked}
                        >
                            -
                        </button>
                        <span className="dup-count">
                            {count}
                        </span>
                        <button
                            className="dup-btn"
                            onClick={(e) => handleAddDuplicate(optKey, e)}
                            disabled={tempChoices.length >= limit || isLocked}
                        >
                            +
                        </button>
                    </div>
                ) : (
                    isSelected && (
                        <div className="selected-tag">
                            {isLocked ? 'LOCKED' : 'SELECTED'}
                        </div>
                    )
                )}
            </div>
        );
    };

    return (
        <div className="choice-overlay-backdrop" onClick={onClose}>
            <div className="choice-overlay-card" onClick={(e) => e.stopPropagation()}>
                <div className="choice-overlay-header">
                    <div className="header-titles">
                        <h3>Choose for {feature.name}</h3>
                        <span className="choice-limit-hint">
                            Select {isMulti ? `up to ${limit}` : 'one'} ({tempChoices.length}/{limit})
                        </span>
                        {isSubclassChoice && !isLocked && (
                            <p className="subclass-warning" style={{ color: '#ff4444', fontWeight: 'bold', marginTop: '5px', fontSize: '0.85rem' }}>
                                Warning: This choice cannot be changed later.
                            </p>
                        )}
                        {isLocked && (
                            <p className="subclass-locked-msg" style={{ color: '#f1c40f', fontWeight: 'bold', marginTop: '5px', fontSize: '0.85rem' }}>
                                This choice is locked.
                            </p>
                        )}
                    </div>
                    <button className="close-btn" onClick={onClose}>✕</button>
                </div>
                <div className="choice-options-container">
                    {!groupedOptions ? (
                        options.map((opt, idx) => (
                            renderChoiceOption(opt, idx)
                        ))
                    ) : (
                        Object.entries(options).map(([category, feats]) => (
                            <div key={category} className="feat-category-group">
                                <h3 className="feat-category-title">
                                    {category === "origin" && "Origin Feats"}
                                    {category === "general" && "General Feats"}
                                    {category === "epic_boon" && "Epic Boons"}
                                </h3>

                                {feats.map((opt, idx) => (
                                    renderChoiceOption(opt, idx)
                                ))}
                            </div>
                        ))
                    )}
                </div>
                {isMulti && (
                    <div className="choice-overlay-footer">
                        <button className="save-choice-btn" onClick={handleSaveMulti}>
                            Save {tempChoices.length} Selections
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

const SpellCard = ({
    spell,
    availableSlotsObj,
    addAlert,
    spellSlotsCurrent,
    setSpellSlotsCurrent,
    castingSpell,
    setCastingSpell,
    saveCharacter,
    sourceClass
}) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const displayOrder = [
        "school",
        "action",
        "range",
        "components",
        "duration",
        "description",
        "damage",
        "damage_type",
        "spell_type",
        "scaling",
        "level_upgrade"
    ];

    const formatLabel = (key) => {
        return key
            .replaceAll("_", " ")
            .replace(/\b\w/g, l => l.toUpperCase());
    };

    const renderValue = (value) => {
        if (Array.isArray(value)) {
            return value.join(", ");
        }

        if (typeof value === "object" && value !== null) {
            return Object.entries(value)
                .map(([k, v]) =>
                    `${k}: ${renderValue(v)}`
                )
                .join(", ");
        }

        return value;
    };

    const spellLevel =
        spell.level ??
        0;

    const castableLevels = [];
    Object.entries(spellSlotsCurrent || {}).forEach(([poolName, slots]) => {
        Object.entries(slots).forEach(([level, amount]) => {
            if (
                parseInt(level) >= spellLevel &&
                amount > 0
            ) {
                castableLevels.push({
                    poolName,
                    level
                });
            }
        });
    });

    return (
        <div
            className={`prepared-spell-row expandable-spell ${isExpanded ? "expanded" : ""}`}
            onClick={() => setIsExpanded(!isExpanded)}
        >
            <div className="spell-header">
                <span className="spell-name">
                    {spell.name}
                    {sourceClass && (
                        <span className="spell-source-badge" style={{ fontSize: '0.7em', padding: '2px 6px', background: '#444', borderRadius: '4px', marginLeft: '8px', verticalAlign: 'middle' }}>
                            {sourceClass.charAt(0).toUpperCase() + sourceClass.slice(1)}
                        </span>
                    )}
                    {spell.isUnpreparedRitual && (
                        <span className="spell-source-badge ritual-unprepared-badge" style={{ fontSize: '0.7em', padding: '2px 6px', background: '#6b21a8', color: '#fff', borderRadius: '4px', marginLeft: '8px', verticalAlign: 'middle' }}>
                            📜 Ritual (Spellbook)
                        </span>
                    )}
                </span>

                {(
                    <div
                        className="cast-wrapper"
                        onClick={(e) => e.stopPropagation()}
                    >
                        {spell.isUnpreparedRitual ? (
                            <button
                                className="cast-spell-btn ritual-btn"
                                style={{ background: 'linear-gradient(135deg, #7b1fa2, #4a148c)', color: '#fff' }}
                                onClick={() => {
                                    addAlert(`You cast ${spell.name} as a Ritual (takes +10 min, no spell slot used)!`, "info");
                                }}
                            >
                                Cast Ritual (10m)
                            </button>
                        ) : (
                            <button
                                className="cast-spell-btn"
                                onClick={() => {
                                    if (spellLevel === 0) {
                                        addAlert(
                                            `You cast ${spell.name}!`,
                                            "success"
                                        );
                                        return;
                                    }

                                    setCastingSpell(
                                        castingSpell === spell.name
                                            ? null
                                            : spell.name
                                    );
                                }}
                            >
                                Cast
                            </button>
                        )}

                        {!spell.isUnpreparedRitual && spellLevel > 0 && castingSpell === spell.name && (
                            <div className="cast-dropdown">
                                {isRitualSpell(spell) && (
                                    <button
                                        className="cast-level-btn"
                                        style={{ background: '#6b21a8', color: '#fff' }}
                                        onClick={() => {
                                            addAlert(`You cast ${spell.name} as a Ritual (takes +10 min, no spell slot used)!`, "info");
                                            setCastingSpell(null);
                                        }}
                                    >
                                        Cast as Ritual (+10m)
                                    </button>
                                )}
                                {castableLevels.map(({ poolName, level }) => (
                                    <button
                                        key={`${poolName}-${level}`}
                                        className="cast-level-btn"
                                        onClick={() => {
                                            setSpellSlotsCurrent(prev => ({
                                                ...prev,
                                                [poolName]: {
                                                    ...prev[poolName],
                                                    [level]: prev[poolName][level] - 1
                                                }
                                            }));
                                            addAlert(
                                                `You cast ${spell.name} using ${poolName === "pact_magic" ? "Pact Magic" : "Spellcasting"} slot level ${level}!`,
                                                "success"
                                            );
                                            setCastingSpell(null);
                                        }}
                                    >
                                        {poolName === "pact_magic"
                                            ? `Pact Lv ${level}`
                                            : `Lv ${level}`
                                        }
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>

            {isExpanded && (
                <div className="spell-body">
                    {displayOrder.map(field => {
                        const value = spell[field];

                        if (
                            value === null ||
                            value === undefined ||
                            value === "" ||
                            (Array.isArray(value) && value.length === 0) ||
                            (typeof value === "object" && value !== null && Object.keys(value).length === 0)
                        ) {
                            return null
                        }

                        return (
                            <p key={field}>
                                <strong>
                                    {formatLabel(field)}:
                                </strong>{" "}

                                {renderValue(value)}
                            </p>
                        );
                    })}
                </div>
            )}
        </div>
    );
};


const getSpellcastingClasses = (character, allClassRules) => {
    if (!character?.data?.class_levels || !allClassRules) return [];
    const scClasses = [];
    for (const classEntry of character.data.class_levels) {
        const className = classEntry.class_name?.toLowerCase();
        const classData = allClassRules[className];
        if (!classData) continue;

        let rules = null;
        let source = null;

        const subclassName = classEntry.subclass?.toLowerCase();
        if (subclassName && classData.subclasses?.[subclassName]) {
            const subclassFeatures = classData.subclasses[subclassName].features;
            for (const level in subclassFeatures) {
                const feature = subclassFeatures[level]?.find(f => f.name === "Spellcasting" || f.id?.includes("spellcasting"));
                if (feature?.details) {
                    rules = feature.details;
                    source = "Subclass";
                    break;
                }
            }
        }

        if (!rules && classData.spellcasting) {
            rules = classData.spellcasting;
            source = "Class";
        }

        if (rules) {
            scClasses.push({ className, level: classEntry.level, rules: { ...rules, source } });
        }
    }
    return scClasses;
};

const isRitualSpell = (spell) => {
    if (!spell) return false;
    if (spell.ritual) return true;
    if (Array.isArray(spell.action) && spell.action.includes("Ritual")) return true;
    if (typeof spell.action === "string" && spell.action.includes("Ritual")) return true;
    return false;
};

const migrateSpellsData = (spells, scClasses) => {
    let result = {};
    if (Array.isArray(spells)) {
        if (scClasses.length > 0) {
            result = { [scClasses[0].className]: [...spells] };
        }
    } else if (spells) {
        result = { ...spells };
    }

    if (scClasses.some(c => c.className === 'wizard')) {
        const wizardPrepped = result.wizard || [];
        if (!result.wizard_spellbook) {
            result.wizard_spellbook = [...wizardPrepped];
        }
    }
    return result;
};



const SpellcastingWidget = ({
    hasSpellcasting,
    spellcastingRules,
    spellSlotsRules,
    spellSlotsCurrent,
    setSpellSlotsCurrent,
    addAlert,
    saveCharacter,
    character,
    availableSpells,
    isLayoutLocked,
    currentProficiencyBonus,
    onOpenOverlay,
    viewOnly,
    allClassRules
}) => {
    const [castingSpell, setCastingSpell] = useState(null);
    const [spellcastingSearchTerm, setSpellcastingSearchTerm] = useState("");
    const [spellTypeFilter, setSpellTypeFilter] = useState(null);
    const [selectedStatClass, setSelectedStatClass] = useState(null);

    const scClasses = useMemo(() => {
        return getSpellcastingClasses(character, allClassRules);
    }, [character, allClassRules]);

    const activeClassData = useMemo(() => {
        if (scClasses.length === 0) return null;
        return scClasses.find(c => c.className === selectedStatClass) || scClasses[0];
    }, [scClasses, selectedStatClass]);

    const activeRules = activeClassData?.rules || spellcastingRules;
    const activeClassName = activeClassData?.className || scClasses[0]?.className;

    const spellcasting = activeRules || {};
    const ability = spellcasting.ability || "intelligence";
    const abilityScore = character?.data?.abilities?.[ability.toLowerCase()] || 10;
    const mod = calculateModifier(abilityScore);
    const saveDC = 8 + currentProficiencyBonus + mod;
    const attackBonus = currentProficiencyBonus + mod;
    const progression = spellcasting.progression;
    const progressionKey = progression === "pact" ? "pact_magic" : progression;
    const slotsTable = spellSlotsRules?.[progressionKey];

    const availableSlotsObj = useMemo(() => {
        if (character?.data?.spell_slots_max && Object.keys(character.data.spell_slots_max).length > 0) {
            return character.data.spell_slots_max;
        }
        let slots = {};
        if (slotsTable) {
            let classLevel = 0;
            const currentClass = character.data.class_levels.find(
                cls => cls.class_name.toLowerCase() === character.data.class_name.toLowerCase()
            );
            if (currentClass) {
                classLevel = currentClass.level;
            }
            while (classLevel > 0 && !slotsTable[classLevel]) {
                classLevel--;
            }
            if (classLevel > 0) {
                slots = slotsTable[classLevel];
            }
        }
        return slots;
    }, [character, slotsTable]);

    useEffect(() => {
        if (!character || Object.keys(spellSlotsCurrent).length > 0 || Object.keys(availableSlotsObj).length === 0) return;
        setSpellSlotsCurrent(availableSlotsObj);
        saveCharacter({
            spell_slots_current: availableSlotsObj,
            spell_slots_max: availableSlotsObj
        });
    }, [character, spellSlotsCurrent, setSpellSlotsCurrent, availableSlotsObj, saveCharacter]);

    if (!hasSpellcasting || !spellcastingRules || !spellSlotsRules || !character) return null;

    const migratedSpells = migrateSpellsData(character.data.spells, scClasses);

    // Flatten spells for display (exclude non-class metadata like wizard_spellbook)
    const flattenedSelectedSpells = [];
    Object.entries(migratedSpells).forEach(([className, spellList]) => {
        if (className === 'wizard_spellbook' || !Array.isArray(spellList)) return;
        spellList.forEach(spellName => {
            flattenedSelectedSpells.push({ name: spellName, sourceClass: className });
        });
    });

    return (
        <div className="spellcasting-content">
            {!isLayoutLocked && <div className="widget-handle">⠿</div>}
            <div className="spellcasting-header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '15px', flexWrap: 'wrap' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px', flex: 1, flexWrap: 'wrap' }}>
                    <h3>Spellcasting</h3>
                    <div className="search-wrapper spell-search" style={{ margin: 0, flex: 1, minWidth: '200px', maxWidth: '250px' }}>
                        <input
                            type="text"
                            className="search-input"
                            placeholder="Search prepared spells..."
                            value={spellcastingSearchTerm}
                            onFocus={() => { if (spellTypeFilter) setSpellTypeFilter(null); }}
                            onChange={(e) => {
                                setSpellcastingSearchTerm(e.target.value);
                                if (e.target.value && spellTypeFilter) setSpellTypeFilter(null);
                            }}
                        />
                        <i className="fa-solid fa-magnifying-glass"></i>
                    </div>
                    <div className="feature-tabs" style={{ margin: 0 }}>
                        {["Area of Effect", "Buff", "Debuff", "Heal", "Melee Attack", "Ranged Attack", "Summon", "Target Save", "Utility"].map(t => (
                            <button
                                key={t}
                                onClick={() => {
                                    if (spellTypeFilter === t) { setSpellTypeFilter(null); }
                                    else { setSpellTypeFilter(t); setSpellcastingSearchTerm(""); }
                                }}
                                className={spellTypeFilter === t ? "active" : ""}
                            >
                                {t}
                            </button>
                        ))}
                    </div>
                </div>
                {!viewOnly && (
                    <button className="manage-spells-btn" onClick={onOpenOverlay} style={{ flexShrink: 0 }}>
                        📖 Manage Spells
                    </button>
                )}
            </div>

            <div className="spell-limits-summary" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                {scClasses.map(c => {
                    const isSelected = (activeClassName === c.className);
                    const selectedList = migratedSpells[c.className] || [];
                    const cantripsCount = selectedList.filter(name => {
                        for (const lvl in availableSpells) {
                            if (availableSpells[lvl].some(s => s.name === name && lvl === "0")) return true;
                        }
                        return false;
                    }).length;
                    const preparedCount = selectedList.length - cantripsCount;
                    const limitC = resolveScalingValue(c.rules?.cantrips_known, c.level) || 0;
                    const limitP = resolveScalingValue(c.rules?.spells_prepared, c.level) || 0;
                    return (
                        <button
                            type="button"
                            key={c.className}
                            className={`spell-stat-box spell-class-selector-btn ${isSelected ? 'active' : ''}`}
                            onClick={() => setSelectedStatClass(c.className)}
                            title={`Click to view ${c.className.charAt(0).toUpperCase() + c.className.slice(1)} spellcasting stats`}
                            style={{
                                padding: '6px 14px',
                                cursor: 'pointer',
                                color: isSelected ? '#ffffff' : '#e0e0e0',
                                background: isSelected ? 'rgba(255, 215, 0, 0.2)' : 'rgba(255, 255, 255, 0.08)',
                                border: isSelected ? '1px solid var(--accent)' : '1px solid rgba(255, 255, 255, 0.2)',
                                borderRadius: '6px',
                                textAlign: 'left',
                                transition: 'all 0.2s ease',
                                outline: 'none'
                            }}
                        >
                            <span className="spell-stat-label" style={{ marginBottom: '2px', display: 'block', color: isSelected ? '#ffd700' : '#e0e0e0', fontWeight: 'bold' }}>
                                {c.className.charAt(0).toUpperCase() + c.className.slice(1)} {scClasses.length > 1 && isSelected ? '★' : ''}
                            </span>
                            <span style={{ fontSize: '0.85em', color: isSelected ? '#ffffff' : '#b0b0b0', opacity: 0.95 }}>
                                C: {cantripsCount}/{limitC} | P: {preparedCount}/{limitP}
                            </span>
                        </button>
                    );
                })}
            </div>

            <div className="spell-stats-row">
                <div className="spell-stat-box">
                    <span className="spell-stat-label">
                        Ability {activeClassName ? `(${activeClassName.charAt(0).toUpperCase() + activeClassName.slice(1)})` : ''}
                    </span>
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
                {
                    Object.entries(availableSlotsObj).map(
                        ([poolName, slots]) => (
                            <div
                                key={poolName}
                                className={`spell-slot-pool ${poolName === "pact_magic" ? "pact-slot-pool" : "normal-slot-pool"}`}
                            >
                                <h4>
                                    {
                                        poolName === "pact_magic"
                                            ? "Pact Magic Slots"
                                            : "Spell Slots"
                                    }
                                </h4>
                                {
                                    Object.keys(slots).map(level => (
                                        <div
                                            key={`${poolName}-${level}`}
                                            className="spell-slot-box"
                                        >
                                            <span className="slot-lvl">
                                                Lv {level}
                                            </span>
                                            <span className="slot-count">
                                                {
                                                    spellSlotsCurrent?.[poolName]?.[level]
                                                    ?? slots[level]
                                                }
                                            </span>
                                        </div>
                                    ))
                                }
                            </div>
                        ))
                }
            </div>

            <div className="prepared-spells-list scrollable">
                {["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"].map(level => {
                    const spellsAtLevel = availableSpells?.[level] || [];

                    let selectedAtLevel = flattenedSelectedSpells.filter(fs =>
                        spellsAtLevel.some(s => s.name === fs.name)
                    ).map(fs => {
                        const spellData = spellsAtLevel.find(s => s.name === fs.name);
                        return { ...spellData, sourceClass: fs.sourceClass };
                    });

                    let combinedAtLevel = [...selectedAtLevel];

                    const safeString = (val) => {
                        if (!val) return "";
                        if (typeof val === "string") return val;
                        if (Array.isArray(val)) return val.map(safeString).join(" ");
                        if (typeof val === "object") return Object.values(val).map(safeString).join(" ");
                        return String(val);
                    };

                    if (spellTypeFilter) {
                        const filterTerm = spellTypeFilter.toLowerCase();
                        combinedAtLevel = combinedAtLevel.filter(spell =>
                            safeString(spell.spell_type).toLowerCase().includes(filterTerm)
                        );
                    }

                    if (spellcastingSearchTerm) {
                        const term = spellcastingSearchTerm.toLowerCase();
                        combinedAtLevel = combinedAtLevel.filter(spell => {
                            return (
                                safeString(spell.name).toLowerCase().includes(term) ||
                                safeString(spell.school).toLowerCase().includes(term) ||
                                safeString(spell.action).toLowerCase().includes(term) ||
                                safeString(spell.range).toLowerCase().includes(term) ||
                                safeString(spell.components).toLowerCase().includes(term) ||
                                safeString(spell.duration).toLowerCase().includes(term) ||
                                safeString(spell.description).toLowerCase().includes(term) ||
                                safeString(spell.damage).toLowerCase().includes(term) ||
                                safeString(spell.damage_type).toLowerCase().includes(term) ||
                                safeString(spell.spell_type).toLowerCase().includes(term) ||
                                safeString(spell.level_upgrade).toLowerCase().includes(term)
                            );
                        });
                    }

                    if (combinedAtLevel.length === 0) return null;

                    return (
                        <div key={level} className="spell-level-group">
                            <h4>{level === "0" ? "Cantrips" : `Level ${level}`}</h4>
                            {combinedAtLevel.map((spell, idx) => (
                                <SpellCard
                                    key={`${spell.name}-${spell.sourceClass || 'sc'}-${idx}`}
                                    spell={spell}
                                    availableSlotsObj={availableSlotsObj}
                                    addAlert={addAlert}
                                    spellSlotsCurrent={spellSlotsCurrent}
                                    setSpellSlotsCurrent={setSpellSlotsCurrent}
                                    castingSpell={castingSpell}
                                    setCastingSpell={setCastingSpell}
                                    saveCharacter={saveCharacter}
                                    sourceClass={spell.sourceClass}
                                />
                            ))}
                        </div>
                    );
                })}
                {flattenedSelectedSpells.length === 0 && <div className="no-spells-note">No spells selected. Click 'Manage Spells' to choose.</div>}
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
    spellcastingRules,
    spellSlotsRules,
    onToggleSpell,
    allClassRules
}) => {
    const [spellSearchTerm, setSpellSearchTerm] = useState("");
    const [activeSpellClass, setActiveSpellClass] = useState(null);
    const [wizardSubTab, setWizardSubTab] = useState("spellbook");

    const scClasses = useMemo(() => {
        return getSpellcastingClasses(character, allClassRules);
    }, [character, allClassRules]);

    useEffect(() => {
        if (scClasses.length > 0 && (!activeSpellClass || !scClasses.find(c => c.className === activeSpellClass))) {
            setActiveSpellClass(scClasses[0].className);
        }
    }, [scClasses, activeSpellClass]);

    if (!show || !availableSpells) return null;

    const migratedSpells = migrateSpellsData(character.data.spells, scClasses);

    // Total spells selected across all classes
    let totalCantripsCount = 0;
    let totalPreparedCount = 0;

    Object.values(migratedSpells).forEach(spellList => {
        if (!Array.isArray(spellList)) return;
        const cantrips = spellList.filter(name => {
            for (const lvl in availableSpells) {
                if (availableSpells[lvl].some(s => s.name === name && lvl === "0")) return true;
            }
            return false;
        }).length;
        totalCantripsCount += cantrips;
        totalPreparedCount += (spellList.length - cantrips);
    });

    const activeClassData = scClasses.find(c => c.className === activeSpellClass);
    const activeRules = activeClassData?.rules || spellcastingRules;
    const activeLevel = activeClassData?.level || character.level;

    const selectedSpellsActive = migratedSpells[activeSpellClass] || [];
    const wizardSpellbookActive = migratedSpells.wizard_spellbook || [];

    const progression = activeRules?.progression;
    const progressionKey = progression === "pact" ? "pact_magic" : progression;
    const slotsTable = progressionKey ? spellSlotsRules?.[progressionKey] : null;

    let maxSpellLevelForClass = 0;
    if (slotsTable && activeClassData) {
        let classLevel = activeClassData.level;
        while (classLevel > 0 && !slotsTable[classLevel]) {
            classLevel--;
        }
        if (classLevel > 0) {
            const slots = slotsTable[classLevel];
            maxSpellLevelForClass = Math.max(
                ...Object.keys(slots).map(Number)
            );
        }
    }

    const hasCantrips = !!(availableSpells?.["0"]?.length);

    const cantripsKnownLimit = resolveScalingValue(activeRules?.cantrips_known, activeLevel) || 0;
    const spellsPreparedLimit = resolveScalingValue(activeRules?.spells_prepared, activeLevel) || 0;

    const cantripsCountActive = selectedSpellsActive.filter(name => {
        for (const lvl in availableSpells) {
            if (availableSpells[lvl].some(s => s.name === name && lvl === "0")) return true;
        }
        return false;
    }).length;

    const preparedCountActive = selectedSpellsActive.length - cantripsCountActive;

    const cantripsAtLimit = cantripsCountActive >= cantripsKnownLimit;
    const spellsAtLimit = preparedCountActive >= spellsPreparedLimit;

    const hintText = activeSpellClass === "wizard"
        ? (wizardSubTab === "spellbook"
            ? "Spellbook Tab: Choose Level 1+ Wizard spells to learn and record in your Spellbook (starts with 6 at Lv 1, +2 per level up, plus transcribed spells)."
            : "Prepared Spells Tab: Choose Level 1+ spells from your active Spellbook to prepare for daily casting.")
        : (hasCantrips
            ? `Filtering by your max available spell slot level (Cantrips to Level ${maxSpellLevelForClass}). Spells chosen are saved automatically.`
            : `Filtering by your max available spell slot level (Level 1 to Level ${maxSpellLevelForClass}). Spells chosen are saved automatically.`);

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

                {scClasses.length > 1 && (
                    <div className="feature-tabs" style={{ margin: '10px 0' }}>
                        {scClasses.map(c => (
                            <button
                                key={c.className}
                                onClick={() => setActiveSpellClass(c.className)}
                                className={activeSpellClass === c.className ? "active" : ""}
                            >
                                {c.className.charAt(0).toUpperCase() + c.className.slice(1)}
                            </button>
                        ))}
                    </div>
                )}

                {activeSpellClass === "wizard" && (
                    <div className="wizard-tab-toggle" style={{ display: 'flex', justifyContent: 'center', gap: '10px', margin: '12px 0' }}>
                        <button
                            type="button"
                            className={`wizard-subtab-btn ${wizardSubTab === 'spellbook' ? 'active' : ''}`}
                            onClick={() => setWizardSubTab('spellbook')}
                        >
                            📖 Spellbook
                        </button>
                        <button
                            type="button"
                            className={`wizard-subtab-btn ${wizardSubTab === 'prepared' ? 'active' : ''}`}
                            onClick={() => setWizardSubTab('prepared')}
                        >
                            ✨ Prepared Spells
                        </button>
                    </div>
                )}

                {activeSpellClass === "wizard" ? (
                    <div className="overlay-stats-bar">
                        <div className={`stat-pill ${cantripsAtLimit ? 'at-limit' : ''}`}>
                            Cantrips: <strong>{cantripsCountActive} / {cantripsKnownLimit}</strong>
                        </div>
                        {wizardSubTab === "spellbook" ? (
                            <div className="stat-pill">
                                Spellbook Spells: <strong>{wizardSpellbookActive.length} Learned</strong> (min {6 + 2 * (activeLevel - 1)})
                            </div>
                        ) : (
                            <div className={`stat-pill ${spellsAtLimit ? 'at-limit' : ''}`}>
                                Wizard Prepared: <strong>{preparedCountActive} / {spellsPreparedLimit}</strong>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="overlay-stats-bar">
                        <div className={`stat-pill ${cantripsAtLimit ? 'at-limit' : ''}`}>
                            {activeSpellClass ? activeSpellClass.charAt(0).toUpperCase() + activeSpellClass.slice(1) + ' ' : ''}Cantrips: <strong>{cantripsCountActive} / {cantripsKnownLimit}</strong>
                        </div>
                        <div className={`stat-pill ${spellsAtLimit ? 'at-limit' : ''}`}>
                            {activeSpellClass ? activeSpellClass.charAt(0).toUpperCase() + activeSpellClass.slice(1) + ' ' : ''}Prepared: <strong>{preparedCountActive} / {spellsPreparedLimit}</strong>
                        </div>
                        {scClasses.length > 1 && (
                            <div className="stat-pill" style={{ opacity: 0.8 }}>
                                Total Selected: {totalCantripsCount + totalPreparedCount}
                            </div>
                        )}
                    </div>
                )}

                <div className="search-wrapper spell-search" style={{ margin: '15px 0', maxWidth: 'none' }}>
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Search spells by name or description (e.g. 'damage', 'fire', 'heal')..."
                        value={spellSearchTerm}
                        onChange={(e) => setSpellSearchTerm(e.target.value)}
                    />
                    <i className="fa-solid fa-magnifying-glass"></i>
                </div>

                <p className="overlay-hint">{hintText}</p>

                {activeSpellClass === "wizard" && wizardSubTab === "prepared" && wizardSpellbookActive.length === 0 && (
                    <div style={{ background: 'rgba(255, 167, 38, 0.15)', border: '1px solid #ffa726', padding: '12px 16px', borderRadius: '8px', margin: '15px 0', color: '#ffb74d', textAlign: 'center', fontSize: '0.9rem' }}>
                        <i className="fa-solid fa-book-open" style={{ marginRight: '8px' }}></i>
                        Your Spellbook is currently empty! Switch to the <strong>📖 Spellbook</strong> tab above to select spells you have learned before preparing them.
                    </div>
                )}

                <div className="spell-overlay-list">
                    {Object.keys(availableSpells).map(level => {
                        if (parseInt(level) > maxSpellLevelForClass && level !== "0") return null;

                        const term = spellSearchTerm.toLowerCase();
                        let spellsAtLevel = availableSpells[level].filter(s =>
                            s.name.toLowerCase().includes(term) ||
                            (s.description || "").toLowerCase().includes(term)
                        );

                        if (activeSpellClass === "wizard" && wizardSubTab === "prepared" && level !== "0") {
                            spellsAtLevel = spellsAtLevel.filter(s => wizardSpellbookActive.includes(s.name));
                        }

                        if (spellsAtLevel.length === 0 && (spellSearchTerm || (activeSpellClass === "wizard" && wizardSubTab === "prepared"))) return null;

                        return (
                            <div key={level} className="overlay-level-group">
                                <h3>{level === "0" ? "Cantrips" : `Level ${level}`}</h3>
                                <div className="spell-selection-grid">
                                    {spellsAtLevel.map(spell => {
                                        const isCantrip = level === "0";
                                        let isSelectedActive = false;
                                        let canSelect = false;

                                        if (activeSpellClass === "wizard") {
                                            if (isCantrip) {
                                                isSelectedActive = selectedSpellsActive.includes(spell.name);
                                                canSelect = isSelectedActive || !cantripsAtLimit;
                                            } else if (wizardSubTab === "spellbook") {
                                                isSelectedActive = wizardSpellbookActive.includes(spell.name);
                                                canSelect = true;
                                            } else {
                                                isSelectedActive = selectedSpellsActive.includes(spell.name);
                                                canSelect = isSelectedActive || !spellsAtLimit;
                                            }
                                        } else {
                                            isSelectedActive = selectedSpellsActive.includes(spell.name);
                                            canSelect = isSelectedActive || (isCantrip ? !cantripsAtLimit : !spellsAtLimit);
                                        }

                                        const isPreparedInWizard = (migratedSpells.wizard || []).includes(spell.name);
                                        const isInSpellbookWizard = (migratedSpells.wizard_spellbook || []).includes(spell.name);
                                        const selectedInClasses = Object.keys(migratedSpells).filter(cls => cls !== 'wizard_spellbook' && Array.isArray(migratedSpells[cls]) && migratedSpells[cls].includes(spell.name));

                                        return (
                                            <div
                                                key={spell.name}
                                                className={`spell-select-card ${isSelectedActive ? 'selected' : ''} ${!canSelect ? 'disabled' : ''}`}
                                                onClick={() => canSelect && onToggleSpell(spell.name, activeSpellClass, activeSpellClass === "wizard" ? wizardSubTab : "prepared")}
                                                style={{ position: 'relative' }}
                                            >
                                                <div className="spell-name">{spell.name}</div>
                                                <div className="spell-school">{spell.school}</div>

                                                {activeSpellClass === "wizard" && !isCantrip && (
                                                    <div style={{ marginTop: '6px', display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                                                        {isInSpellbookWizard && (
                                                            <span style={{ fontSize: '0.7em', padding: '2px 6px', background: '#2e7d32', color: '#fff', borderRadius: '4px' }}>
                                                                📖 In Book
                                                            </span>
                                                        )}
                                                        {isPreparedInWizard && (
                                                            <span style={{ fontSize: '0.7em', padding: '2px 6px', background: '#1565c0', color: '#fff', borderRadius: '4px' }}>
                                                                ✨ Prepared
                                                            </span>
                                                        )}
                                                    </div>
                                                )}

                                                {selectedInClasses.length > 0 && activeSpellClass !== "wizard" && (
                                                    <div className="spell-source-tags" style={{ marginTop: '5px', display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                                                        {selectedInClasses.map(cls => (
                                                            <span key={cls} style={{ fontSize: '0.75em', padding: '2px 6px', background: '#333', color: '#fff', borderRadius: '4px' }}>
                                                                {cls.charAt(0).toUpperCase() + cls.slice(1)}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                                {isSelectedActive && <div className="spell-check">✓</div>}
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
    const { token, user: currentUser } = useAuth();
    const { addAlert, updateAlert, confirm } = useNotification();
    const location = useLocation();

    const isEditMode = location.pathname.endsWith('/edit');
    const [character, setCharacter] = useState(null);

    const isOwner = currentUser?.id && character?.user_id === currentUser?.id;
    const isAdmin = currentUser?.is_admin;
    const [activeSession, setActiveSession] = useState(null);
    const [sessionParticipants, setSessionParticipants] = useState([]);
    const [showTransferModal, setShowTransferModal] = useState(false);
    const [itemToTransfer, setItemToTransfer] = useState(null);
    const [showRestOverlay, setShowRestOverlay] = useState(false);
    const [pendingRestType, setPendingRestType] = useState(null);
    const [statModConfig, setStatModConfig] = useState({ isOpen: false, type: null, statKey: null, value: 0, label: "" });
    const [showGoldTransferModal, setShowGoldTransferModal] = useState(false);
    const [goldTransferAmount, setGoldTransferAmount] = useState(1);
    const [goldTransferRecipient, setGoldTransferRecipient] = useState(null);
    const [revealedGifts, setRevealedGifts] = useState({ gold: [], items: [] }); // { gold: [ids/timestamps], items: [originalIndexes] }
    const [pendingGifts, setPendingGifts] = useState({ gold: [], items: [] });
    const [isGiftsLoading, setIsGiftsLoading] = useState(false);
    const [isApplyingStatMod, setIsApplyingStatMod] = useState(false);
    const [levelingUpAlertId, setLevelingUpAlertId] = useState(null);


    // Experience Editor State
    const [xp, setXp] = useState(0);
    const [tempXp, setTempXp] = useState("");
    const [showXpEditor, setShowXpEditor] = useState(false);
    const [showMulticlassSelection, setShowMulticlassSelection] = useState(false);
    const [selectedLevelUpClass, setSelectedLevelUpClass] = useState(null);
    const [multiclassRules, setMulticlassRules] = useState({});
    // eslint-disable-next-line no-unused-vars
    const [levelUpPreviewMode, setLevelUpPreviewMode] = useState(false);
    const [allClassRules, setAllClassRules] = useState({});

    // Level Up Preview State
    const [previewLevel, setPreviewLevel] = useState(1);
    const [previewPage, setPreviewPage] = useState(1);
    const [isFeatureListTransitioning, setIsFeatureListTransitioning] = useState(false);
    const [previewChoices, setPreviewChoices] = useState({});
    const [previewExpandedFeatures, setPreviewExpandedFeatures] = useState({});
    const [previewSpells, setPreviewSpells] = useState([]);
    const [spellOverlayPreviewMode, setSpellOverlayPreviewMode] = useState(false);

    useEffect(() => {
        if (showXpEditor && !selectedLevelUpClass) {
            setPreviewLevel(character?.level || 1);
            setPreviewPage(1);
            setPreviewChoices({});
            setPreviewExpandedFeatures({});
        }
    }, [showXpEditor, character?.level, selectedLevelUpClass]);

    useEffect(() => {
        if (selectedLevelUpClass) {
            const className = selectedLevelUpClass.toLowerCase();
            if (!allClassRules[className]) {
                fetch(`${API_BASE_URL}/api/classes/${className}`)
                    .then(res => res.json())
                    .then(data => {
                        setAllClassRules(prev => ({
                            ...prev,
                            [className]: data
                        }));
                    })
                    .catch(err => console.error("Error fetching class rules for preview:", err));
            }
        }
    }, [selectedLevelUpClass, allClassRules]);

    const handlePreviewLevelChange = (lvl) => {
        if (lvl === previewLevel) return;
        setIsFeatureListTransitioning(true);
        setTimeout(() => {
            setPreviewLevel(lvl);
            setPreviewPage(1);
            setIsFeatureListTransitioning(false);
        }, 300);
    };

    const handlePreviewPageChange = (page) => {
        if (page === previewPage) return;
        setIsFeatureListTransitioning(true);
        setTimeout(() => {
            setPreviewPage(page);
            setIsFeatureListTransitioning(false);
        }, 300);
    };

    const isDM = activeSession && activeSession.dm_id === currentUser?.id;
    const isAuthorized = isOwner || isAdmin || isDM;
    const canEdit = isEditMode && (isOwner || isAdmin || isDM);
    const viewOnly = !canEdit;

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [ruleOptions, setRuleOptions] = useState({});
    const [choiceOverlay, setChoiceOverlay] = useState({ isOpen: false, feature: null });

    const [skills, setSkills] = useState({}); // Renamed from skillProficiencies
    const [maxHpModifier] = useState(0); // Renamed from damageModInput
    const [inventoryItems, setInventoryItems] = useState([]); // Renamed from inventory
    const [gold, setGold] = useState(0);
    const [inventoryFilter, setInventoryFilter] = useState("All");
    const [classRules, setClassRules] = useState(null);
    const [layout, setLayout] = useState(null);
    const [isLayoutLocked, setIsLayoutLocked] = useState(true);
    const [expandedFeatures, setExpandedFeatures] = useState({});
    const [featureFilter, setFeatureFilter] = useState("All");
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
    const [featureChoices, setFeatureChoices] = useState({});
    const [featureNotes, setFeatureNotes] = useState({});
    const [spellSlotsCurrent, setSpellSlotsCurrent] = useState({});

    // Character Name Editing State
    const [isEditingName, setIsEditingName] = useState(false);
    const [nameInput, setNameInput] = useState("");

    // Level Up Overlay State
    const [showLevelUpOverlay, setShowLevelUpOverlay] = useState(false);
    const [levelUpMinimized, setLevelUpMinimized] = useState(false);
    const [previousLevel, setPreviousLevel] = useState(0);
    const [levelUpClass, setLevelUpClass] = useState(null);

    // Drag and Drop state for Inventory
    const [draggedItemIndex, setDraggedItemIndex] = useState(null);

    // Handle character rename
    const handleRenameName = async (newName) => {
        const trimmed = newName.trim();
        if (!trimmed || trimmed === character.name) {
            setIsEditingName(false);
            return;
        }
        try {
            const response = await fetch(`${API_BASE_URL}/api/characters/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name: trimmed })
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to rename character');
            }
            setCharacter(prev => prev ? { ...prev, name: trimmed } : prev);
            setIsEditingName(false);
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };
    const [dragOverItemIndex, setDragOverItemIndex] = useState(null);

    // New HP related states
    const [currentHp, setCurrentHp] = useState(0);
    const [baseMaxHp, setBaseMaxHp] = useState(0);
    const [effectiveMaxHp, setEffectiveMaxHp] = useState(0);

    const [characterLoaded, setCharacterLoaded] = useState(false);

    const openLevelUpSelection = useCallback(() => {
        setShowXpEditor(true);
        setLevelUpPreviewMode(true);

        if (character?.class?.name) {
            setSelectedLevelUpClass(character.class.name);

            const existingClasses = character.data?.class_levels || [];
            const primaryClassLevelInfo = existingClasses.find(
                c => c.class_name.toLowerCase() === character.class.name.toLowerCase()
            );

            const nextLevel = primaryClassLevelInfo
                ? primaryClassLevelInfo.level + 1
                : 1;

            setPreviewLevel(nextLevel);
        }

        setTimeout(() => {
            setShowMulticlassSelection(true);
        }, 50);

    }, [character]);

    // Consolidated Loading Logic
    const fetchData = useCallback(async () => {
        try {
            // 1. Fetch Global Rules first (Optional but good to have ready)
            const [weaponRes, armorRes, spellSlotsRes] = await Promise.all([
                fetch(`${API_BASE_URL}/api/rules/weapons`),
                fetch(`${API_BASE_URL}/api/rules/armor`),
                fetch(`${API_BASE_URL}/api/rules/spell_slots`)
            ]);

            const wRules = await weaponRes.json();
            const aRules = await armorRes.json();
            const sSlotsRules = await spellSlotsRes.json();

            setWeaponRules(wRules);
            setArmorRules(aRules);
            setSpellSlotsRules(sSlotsRules);

            // 2. Fetch Character Data
            const charRes = await fetch(`${API_BASE_URL}/api/characters/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!charRes.ok) {
                if (charRes.status === 404) throw new Error("Character not found");
                throw new Error("Failed to load character");
            }
            const data = await charRes.json();

            // Check for pending rest
            if (data.pending_rest) {
                setPendingRestType(data.pending_rest);
                setShowRestOverlay(true);
            } else {
                setPendingRestType(null);
            }

            // Set immediate basic state
            console.log("CHARACTER DATA DEBUG:", data.data);
            setCharacter(data);
            setSkills(data.data.skillProficiencies || {});
            setGold(data.data.gold || 0);
            setXp(data.data.xp || 0);
            setTempXp(data.data.xp || 0);
            setActiveFeatures(data.data.activeFeatures || []);
            setFeatureUses(data.data.featureUses || {});
            setFeatureChoices(data.data.featureChoices || {});
            setFeatureNotes(data.data.featureNotes || {});
            setSpellSlotsCurrent(data.data.spell_slots_current || {});
            setCharacterLoaded(true);

            // Initialize HP
            const initialBaseMaxHp = data.data.hp_max_base || 0;
            const initialMaxHpModifier = data.data.hp_modifier || 0;
            setBaseMaxHp(initialBaseMaxHp);
            setEffectiveMaxHp(initialBaseMaxHp + initialMaxHpModifier);
            setCurrentHp(data.data.hp_current || 0);

            // 3. Normalize Inventory (Needs wRules and aRules)
            const rawInventory = data.data.inventory || [];
            const normalizedInventory = rawInventory.map((item, idx) => {
                let normalized = typeof item === 'string' ? { name: item, quantity: 1, category: "Other", equipped: false } : { equipped: false, ...item };
                normalized.originalIndex = idx;
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
            const classFetches = {};
            if (data.data?.class_levels) {
                data.data.class_levels.forEach(cls => {
                    const className = cls.class_name.toLowerCase();
                    if (!classFetches[className]) {
                        classFetches[className] = fetch(
                            `${API_BASE_URL}/api/classes/${className}`
                        ).then(r => r.json());
                    }
                });
            } else if (data.class?.name) {
                const className = data.class.name.toLowerCase();
                classFetches[className] = fetch(
                    `${API_BASE_URL}/api/classes/${className}`
                ).then(r => r.json());
            }
            const classNames = Object.keys(classFetches);
            const classRulesPromises = classNames.map(
                name => classFetches[name]
            );
            rulePromises.push(...classRulesPromises);
            // Fetch spells for all character classes (multiclass support)
            const characterClasses = data.data?.class_levels?.length
                ? data.data.class_levels.map(cls => cls.class_name.toLowerCase())
                : [data.class?.name?.toLowerCase()].filter(Boolean);

            characterClasses.forEach(className => {
                rulePromises.push(
                    fetch(`${API_BASE_URL}/api/spells/${className}`)
                        .then(r => r.json())
                );
            });
            if (data.data?.species) {
                rulePromises.push(fetch(`${API_BASE_URL}/api/species`).then(r => r.json()));
            }
            if (data.data?.background) {
                rulePromises.push(fetch(`${API_BASE_URL}/api/backgrounds`).then(r => r.json()));
            }

            const ruleResults = await Promise.all(rulePromises);
            let resultIdx = 0;

            let resolvedClassRules = null;
            const loadedClassRules = {};
            classNames.forEach(className => {
                loadedClassRules[className] = ruleResults[resultIdx++];
            });
            setAllClassRules(loadedClassRules);
            if (data.class?.name) {
                resolvedClassRules = loadedClassRules[data.class.name.toLowerCase()];
                setClassRules(resolvedClassRules);

                // Merge spell lists from all classes
                const mergedSpells = {};

                const characterClasses = data.data?.class_levels?.length
                    ? data.data.class_levels.map(cls => cls.class_name.toLowerCase())
                    : [data.class.name.toLowerCase()];

                characterClasses.forEach(() => {
                    const classSpells = ruleResults[resultIdx++];

                    Object.entries(classSpells).forEach(([level, spells]) => {

                        if (!mergedSpells[level]) {
                            mergedSpells[level] = [];
                        }

                        spells.forEach(spell => {
                            const alreadyExists = mergedSpells[level]
                                .some(existing => existing.name === spell.name);

                            if (!alreadyExists) {
                                mergedSpells[level].push(spell);
                            }
                        });
                    });
                });

                setAvailableSpells(mergedSpells);
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

            fetch(`${API_BASE_URL}/api/classes/multiclass-data`, {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            })
                .then(res => res.json())
                .then(data => {
                    setMulticlassRules(data)
                })

            // 4b. Fetch Global Rule Options (Weapon Mastery, Metamagic, Invocations)
            const optionsRes = await fetch(`${API_BASE_URL}/api/rules/options`);
            const featsRes = await fetch(`${API_BASE_URL}/api/feats`);

            if (optionsRes.ok && featsRes.ok) {
                const optionsData = await optionsRes.json();
                const featsData = await featsRes.json();
                setRuleOptions({ ...optionsData, ...featsData });
            }

            // 5. Check for Active Session Participation
            const sessionRes = await fetch(`${API_BASE_URL}/api/host/active`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (sessionRes.ok) {
                const activeSessions = await sessionRes.json();
                for (const s of activeSessions) {
                    if (!s.can_enter) continue;
                    const detailRes = await fetch(`${API_BASE_URL}/api/host/details/${s.id}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (detailRes.ok) {
                        const details = await detailRes.json();
                        const me = details.participants.find(p => p.character && p.character.id === parseInt(id));
                        if (me) {
                            setActiveSession(details);
                            setSessionParticipants(details.participants.filter(p => p.character && p.character.id !== parseInt(id)));
                            break;
                        }
                    }
                }
            }

            // 6. Final Step: Layout Initialization
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

            if (data.data?.level_one_pending) {
                const fetchIsOwner = currentUser?.id && data.user_id === currentUser?.id;
                const fetchIsAdmin = currentUser?.is_admin;

                if (fetchIsOwner || fetchIsAdmin) {
                    setShowLevelUpOverlay(true);

                    setPreviousLevel(0);

                    setLevelUpClass(
                        data.data.class_name
                    );
                }
            }

            setLoading(false);

        } catch (err) {
            console.error("Load failed:", err);
            setError(err.message);
            setLoading(false);
        }
    }, [id, token, currentUser]);

    useEffect(() => {
        if (
            character &&
            character.data?.level_up_pending &&
            isOwner &&
            !showXpEditor
        ) {
            openLevelUpSelection();
        }

    }, [
        character,
        isOwner,
        showXpEditor,
        openLevelUpSelection
    ]);

    useEffect(() => {
        if (showLevelUpOverlay && levelingUpAlertId) {
            updateAlert(levelingUpAlertId, `Ascended! Time to choose your new powers.`, 'success', 5000);
            setLevelingUpAlertId(null);
        }
    }, [showLevelUpOverlay, levelingUpAlertId, updateAlert]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    // Live Polling Effect
    useEffect(() => {
        if (!token || !activeSession) return;

        const interval = setInterval(() => {
            fetchData();
        }, 5000);

        return () => clearInterval(interval);
    }, [token, activeSession, fetchData]);

    // Gift Reveal Logic
    useEffect(() => {
        if (!character) return;

        const newGoldGifts = (character.data.gold_gifts || []).filter(g =>
            !revealedGifts.gold.includes(g.id || `${g.amount}-${g.from_character_name}`) &&
            !pendingGifts.gold.some(p => (p.id === g.id && p.id !== undefined) || (p.amount === g.amount && p.from_character_name === g.from_character_name))
        );

        const newItems = inventoryItems.filter(item =>
            item.is_new_gift &&
            !revealedGifts.items.includes(item.originalIndex) &&
            !pendingGifts.items.some(p => p.originalIndex === item.originalIndex)
        );

        if (newGoldGifts.length > 0 || newItems.length > 0) {
            setIsGiftsLoading(true);
            setPendingGifts(prev => ({
                gold: [...prev.gold, ...newGoldGifts],
                items: [...prev.items, ...newItems]
            }));

            // Smoothly transit to notification after 5 seconds
            setTimeout(() => {
                setPendingGifts(prev => {
                    const goldToReveal = prev.gold;
                    const itemsToReveal = prev.items;

                    setRevealedGifts(rev => ({
                        gold: [...rev.gold, ...goldToReveal.map(g => g.id || `${g.amount}-${g.from_character_name}`)],
                        items: [...rev.items, ...itemsToReveal.map(i => i.originalIndex)]
                    }));

                    return { gold: [], items: [] };
                });
                setIsGiftsLoading(false);
            }, 5000);
        }
    }, [character, inventoryItems, revealedGifts, pendingGifts]);

    // Effect to update effectiveMaxHp when baseMaxHp or maxHpModifier changes
    useEffect(() => {
        setEffectiveMaxHp(baseMaxHp + maxHpModifier);
    }, [baseMaxHp, maxHpModifier]);

    const saveCharacter = useCallback((updates) => {
        fetch(`${API_BASE_URL}/api/characters/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
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
    }, [id, token]);

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

    const handleFeatureChoice = useCallback((featureId, choice, feature = null, isPreview = false) => {
        if (isPreview) {
            setPreviewChoices(prev => ({ ...prev, [featureId]: choice }));
            return;
        }
        setFeatureChoices(prev => {
            const next = { ...prev };
            // If the main feat/boon choice changes, remove any old sub-choices
            if (
                feature &&
                (featureId.includes("feat_or_asi") || featureId.includes("epic_boon")) &&
                !featureId.includes("_sub_")
            ) {
                Object.keys(next).forEach(key => {
                    if (key.startsWith(`${featureId}_sub_`)) {
                        delete next[key];
                    }
                });
            }
            // Save the new choice
            next[featureId] = choice;
            // Check if this choice is a subclass choice
            const updatePayload = { featureChoices: next };
            const isSubclassChoice = featureId.includes('_subclass');
            if (isSubclassChoice) {
                const subclassId = Array.isArray(choice)
                    ? (typeof choice[0] === 'string'
                        ? choice[0]
                        : (choice[0].id || choice[0].name))
                    : (typeof choice === 'string'
                        ? choice
                        : (choice.id || choice.name));

                updatePayload.subclass = subclassId;
                updatePayload.subclass_class = feature.classId;
                // Update local state IMMEDIATELY so features appear without reload
                setCharacter(prevChar => {
                    if (!prevChar) return prevChar;
                    const updatedClassLevels = prevChar.data.class_levels.map(cls => {
                        if (
                            feature &&
                            cls.class_name.toLowerCase() === feature.classId.toLowerCase()
                        ) {
                            return {
                                ...cls,
                                subclass: subclassId
                            };
                        }
                        return cls;
                    });
                    return {
                        ...prevChar,
                        class: {
                            ...prevChar.class,
                            subclass: subclassId
                        },
                        data: {
                            ...prevChar.data,
                            subclass: subclassId,
                            class_levels: updatedClassLevels
                        }
                    };
                });
            }
            saveCharacter(updatePayload);
            return next;
        });
    }, [saveCharacter]);

    const handleLevelUp = () => {
        if (!character) return;

        if (!selectedLevelUpClass) {
            addAlert("Choose a class before leveling up.", "warning");
            return;
        }
        const nextLevel = character.level + 1;
        const requiredXp = XP_THRESHOLDS[nextLevel] || 0;

        if (xp < requiredXp) {
            addAlert(`Not enough XP to level up to ${nextLevel}. Required: ${requiredXp}`, 'warning');
            return;
        }

        const loadingId = addAlert(`Initiating Level Up to Level ${nextLevel}...`, 'loading', 0);
        setLevelingUpAlertId(loadingId);

        fetch(`${API_BASE_URL}/api/characters/${id}/levelup`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                class_name: selectedLevelUpClass
            })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {

                    setShowXpEditor(false);
                    setShowMulticlassSelection(false);
                    setPreviewChoices({});
                    setLevelUpPreviewMode(false);
                    setSelectedLevelUpClass(null);

                    setPreviousLevel(character.level);
                    setLevelUpClass(selectedLevelUpClass);

                    setShowLevelUpOverlay(true);

                    updateAlert(
                        loadingId,
                        "Level up complete!",
                        "success",
                        5000
                    );

                    fetchData();
                } else {
                    updateAlert(loadingId, data.error || "Level up failed", 'error', 5000);
                    setLevelingUpAlertId(null);
                }
            })
            .catch(err => {
                console.error("Error during level up:", err);
                updateAlert(loadingId, "A mystical error occurred during Level Up.", 'error', 5000);
                setLevelingUpAlertId(null);
            });
    };

    const handleLevelDown = async () => {
        if (!(await confirm("Are you sure you want to level down? This will reset your stats for the previous level."))) return;

        try {
            const res = await fetch(`${API_BASE_URL}/api/characters/${id}/leveldown`, {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}` }
            });
            const data = await res.json();
            if (res.ok) {
                addAlert("Level down successful", "info");

                if (data.data?.spell_slots_current) {
                    setSpellSlotsCurrent(
                        data.data.spell_slots_current
                    );
                }

                fetchData();
            } else {
                addAlert(data.error || "Level down failed", 'error');
            }
        } catch (err) {
            addAlert("An error occurred during level down", 'error');
        }
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

    const getMulticlassStatus = (cls) => {
        const className = cls.toLowerCase();

        const existingClasses = character?.data?.class_levels || [];

        const alreadyHasClass = existingClasses.some(
            c => c.class_name.toLowerCase() === className
        );

        if (alreadyHasClass) {
            return "owned";
        }

        const targetClass = multiclassRules[className];

        if (!targetClass) {
            return "blocked";
        }

        // Supports both:
        // "Strength"
        // ["Strength", "Dexterity"]
        const requiredAbilities = Array.isArray(targetClass.primary_ability)
            ? targetClass.primary_ability
            : [targetClass.primary_ability];


        const hasRequirement = requiredAbilities.some(ability => {
            const abilityKey = ability.toLowerCase();

            const score = character?.data?.abilities?.[abilityKey] || 0;

            return score >= 13;
        });


        if (!hasRequirement) {
            return "blocked";
        }

        return "available";
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

    const toggleFeatureActive = (featureId) => {
        setActiveFeatures(prevActive => {
            const isActive = prevActive.includes(featureId);

            const nextActive = isActive
                ? prevActive.filter(id => id !== featureId)
                : [...prevActive, featureId];

            setFeatureUses(prevUses => {
                const currentUses = prevUses?.[featureId] ?? 0;

                const nextUses = {
                    ...prevUses,
                    [featureId]: isActive
                        ? currentUses + 1
                        : Math.max(0, currentUses - 1)
                };

                return nextUses;
            });

            return nextActive;
        });
    };

    const updateCurrentHp = (value) => {
        let val = parseInt(value) || 0;
        val = Math.min(val, effectiveMaxHp);
        val = Math.max(0, val);
        setCurrentHp(val);
        saveCharacter({ hp_current: val });
    };

    useEffect(() => {
        if (!characterLoaded) return;
        saveCharacter({
            activeFeatures,
            featureUses,
            featureNotes
        });
    }, [activeFeatures, featureUses, featureNotes, characterLoaded, saveCharacter]);

    useEffect(() => {
        if (Object.keys(spellSlotsCurrent).length === 0) return;

        saveCharacter({
            spell_slots_current: spellSlotsCurrent
        });
    }, [spellSlotsCurrent, saveCharacter]);

    const applyStatModifier = async (type, statKey, newValue) => {
        setIsApplyingStatMod(true);
        const loadingId = addAlert(`Applying changes to ${statModConfig.label}...`, "loading", 0);

        try {
            const response = await fetch(`${API_BASE_URL}/api/characters/${id}/mod-stats`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ type, stat: statKey, value: newValue })
            });

            if (!response.ok) throw new Error("Failed to update stat modifier");

            await fetchData(); // Sync all independent state variables
            updateAlert(loadingId, `${statModConfig.label} updated successfully!`, "success", 5000);
            setStatModConfig({ isOpen: false });
        } catch (err) {
            updateAlert(loadingId, err.message, "error", 5000);
        } finally {
            setIsApplyingStatMod(false);
        }
    };

    const handleCompleteRest = async (restType, restData) => {
        const loadingId = addAlert(`Processing ${restType.charAt(0).toUpperCase() + restType.slice(1)} Rest...`, "loading", 0);
        try {
            const endpoint = restType === 'long' ? 'long' : 'short';
            const response = await fetch(`${API_BASE_URL}/api/characters/${id}/rest/${endpoint}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(restData)
            });

            if (!response.ok) throw new Error(`Failed to process ${restType} rest`);

            // Apply precise feature use restoration based on rechargeInfo objects
            if (restData.rechargedFeatures?.length) {
                setFeatureUses(prev => {
                    const updatedUses = { ...prev };
                    restData.rechargedFeatures.forEach(info => {
                        if (!info || !info.id) return;
                        if (info.restore === 'full' || !info.maxUses) {
                            // Full restore: delete the key so UI falls back to showing maxUses
                            delete updatedUses[info.id];
                        } else if (info.restore === 'partial') {
                            // Partial restore: add `amount` uses, capped at maxUses
                            const current = updatedUses[info.id] !== undefined
                                ? updatedUses[info.id]
                                : info.maxUses;
                            updatedUses[info.id] = Math.min(info.maxUses, current + info.amount);
                        }
                    });
                    return updatedUses;
                });
            }

            await fetchData(); // Sync all independent state variables (HP, Hit Dice, etc)
            updateAlert(loadingId, `${restType.charAt(0).toUpperCase() + restType.slice(1)} Rest complete!`, "success", 5000);
        } catch (err) {
            updateAlert(loadingId, err.message, "error", 5000);
            throw err;
        }
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

    const removeFromInventory = async (index) => {
        const itemToRemove = inventoryItems[index];
        if (!itemToRemove) return;

        let shouldRemoveAll = false;
        if (itemToRemove.quantity > 1) {
            const result = await confirm(`This item has ${itemToRemove.quantity} copies. \n\nConfirm to remove JUST ONE copy, or Cancel to proceed to STACK REMOVAL option.`);
            if (result) {
                shouldRemoveAll = false;
            } else {
                if (await confirm(`Are you sure you want to remove ALL copies of ${itemToRemove.name}?`)) {
                    shouldRemoveAll = true;
                } else {
                    return;
                }
            }
        } else {
            if (!(await confirm(`Are you sure you want to remove ${itemToRemove.name} from your inventory?`))) return;
            shouldRemoveAll = true;
        }

        try {
            const res = await fetch(`${API_BASE_URL}/api/characters/${id}/inventory/remove`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ index, remove_all: shouldRemoveAll })
            });

            if (res.ok) {
                addAlert("Item removed", 'info');
                fetchData();
            } else {
                addAlert("Failed to remove item", 'error');
            }
        } catch (err) {
            addAlert("An error occurred", 'error');
        }
    };

    const groupedInventory = useMemo(() => inventoryItems.reduce((acc, item, originalIndex) => {
        let category = item.category || "Other";
        if (armorRules[item.name]) category = "Armor";
        else if (weaponRules[item.name]) category = "Weapon";

        const term = (character?.data?.inventorySearchTerm || "").toLowerCase();
        if (term && !item.name.toLowerCase().includes(term)) return acc;

        const itemWithCat = { ...item, category, originalIndex };

        if (!acc[category]) acc[category] = [];
        acc[category].push(itemWithCat);

        // Populate the "All" category
        acc["All"].push(itemWithCat);

        return acc;
    }, { "All": [] }), [inventoryItems, armorRules, weaponRules, character?.data?.inventorySearchTerm]);

    const displayedItems = groupedInventory[inventoryFilter] || [];

    // --- Drag and Drop Handlers for Inventory ---
    const togglePrivacy = () => {
        if (!isOwner && !isAdmin) return;

        fetch(`${API_BASE_URL}/api/characters/${id}/toggle-privacy`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    setCharacter(prev => ({ ...prev, is_private: data.is_private }));
                }
            })
            .catch(err => console.error("Error toggling privacy:", err));
    };

    const handleAcceptItemWithScroll = async (originalIndex) => {
        const itemElement = document.getElementById(`inv-item-${originalIndex}`);
        if (itemElement) {
            itemElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            itemElement.classList.add('highlight-gift-flash');

            // Wait for user to see the highlight
            setTimeout(async () => {
                await handleAcknowledgeItem(originalIndex);
                itemElement.classList.remove('highlight-gift-flash');
            }, 2500);
        } else {
            // Fallback if element not found (e.g. filtered out)
            setInventoryFilter("All");
            setTimeout(() => {
                const retryEl = document.getElementById(`inv-item-${originalIndex}`);
                if (retryEl) {
                    retryEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    retryEl.classList.add('highlight-gift-flash');
                }
                handleAcknowledgeItem(originalIndex);
            }, 100);
        }
    };

    const transferItem = async (index, targetCharId) => {
        const itemToTransfer = inventoryItems[index];
        if (!await confirm(`Are you sure you want to send ${itemToTransfer.name} to this character?`)) return;

        try {
            const res = await fetch(`${API_BASE_URL}/api/host/${activeSession.id}/transfer-item`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    sender_char_id: id,
                    receiver_char_id: targetCharId,
                    item_index: index
                })
            });
            const data = await res.json();
            if (res.ok) {
                addAlert(`Sent ${itemToTransfer.name}!`, 'success');
                fetchData();
                setShowTransferModal(false);
            } else {
                addAlert(data.error || "Transfer failed", 'error');
            }
        } catch (err) {
            addAlert("An error occurred during transfer", 'error');
        }
    };

    const transferGold = async (targetCharId) => {
        if (!await confirm(`Are you sure you want to send ${goldTransferAmount} GP to this character?`)) return;

        try {
            const res = await fetch(`${API_BASE_URL}/api/host/${activeSession.id}/transfer-gold`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    sender_char_id: id,
                    receiver_char_id: targetCharId,
                    amount: goldTransferAmount
                })
            });
            const data = await res.json();
            if (res.ok) {
                addAlert(`Sent ${goldTransferAmount} GP!`, 'success');
                fetchData();
                setShowGoldTransferModal(false);
            } else {
                addAlert(data.error || "Transfer failed", 'error');
            }
        } catch (err) {
            addAlert("An error occurred during gold transfer", 'error');
        }
    };

    const handleAcknowledgeGold = async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/api/characters/${id}/acknowledge-gold-gift`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (res.ok) {
                setCharacter(prev => ({
                    ...prev,
                    data: { ...prev.data, gold_gifts: [] }
                }));
            }
        } catch (err) {
            console.error("Failed to acknowledge gold gift:", err);
        }
    };

    const handleBack = () => {
        // If history length is 1, it means this was likely opened in a new tab
        if (window.history.length > 1) {
            navigate(-1);
        } else {
            // Try to close the window, fallback to hub if it fails
            window.close();
            // A small delay to check if close worked, otherwise navigate
            setTimeout(() => {
                navigate('/characters-hub');
            }, 100);
        }
    };

    const handleAcknowledgeItem = async (itemIndex) => {
        try {
            const res = await fetch(`${API_BASE_URL}/api/characters/${id}/acknowledge-item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ item_index: itemIndex })
            });

            if (res.ok) {
                // Update local inventory
                const newInventory = inventoryItems.map((item, idx) => {
                    if (idx === itemIndex) {
                        return { ...item, is_new_gift: false };
                    }
                    return item;
                });
                setInventoryItems(newInventory);
            }
        } catch (err) {
            console.error("Failed to acknowledge item:", err);
        }
    };

    const updateNotes = (newNotes) => {
        if (viewOnly || loading) return;
        saveCharacter({ notes: newNotes });
    };

    const handleSaveLayout = (current, all) => {
        if (viewOnly || isLayoutLocked || loading) return;
        setLayout(all);
        saveCharacter({ layout: all });
    };

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

    const handleDismissLevelUp = () => {
        setShowLevelUpOverlay(false);
        saveCharacter({ level_up_pending: false, level_one_pending: false });
    };

    // --- Rich Rendering Components ---

    // --- Dynamic Feature Logic ---
    const availableFeatures = useMemo(() => {
        if (!character) return [];

        const allFeatures = [];
        const currentLevel = character.level;

        // 1. Add Class Features (Multiclass Support)
        const classLevels = character.data?.class_levels || [];
        classLevels.forEach(classEntry => {
            const classId = classEntry.class_name.toLowerCase();
            const classLevel = classEntry.level;
            const rules = allClassRules?.[classId];
            if (!rules?.features) return;
            Object.keys(rules.features).forEach(lvl => {
                if (parseInt(lvl) <= classLevel) {
                    allFeatures.push(...rules.features[lvl].map(f => ({
                        ...f,
                        id: `${classId}_${f.id}_${lvl}`,
                        source: `Class: ${rules.name}`,
                        level: lvl,
                        classId: classId,
                        classLevel: parseInt(lvl)
                    })));
                }
            });
        });

        // 2. Add Subclass Features
        classLevels.forEach(classEntry => {
            const classId = classEntry.class_name.toLowerCase();
            const subclassId = classEntry.subclass;
            const rules = allClassRules?.[classId];

            if (!subclassId || !rules?.subclasses) return;

            const subclassInfo = rules.subclasses[subclassId];

            if (!subclassInfo?.features) return;

            Object.keys(subclassInfo.features).forEach(lvl => {
                if (parseInt(lvl) <= classEntry.level) {
                    allFeatures.push(
                        ...subclassInfo.features[lvl].map(f => ({
                            ...f,
                            source: `Subclass: ${subclassInfo.name}`,
                            level: lvl,
                            classId: classId,
                            classLevel: parseInt(lvl)
                        }))
                    );
                }
            });
        });

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

        // 5. Add Chosen Feats from feature choices
        const savedChoices = character.data?.featureChoices || {};
        Object.keys(savedChoices).forEach(choiceId => {
            if (choiceId.includes('feat_or_asi') || choiceId.includes('epic_boon')) {
                const choices = savedChoices[choiceId];
                const choiceArr = Array.isArray(choices) ? choices : (choices ? [choices] : []);

                const levelMatch = choiceId.match(/_(\d+)$/);
                const featLevel = levelMatch ? parseInt(levelMatch[1]) : 1;

                if (featLevel <= currentLevel) {
                    choiceArr.forEach(choiceName => {
                        const skipStats = ['Feat', 'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'];
                        if (skipStats.includes(choiceName)) return; // Skip ASI stats or placeholders

                        const pools = [...(ruleOptions.origin || []), ...(ruleOptions.general || []), ...(ruleOptions.epic_boon || [])];
                        const featData = pools.find(f => (f.name || f.id) === choiceName);

                        if (featData) {
                            allFeatures.push({
                                id: `chosen_feat_${choiceId}_${choiceName.replace(/\s+/g, '')}`,
                                name: `Feat: ${featData.name}`,
                                description: featData.description || (featData.effects ? featData.effects.join("\n\n") : ""),
                                source: 'Selected Feat',
                                level: featLevel.toString(),
                                details: featData.details || {},
                                effects: featData.effects,
                                prerequisite: featData.prerequisite
                            });
                        }
                    });
                }
            }
        });

        return allFeatures;
    }, [allClassRules, character, speciesRules, backgroundRules, ruleOptions]);

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

        const acModifier = character.data.ac_modifier || 0;
        return baseAC + dexBonus + shieldBonus + acModifier;
    }, [character, inventoryItems, armorRules, availableFeatures]);


    // --- Dynamic Defenses Logic ---
    const defenses = useMemo(() => {
        const result = { resistances: [], immunities: [] };

        if (!availableFeatures) return result;

        availableFeatures.forEach(f => {
            const isActive = activeFeatures.includes(f.id);

            // Rage special case
            if (
                f.id === "barbarian_rage" &&
                !isActive
            ) {
                return;
            }

            if (f.details?.Resistances) {
                const res = typeof f.details.Resistances === "string"
                    ? f.details.Resistances.split(", ")
                    : f.details.Resistances;

                result.resistances = [...new Set([...result.resistances, ...res])];
            }

            if (f.details?.Immunities) {
                const imm = typeof f.details.Immunities === "string"
                    ? f.details.Immunities.split(", ")
                    : f.details.Immunities;

                result.immunities = [...new Set([...result.immunities, ...imm])];
            }
        });

        return result;
    }, [availableFeatures, activeFeatures]);

    const conditions = useMemo(() => character?.data?.conditions || { exhaustion: 0 }, [character]);

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

    const toggleSpellSelection = (name, className, mode = "prepared") => {
        const scClasses = getSpellcastingClasses(character, allClassRules);
        const migratedSpells = migrateSpellsData(character.data.spells, scClasses);

        if (className === "wizard" && mode === "spellbook") {
            const spellbookList = migratedSpells.wizard_spellbook ? [...migratedSpells.wizard_spellbook] : [];
            const preparedList = migratedSpells.wizard ? [...migratedSpells.wizard] : [];

            const isCantrip = availableSpells["0"]?.some(s => s.name === name);
            if (isCantrip) {
                const classData = scClasses.find(c => c.className === "wizard");
                const activeRules = classData?.rules || spellcastingRules;
                const activeLevel = classData?.level || character.level;
                const cantripsKnownLimit = resolveScalingValue(activeRules?.cantrips_known, activeLevel) || 0;
                const cantripsCount = preparedList.filter(n => availableSpells["0"]?.some(s => s.name === n)).length;

                if (preparedList.includes(name)) {
                    migratedSpells.wizard = preparedList.filter(n => n !== name);
                } else if (cantripsCount < cantripsKnownLimit) {
                    migratedSpells.wizard = [...preparedList, name];
                }
            } else {
                if (spellbookList.includes(name)) {
                    migratedSpells.wizard_spellbook = spellbookList.filter(n => n !== name);
                    migratedSpells.wizard = preparedList.filter(n => n !== name);
                } else {
                    migratedSpells.wizard_spellbook = [...spellbookList, name];
                }
            }
            saveCharacter({ spells: migratedSpells });
            setCharacter(prev => ({ ...prev, data: { ...prev.data, spells: migratedSpells } }));
            return;
        }

        if (className === "wizard" && mode === "prepared") {
            const preparedList = migratedSpells.wizard ? [...migratedSpells.wizard] : [];
            const spellbookList = migratedSpells.wizard_spellbook ? [...migratedSpells.wizard_spellbook] : [];
            const isCantrip = availableSpells["0"]?.some(s => s.name === name);

            if (isCantrip) {
                const classData = scClasses.find(c => c.className === "wizard");
                const activeRules = classData?.rules || spellcastingRules;
                const activeLevel = classData?.level || character.level;
                const cantripsKnownLimit = resolveScalingValue(activeRules?.cantrips_known, activeLevel) || 0;
                const cantripsCount = preparedList.filter(n => availableSpells["0"]?.some(s => s.name === n)).length;

                if (preparedList.includes(name)) {
                    migratedSpells.wizard = preparedList.filter(n => n !== name);
                } else if (cantripsCount < cantripsKnownLimit) {
                    migratedSpells.wizard = [...preparedList, name];
                }
            } else {
                if (!spellbookList.includes(name)) return;

                const classData = scClasses.find(c => c.className === "wizard");
                const activeRules = classData?.rules || spellcastingRules;
                const activeLevel = classData?.level || character.level;
                const spellsPreparedLimit = resolveScalingValue(activeRules?.spells_prepared, activeLevel) || 0;
                const cantripsCount = preparedList.filter(n => availableSpells["0"]?.some(s => s.name === n)).length;
                const preparedCount = preparedList.length - cantripsCount;

                if (preparedList.includes(name)) {
                    migratedSpells.wizard = preparedList.filter(n => n !== name);
                } else if (preparedCount < spellsPreparedLimit) {
                    migratedSpells.wizard = [...preparedList, name];
                }
            }
            saveCharacter({ spells: migratedSpells });
            setCharacter(prev => ({ ...prev, data: { ...prev.data, spells: migratedSpells } }));
            return;
        }

        const currentList = migratedSpells[className] ? [...migratedSpells[className]] : [];

        if (currentList.includes(name)) {
            // Remove
            migratedSpells[className] = currentList.filter(n => n !== name);
            saveCharacter({ spells: migratedSpells });
            setCharacter(prev => ({ ...prev, data: { ...prev.data, spells: migratedSpells } }));
        } else {
            // Add
            const classData = scClasses.find(c => c.className === className);
            if (!classData) return;
            const activeRules = classData.rules;
            const activeLevel = classData.level;

            const cantripsKnownLimit = resolveScalingValue(activeRules.cantrips_known, activeLevel) || 0;
            const spellsPreparedLimit = resolveScalingValue(activeRules.spells_prepared, activeLevel) || 0;

            const cantripsCount = currentList.filter(n => {
                for (const lvl in availableSpells) {
                    if (availableSpells[lvl].some(s => s.name === n && lvl === "0")) return true;
                }
                return false;
            }).length;

            const preparedCount = currentList.length - cantripsCount;

            let isNewCantrip = false;
            if (availableSpells["0"]?.some(s => s.name === name)) {
                isNewCantrip = true;
            }

            if (isNewCantrip) {
                if (cantripsCount >= cantripsKnownLimit) return;
            } else {
                if (preparedCount >= spellsPreparedLimit) return;
            }

            currentList.push(name);
            migratedSpells[className] = currentList;
            saveCharacter({ spells: migratedSpells });
            setCharacter(prev => ({ ...prev, data: { ...prev.data, spells: migratedSpells } }));
        }
    };

    // --- Dynamic Spellcasting Rule Resolution ---
    const spellcastingRules = useMemo(() => {
        if (!character || !allClassRules) return null;
        let rules = null;
        let source = null;
        const classLevels = character.data?.class_levels || [];

        // Check every class the character has
        for (const classEntry of classLevels) {
            const className = classEntry.class_name?.toLowerCase();
            const classData = allClassRules[className];
            if (!classData) continue;

            // Check subclass spellcasting
            const subclassName = classEntry.subclass?.toLowerCase();
            if (subclassName && classData.subclasses?.[subclassName]) {
                const subclassFeatures = classData.subclasses[subclassName].features;
                for (const level in subclassFeatures) {
                    const feature = subclassFeatures[level]
                        .find(f =>
                            f.name === "Spellcasting" ||
                            f.id?.includes("spellcasting")
                        );
                    if (feature?.details) {
                        rules = {
                            ...feature.details
                        };
                        source = "Subclass";
                        break;
                    }
                }
            }

            // Check normal class spellcasting
            if (!rules && classData.spellcasting) {
                rules = {
                    ...classData.spellcasting
                };
                source = "Class";
            }
            if (rules) break;
        }
        return rules
            ? {
                ...rules,
                source
            }
            : null;
    }, [allClassRules, character]);

    const hasSpellcasting = useMemo(() => {
        return spellcastingRules !== null;
    }, [spellcastingRules]);

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
        <div className={`character-sheet-container premium-theme ${!isLayoutLocked ? "layout-unlocked" : ""} ${viewOnly ? "view-only-mode" : "edit-mode"}`}>
            {showTransferModal && (
                <div className="modal-overlay transfer-modal-overlay" onClick={() => setShowTransferModal(false)}>
                    <div className="transfer-modal card premium-theme" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3><i className="fa-solid fa-gift"></i> Send Item</h3>
                            <button className="close-btn" onClick={() => setShowTransferModal(false)}>✕</button>
                        </div>
                        <div className="transfer-target-list">
                            <p className="notice">Select a recipient in <strong>{activeSession.run.title}</strong>:</p>
                            {sessionParticipants.map(participant => (
                                <div
                                    key={participant.character.id}
                                    className="recipient-option"
                                    onClick={() => transferItem(itemToTransfer.originalIndex, participant.character.id)}
                                >
                                    <div className="recipient-info">
                                        <span className="char-name">{participant.character.name}</span>
                                        <span className="owner-name">Owner: {participant.username}</span>
                                    </div>
                                    <i className="fa-solid fa-chevron-right"></i>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}


            <BackToTop />
            <div className="sheet-top-bar">
                <div className="top-bar-left">
                    <button onClick={handleBack} className="back-button">
                        <i className="fa-solid fa-arrow-left"></i> Back
                    </button>
                    {(isOwner || isAdmin || isDM) && (
                        <button
                            className="mode-toggle-btn"
                            onClick={() => navigate(isEditMode ? `/characters/${id}` : `/characters/${id}/edit`, { replace: true })}
                        >
                            {isEditMode ? "👁 Switch to View Mode" : "✎ Switch to Edit Mode"}
                        </button>
                    )}
                </div>

                <div className="top-bar-right">
                    {(isOwner || isAdmin) && (
                        <button
                            className={`privacy-toggle-btn ${character.is_private ? 'is-private' : 'is-public'}`}
                            onClick={togglePrivacy}
                            title={character.is_private ? "Character is Private" : "Character is Public"}
                        >
                            {character.is_private ? "🔒 Private" : "🔓 Public"}
                        </button>
                    )}

                    {!viewOnly && (
                        <button
                            onClick={() => setIsLayoutLocked(!isLayoutLocked)}
                            className={`lock-button ${isLayoutLocked ? "locked" : "unlocked"}`}
                        >
                            {isLayoutLocked ? "🔒 Unlock Layout" : "🔓 Lock & Save Layout"}
                        </button>
                    )}
                </div>
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
                isDraggable={!isLayoutLocked && !viewOnly}
                isResizable={!isLayoutLocked && !viewOnly}
                onLayoutChange={handleSaveLayout}
            >
                <div key="header" className="widget card header-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <div className="header-content">
                        <div className="header-main">
                            <div>
                                {!viewOnly && isEditingName ? (
                                    <div className="char-name-edit-container">
                                        <input
                                            className="char-name-input"
                                            type="text"
                                            value={nameInput}
                                            autoFocus
                                            maxLength={30}
                                            onChange={e => setNameInput(e.target.value)}
                                            onKeyDown={e => {
                                                if (e.key === 'Enter') handleRenameName(nameInput);
                                                if (e.key === 'Escape') setIsEditingName(false);
                                            }}
                                        />
                                        <span className="level-badge">Lvl {character.level}</span>
                                        <div className="char-name-actions">
                                            <button className="icon-btn save" onClick={() => handleRenameName(nameInput)} title="Save Name"><i className="fa-solid fa-check"></i></button>
                                            <button className="icon-btn cancel" onClick={() => setIsEditingName(false)} title="Cancel"><i className="fa-solid fa-xmark"></i></button>
                                        </div>
                                    </div>
                                ) : (
                                    <h2
                                        className={!viewOnly ? 'char-name-editable' : ''}
                                        onClick={() => {
                                            if (!viewOnly) {
                                                setNameInput(character.name);
                                                setIsEditingName(true);
                                            }
                                        }}
                                        title={!viewOnly ? 'Click to rename' : ''}
                                    >
                                        {character.name} <span className="level-badge">Lvl {character.level}</span>
                                        {!viewOnly && <i className="fa-solid fa-pen-to-square char-name-edit-icon"></i>}
                                    </h2>
                                )}
                                <div
                                    className="xp-bar-container"
                                    onClick={() => !viewOnly && setShowXpEditor(true)}
                                    style={{ cursor: viewOnly ? "default" : "pointer" }}
                                    title={viewOnly ? "" : "Edit Experience"}
                                >
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
                            {!viewOnly && (
                                <div className="header-actions">
                                    <button
                                        className="rest-trigger-btn"
                                        onClick={() => setShowRestOverlay(true)}
                                    >
                                        <i className="fa-solid fa-campground"></i> Take a Rest
                                    </button>
                                    {character?.level < 20 && (isOwner || isAdmin) && (
                                        <button
                                            className={`levelup-button ${xp >= (XP_THRESHOLDS[character.level + 1] || 0) ? "available" : "locked"}`}
                                            onClick={openLevelUpSelection}
                                            disabled={xp < (XP_THRESHOLDS[character.level + 1] || 0)}
                                        >
                                            {xp >= (XP_THRESHOLDS[character.level + 1] || 0) ? "✧ LEVEL UP ✧" : "Level Up"}
                                        </button>
                                    )}
                                </div>
                            )}
                        </div>
                        <div className="header-details">
                            {character.data.class_levels?.map((cls, index) => (
                                <span key={index} className="detail-pill class-pill">
                                    {cls.class_name} {cls.level}
                                </span>
                            ))}
                            <span className="detail-pill species-pill">
                                {character.data.species}
                                {character.data.species_variant ? ` (${character.data.species_variant})` : ""} |
                                {character.data.size || speciesRules?.size || "Medium"} |
                                {speciesRules?.speed || "30 ft."}
                            </span>
                            <span className="detail-pill background-pill">{character.data.background}</span>
                        </div>
                        <div className="header-proficiencies">
                            {character.data.proficiencies && (
                                <>
                                    {character.data.proficiencies.armor?.length > 0 && (
                                        <div className="proficiency-group">
                                            <span className="proficiency-label">Armor:</span>
                                            <span>{character.data.proficiencies.armor.join(", ")}</span>
                                        </div>
                                    )}
                                    {character.data.proficiencies.weapons?.length > 0 && (
                                        <div className="proficiency-group">
                                            <span className="proficiency-label">Weapons:</span>
                                            <span>{character.data.proficiencies.weapons.join(", ")}</span>
                                        </div>
                                    )}
                                    {character.data.proficiencies.tools?.length > 0 && (
                                        <div className="proficiency-group">
                                            <span className="proficiency-label">Tools:</span>
                                            <span>{character.data.proficiencies.tools.join(", ")}</span>
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                        {(defenses.resistances.length > 0 || defenses.immunities.length > 0 || conditions.exhaustion > 0) && (
                            <div className="header-defenses">
                                {(defenses.resistances.length > 0 || defenses.immunities.length > 0) && (
                                    <>
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
                                    </>
                                )}
                                {conditions.exhaustion > 0 && (
                                    <div className="defense-group conditions-group">
                                        <span className="defense-label">Conditions:</span>
                                        <div className="defense-tags">
                                            <span className="defense-tag condition exhaustion">Exhaustion (Level {conditions.exhaustion})</span>
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
                            {viewOnly ? (
                                <span className="hp-current-view">{currentHp}</span>
                            ) : (
                                <input
                                    type="number"
                                    value={currentHp}
                                    onChange={(e) => updateCurrentHp(e.target.value)}
                                    className="hp-current-input"
                                />
                            )}
                            <span
                                className="hp-sep"
                                onClick={() => !viewOnly && setStatModConfig({
                                    isOpen: true,
                                    type: "hp_max",
                                    statKey: null,
                                    value: maxHpModifier,
                                    label: "Max HP Modifier"
                                })}
                            >/</span>
                            <span className={`hp-max ${!viewOnly ? 'clickable' : ''}`} onClick={() => !viewOnly && setStatModConfig({
                                isOpen: true,
                                type: "hp_max",
                                statKey: null,
                                value: maxHpModifier,
                                label: "Max HP Modifier"
                            })}>
                                {effectiveMaxHp}
                            </span>
                            <div className="ac-display" title="Armor Class">
                                <div
                                    className={`ac-shield ${!viewOnly ? 'clickable' : ''}`}
                                    onClick={() => !viewOnly && setStatModConfig({
                                        isOpen: true,
                                        type: "ac",
                                        statKey: null,
                                        value: character.data.ac_modifier || 0,
                                        label: "Armor Class Modifier"
                                    })}
                                >
                                    <span className="ac-value">{ac}</span>
                                    <span className="ac-label">AC</span>
                                </div>
                            </div>
                        </div>
                        {/* Old HP Modifier UI Removed */}
                    </div>
                </div>

                <div key="abilities" className="widget card abilities-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <h3>Abilities</h3>
                    <div className="ability-grid">
                        {ABILITY_SCORES.map(({ name, key }) => {
                            const score = character.data?.abilities?.[key] ?? 10;
                            const mod = calculateModifier(score);
                            const hasAdvantage =
                                activeFeatures.includes("barbarian_rage") &&
                                key === "strength";
                            return (
                                <div
                                    key={key}
                                    className={`ability-box ${hasAdvantage ? 'has-adv' : ''} ${!viewOnly ? 'clickable' : ''}`}
                                    onClick={() => !viewOnly && setStatModConfig({
                                        isOpen: true,
                                        type: "ability",
                                        statKey: key,
                                        value: score,
                                        label: name
                                    })}
                                >
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
                            const hasAdvantage =
                                activeFeatures.includes("barbarian_rage") &&
                                key === "strength";
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
                                <div key={skill.key} className={`skill-row ${isFromBackground || viewOnly ? 'is-locked' : ''}`} title={isFromBackground ? `Gained from background (${character.data.background})` : ""}>
                                    <span
                                        className={`prof-toggle ${isProficient ? "is-prof" : ""} ${isFromBackground || viewOnly ? "locked" : ""}`}
                                        onClick={() => !isFromBackground && !viewOnly && toggleSkillProficiency(skill.key)}
                                    >
                                        {(isFromBackground || viewOnly) && <span className="lock-icon-tiny">🔒</span>}
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
                                characterData={character}
                                classRules={classRules}
                                allClassRules={allClassRules}
                                ruleOptions={ruleOptions}
                                featureChoices={featureChoices}
                                onUpdateChoice={(feature, options) => setChoiceOverlay({ isOpen: true, feature, options })}
                                featureNotes={featureNotes}
                                setFeatureNotes={setFeatureNotes}
                                availableSpells={availableSpells}
                                viewOnly={viewOnly}
                                isAuthorized={isAuthorized}
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
                                    characterData={character}
                                    classRules={classRules}
                                    ruleOptions={ruleOptions}
                                    featureChoices={featureChoices}
                                    onUpdateChoice={(feature, options) => setChoiceOverlay({ isOpen: true, feature, options })}
                                    featureNotes={featureNotes}
                                    setFeatureNotes={setFeatureNotes}
                                    availableSpells={availableSpells}
                                    viewOnly={viewOnly}
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
                            viewOnly={viewOnly}
                        />
                    </div>
                </div>

                <div key="notes" className="widget card notes-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <NotesWidget
                        notes={character.data.notes || []}
                        onUpdateNotes={updateNotes}
                        isEditMode={isEditMode}
                        viewOnly={viewOnly}
                    />
                </div>

                <div key="inventory" className="widget card inventory-widget">
                    {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                    <div className="inventory-header-row">
                        <h3>Inventory</h3>
                        <div className="search-wrapper inventory-search" style={{ margin: '0 15px', flex: 1 }}>
                            <input
                                type="text"
                                className="search-input"
                                placeholder="Search inventory..."
                                value={character.data.inventorySearchTerm || ""}
                                onChange={(e) => {
                                    const term = e.target.value;
                                    setCharacter(prev => ({ ...prev, data: { ...prev.data, inventorySearchTerm: term } }));
                                }}
                            />
                            <i className="fa-solid fa-magnifying-glass"></i>
                        </div>
                        <div className="gold-box" onClick={() => isAuthorized && activeSession && setShowGoldTransferModal(true)}>
                            <i className="fa-solid fa-coins"></i> Gold: {gold} GP
                            {isAuthorized && activeSession && <i className="fa-solid fa-right-left transfer-hint-icon"></i>}
                        </div>
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
                                id={`inv-item-${item.originalIndex}`}
                                className={`inventory-row ${item.is_new_gift ? 'is-gift' : ''} ${dragOverItemIndex === idx ? 'drag-over' : ''} ${draggedItemIndex === idx ? 'is-dragging' : ''}`}
                                draggable={inventoryFilter === "All"}
                                onDragStart={(e) => handleDragStart(e, idx)}
                                onDragOver={(e) => handleDragOver(e, idx)}
                                onDrop={(e) => handleDrop(e, idx)}
                                onDragEnd={handleDragEnd}
                            >
                                <div className="inv-item-info">
                                    <span className="drag-handle">⠿</span>
                                    <div className="item-name-stack">
                                        <div className="name-row">
                                            <span className="item-name">{item.name}</span>
                                            {item.is_new_gift && <span className="gift-badge">🎁 GIFT</span>}
                                        </div>
                                        {item.is_new_gift && (
                                            <span className="gift-source">From {item.from_character_name}</span>
                                        )}
                                    </div>
                                    {item.quantity > 1 && <span className="item-qty">x{item.quantity}</span>}
                                    <span className="item-cat-tag">{item.category}</span>
                                    {item.equipped && <span className="equipped-tag">E</span>}
                                </div>
                                <div className="inv-item-actions">
                                    {item.is_new_gift && isOwner && (
                                        <button
                                            className="acknowledge-btn"
                                            onClick={() => handleAcknowledgeItem(item.originalIndex)}
                                        >
                                            Accept
                                        </button>
                                    )}
                                    {!viewOnly && item.category === "Armor" && (
                                        <button
                                            className={`equip-btn ${item.equipped ? 'equipped' : ''}`}
                                            onClick={() => toggleEquip(item)}
                                        >
                                            {item.equipped ? "Unequip" : "Equip"}
                                        </button>
                                    )}
                                    {isAuthorized && activeSession && sessionParticipants.length > 0 && (
                                        <button
                                            className="send-item-btn"
                                            title="Send to another character"
                                            onClick={() => {
                                                setItemToTransfer({ ...item, originalIndex: item.originalIndex });
                                                setShowTransferModal(true);
                                            }}
                                        >
                                            <i className="fa-solid fa-paper-plane"></i>
                                        </button>
                                    )}
                                    {!viewOnly && <button className="del-btn" onClick={() => removeFromInventory(item.originalIndex)}>✕</button>}
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
                {hasSpellcasting && spellcastingRules && (
                    <div key="spellcasting" className="widget card spellcasting-widget">
                        <SpellcastingWidget
                            hasSpellcasting={hasSpellcasting}
                            spellcastingRules={spellcastingRules}
                            spellSlotsRules={spellSlotsRules}
                            character={character}
                            availableSpells={availableSpells}
                            isLayoutLocked={isLayoutLocked}
                            currentProficiencyBonus={currentProficiencyBonus}
                            onOpenOverlay={() => { setShowSpellOverlay(true); setSpellOverlayMinimized(false); }}
                            viewOnly={viewOnly}
                            spellSlotsCurrent={spellSlotsCurrent}
                            setSpellSlotsCurrent={setSpellSlotsCurrent}
                            addAlert={addAlert}
                            saveCharacter={saveCharacter}
                            allClassRules={allClassRules}
                        />
                    </div>
                )}
            </ResponsiveGridLayout>

            {(isOwner || isAdmin) && (
                <LevelUpOverlay
                    show={showLevelUpOverlay}
                    minimized={levelUpMinimized}
                    character={character}
                    previousLevel={previousLevel}
                    leveledUpClass={levelUpClass}
                    availableFeatures={availableFeatures}
                    onClose={handleDismissLevelUp}
                    onMinimize={() => setLevelUpMinimized(true)}
                    onRestore={() => setLevelUpMinimized(false)}
                    onOpenSpells={() => setShowSpellOverlay(true)}
                    spellcastingRules={classRules?.spellcasting}
                    featureUses={featureUses}
                    activeFeatures={activeFeatures}
                    onToggleFeature={toggleFeatureActive}
                    featureChoices={featureChoices}
                    onUpdateChoice={(feat, options) => {
                        if (levelUpMinimized) setLevelUpMinimized(false);
                        setChoiceOverlay({ isOpen: true, feature: feat, options });
                    }}
                    resolveOptionsForFeature={(feat) =>
                        resolveOptionsForFeature(
                            feat,
                            character,
                            classRules,
                            allClassRules,
                            ruleOptions,
                            availableSpells
                        )
                    }
                    classRules={classRules}
                    ruleOptions={ruleOptions}
                />
            )}

            <SpellOverlay
                show={showSpellOverlay}
                minimized={spellOverlayMinimized}
                onClose={() => {
                    setShowSpellOverlay(false);
                    setSpellOverlayPreviewMode(false);
                }}
                onMinimize={() => setSpellOverlayMinimized(true)}
                onRestore={() => setSpellOverlayMinimized(false)}
                availableSpells={availableSpells}
                character={spellOverlayPreviewMode ? { ...character, level: previewLevel, data: { ...character.data, spells: previewSpells } } : character}
                spellcastingRules={spellcastingRules}
                spellSlotsRules={spellSlotsRules}
                allClassRules={allClassRules}
                onToggleSpell={spellOverlayPreviewMode ? (name, className) => {
                    setPreviewSpells(prev => {
                        const migrated = migrateSpellsData(prev, getSpellcastingClasses(character, allClassRules));
                        const current = migrated[className] || [];
                        if (current.includes(name)) { migrated[className] = current.filter(n => n !== name); }
                        else { migrated[className] = [...current, name]; }
                        return migrated;
                    });
                } : toggleSpellSelection}
            />

            <RestOverlay
                show={showRestOverlay}
                preselectedRest={pendingRestType}
                character={character}
                currentHp={currentHp}
                maxHp={effectiveMaxHp}
                classRules={classRules}
                availableFeatures={availableFeatures}
                onClose={() => setShowRestOverlay(false)}
                onCompleteRest={handleCompleteRest}
            />

            <StatModifierOverlay
                config={statModConfig}
                onClose={() => setStatModConfig({ isOpen: false })}
                onApply={applyStatModifier}
                baseValue={statModConfig.type === 'ability' ? (character.data.base_abilities?.[statModConfig.statKey] ?? 10) : character.data.hp_max_base}
                isApplying={isApplyingStatMod}
            />

            {showXpEditor && (
                <div className="xp-editor-overlay" onClick={() => {
                    setIsFeatureListTransitioning(true);
                    setTimeout(() => {
                        setShowXpEditor(false);
                        setIsFeatureListTransitioning(false);
                        setIsFeatureListTransitioning(false);
                        setShowMulticlassSelection(false);
                        setSelectedLevelUpClass(null);
                        setPreviewChoices({});
                    }, 300);
                }}>
                    <div className={`xp-editor-panel ${showMulticlassSelection ? 'is-preview-active' : ''}`} onClick={e => e.stopPropagation()}>
                        <div className="xp-editor-header">
                            <h3>✧ Experience Editor ✧</h3>
                            <button className="close-btn" onClick={() => {
                                setIsFeatureListTransitioning(true);
                                setTimeout(() => {
                                    setShowXpEditor(false);
                                    setShowMulticlassSelection(false);
                                    setShowMulticlassSelection(false);
                                    setSelectedLevelUpClass(null);
                                    setIsFeatureListTransitioning(false);
                                    setPreviewChoices({});
                                }, 300);
                            }}>×</button>
                        </div>

                        <div className={`xp-editor-body ${showMulticlassSelection ? 'xp-editor-layout' : ''}`}>
                            {showMulticlassSelection && (
                                <div className="preview-section multiclass-selection-panel">
                                    <div className="preview-features-container">
                                        <h3>
                                            Choose Your Next Class
                                        </h3>

                                        <div className="multiclass-class-grid">
                                            {[
                                                "Barbarian",
                                                "Bard",
                                                "Cleric",
                                                "Druid",
                                                "Fighter",
                                                "Monk",
                                                "Paladin",
                                                "Ranger",
                                                "Rogue",
                                                "Sorcerer",
                                                "Warlock",
                                                "Wizard"
                                            ].map(cls => (
                                                <button
                                                    key={cls}
                                                    className={`multiclass-btn ${getMulticlassStatus(cls)}`}
                                                    onClick={() => {
                                                        const status = getMulticlassStatus(cls);

                                                        if (status === "blocked") {
                                                            const classData = multiclassRules?.[cls.toLowerCase()];

                                                            if (!classData) {
                                                                addAlert(
                                                                    `Unable to check requirements for ${cls}.`,
                                                                    "warning"
                                                                );
                                                                return;
                                                            }

                                                            const requiredAbilities = Array.isArray(classData.primary_ability)
                                                                ? classData.primary_ability
                                                                : [classData.primary_ability];

                                                            const missing = requiredAbilities
                                                                .filter(ability => {
                                                                    const score = character?.data?.abilities?.[ability.toLowerCase()] || 0;
                                                                    return score < 13;
                                                                })
                                                                .map(ability => `${ability} 13+`)
                                                                .join(" or ");

                                                            addAlert(
                                                                `You do not meet the requirements for ${cls}. Required: ${missing}`,
                                                                "warning"
                                                            );

                                                            return;
                                                        }

                                                        setSelectedLevelUpClass(cls);

                                                        // Auto-set preview level to the level the character would actually gain
                                                        const existingClasses = character?.data?.class_levels || [];
                                                        const existingEntry = existingClasses.find(
                                                            c => c.class_name.toLowerCase() === cls.toLowerCase()
                                                        );
                                                        const nextLevelForClass = existingEntry
                                                            ? (existingEntry.level || 0) + 1
                                                            : 1;
                                                        handlePreviewLevelChange(nextLevelForClass);
                                                    }}
                                                >
                                                    {cls}
                                                </button>
                                            ))}
                                        </div>

                                        {selectedLevelUpClass && (
                                            <div className="preview-section">
                                                <h4>Preview Level: {previewLevel}</h4>

                                                <div className="level-selector">
                                                    {Array.from({ length: 20 }, (_, i) => i + 1).map(lvl => (
                                                        <button
                                                            key={lvl}
                                                            className={`level-btn ${previewLevel === lvl ? 'active' : ''}`}
                                                            onClick={() => handlePreviewLevelChange(lvl)}
                                                        >
                                                            {lvl}
                                                        </button>
                                                    ))}
                                                </div>

                                                <div className="preview-features-container">
                                                    {spellcastingRules && (
                                                        <button
                                                            className="preview-choice-btn preview-spell-launcher"
                                                            onClick={() => {
                                                                setSpellOverlayPreviewMode(true);
                                                                setPreviewSpells(character.data.spells || []);
                                                                setShowSpellOverlay(true);
                                                            }}
                                                        >
                                                            📖 Manage Spells (Preview - Level {previewLevel})
                                                        </button>
                                                    )}
                                                    <div className={`preview-features-list ${isFeatureListTransitioning ? 'transitioning' : 'active'}`}>
                                                        {(() => {
                                                            const levelFeatures = [];
                                                            const previewClassRules = selectedLevelUpClass ? allClassRules[selectedLevelUpClass.toLowerCase()] : classRules;

                                                            // 1. Resolve Class features
                                                            if (previewClassRules?.features?.[previewLevel.toString()]) {
                                                                levelFeatures.push(...previewClassRules.features[previewLevel.toString()].map(f => ({ ...f, source: previewClassRules.name })));
                                                            }

                                                            // 2. Resolve Subclass features (handling preview choices)
                                                            const previewSubclassKey = Object.keys(previewChoices).find(k => k.endsWith('_subclass'));
                                                            const previewSubclassChoice = previewSubclassKey ? previewChoices[previewSubclassKey] : null;
                                                            const previewSubclassId = previewSubclassChoice ? (typeof previewSubclassChoice === 'string' ? previewSubclassChoice : (previewSubclassChoice.id || previewSubclassChoice.name)) : null;

                                                            const effectiveSubclassId = previewSubclassId || character.class?.subclass;
                                                            const scInfo = previewClassRules?.subclasses?.[effectiveSubclassId];

                                                            if (effectiveSubclassId && scInfo?.features?.[previewLevel.toString()]) {
                                                                levelFeatures.push(...scInfo.features[previewLevel.toString()].map(f => ({ ...f, source: scInfo.name })));
                                                            }

                                                            // 3. Resolve Chosen Feats (from previewChoices or saved featureChoices)
                                                            const combinedChoices = { ...(character.data?.featureChoices || {}), ...previewChoices };
                                                            Object.keys(combinedChoices).forEach(choiceId => {
                                                                if (choiceId.includes('feat_or_asi') || choiceId.includes('epic_boon')) {
                                                                    const choices = combinedChoices[choiceId];
                                                                    const choiceArr = Array.isArray(choices) ? choices : (choices ? [choices] : []);

                                                                    const levelMatch = choiceId.match(/_(\d+)$/);
                                                                    const featLevel = levelMatch ? parseInt(levelMatch[1]) : 1;

                                                                    if (featLevel === previewLevel) {
                                                                        choiceArr.forEach(choiceName => {
                                                                            const skipStats = ['Feat', 'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'];
                                                                            if (skipStats.includes(choiceName)) return;

                                                                            const pools = [...(ruleOptions.origin || []), ...(ruleOptions.general || []), ...(ruleOptions.epic_boon || [])];
                                                                            const featData = pools.find(f => (f.name || f.id) === choiceName);

                                                                            if (featData) {
                                                                                levelFeatures.push({
                                                                                    id: `chosen_feat_${choiceId}_${choiceName.replace(/\s+/g, '')}`,
                                                                                    name: `Feat: ${featData.name}`,
                                                                                    description: featData.description || (featData.effects ? featData.effects.join("\n\n") : ""),
                                                                                    source: 'Selected Feat (Preview)',
                                                                                    level: featLevel.toString(),
                                                                                    details: featData.details || {},
                                                                                    effects: featData.effects,
                                                                                    prerequisite: featData.prerequisite
                                                                                });
                                                                            }
                                                                        });
                                                                    }
                                                                }
                                                            });

                                                            if (levelFeatures.length === 0) {
                                                                return <div className="no-features-msg">No new features at this level.</div>;
                                                            }

                                                            const ITEMS_PER_PAGE = 3;
                                                            const totalPages = Math.ceil(levelFeatures.length / ITEMS_PER_PAGE);
                                                            const startIndex = (previewPage - 1) * ITEMS_PER_PAGE;
                                                            const visibleFeatures = levelFeatures.slice(startIndex, startIndex + ITEMS_PER_PAGE);

                                                            return (
                                                                <>
                                                                    {visibleFeatures.map(feature => {
                                                                        const options = resolveOptionsForFeature(feature, character, previewClassRules, ruleOptions, availableSpells);
                                                                        const choiceLimit = getChoiceLimitForFeature(feature, previewLevel);
                                                                        const hasChoices = options.length > 0 && choiceLimit > 0;
                                                                        const choice = previewChoices[feature.id];
                                                                        const isExpanded = previewExpandedFeatures[feature.id];

                                                                        return (
                                                                            <div key={feature.id} className={`preview-feature-card ${isExpanded ? 'expanded' : 'collapsed'}`}>
                                                                                <div
                                                                                    className="preview-feature-header"
                                                                                    onClick={() => setPreviewExpandedFeatures(prev => ({ ...prev, [feature.id]: !prev[feature.id] }))}
                                                                                >
                                                                                    <div className="preview-feature-header-left">
                                                                                        <span className="preview-feature-name">{feature.name}</span>
                                                                                        {(() => {
                                                                                            const currentChoices = Array.isArray(choice) ? choice : (choice ? [choice] : []);
                                                                                            const resolvedChoices = currentChoices.map(c => {
                                                                                                const found = options.find(o => (typeof o === 'string' ? o : (o.id || o.name)) === c);
                                                                                                return found ? (typeof found === 'string' ? { name: found } : found) : { name: c };
                                                                                            });
                                                                                            return resolvedChoices.map((rc, idx) => (
                                                                                                <span key={idx} className="feature-choice-badge">{rc.name}</span>
                                                                                            ));
                                                                                        })()}
                                                                                    </div>
                                                                                    <div className="preview-feature-header-right">
                                                                                        {hasChoices && (
                                                                                            <button
                                                                                                className="preview-choice-btn-compact"
                                                                                                onClick={(e) => {
                                                                                                    e.stopPropagation();
                                                                                                    setChoiceOverlay({
                                                                                                        isOpen: true,
                                                                                                        feature,
                                                                                                        options,
                                                                                                        isPreview: true
                                                                                                    });
                                                                                                }}
                                                                                            >
                                                                                                {choice ? "Change" : "Choose"}
                                                                                            </button>
                                                                                        )}
                                                                                        <i className={`fa-solid fa-chevron-${isExpanded ? 'up' : 'down'}`}></i>
                                                                                    </div>
                                                                                </div>
                                                                                {isExpanded && (
                                                                                    <div className="preview-feature-desc-container">
                                                                                        <PreviewChoiceDetails
                                                                                            feature={feature}
                                                                                            choice={choice}
                                                                                            character={character}
                                                                                            level={previewLevel}
                                                                                        />
                                                                                        {/* Render chosen feat details for feat_or_asi features */}
                                                                                        {feature.id?.includes('feat_or_asi') && choice && (() => {
                                                                                            const currentChoices = Array.isArray(choice) ? choice : [choice];
                                                                                            const chosenFeats = currentChoices.map(c => {
                                                                                                const found = options.find(o => (typeof o === 'string' ? o : (o.id || o.name)) === c);
                                                                                                return found ? (typeof found === 'string' ? { name: found } : found) : { name: c };
                                                                                            });
                                                                                            return (
                                                                                                <div className="chosen-options-list">
                                                                                                    {chosenFeats.map((opt, idx) => {
                                                                                                        const subChoiceId = `${feature.id}_sub_${idx}`;
                                                                                                        const rawSubChoice = previewChoices[subChoiceId];
                                                                                                        const currentSubChoices = Array.isArray(rawSubChoice) ? rawSubChoice : (rawSubChoice ? [rawSubChoice] : []);
                                                                                                        const hasSubChoices = !!opt.choice;

                                                                                                        return (
                                                                                                            <div key={idx} className="chosen-option-block">
                                                                                                                <div className="chosen-option-header">
                                                                                                                    <h4>Selected: {opt.name}</h4>
                                                                                                                    {hasSubChoices && (
                                                                                                                        <button
                                                                                                                            className="feature-choice-btn sub-choice-btn"
                                                                                                                            onClick={(e) => {
                                                                                                                                e.stopPropagation();
                                                                                                                                const virtualFeature = {
                                                                                                                                    ...feature,
                                                                                                                                    id: subChoiceId,
                                                                                                                                    name: `${opt.name} Choice`,
                                                                                                                                    details: { choice: opt.choice }
                                                                                                                                };
                                                                                                                                setChoiceOverlay({
                                                                                                                                    isOpen: true,
                                                                                                                                    feature: virtualFeature,
                                                                                                                                    options: opt.choice.options,
                                                                                                                                    isPreview: true
                                                                                                                                });
                                                                                                                            }}
                                                                                                                        >
                                                                                                                            {currentSubChoices.length > 0 ? 'Change' : 'Choose'}
                                                                                                                        </button>
                                                                                                                    )}
                                                                                                                </div>
                                                                                                                {currentSubChoices.length > 0 && (
                                                                                                                    <div className="sub-choice-badges">
                                                                                                                        {currentSubChoices.map((c, i) => (
                                                                                                                            <span key={i} className="feature-choice-badge sub-badge">{c}</span>
                                                                                                                        ))}
                                                                                                                    </div>
                                                                                                                )}
                                                                                                            </div>
                                                                                                        );
                                                                                                    })}
                                                                                                </div>
                                                                                            );
                                                                                        })()}
                                                                                        <div className="preview-feature-desc">
                                                                                            {feature.prerequisite && (() => {
                                                                                                const warning = checkPrerequisites(feature.prerequisite, character, previewLevel, classRules);
                                                                                                return (
                                                                                                    <div className={`feat-prerequisite-line ${warning ? 'unmet' : 'met'}`}>
                                                                                                        <span className="prereq-icon">{warning ? '⚠' : '✓'}</span>
                                                                                                        <span className="prereq-text">
                                                                                                            Prerequisite: {Array.isArray(feature.prerequisite) ? feature.prerequisite.flat().join(', ') : feature.prerequisite}
                                                                                                        </span>
                                                                                                        {warning && (
                                                                                                            <span className="prereq-warning-inline"> — Not met: {warning}</span>
                                                                                                        )}
                                                                                                    </div>
                                                                                                );
                                                                                            })()}

                                                                                            {feature.effects && Array.isArray(feature.effects) && (
                                                                                                <div className="feat-effects-list">
                                                                                                    {feature.effects.map((eff, i) => (
                                                                                                        <p key={i} className="feat-effect-item">{processRichText(eff)}</p>
                                                                                                    ))}
                                                                                                </div>
                                                                                            )}
                                                                                            {feature.description}
                                                                                        </div>
                                                                                    </div>
                                                                                )}
                                                                            </div>
                                                                        );
                                                                    })}

                                                                    {totalPages > 1 && (
                                                                        <div className="preview-pagination">
                                                                            {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                                                                                <button
                                                                                    key={p}
                                                                                    className={`page-dot ${previewPage === p ? 'active' : ''}`}
                                                                                    onClick={() => handlePreviewPageChange(p)}
                                                                                />
                                                                            ))}
                                                                        </div>
                                                                    )}
                                                                </>
                                                            );
                                                        })()}
                                                    </div>

                                                    <div className="selected-class-info" style={{ marginTop: '20px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '15px' }}>
                                                        <span style={{ fontSize: '1.2em', color: '#ffb347' }}>
                                                            Selected: {selectedLevelUpClass} (Level {previewLevel})
                                                        </span>

                                                        <button
                                                            className="action-btn levelup-btn"
                                                            onClick={handleLevelUp}
                                                            disabled={xp < (XP_THRESHOLDS[character.level + 1] || 0) || character.level >= 20}
                                                        >
                                                            ✧ Confirm Level Up ✧
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            <div className={showMulticlassSelection ? 'xp-editor-main' : ''}>
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
                                                if (rawVal.length > 7) rawVal = rawVal.slice(0, 7);
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
                                    {(isOwner || isAdmin) && (
                                        <button
                                            className="action-btn levelup-btn"
                                            onClick={() => {
                                                if (showMulticlassSelection) {
                                                    setShowMulticlassSelection(false);
                                                    setSelectedLevelUpClass(null);
                                                } else {
                                                    openLevelUpSelection();
                                                }
                                            }}
                                        >
                                            {showMulticlassSelection ? "Cancel Level Up" : "✧ Level Up ✧"}
                                        </button>
                                    )}
                                    {(isOwner || isAdmin) && (
                                        <button
                                            className="action-btn leveldown-btn"
                                            onClick={handleLevelDown}
                                            disabled={character.level <= 1 || xp !== (XP_THRESHOLDS[character.level] || 0)}
                                            title={xp !== (XP_THRESHOLDS[character.level] || 0) ? `Reset XP to ${XP_THRESHOLDS[character.level]} to Level Down` : ""}
                                        >
                                            ⚠ Level Down
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <FeatureChoiceOverlay
                isOpen={choiceOverlay.isOpen}
                feature={choiceOverlay.feature}
                options={choiceOverlay.options || []}
                onSelect={(fid, c) => handleFeatureChoice(fid, c, choiceOverlay.feature, choiceOverlay.isPreview)}
                currentChoice={choiceOverlay.feature ? (choiceOverlay.isPreview ? previewChoices[choiceOverlay.feature.id] : featureChoices[choiceOverlay.feature.id]) : null}
                onClose={() => setChoiceOverlay({ isOpen: false, feature: null })}
                level={choiceOverlay.isPreview ? previewLevel : character.level}
                character={character}
            />

            {showGoldTransferModal && (
                <div className="modal-overlay gold-transfer-overlay" onClick={() => setShowGoldTransferModal(false)}>
                    <div className="transfer-modal card premium-theme gold-modal" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3><i className="fa-solid fa-money-bill-transfer"></i> Transfer Gold</h3>
                            <button className="close-btn" onClick={() => setShowGoldTransferModal(false)}>✕</button>
                        </div>
                        <div className="gold-transfer-content">
                            <div className="gold-stats">
                                <div className="stat-item">
                                    <span className="label">Current Balance:</span>
                                    <span className="value">{gold} GP</span>
                                </div>
                                <div className="stat-item highlight">
                                    <span className="label">New Balance:</span>
                                    <span className="value">{gold - (parseInt(goldTransferAmount) || 0)} GP</span>
                                </div>
                            </div>

                            <div className="amount-input-group">
                                <label>Amount to Send:</label>
                                <div className="input-with-unit">
                                    <input
                                        type="number"
                                        min="1"
                                        max={gold}
                                        value={goldTransferAmount}
                                        onChange={(e) => setGoldTransferAmount(Math.max(1, Math.min(gold, parseInt(e.target.value) || 0)))}
                                    />
                                    <span>GP</span>
                                </div>
                            </div>

                            <div className="transfer-target-list">
                                <p className="notice">Select a recipient:</p>
                                {sessionParticipants.map(participant => (
                                    <div
                                        key={participant.character.id}
                                        className={`recipient-option ${goldTransferRecipient === participant.character.id ? 'selected' : ''}`}
                                        onClick={() => setGoldTransferRecipient(participant.character.id)}
                                    >
                                        <div className="recipient-info">
                                            <span className="char-name">{participant.character.name}</span>
                                            <span className="owner-name">Owner: {participant.username}</span>
                                        </div>
                                        {goldTransferRecipient === participant.character.id && <i className="fa-solid fa-circle-check"></i>}
                                    </div>
                                ))}
                            </div>

                            <button
                                className="confirm-transfer-btn"
                                disabled={!goldTransferRecipient || goldTransferAmount <= 0 || goldTransferAmount > gold}
                                onClick={() => transferGold(goldTransferRecipient)}
                            >
                                <i className="fa-solid fa-paper-plane"></i> Confirm Gold Transfer
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {(isGiftsLoading || revealedGifts.gold.length > 0 || revealedGifts.items.length > 0) && (
                <div className="gifts-notice-container">
                    {isGiftsLoading && (
                        <div className="gift-loading-notice">
                            <i className="fa-solid fa-spinner fa-spin"></i>
                            <span>Processing incoming gifts...</span>
                        </div>
                    )}

                    {character?.data?.gold_gifts?.filter(g => revealedGifts.gold.includes(g.id || `${g.amount}-${g.from_character_name}`)).map((gift, idx) => (
                        <div key={`gold-${idx}`} className="gold-gift-notice">
                            <div className="gift-text">
                                <i className="fa-solid fa-coins"></i>
                                <span>You received <strong>{gift.amount} GP</strong> from <strong>{gift.from_character_name}</strong>!</span>
                            </div>
                            <button className="gold-accept-btn" onClick={handleAcknowledgeGold}>Accept</button>
                        </div>
                    ))}

                    {inventoryItems.filter(item => item.is_new_gift && revealedGifts.items.includes(item.originalIndex)).map((item, idx) => (
                        <div key={`item-${idx}`} className="item-gift-notice">
                            <div className="gift-text">
                                <i className="fa-solid fa-gift"></i>
                                <span>Received <strong>{item.name}</strong> from <strong>{item.from_character_name}</strong>!</span>
                            </div>
                            <button className="item-accept-btn" onClick={() => handleAcceptItemWithScroll(item.originalIndex)}>Accept</button>
                        </div>
                    ))}
                </div>
            )}
            <BackToTop />
        </div>
    );
}

export default CharacterSheet;