import React, { useState, useEffect } from 'react';
import '../styles/CharacterSheet.css';

const StatModifierOverlay = ({ config, onClose, onApply, baseValue, isApplying }) => {
    // 'val' now represents the ADJUSTMENT the user wants to make, not the total score.
    const [adjustment, setAdjustment] = useState(0);

    useEffect(() => {
        if (config.isOpen) {
            setAdjustment(0); // Reset adjustment when opening
        }
    }, [config.isOpen]);

    if (!config.isOpen) return null;

    const handleAdjust = (amt) => setAdjustment(prev => {
        const next = prev + amt;
        return Math.max(-10, Math.min(10, next));
    });

    const isHP = config.type === 'hp_max' || config.type === 'ac';
    const isAbility = config.type === 'ability';

    // Current total value (before adjustment)
    const currentValue = config.value; 

    // Result value after applying adjustment
    let resultValue = currentValue + adjustment;
    
    // Constraints
    if (isAbility) {
        // Enforce 0-35 score range
        resultValue = Math.max(0, Math.min(35, resultValue));
        // Recalculate adjustment if it hit the cap
        // adjustment = resultValue - currentValue; // We keep adjustment visual, but apply will cap it
    }

    const currentModifier = isAbility 
        ? Math.floor((currentValue - 10) / 2)
        : currentValue; // For HP, the modifier IS the value

    const newModifier = isAbility 
        ? Math.floor((resultValue - 10) / 2)
        : resultValue;

    const handleApply = () => {
        onApply(config.type, config.statKey, resultValue);
        setAdjustment(0);
    };

    const handleResetToBase = () => {
        if (isHP) {
            onApply(config.type, null, 0); // Reset modifier to 0
        } else {
            onApply('ability', config.statKey, baseValue); // Reset Ability to base score
        }
        setAdjustment(0);
    };

    return (
        <div className={`modal-overlay stat-mod-overlay-backdrop ${isApplying ? 'is-applying' : ''}`} onClick={!isApplying ? onClose : undefined}>
            <div className="stat-mod-card premium-theme animated-in" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>Adjust {config.label}</h3>
                    <button className="close-btn" onClick={onClose} title="Close" disabled={isApplying}>✕</button>
                </div>
                <div className="stat-mod-body">
                    <div className="stat-preview">
                        <div className="stat-status-row">
                            <div className="stat-sub">Current {isHP ? 'Modifier' : 'Score'}: <strong>{currentValue}</strong></div>
                            {isAbility && (
                                <div className="stat-sub modifier-preview">
                                    Modifier: <strong>{currentModifier >= 0 ? "+" : ""}{currentModifier}</strong>
                                </div>
                            )}
                        </div>

                        <div className="stat-main-result">
                            <span className="stat-label hp-modifier-adjust-label">Adjustment:</span>
                            <span className={`adjustment-value ${adjustment > 0 ? 'pos' : (adjustment < 0 ? 'neg' : '')}`}>
                                {adjustment > 0 ? "+" : ""}{adjustment}
                            </span>
                        </div>

                        <div className="stat-result-preview">
                            <span className="stat-label">Resulting {isHP ? 'Modifier' : 'Score'}:</span>
                            <span className="stat-value highlight">{resultValue}</span>
                            {isAbility && (
                                <span className="new-modifier-hint">
                                    (Mod: {newModifier >= 0 ? "+" : ""}{newModifier})
                                </span>
                            )}
                        </div>
                    </div>

                    <div className="stat-controls">
                        <div className="increment-row">
                            <button className="mod-btn dec" onClick={() => handleAdjust(-10)} disabled={isApplying}>-10</button>
                            <button className="mod-btn dec" onClick={() => handleAdjust(-1)} disabled={isApplying}>-1</button>
                            <input 
                                type="number" 
                                value={adjustment} 
                                min="-10"
                                max="10"
                                onChange={(e) => {
                                    const v = parseInt(e.target.value) || 0;
                                    setAdjustment(Math.max(-10, Math.min(10, v)));
                                }} 
                                className="stat-input"
                                disabled={isApplying}
                            />
                            <button className="mod-btn inc" onClick={() => handleAdjust(1)} disabled={isApplying}>+1</button>
                            <button className="mod-btn inc" onClick={() => handleAdjust(10)} disabled={isApplying}>+10</button>
                        </div>
                        <div className="quick-actions">
                            <button className="reset-btn" onClick={handleResetToBase} disabled={isApplying}>
                                <i className="fa-solid fa-rotate-left"></i> Reset to Base ({isAbility ? baseValue : 0})
                            </button>
                        </div>
                    </div>

                    <div className="stat-actions">
                        <button className="cancel-btn" onClick={onClose} disabled={isApplying}>Cancel</button>
                        <button 
                            className={`apply-btn premium ${isApplying ? 'loading' : ''}`} 
                            onClick={handleApply}
                            disabled={isApplying}
                        >
                            {isApplying ? (
                                <><i className="fa-solid fa-spinner fa-spin"></i> Applying...</>
                            ) : (
                                "Apply Change"
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StatModifierOverlay;
