import { useState, useEffect, useMemo, useCallback } from "react";
import { useNotification } from "../context/NotificationContext";
import "../styles/CharacterSheet.css";

const resolveScaledUses = (scalingData, level) => {
    if (!scalingData) return null;
    if (typeof scalingData === 'number') return scalingData;
    if (typeof scalingData !== 'object') return null;

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

const RestOverlay = ({
    show,
    character,
    currentHp,
    maxHp,
    classRules,
    availableFeatures,
    onClose,
    onCompleteRest
}) => {
    const [hpRegained, setHpRegained] = useState(0);
    const [rollResults, setRollResults] = useState([]);
    const [spentDiceCount, setSpentDiceCount] = useState(0);
    const [diceToSpend, setDiceToSpend] = useState(1);
    const [rolling, setRolling] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { confirm } = useNotification();

    const conMod = Math.floor(((character?.data?.abilities?.constitution || 10) - 10) / 2);
    const availableDice = character?.data?.hit_dice_remaining || 0;
    const hitDieValue = parseInt(classRules?.hit_die?.replace('d', '') || 8);
    const tempHp = Math.min(maxHp, currentHp + hpRegained);

    const analyzeRecharge = useCallback((feature, restType) => {
        const level = character?.level || 1;
        const details = feature.details || {};
        const rechargeRaw = (details.recharge || details.Recharge || "").toLowerCase();
        const triggerRaw = (details.trigger || details.Trigger || "").toLowerCase();

        const usesData = details.Uses ?? details.uses;
        const maxUses = resolveScaledUses(usesData, level);

        const combined = (
            (feature.description || "") + " " +
            (feature.summary || "") + " " +
            JSON.stringify(details)
        ).toLowerCase();

        const isShort = restType === 'short';
        const isLong = restType === 'long';

        // 1. Check explicit Recharge field
        let rechargeMatch = false;
        if (rechargeRaw) {
            if (isShort) rechargeMatch = rechargeRaw.includes("short rest") || rechargeRaw.includes("short or long rest");
            if (isLong) rechargeMatch = rechargeRaw.includes("long rest") || rechargeRaw.includes("short or long rest");
        } else if (usesData !== undefined) {
            if (isLong && !combined.includes("short rest")) rechargeMatch = true;
        } else {
            if (isShort) rechargeMatch = combined.includes("short rest") && !combined.includes("long rest only");
            if (isLong) rechargeMatch = combined.includes("long rest");
        }

        // 2. Check explicit Trigger field
        let triggerMatch = false;
        if (triggerRaw) {
            if (isShort) triggerMatch = triggerRaw.includes("short rest") || triggerRaw.includes("short or long rest");
            if (isLong) triggerMatch = triggerRaw.includes("long rest") || triggerRaw.includes("short or long rest");
        }

        if (rechargeMatch && maxUses) {
            const shortPartialMatch = rechargeRaw.match(/regain (\d+)/i) || combined.match(/regain (\d+)/i);
            if (shortPartialMatch && isShort) {
                return { type: 'recharge', restore: 'partial', amount: parseInt(shortPartialMatch[1]), maxUses };
            }
            return { type: 'recharge', restore: 'full', maxUses };
        }

        if (triggerMatch || (rechargeMatch && !maxUses)) {
            return { type: 'trigger' };
        }

        return null;
    }, [character]);

    const restFeatures = useMemo(() => {
        const getFeatures = (type) => {
            const recharging = [];
            const triggering = [];
            availableFeatures.forEach(feature => {
                const info = analyzeRecharge(feature, type);
                if (info) {
                    if (info.type === 'recharge') recharging.push({ ...feature, _rechargeInfo: info });
                    else triggering.push(feature);
                }
            });
            return { recharging, triggering };
        };
        return {
            short: getFeatures('short'),
            long: getFeatures('long')
        };
    }, [availableFeatures, analyzeRecharge]);

    useEffect(() => {
        if (show) {
            setHpRegained(0);
            setRollResults([]);
            setSpentDiceCount(0);
            setRolling(false);
            setIsSubmitting(false);
        }
    }, [show]);

    if (!show || !character) return null;

    const handleShortRestRoll = async () => {
        const actualAvailable = availableDice - spentDiceCount;
        const actualSpend = Math.min(diceToSpend, actualAvailable);

        if (actualSpend <= 0) return;
        if (tempHp >= maxHp) return;

        setRolling(true);
        let runningRegained = hpRegained;

        for (let i = 0; i < actualSpend; i++) {
            if (currentHp + runningRegained >= maxHp) break;

            const roll = Math.floor(Math.random() * hitDieValue) + 1;
            const total = Math.max(1, roll + conMod);
            runningRegained += total;

            setRollResults(prev => [...prev, { roll, conMod, total }]);
            setHpRegained(runningRegained);
            setSpentDiceCount(prev => prev + 1);

            await new Promise(r => setTimeout(r, 600));
        }
        setRolling(false);
    };

    const handleConfirmRest = async (type) => {
        if (rolling || isSubmitting) return;

        const features = restFeatures[type];
        const rechargedFeatures = features.recharging.map(f => ({
            id: f.id,
            restore: f._rechargeInfo.restore,
            amount: f._rechargeInfo.amount,
            maxUses: f._rechargeInfo.maxUses
        }));

        const isLong = type === 'long';
        const msg = isLong
            ? "Are you sure you want to take a Long Rest? Your HP and Hit Dice will be fully restored, and all spell slots will be regained."
            : `Confirm Short Rest? You will spend ${spentDiceCount} Hit Dice and regain ${hpRegained} HP.`;

        if (await confirm(msg)) {
            setIsSubmitting(true);
            try {
                await onCompleteRest(type, {
                    diceSpent: isLong ? 0 : spentDiceCount,
                    hpRegained: isLong ? (maxHp - currentHp) : hpRegained,
                    rechargedFeatures
                });
                onClose();
            } catch (err) {
                console.error("Rest failed", err);
                setIsSubmitting(false);
            }
        }
    };

    const isWarlock = classRules?.id === 'warlock' || classRules?.name === 'Warlock';
    const hasSpellcasting = !!classRules?.spellcasting;

    return (
        <div className="spell-overlay rest-overlay-backdrop">
            <div className="spell-overlay-content rest-overlay-content premium-theme">
                <div className="overlay-header">
                    <h2><i className="fa-solid fa-campground"></i> Take a Rest</h2>
                    <button className="close-btn" onClick={onClose} disabled={isSubmitting}>✕</button>
                </div>

                <p className="rest-tip">Choose your rest type. Resources will be restored based on your class features.</p>

                <div className="rest-body scrollable">
                    <div className="rest-layout-split">
                        {/* SHORT REST COLUMN */}
                        <div className="rest-column left">
                            <div className="column-head">
                                <h3>Short Rest</h3>
                            </div>

                            <div className="rest-section">
                                <div className="hp-preview-bar">
                                    <div className="hp-stat">
                                        <span className="label">Preview HP</span>
                                        <span className="value">{tempHp} / {maxHp}</span>
                                    </div>
                                    <div className="hp-progress-container">
                                        <div className="hp-progress-fill healed" style={{ width: `${(tempHp / maxHp) * 100}%` }}></div>
                                        <div className="hp-progress-fill original" style={{ width: `${(currentHp / maxHp) * 100}%` }}></div>
                                    </div>
                                </div>

                                <div className="hit-dice-action">
                                    <div className="hd-status">
                                        <span className="hd-label">Available Hit Dice ({classRules?.hit_die}):</span>
                                        <span className="hd-value">{availableDice - spentDiceCount}</span>
                                    </div>

                                    {(availableDice - spentDiceCount) > 0 && currentHp < maxHp && !rolling && !isSubmitting && (
                                        <div className="hd-controls">
                                            <div className="hd-input-group">
                                                <label>Spend:</label>
                                                <input
                                                    type="number" min="1" max={availableDice - spentDiceCount}
                                                    value={diceToSpend}
                                                    onChange={(e) => setDiceToSpend(Math.max(1, Math.min(availableDice - spentDiceCount, parseInt(e.target.value) || 1)))}
                                                    className="hd-spend-input"
                                                />
                                            </div>
                                            <button className="roll-hd-btn premium" onClick={handleShortRestRoll}>
                                                Roll & Heal
                                            </button>
                                        </div>
                                    )}
                                    {rolling && <div className="rolling-loader">Rolling... 🎲</div>}
                                    <div className="roll-results-list">
                                        {rollResults.slice(-3).map((res, i) => (
                                            <div key={i} className="roll-result-item animated-in">
                                                <span>Roll: <strong>{res.roll}</strong> + {res.conMod} = <strong>{res.total}</strong> HP</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="rest-benefits-summary">
                                    <h4>Rest Benefits:</h4>
                                    <div className="benefit-item"><i className="fa-solid fa-heart-pulse"></i> HP Recovery</div>
                                    {isWarlock && <div className="benefit-item highlight"><i className="fa-solid fa-wand-magic-sparkles"></i> Pact Magic Slots</div>}
                                </div>

                                {(restFeatures.short.recharging.length > 0 || restFeatures.short.triggering.length > 0) && (
                                    <div className="recharge-section">
                                        {restFeatures.short.recharging.length > 0 && (
                                            <div className="recharge-group">
                                                <h5>Recharging:</h5>
                                                {restFeatures.short.recharging.map(f => (
                                                    <div key={f.id} className="recharge-item">
                                                        <span>{f.name}</span>
                                                        <span className="amount">{f._rechargeInfo.restore === 'partial' ? `+${f._rechargeInfo.amount}` : 'Full'}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                        {restFeatures.short.triggering.length > 0 && (
                                            <div className="recharge-group">
                                                <h5>Triggering:</h5>
                                                {restFeatures.short.triggering.map(f => (
                                                    <div key={f.id} className="recharge-item trigger">
                                                        <span>{f.name}</span>
                                                        <i className="fa-solid fa-bolt-lightning"></i>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                            <div className="column-footer">
                                <button
                                    className="confirm-btn premium short-btn"
                                    onClick={() => handleConfirmRest('short')}
                                    disabled={rolling || isSubmitting || (currentHp === maxHp && spentDiceCount === 0 && restFeatures.short.recharging.length === 0 && restFeatures.short.triggering.length === 0)}
                                >
                                    {isSubmitting ? "Resting..." : "Finish Short Rest"}
                                </button>
                            </div>
                        </div>

                        {/* LONG REST COLUMN */}
                        <div className="rest-column right">
                            <div className="column-head">
                                <h3>Long Rest</h3>
                            </div>

                            <div className="rest-section">
                                <div className="long-rest-benefits">
                                    <div className="benefit-card">
                                        <i className="fa-solid fa-heart"></i>
                                        <div className="benefit-info"><span className="title">Full HP</span><span className="desc"> Restore to max</span></div>
                                    </div>
                                    <div className="benefit-card">
                                        <i className="fa-solid fa-dice-d20"></i>
                                        <div className="benefit-info"><span className="title">Hit Dice</span><span className="desc"> Regain to max</span></div>
                                    </div>
                                    {hasSpellcasting && (
                                        <div className="benefit-card highlight">
                                            <i className="fa-solid fa-sparkles"></i>
                                            <div className="benefit-info"><span className="title">Spell Slots</span><span className="desc">Full restoration</span></div>
                                        </div>
                                    )}
                                </div>

                                {(restFeatures.long.recharging.length > 0 || restFeatures.long.triggering.length > 0) && (
                                    <div className="recharge-section">
                                        {restFeatures.long.recharging.length > 0 && (
                                            <div className="recharge-group">
                                                <h5>Recharging:</h5>
                                                {restFeatures.long.recharging.map(f => (
                                                    <div key={f.id} className="recharge-item">
                                                        <span>{f.name}</span>
                                                        <span className="amount">Full</span>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                        {restFeatures.long.triggering.length > 0 && (
                                            <div className="recharge-group">
                                                <h5>Triggering:</h5>
                                                {restFeatures.long.triggering.map(f => (
                                                    <div key={f.id} className="recharge-item trigger">
                                                        <span>{f.name}</span>
                                                        <i className="fa-solid fa-bolt-lightning"></i>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                            <div className="column-footer">
                                <button
                                    className="confirm-btn premium long-btn"
                                    onClick={() => handleConfirmRest('long')}
                                    disabled={rolling || isSubmitting}
                                >
                                    {isSubmitting ? "Resting..." : "Finish Long Rest"}
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
