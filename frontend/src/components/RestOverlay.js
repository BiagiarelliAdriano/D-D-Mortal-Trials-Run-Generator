import React, { useState, useEffect } from 'react';
import { useNotification } from "../context/NotificationContext";
import '../styles/CharacterSheet.css';


const RestOverlay = ({
    show,
    character,
    classRules,
    availableFeatures,
    onClose,
    onCompleteRest
}) => {
    const { notify, confirm } = useNotification();
    const [diceToSpend, setDiceToSpend] = useState(1);
    const [rolling, setRolling] = useState(false);
    const [rollResults, setRollResults] = useState([]);
    const [tempHp, setTempHp] = useState(0);
    const [spentDiceCount, setSpentDiceCount] = useState(0);

    const hitDieValue = classRules?.hit_die ? parseInt(classRules.hit_die.replace('d', '')) : 8;
    const conMod = Math.floor(((character?.data?.abilities?.constitution || 10) - 10) / 2);
    const currentHp = character?.data?.hp_current || 0;
    const maxHp = (character?.data?.hp_max_base || 0) + (character?.data?.hp_modifier || 0);
    const availableDice = character?.data?.hit_dice_remaining || 0;

    const findRechargeableFeatures = (type) => {
        const recharged = [];
        availableFeatures.forEach(feature => {
            const desc = (feature.description || "").toLowerCase();
            const summary = (feature.summary || "").toLowerCase();
            const details = JSON.stringify(feature.details || "").toLowerCase();
            const combined = desc + " " + summary + " " + details;

            if (type === 'long') {
                if (combined.includes("long rest") || combined.includes("short or long rest") || combined.includes("short rest")) {
                    recharged.push(feature);
                }
            } else {
                if (combined.includes("short rest") || combined.includes("short or long rest")) {
                    recharged.push(feature);
                }
            }
        });
        return recharged;
    };

    useEffect(() => {
        if (show) {
            setTempHp(currentHp);
            setRollResults([]);
            setSpentDiceCount(0);
            setRolling(false);
        }
    }, [show, currentHp]);

    if (!show || !character) return null;

    const shortRechargeable = findRechargeableFeatures('short');
    const longRechargeable = findRechargeableFeatures('long');

    const handleShortRestRoll = async () => {
        if (diceToSpend <= 0 || diceToSpend > availableDice) return;
        if (tempHp >= maxHp) {
            notify("You are already at maximum Hit Points!", "info");
            return;
        }

        setRolling(true);
        let currentTempHp = tempHp;
        let unneededDice = 0;
        const newResults = [];

        for (let i = 0; i < diceToSpend; i++) {
            if (currentTempHp >= maxHp) {
                unneededDice = diceToSpend - i;
                break;
            }

            const roll = Math.floor(Math.random() * hitDieValue) + 1;
            const total = Math.max(1, roll + conMod);
            currentTempHp = Math.min(maxHp, currentTempHp + total);
            
            newResults.push({ roll, conMod, total });
            setRollResults([...newResults]);
            setTempHp(currentTempHp);
            setSpentDiceCount(i + 1);

            // Small delay for animation feel
            await new Promise(r => setTimeout(r, 600));
        }

        if (unneededDice > 0) {
            notify(`${unneededDice} Hit Dice were not needed and have been returned.`, "info");
        }
        setRolling(false);
    };

    const handleConfirmRest = async (type) => {
        if (rolling) return;

        const rechargedFeatures = findRechargeableFeatures(type);

        const msg = type === 'long' 
            ? "Are you sure you want to take a Long Rest? Your HP and Hit Dice will be fully restored, and your ability scores will return to base."
            : `Confirm Short Rest? You will spend ${spentDiceCount} Hit Dice and regain ${tempHp - currentHp} HP.`;

        if (await confirm(msg)) {
            onCompleteRest(type, {
                diceSpent: type === 'short' ? spentDiceCount : 0,
                hpRegained: type === 'short' ? (tempHp - currentHp) : (maxHp - currentHp),
                rechargedFeatures: rechargedFeatures.map(f => f.id)
            });
            onClose();
        }
    };

    return (
        <div className="spell-overlay rest-overlay-backdrop">
            <div className="spell-overlay-content rest-overlay-content premium-theme">
                <div className="overlay-header">
                    <h2><i className="fa-solid fa-campground"></i> Take a Rest</h2>
                    <button className="close-btn" onClick={onClose}>✕</button>
                </div>
                
                <p className="rest-tip">Choose the rest type that fits your situation.</p>

                <div className="rest-body scrollable">
                    <div className="rest-layout-split">
                        {/* LEFT COLUMN: SHORT REST */}
                        <div className="rest-column left">
                            <h3>Short Rest</h3>
                            <div className="rest-section short-rest-ui">
                                <div className="hp-preview-bar">
                                    <div className="hp-stat">
                                        <span className="label">Current HP</span>
                                        <span className="value">{tempHp} / {maxHp}</span>
                                    </div>
                                    <div className="hp-progress-container">
                                        <div 
                                            className="hp-progress-fill healed" 
                                            style={{ width: `${(tempHp / maxHp) * 100}%` }}
                                        ></div>
                                        <div 
                                            className="hp-progress-fill original" 
                                            style={{ width: `${(currentHp / maxHp) * 100}%` }}
                                        ></div>
                                    </div>
                                </div>

                                <div className="hit-dice-action">
                                    <div className="hd-status">
                                        <span className="hd-label">Available Hit Dice ({classRules?.hit_die}):</span>
                                        <span className="hd-value">{availableDice}</span>
                                    </div>
                                    
                                    {availableDice > 0 && currentHp < maxHp && !rolling && (
                                        <div className="hd-controls">
                                            <div className="hd-input-group">
                                                <label>Dice to Spend:</label>
                                                <input 
                                                    type="number" 
                                                    min="1" 
                                                    max={availableDice} 
                                                    value={diceToSpend}
                                                    onChange={(e) => setDiceToSpend(Math.max(1, Math.min(availableDice, parseInt(e.target.value) || 0)))}
                                                />
                                            </div>
                                            <button className="rest-action-btn premium" onClick={handleShortRestRoll}>
                                                Roll Hit Dice
                                            </button>
                                        </div>
                                    )}

                                    {rolling && <div className="rolling-loader">Rolling... 🎲</div>}

                                    <div className="roll-results-list">
                                        {rollResults.map((res, i) => (
                                            <div key={i} className="roll-result-item animated-in">
                                                <span className="roll-num">Die {i+1}: <strong>{res.roll}</strong></span>
                                                <span className="roll-mod"> + {res.conMod} (Con)</span>
                                                <span className="roll-total"> = <strong>{res.total}</strong> HP</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="recharge-section">
                                    <h4><i className="fa-solid fa-bolt"></i> Recharging</h4>
                                    {shortRechargeable.length > 0 ? (
                                        <div className="recharge-list mini">
                                            {shortRechargeable.map(f => (
                                                <div key={f.id} className="recharge-item-short">
                                                    <span className="feat-name">{f.name}</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <p className="no-recharge">No short rest features.</p>
                                    )}
                                </div>
                            </div>
                            
                            <div className="column-footer">
                                <button 
                                    className="confirm-btn premium short-btn" 
                                    onClick={() => handleConfirmRest('short')}
                                    disabled={rolling || (currentHp === maxHp && spentDiceCount === 0)}
                                >
                                    Finish Short Rest
                                </button>
                            </div>
                        </div>

                        <div className="rest-separator"></div>

                        {/* RIGHT COLUMN: LONG REST */}
                        <div className="rest-column right">
                            <h3>Long Rest</h3>
                            <div className="rest-section long-rest-ui">
                                <div className="long-rest-benefits">
                                    <div className="benefit-card">
                                        <i className="fa-solid fa-heart-pulse"></i>
                                        <span>Full HP restoration: <strong>{maxHp}</strong></span>
                                    </div>
                                    <div className="benefit-card">
                                        <i className="fa-solid fa-dice-d20"></i>
                                        <span>Regain all <strong>{character.level}</strong> Hit Dice</span>
                                    </div>
                                    <div className="benefit-card">
                                        <i className="fa-solid fa-person-running"></i>
                                        <span>Exhaustion reduced by <strong>1</strong></span>
                                    </div>
                                    <div className="benefit-card">
                                        <i className="fa-solid fa-arrows-rotate"></i>
                                        <span>Ability Scores return to base</span>
                                    </div>
                                </div>

                                <div className="recharge-section">
                                    <h4><i className="fa-solid fa-bolt"></i> Recharging All</h4>
                                    {longRechargeable.length > 0 ? (
                                        <div className="recharge-list mini">
                                            {longRechargeable.map(f => (
                                                <div key={f.id} className="recharge-item-short">
                                                    <span className="feat-name">{f.name}</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <p className="no-recharge">No long rest features.</p>
                                    )}
                                </div>
                            </div>

                            <div className="column-footer">
                                <button 
                                    className="confirm-btn premium long-btn" 
                                    onClick={() => handleConfirmRest('long')}
                                    disabled={rolling}
                                >
                                    Finish Long Rest
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default RestOverlay;
