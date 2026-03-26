import React, { useState } from 'react';
import '../styles/CharacterSheet.css'; // Assuming styles are added here

/**
 * Computes the scaling value for a given dictionary at a specific level
 */
const resolveScalingValue = (scalingData, level) => {
    if (typeof scalingData !== 'object' || scalingData === null) return scalingData;

    let bestValue = null;
    let highestLevelFound = -1;

    for (const [range, value] of Object.entries(scalingData)) {
        const parts = range.split('-');
        if (parts.length === 2) {
            const min = parseInt(parts[0]);
            const max = parseInt(parts[1]);
            if (level >= min && level <= max) return value;
        } else if (range.endsWith('+')) {
            const min = parseInt(range);
            if (level >= min && min > highestLevelFound) {
                highestLevelFound = min;
                bestValue = value;
            }
        } else {
            const milestone = parseInt(range);
            if (!isNaN(milestone) && level >= milestone && milestone > highestLevelFound) {
                highestLevelFound = milestone;
                bestValue = value;
            }
        }
    }
    return bestValue;
};

const proficiencyBonus = (level) => {
    if (level >= 17) return 6;
    if (level >= 13) return 5;
    if (level >= 9) return 4;
    if (level >= 5) return 3;
    return 2;
};

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

const LevelUpOverlay = ({
    show,
    minimized,
    character,
    previousLevel,
    availableFeatures,
    onClose, // Dismiss permanently
    onMinimize,
    onRestore,
    onOpenSpells,
    spellcastingRules,
    featureUses,
    activeFeatures,
    onToggleFeature, // Reusing CharacterSheet expands
    featureChoices,
    onUpdateChoice, // Trigger choice modal
    resolveOptionsForFeature // Function passed down
}) => {
    const [expandedFeatures, setExpandedFeatures] = useState({});

    // We only show it if meant to be shown and we have a character
    if (!show || !character) return null;

    const currentLevel = character.level;
    const oldLevel = previousLevel > 0 ? previousLevel : (currentLevel > 1 ? currentLevel - 1 : 0);

    // HP Calculation
    const conScore = character.data.abilities?.constitution || 10;
    const conMod = Math.floor((conScore - 10) / 2);
    const hpRolls = character.data.hp_rolls || [];
    
    // Total max HP right now
    const baseHp = hpRolls.reduce((a, b) => a + b, 0);
    const conBonus = currentLevel * conMod;
    const currentMaxHp = baseHp + conBonus;

    // Previous max HP
    const prevRolls = hpRolls.slice(0, oldLevel);
    const prevBaseHp = prevRolls.reduce((a, b) => a + b, 0);
    const prevConBonus = oldLevel * conMod;
    const prevMaxHp = prevBaseHp + prevConBonus;

    const hpGained = currentMaxHp - prevMaxHp;

    // Proficiency
    const oldProf = proficiencyBonus(oldLevel);
    const newProf = proficiencyBonus(currentLevel);
    const profChanged = newProf > oldProf;

    // Splitting features into New vs Upgraded
    const newFeatures = [];
    const upgradedFeatures = [];

    // Diff logic for features
    availableFeatures.forEach(feature => {
        // Only classify things strictly tied to a level. Species/Backgrounds generally won't "level up" this way.
        const fLevel = parseInt(feature.level);
        if (isNaN(fLevel)) return; 

        if (fLevel > oldLevel && fLevel <= currentLevel) {
            newFeatures.push(feature);
        } else if (fLevel <= oldLevel) {
            // Check if upgraded
            if (feature.details) {
                let isUpgraded = false;
                const upgrades = [];

                for (const [key, val] of Object.entries(feature.details)) {
                    if (typeof val === 'object' && val !== null && !Array.isArray(val) && Object.keys(val).some(k => k.match(/^\d+(-?\d+)?$/))) {
                        // It's a scaling dict
                        const oldVal = resolveScalingValue(val, oldLevel);
                        const newVal = resolveScalingValue(val, currentLevel);
                        
                        if (oldVal !== newVal) {
                            isUpgraded = true;
                            upgrades.push({ key, oldVal, newVal });
                        }
                    } else if (key === 'weapons_mastered' && val.scaling) {
                         const oldVal = resolveScalingValue(val.scaling, oldLevel);
                         const newVal = resolveScalingValue(val.scaling, currentLevel);
                         if (oldVal !== newVal) {
                             isUpgraded = true;
                             upgrades.push({ key: 'Weapons Mastered', oldVal, newVal });
                         }
                    } else if (key === 'effects_count' && currentLevel===17 && feature.id==="barbarian_brutal_strike_upgrade") {
                         // Extremely specific override if needed, though strictly brutal_strike_upgrade is a new feature at 17, so handled by logic above.
                    }
                }

                if (isUpgraded) {
                    upgradedFeatures.push({ feature, upgrades });
                }
            }
        }
    });

    const toggleExpand = (id) => {
        setExpandedFeatures(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const handleConfirmClose = () => {
        if (window.confirm("Are you sure you want to dismiss the level up summary? Make sure you have made all your choices!")) {
            onClose();
        }
    };

    if (minimized) {
        return (
            <div className="spell-overlay-minimized lu-overlay-minimized">
                <span className="overlay-minimized-title">✨ Level Up Details</span>
                <button className="overlay-eye-btn" title="Restore level up panel" onClick={onRestore}>👁</button>
                <button className="close-btn overlay-close-min" onClick={handleConfirmClose}>✕</button>
            </div>
        );
    }

    return (
        <div className="spell-overlay level-up-backdrop">
            <div className="spell-overlay-content level-up-overlay-content">
                <div className="overlay-header">
                    <h2>Level {currentLevel} Reached!</h2>
                    <div className="overlay-header-actions">
                        <button className="overlay-eye-btn" title="Minimize — keep panel open while viewing sheet" onClick={onMinimize}>👁</button>
                        <button className="close-btn" onClick={handleConfirmClose}>✕</button>
                    </div>
                </div>
                
                <div className="lu-stats-row">
                    <div className="lu-stat-card">
                        <span className="lu-stat-label">Hit Points</span>
                        <span className="lu-stat-val">+{hpGained > 0 ? hpGained : 0}</span>
                        <span className="lu-stat-sub">({prevMaxHp} → {currentMaxHp})</span>
                    </div>
                    {profChanged && (
                        <div className="lu-stat-card highlight">
                            <span className="lu-stat-label">Proficiency Bonus</span>
                            <span className="lu-stat-val">+{newProf}</span>
                            <span className="lu-stat-sub">({oldProf} → {newProf})</span>
                        </div>
                    )}
                    {spellcastingRules && (
                        <div className="lu-stat-card selectable" onClick={onOpenSpells}>
                            <span className="lu-stat-label">Magic</span>
                            <span className="lu-stat-val">Spells</span>
                            <button className="lu-btn-small">Manage Spells</button>
                        </div>
                    )}
                </div>

                <div className="lu-scrollable-content">
                    {newFeatures.length > 0 && (
                        <div className="lu-section">
                            <h3>New Features</h3>
                            <div className="lu-feature-list">
                                {newFeatures.map(f => (
                                    <LuFeatureCard 
                                        key={f.id} 
                                        feature={f} 
                                        isExpanded={expandedFeatures[f.id]}
                                        onToggle={() => toggleExpand(f.id)}
                                        currentLevel={currentLevel}
                                        featureChoices={featureChoices}
                                        onUpdateChoice={onUpdateChoice}
                                        resolveOptionsForFeature={resolveOptionsForFeature}
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {upgradedFeatures.length > 0 && (
                        <div className="lu-section">
                            <h3>Upgraded Features</h3>
                            <div className="lu-feature-list">
                                {upgradedFeatures.map(({feature: f, upgrades}) => (
                                    <LuFeatureCard 
                                        key={f.id} 
                                        feature={f} 
                                        isExpanded={expandedFeatures[f.id]}
                                        onToggle={() => toggleExpand(f.id)}
                                        currentLevel={currentLevel}
                                        upgrades={upgrades}
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {newFeatures.length === 0 && upgradedFeatures.length === 0 && (
                        <p className="no-features-text">No standard class features gained at this level.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

// Internal reusable card
const LuFeatureCard = ({ feature, isExpanded, onToggle, currentLevel, upgrades, featureChoices, onUpdateChoice, resolveOptionsForFeature }) => {
    
    // Check if choice needed
    let hasChoices = false;
    let options = [];
    let currentChoice = null;

    if (resolveOptionsForFeature && onUpdateChoice) {
        options = resolveOptionsForFeature(feature);
        if (options && options.length > 0) {
            hasChoices = true;
            currentChoice = featureChoices?.[feature.id];
        }
    }

    return (
        <div className={`feature-card ${isExpanded ? "expanded" : "collapsed"} lu-animated-card`}>
            <div className="feature-title" onClick={onToggle}>
                <div className="feature-title-left">
                    <span className="feature-name">{feature.name}</span>
                    {upgrades && <span className="lu-upgrade-badge">UPGRADED</span>}
                </div>
                <div className="feature-title-right">
                    {hasChoices && (
                        <button 
                            className="feature-choice-btn" 
                            onClick={(e) => {
                                e.stopPropagation();
                                onUpdateChoice(feature, options);
                            }}
                        >
                            {currentChoice ? "Change Choice" : "Choose"}
                        </button>
                    )}
                </div>
            </div>
            
            {isExpanded && (
                <div className="feature-body">
                    {upgrades && (
                        <div className="lu-upgrade-details detail-pairs">
                            {upgrades.map((u, i) => (
                                <div key={i} className="detail-pair lu-diff-pair">
                                    <span className="detail-label">{u.key}:</span>
                                    <span className="detail-value diff-values">
                                        <span className="diff-old">{u.oldVal}</span>
                                        <span className="diff-arrow">→</span>
                                        <span className="diff-new highlight">{u.newVal}</span>
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}

                    {feature.summary && <p className="feature-summary"><strong>Summary:</strong> {processRichText(feature.summary)}</p>}
                    {feature.description && (
                        <div className="feature-description">
                            {feature.description.split('\n').map((para, i) => (
                                <p key={i}>{processRichText(para)}</p>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default LevelUpOverlay;
