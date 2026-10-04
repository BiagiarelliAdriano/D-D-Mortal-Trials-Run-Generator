import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useNotification } from '../../context/NotificationContext';
import BackToTop from '../common/BackToTop';
import UserProfilePill from '../UserProfilePill';
import '../../styles/HostedRunPage.css';
import API_BASE_URL from '../../config';

const HostedRunPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { token, user: currentUser, isAdmin } = useAuth();
    const { addAlert, confirm } = useNotification();

    const [userCharacters, setUserCharacters] = useState([]);
    const [showCharPicker, setShowCharPicker] = useState(false);
    const [session, setSession] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('trial');
    const [isEditingTitle, setIsEditingTitle] = useState(false);
    const [runTitleInput, setRunTitleInput] = useState('');
    const [expandedEncounters, setExpandedEncounters] = useState({});
    const [wildSurgeVisible, setWildSurgeVisible] = useState({});
    const [activeWildSurgeId, setActiveWildSurgeId] = useState(null);
    const [notice, setNotice] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [wildSurgesExpanded, setWildSurgesExpanded] = useState(false);
    const [shopConfirm, setShopConfirm] = useState(null);
    const [showSellModal, setShowSellModal] = useState(false);
    const [selectedSellItems, setSelectedSellItems] = useState({});
    const [sellPrices, setSellPrices] = useState({});
    const [isBuildingShop, setIsBuildingShop] = useState(false);
    const [shopPrevPhase, setShopPrevPhase] = useState(null);
    const [showCommonItems, setShowCommonItems] = useState(false);
    const [levelUpReveal, setLevelUpReveal] = useState(null); // Stores character info for modal
    const [dismissedLevelUps, setDismissedLevelUps] = useState(new Set()); // Local tracking for this session

    const formatRations = (value) => {
        const numeric = Number(value || 0);
        return Number.isInteger(numeric) ? numeric.toString() : numeric.toFixed(1);
    };

    const fetchSessionDetails = useCallback(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/details/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Failed to fetch session details');
            const data = await response.json();
            setSession(data);
        } catch (err) {
            addAlert(err.message, 'error');
        } finally {
            setLoading(false);
        }
    }, [id, token, addAlert]);

    const fetchUserCharacters = useCallback(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/characters`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setUserCharacters(data);
            }
        } catch (err) {
            addAlert('Failed to fetch characters', 'error');
        }
    }, [token, addAlert]);

    useEffect(() => {
        fetchSessionDetails();
        fetchUserCharacters();
        const interval = setInterval(fetchSessionDetails, 5000); // Polling every 5s
        return () => clearInterval(interval);
    }, [fetchSessionDetails, fetchUserCharacters]);

    // Watch for shop phase transitions from selection -> shopping to trigger animation
    useEffect(() => {
        if (session && session.shop_state) {
            const currentPhase = session.shop_state.phase;
            if (shopPrevPhase === 'selection' && currentPhase === 'shopping') {
                setIsBuildingShop(true);
                // Check for Wondrous category and notify
                if (session.shop_state.items && session.shop_state.items.Wondrous) {
                    addAlert("A rare Wondrous category has appeared in the shop!", "info");
                }

                setTimeout(() => setIsBuildingShop(false), 2000);
            }
            setShopPrevPhase(currentPhase);
        }
    }, [session, shopPrevPhase, addAlert]);

    // Handle Level Up Detection
    useEffect(() => {
        if (!session || !currentUser) return;
        const myChar = session.participants.find(p => p.user_id === currentUser.id && p.character_id)?.character;
        if (myChar && myChar.data?.level_up_pending) {
            const levelKey = `${myChar.id}_${myChar.level}`;
            if (!dismissedLevelUps.has(levelKey) && !levelUpReveal) {
                setLevelUpReveal(myChar);
            }
        }
    }, [session, currentUser, levelUpReveal, dismissedLevelUps]);

    const handleLinkCharacter = async (charId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/link-character`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ character_id: charId })
            });
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.error || 'Failed to link character');
            }
            setShowCharPicker(false);
            fetchSessionDetails();
            fetchUserCharacters();
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const startEditingTitle = () => {
        setRunTitleInput(session.run.title);
        setIsEditingTitle(true);
    };

    const handleRenameRun = async () => {
        if (!runTitleInput.trim() || runTitleInput.trim() === session.run.title) {
            setIsEditingTitle(false);
            return;
        }
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/rename`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title: runTitleInput.trim() })
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to rename run');
            }
            setIsEditingTitle(false);
            fetchSessionDetails();
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const handleCompleteAndArchive = async () => {
        if (!(await confirm("Are you ready to Complete & Archive this Run? All participants will be honored as Ascended Champions and this Trial will be permanently sealed in the Hall of Ascension."))) return;

        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to complete run');
            addAlert(data.message || 'Trial completed and archived!', 'success');
            fetchSessionDetails();
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const handleCompleteEncounter = async (num) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/complete-encounter`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ encounter_num: num })
            });
            if (response.ok) {
                const data = await response.json();
                // Immediately update rations in local state so pill reflects new value at once
                if (data.rations !== undefined) {
                    setSession(prev => prev ? { ...prev, rations: data.rations } : prev);
                }
                fetchSessionDetails();
                const rationText = data.rations_found > 0 ? ` +${formatRations(data.rations_found)} ration${data.rations_found === 1 ? '' : 's'}.` : '';
                setNotice({ message: `Encounter #${num} marked as complete!${rationText}`, type: 'success' });
                setTimeout(() => setNotice(null), 3000);
            } else {
                const data = await response.json();
                addAlert(data.error || "Failed to complete encounter", "error");
            }
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const getDisplayItemName = (item) => {
        if (!item) return 'No item';
        if (typeof item === 'string') return item;
        if (typeof item.name === 'string') return item.name;
        if (item.name && typeof item.name === 'object' && typeof item.name.name === 'string') return item.name.name;
        return 'Unknown item';
    };

    // Splits a blessing text into named ability blocks.
    // Ability names are detected as one or two capitalised words followed by a full stop
    // at a sentence boundary (e.g. "Echo Link. …" / "Perfect Reflection. …").
    const parseGraceAbilities = (text) => {
        if (!text) return null;
        // Match "Word Word." or "Word." at the very start of a "sentence" within the string.
        // We split on the pattern: look-behind for a period+whitespace or start-of-string,
        // then capture "CapWord[ CapWord]." as the ability name header.
        const abilityPattern = /(?:^|\s)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\.\s/g;
        const matches = [];
        let match;
        while ((match = abilityPattern.exec(text)) !== null) {
            matches.push({ name: match[1], index: match.index + (match[0].length - match[1].length - 2) });
        }
        if (matches.length < 2) return null; // not structured — fall back to plain text
        const abilities = matches.map((m, i) => {
            const bodyStart = m.index + m.name.length + 1; // skip "Name."
            const bodyEnd = i + 1 < matches.length ? matches[i + 1].index : text.length;
            return { name: m.name, body: text.slice(bodyStart, bodyEnd).trim() };
        });
        return abilities;
    };

    const groupCycleMonsters = (monsters, cycleNum) => {
        const groups = [];
        monsters.forEach((monster, index) => {
            const encounterNumber = monster.encounter_number ?? 1;
            let group = groups[groups.length - 1];
            if (!group || group.encounterNumber !== encounterNumber) {
                group = { encounterNumber, monsters: [] };
                groups.push(group);
            }
            group.monsters.push({
                ...monster,
                _globalIndex: index,
                _id: `c${cycleNum}_m${index}`,
                _isCompleted: (session?.completed_encounters || []).includes(`c${cycleNum}_m${index}`)
            });
        });
        return groups;
    };

    const handleCompleteMonster = async (cycleNum, monsterIndex, monster) => {
        const monsterId = `c${cycleNum}_m${monsterIndex}`;
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/complete-encounter`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    encounter_num: monsterId,
                    monster_id: monsterId,
                    cycle: cycleNum,
                    monster_index: monsterIndex
                })
            });
            if (response.ok) {
                const data = await response.json();
                if (data.rations !== undefined) {
                    setSession(prev => prev ? { ...prev, rations: data.rations } : prev);
                }
                fetchSessionDetails();
                const noticeMessage = data.shop_started
                    ? `${data.shop_cycle_name} complete! The shop is open for players.`
                    : `${monster.name} defeated and rewards granted!`;
                setNotice({ message: noticeMessage, type: 'success' });
                setTimeout(() => setNotice(null), 3000);
            } else {
                const data = await response.json();
                addAlert(data.error || "Failed to complete monster", "error");
            }
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const handleUseRations = async (restType) => {
        const cost = restType === 'long' ? 1 : 0.5;
        const label = restType === 'long' ? 'Long Rest' : 'Short Rest';
        if (!await confirm(`Spend ${cost} ration${cost === 1 ? '' : 's'} to prepare a party ${label}?`)) return;

        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/spend-rations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ rest_type: restType })
            });
            const data = await response.json();
            if (response.ok) {
                addAlert(`${label} prepared for linked characters.`, "success");
                setSession(prev => prev ? { ...prev, rations: data.rations } : prev);
                fetchSessionDetails();
            } else {
                addAlert(data.error || `Failed to prepare ${label}`, "error");
            }
        } catch (err) {
            addAlert(err.message, "error");
        }
    };

    const handleClaimItem = async (index) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/claim-item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ item_index: index })
            });
            const data = await response.json();
            if (response.ok) {
                addAlert("Item claimed successfully!", "success");
                fetchSessionDetails();
            } else {
                addAlert(data.error || "Failed to claim item", "error");
            }
        } catch (err) {
            addAlert("An error occurred while claiming the item.", "error");
        }
    };

    const handleClaimGold = async (shareIndex) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/claim-gold`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ share_index: shareIndex })
            });
            const data = await response.json();
            if (response.ok) {
                addAlert("Gold claimed successfully!", "success");
                fetchSessionDetails();
            } else {
                addAlert(data.error || "Failed to claim gold", "error");
            }
        } catch (err) {
            addAlert("An error occurred while claiming the gold.", "error");
        }
    };

    const handleCategorySelect = async (category) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/shop/select-category`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ category })
            });
            const data = await response.json();
            if (!response.ok) {
                addAlert(data.error || "Failed to select category", "error");
            } else {
                fetchSessionDetails();
            }
        } catch (err) {
            addAlert("An error occurred selecting a category.", "error");
        }
    };

    const handleBuyItem = async () => {
        if (!shopConfirm) return;
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/shop/buy-item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    category: shopConfirm.category,
                    item_index: shopConfirm.itemIndex,
                    is_common: shopConfirm.isCommon,
                    trade_in_indices: shopConfirm.tradeIns || []
                })
            });
            const data = await response.json();
            if (response.ok) {
                addAlert(data.message, "success");
                setShopConfirm(null);
                fetchSessionDetails();
            } else {
                addAlert(data.error || "Failed to buy item", "error");
            }
        } catch (err) {
            addAlert("An error occurred while buying the item.", "error");
        }
    };

    const fetchSellPrices = async () => {
        const myParticipant =
            session.participants.find(
                p => p.user_id === currentUser.id
            );
        const inventory =
            myParticipant?.character?.data?.inventory || [];
        try {
            const res = await fetch(
                `${API_BASE_URL}/api/host/${session.id}/shop/sell-price`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        items: inventory
                    })
                }
            );
            const data = await res.json();
            if (res.ok) {
                setSellPrices(data.prices);
            }
        }
        catch (err) {
            console.error(
                "Failed fetching sell prices:",
                err
            );
        }
    };

    const handleSellItems = async () => {
        try {
            const items = Object.entries(selectedSellItems).map(([index, quantity]) => ({
                index: Number(index),
                quantity
            }));
            const res = await fetch(
                `${API_BASE_URL}/api/host/${session.id}/shop/sell-items`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        items
                    })
                }
            );
            const data = await res.json();
            if (res.ok) {
                addAlert(
                    `Sold items for ${data.gold_gained} gp`,
                    "success"
                );

                setShowSellModal(false);
                setSelectedSellItems({});
                fetchSessionDetails();
            }
            else {
                addAlert(
                    data.error || "Selling failed",
                    "error"
                );
            }
        }
        catch (err) {
            addAlert(
                "Error selling items",
                "error"
            );
        }
    };

    const handleToggleShopLock = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/shop/toggle-lock`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (response.ok) {
                addAlert(data.message, "success");
                fetchSessionDetails();
            } else {
                addAlert(data.error || "Failed to toggle shop lock", "error");
            }
        } catch (err) {
            addAlert("An error occurred while toggling the shop lock.", "error");
        }
    };

    const handleDismissLevelUpReveal = () => {
        if (levelUpReveal) {
            const levelKey = `${levelUpReveal.id}_${levelUpReveal.level}`;
            setDismissedLevelUps(prev => new Set(prev).add(levelKey));
            setLevelUpReveal(null);
        }
    };

    const handleDeleteSession = async () => {
        if (!await confirm("WARNING: This will permanently delete this session and all its progress. This action cannot be undone. Are you sure?")) return;

        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                addAlert("Session deleted successfully", "success");
                navigate('/hosting');
            } else {
                const data = await response.json();
                addAlert(data.error || "Failed to delete session", "error");
            }
        } catch (err) {
            addAlert(err.message, "error");
        }
    };

    const handleLeaveSession = async () => {
        if (!await confirm("Are you sure you want to leave this trial?")) return;

        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${id}/leave`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (response.ok) {
                addAlert("Left trial successfully", "success");
                navigate('/hosting');
            } else {
                addAlert(data.error || "Failed to leave trial", "error");
            }
        } catch (err) {
            addAlert(err.message, "error");
        }
    };

    const toggleEncounter = (num) => {
        setExpandedEncounters(prev => ({ ...prev, [num]: !prev[num] }));
    };

    const toggleWildSurge = (e, num) => {
        e.stopPropagation();
        setWildSurgeVisible(prev => ({ ...prev, [num]: !prev[num] }));
    };

    const renderInteractiveShop = (num) => {
        const state = session.shop_state;
        const phase = state.phase;

        if (phase === "selection") {
            const eligibleParticipants = session.participants.filter(p => p.role === 'Ascendant' && p.character_id);
            const neededChoices = Object.keys(state.selections).length;
            const targetChoices = Math.min(4, eligibleParticipants.length);

            const myCharId = eligibleParticipants.find(p => p.user_id === currentUser.id)?.character_id;
            const myChoice = myCharId ? state.selections[myCharId] : null;

            const isDMOrAdmin = currentUser.id === session.dm_id || isAdmin;
            const isLocked = !!state.locked;
            return (
                <div className={`shop-phase-container ${isLocked ? 'is-locked' : ''}`}>
                    <div className="shop-header-box">
                        <div className="shb-title-row">
                            <h3><i className="fa-solid fa-cart-shopping"></i>The Chamber of Brief Mercy {isLocked && <span className="locked-badge"><i className="fa-solid fa-lock"></i> LOCKED</span>}</h3>
                            {isDMOrAdmin && (
                                <button
                                    className={`shop-lock-toggle-btn ${isLocked ? 'locked' : 'unlocked'}`}
                                    onClick={(e) => { e.stopPropagation(); handleToggleShopLock(); }}
                                    title={isLocked ? "Unlock Shop for players" : "Lock Shop interactions"}
                                >
                                    <i className={`fa-solid fa-lock${isLocked ? '-open' : ''}`}></i> {isLocked ? 'Unlock' : 'Lock'}
                                </button>
                            )}
                        </div>
                        <p>{isLocked ? "This shop is currently locked by the Dungeon Master." : "Choose a category to stock the shop's shelves."}</p>
                    </div>
                    <div className="shop-category-grid">
                        {state.categories_available.map(cat => {
                            const chosenByAnyone = Object.values(state.selections).includes(cat);
                            const chosenByMe = myChoice === cat;
                            let btnClass = "shop-cat-btn ";
                            if (chosenByMe) btnClass += "chosen-me";
                            else if (chosenByAnyone) btnClass += "chosen-other";
                            else btnClass += "available";

                            return (
                                <button
                                    key={cat}
                                    className={btnClass}
                                    onClick={() => !chosenByAnyone && !myChoice && !isDMOrAdmin && !isLocked && handleCategorySelect(cat)}
                                    disabled={chosenByAnyone || !!myChoice || isDMOrAdmin || isLocked}
                                    title={isLocked ? "Shop is locked" : (chosenByAnyone && !chosenByMe ? "Another party member already chose this." : "")}
                                >
                                    <span className="cat-name">{cat}</span>
                                </button>
                            );
                        })}
                    </div>
                    {myChoice && !isLocked && (
                        <div className="shop-awaiting-msg">
                            <em><i className="fa-solid fa-hourglass-half"></i> Thank you for choosing. Awaiting the rest of the party... ({neededChoices}/{targetChoices})</em>
                        </div>
                    )}
                </div>
            );
        }

        if (isBuildingShop) {
            return (
                <div className="shop-phase-container build-anim">
                    <div className="shop-building-msg">
                        <h2><i className="fa-solid fa-hammer"></i> Building shop...</h2>
                    </div>
                </div>
            );
        }

        if (phase === "shopping") {
            const myParticipant = session.participants.find(p => p.user_id === currentUser.id);
            const myGold = myParticipant?.character?.data?.gold || 0;

            const isDMOrAdmin = currentUser.id === session.dm_id || isAdmin;
            const isLocked = !!state.locked;

            const renderItemsList = (itemDict, isCommonSec) => {
                const entries = Object.entries(itemDict);
                // Place Wondrous at the end of the generated items list
                entries.sort(([a], [b]) => {
                    if (a === "Wondrous") return 1;
                    if (b === "Wondrous") return -1;
                    return 0;
                });

                return entries.map(([cat, list]) => (
                    <div key={cat} className="shop-items-category">
                        <h5>{cat}</h5>
                        <div className="shop-items-grid">
                            {list.map((item, idx) => {
                                const sold = item.sold_to;
                                const affordable = myGold >= item.cost;
                                let btnClass = "shop-item-btn ";
                                if (sold) btnClass += "sold";
                                else if (!affordable) btnClass += "broke";
                                else btnClass += "affordable";

                                return (
                                    <button
                                        key={idx}
                                        className={btnClass}
                                        onClick={() => !sold && affordable && !isDMOrAdmin && !isLocked && setShopConfirm({ category: cat, itemIndex: idx, item, isCommon: isCommonSec, tradeIns: [] })}
                                        disabled={!!sold || !affordable || isDMOrAdmin || isLocked}
                                        title={isLocked ? "Shop is locked" : (sold ? `Bought by ${sold.char_name}` : (!affordable ? `You need ${item.cost} gp (You have ${myGold} gp)` : ""))}
                                    >
                                        <div className="si-details">
                                            <span className="si-name">{item.name}</span>
                                            {sold && <span className="si-sold-badge">Sold</span>}
                                        </div>
                                        <div className="si-cost">
                                            {item.cost} <i className="fa-solid fa-coins"></i>
                                        </div>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                ));
            };

            return (
                <div className={`shop-phase-container ${isLocked ? 'is-locked' : ''}`}>
                    <div className="shop-header-box border-bottom">
                        <div className="shb-title-row">
                            <h3>
                                <i className="fa-solid fa-cart-shopping"></i>
                                The Chamber of Brief Mercy
                                {isLocked && (
                                    <span className="locked-badge">
                                        <i className="fa-solid fa-lock"></i> LOCKED
                                    </span>
                                )}
                            </h3>
                            {!isDMOrAdmin && !isLocked && (
                                <button
                                    className="shop-sell-btn"
                                    onClick={() => {
                                        fetchSellPrices();
                                        setShowSellModal(true);
                                    }}
                                >
                                    <i className="fa-solid fa-coins"></i>
                                    Sell Items
                                </button>
                            )}
                            {isDMOrAdmin && (
                                <button
                                    className={`shop-lock-toggle-btn ${isLocked ? 'locked' : 'unlocked'}`}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        handleToggleShopLock();
                                    }}
                                    title={isLocked ? "Unlock Shop for players" : "Lock Shop interactions"}
                                >
                                    <i className={`fa-solid fa-lock${isLocked ? '-open' : ''}`}></i>
                                    {isLocked ? "Unlock" : "Lock"}
                                </button>
                            )}
                        </div>
                        <p>{isLocked ? "This shop is currently locked by the Dungeon Master." : "Welcome, travelers. See anything you like?"}</p>
                    </div>

                    <div className="shop-sections-wrap">
                        <section className="shop-items-section generated">
                            {renderItemsList(state.items, false)}
                        </section>

                        <div className="common-dropdown-wrap">
                            <button className="common-toggle-btn" onClick={() => setShowCommonItems(!showCommonItems)}>
                                <i className={`fa-solid fa-chevron-${showCommonItems ? 'down' : 'right'}`}></i> Common Goods <span>Always Available</span>
                            </button>
                            {showCommonItems && (
                                <section className="shop-items-section common-area">
                                    {renderItemsList(state.common_items, true)}
                                </section>
                            )}
                        </div>
                    </div>
                </div>
            );
        }

        return null;
    };

    const renderEncounterContent = (num, encounter) => {
        if (encounter.type === "Shop Encounter") {
            // Interactive Shop
            if (session.shop_state && session.shop_state.encounter_num === parseInt(num)) {
                return <div className="encounter-details">{renderInteractiveShop(num)}</div>;
            }
            // Fallback / historical view
            return (
                <div className="encounter-details">
                    <div className="detail-section highlight">
                        <h4><i className="fa-solid fa-gem"></i> Item Rarity Mix</h4>
                        <div className="rarity-grid">
                            {Object.entries(encounter.rarity_mix || {}).map(([rarity, count]) => (
                                <div key={rarity} className={`rarity-tag ${rarity.toLowerCase()}`}>
                                    {rarity}: {count}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="detail-section">
                        <h4><i className="fa-solid fa-shop"></i> Shop Inventory</h4>
                        {Object.entries(encounter.items_by_category || {}).map(([category, items]) => (
                            <div key={category} className="item-category">
                                <h5>{category}</h5>
                                <ul>
                                    {items.map((item, idx) => (
                                        <li key={idx}>{typeof item === 'string' ? item : item.name}</li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>
                </div>
            );
        }

        return (
            <div className="encounter-details">
                <div className="stats-row">
                    {encounter.xp && <div className="stat-pill"><strong>XP:</strong> {encounter.xp}</div>}
                    {encounter.total_xp && <div className="stat-pill"><strong>Total XP:</strong> {encounter.total_xp}</div>}
                    {encounter.gold && <div className="stat-pill gold"><strong>Gold:</strong> {encounter.gold}g</div>}
                    {encounter.is_levelup && <div className="stat-pill level-up"><strong>LEVEL UP!</strong></div>}
                </div>

                {encounter.note && <p className="encounter-note"><em>{encounter.note}</em></p>}

                {encounter.monsters && (
                    <div className="detail-section">
                        <h4><i className="fa-solid fa-skull"></i> Monsters</h4>
                        <ul className="monster-list">
                            {encounter.monsters.map((m, i) => <li key={i}>{m}</li>)}
                        </ul>
                    </div>
                )}

                {encounter.magic_items && (
                    <div className="detail-section highlight">
                        <h4><i className="fa-solid fa-wand-magic-sparkles"></i> Divine Gifts</h4>
                        <ul className="gift-list">
                            {encounter.magic_items.map((item, i) => (
                                <li key={i}>{typeof item === 'string' ? item : item.name}</li>
                            ))}
                        </ul>
                    </div>
                )}

                {encounter.wild_surge && (
                    <div className="wild-surge-box">
                        <button
                            className={`wild-surge-toggle ${wildSurgeVisible[num] ? 'active' : ''}`}
                            onClick={(e) => toggleWildSurge(e, num)}
                        >
                            <i className="fa-solid fa-bolt"></i> {encounter.wild_surge.name}
                        </button>
                        {wildSurgeVisible[num] && (
                            <div className="wild-surge-content">
                                <p><strong>Description:</strong> {encounter.wild_surge.description}</p>
                                <p className="echo-asc"><strong>Echo Of Ascendance:</strong> {encounter.wild_surge["echo of ascendance"]}</p>
                                <p className="echo-ruin"><strong>Echo Of Ruin:</strong> {encounter.wild_surge["echo of ruin"]}</p>
                                <p className="worldshift"><strong>Worldshift Trait:</strong> {encounter.wild_surge["worldshift trait"]}</p>
                            </div>
                        )}
                    </div>
                )}

                {encounter.rations !== undefined && (
                    <div className="ration-info">
                        <i className="fa-solid fa-utensils"></i> Rations: {encounter.rations}
                    </div>
                )}
            </div>
        );
    };

    if (loading) return <div className="hosted-page-container"><div className="loading-screen">Echoing through the Spire...</div></div>;
    if (!session) return <div className="hosted-page-container"><div className="error-message">Session not found or connection lost.</div></div>;

    const isDM = currentUser?.id === session.dm_id;
    const isDMOrAdmin = isDM || isAdmin;

    const isEndless = session.run?.data?.mode === 'The Endless Trials';
    const totalEncounters = isEndless
        ? (session.run?.data?.cycles?.reduce((sum, c) => sum + (c.monsters?.length || 0), 0) || 0)
        : (session.run?.data?.encounters?.length || 0);
    const completedEncountersCount = (session.completed_encounters || []).length;
    const allEncountersCompleted = totalEncounters > 0 && completedEncountersCount >= totalEncounters;

    return (
        <div className="hosted-page-container">
            {notice && (
                <div className={`global-notice ${notice.type}`}>
                    <i className="fa-solid fa-circle-check"></i>
                    {notice.message}
                </div>
            )}
            <header className="session-header">
                <div className="session-info">
                    <button className="back-link" onClick={() => navigate('/hosting')}>
                        <i className="fa-solid fa-arrow-left"></i> Hub
                    </button>
                    {isEditingTitle ? (
                        <div className="title-edit-container">
                            <input
                                className="rename-input"
                                type="text"
                                value={runTitleInput}
                                maxLength={24}
                                onChange={(e) => setRunTitleInput(e.target.value)}
                                autoFocus
                                onKeyDown={(e) => e.key === 'Enter' && handleRenameRun()}
                            />
                            <div className="rename-actions">
                                <button className="icon-btn save" onClick={handleRenameRun} title="Save"><i className="fa-solid fa-check"></i></button>
                                <button className="icon-btn cancel" onClick={() => setIsEditingTitle(false)} title="Cancel"><i className="fa-solid fa-xmark"></i></button>
                            </div>
                        </div>
                    ) : (
                        <h1 className="editable-title">
                            {session.run.title}
                            {isDM ? (
                                <div className="dm-actions">
                                    {!session.is_completed && (
                                        <button className="edit-title-btn" onClick={startEditingTitle} title="Rename Run">
                                            <i className="fa-solid fa-pen-to-square"></i>
                                        </button>
                                    )}
                                    {(!session.is_completed || isAdmin) && (
                                        <button className="delete-session-btn" onClick={handleDeleteSession} title={isAdmin ? "Admin: Delete Run" : "Delete Run"}>
                                            <i className="fa-solid fa-trash-can"></i>
                                        </button>
                                    )}
                                </div>
                            ) : (
                                <div className="dm-actions">
                                    {isAdmin && (
                                        <button className="delete-session-btn" onClick={handleDeleteSession} title="Admin: Delete Run">
                                            <i className="fa-solid fa-trash-can"></i>
                                        </button>
                                    )}
                                    {!session.is_completed && (
                                        <button className="leave-session-header-btn" onClick={handleLeaveSession} title="Leave Trial">
                                            <i className="fa-solid fa-right-from-bracket"></i> Leave Trial
                                        </button>
                                    )}
                                </div>
                            )}
                        </h1>
                    )}
                    <div className="invite-badge">
                        CODE: <span>{session.invite_code}</span>
                    </div>
                </div>
                <div className="session-header-tools">
                    {isDM && allEncountersCompleted && !session.is_completed && (
                        <button
                            className="complete-archive-btn"
                            onClick={handleCompleteAndArchive}
                            title="All encounters cleared! Click to Complete & Archive this Run"
                        >
                            <i className="fa-solid fa-crown"></i> Complete & Archive Run
                        </button>
                    )}
                    {session.is_completed && (
                        <div className="ascended-trial-badge" title="This Trial has been completed and permanently archived in the Hall of Ascension.">
                            <i className="fa-solid fa-trophy"></i> TRIAL ASCENDED
                        </div>
                    )}
                    <div className="rations-pill" title="Party rations for this hosted run">
                        <div className="rations-pill-main">
                            <i className="fa-solid fa-bowl-food"></i>
                            <span className="rations-label">Rations</span>
                            <strong>{formatRations(session.rations)}</strong>
                        </div>
                        {isDMOrAdmin && !session.is_completed ? (
                            <div className="rations-actions">
                                <button
                                    onClick={() => handleUseRations('short')}
                                    disabled={Number(session.rations || 0) < 0.5}
                                    title="Spend 0.5 ration to prepare a party Short Rest"
                                >
                                    Short
                                </button>
                                <button
                                    onClick={() => handleUseRations('long')}
                                    disabled={Number(session.rations || 0) < 1}
                                    title="Spend 1 ration to prepare a party Long Rest"
                                >
                                    Long
                                </button>
                            </div>
                        ) : isDMOrAdmin && session.is_completed ? (
                            <span className="rations-helper-text">
                                Trial Archived
                            </span>
                        ) : (
                            <span className="rations-helper-text">
                                Only the DM can give Rests
                            </span>
                        )}
                    </div>
                    <UserProfilePill />
                </div>


                <nav className="session-tabs">
                    <button className={activeTab === 'trial' ? 'active' : ''} onClick={() => { setActiveTab('trial'); setSearchTerm(''); }}>Trial</button>
                    <button className={activeTab === 'party' ? 'active' : ''} onClick={() => { setActiveTab('party'); setSearchTerm(''); }}>Party</button>
                    <button className={activeTab === 'inventory' ? 'active' : ''} onClick={() => { setActiveTab('inventory'); setSearchTerm(''); }}>Vault</button>
                </nav>
            </header>

            <main className="session-content">
                {activeTab === 'trial' && (
                    <div className="trial-view">
                        <section className="blessing-banner">
                            <h3>Divine Blessing: {session.run.data.divine_blessing?.name}</h3>
                            {session.run.data.divine_blessing?.title && (
                                <p className="blessing-title"><em>{session.run.data.divine_blessing.title}</em></p>
                            )}
                            {session.run.data.divine_blessing?.description && (
                                <p className="blessing-desc">{session.run.data.divine_blessing.description}</p>
                            )}
                            <div className="blessing-effect">
                                <span className="grace-label">Grace</span>
                                {(() => {
                                    const blessingText = session.run.data.divine_blessing?.blessing;
                                    const abilities = parseGraceAbilities(blessingText);
                                    if (abilities) {
                                        return (
                                            <div className="grace-abilities">
                                                {abilities.map((ability, i) => (
                                                    <div key={i} className="grace-ability-block">
                                                        <span className="grace-ability-name">{ability.name}</span>
                                                        <p className="grace-ability-body">{ability.body}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        );
                                    }
                                    return <p className="grace-ability-body">{blessingText}</p>;
                                })()}
                            </div>
                        </section>

                        <div className="search-wrapper" style={{ maxWidth: '100%', marginBottom: '20px' }}>
                            <input
                                type="text"
                                className="search-input"
                                placeholder={isEndless ? "Search monsters, CR, items, rules..." : "Search Trial encounters (types, monsters, notes)..."}
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <i className="fa-solid fa-magnifying-glass"></i>
                        </div>

                        {!isDM && (
                            <div className="player-info-note">
                                <i className="fa-solid fa-circle-info"></i>
                                {isEndless
                                    ? "Completed monsters and their rewards will appear below as you progress."
                                    : "Completed trial encounters and their rewards will appear below as you progress."}
                            </div>
                        )}

                        {isEndless ? (
                            <div className="endless-trials-results">
                                <div className="endless-trials-summary">
                                    <div className="summary-badge">{session.run.data.mode}</div>
                                </div>

                                {isDM && session.run.data.wild_surges && (
                                    <section className="wild-surge-deck-card">
                                        <div className="wild-surge-deck-header">
                                            <h3><i className="fa-solid fa-bolt"></i> Wild Surge Deck</h3>
                                            <button
                                                type="button"
                                                className={`wild-surge-expand-btn ${wildSurgesExpanded ? 'active' : ''}`}
                                                onClick={() => setWildSurgesExpanded(prev => !prev)}
                                                aria-expanded={wildSurgesExpanded}
                                            >
                                                {wildSurgesExpanded ? 'Hide' : 'View'}
                                                <i className={`fa-solid fa-chevron-${wildSurgesExpanded ? 'up' : 'down'}`}></i>
                                            </button>
                                        </div>
                                        {wildSurgesExpanded && (
                                            <ol className="wild-surge-deck-list">
                                                {session.run.data.wild_surges.map((surge, index) => {
                                                    const surgeId = String(surge.id ?? index);
                                                    const isSurgeActive = activeWildSurgeId === surgeId;
                                                    const surgeKey = `endless-${surgeId}`;

                                                    return (
                                                        <li key={surgeId}>
                                                            <div className="wild-surge-box">
                                                                <div className="wild-surge-deck-entry">
                                                                    <button
                                                                        type="button"
                                                                        className={`wild-surge-toggle ${wildSurgeVisible[surgeKey] ? 'active' : ''}`}
                                                                        onClick={(e) => toggleWildSurge(e, surgeKey)}
                                                                        aria-expanded={!!wildSurgeVisible[surgeKey]}
                                                                    >
                                                                        <i className="fa-solid fa-bolt"></i> {surge.name}
                                                                    </button>
                                                                    <button
                                                                        type="button"
                                                                        className={`complete-btn monster-complete-btn wild-surge-active-btn ${isSurgeActive ? 'active' : ''}`}
                                                                        onClick={() => setActiveWildSurgeId(current => current === surgeId ? null : surgeId)}
                                                                        title={isSurgeActive ? `Deactivate ${surge.name}` : `Activate ${surge.name}`}
                                                                        aria-label={isSurgeActive ? `Deactivate ${surge.name}` : `Activate ${surge.name}`}
                                                                        aria-pressed={isSurgeActive}
                                                                    >
                                                                        <i className="fa-solid fa-check"></i>
                                                                    </button>
                                                                </div>
                                                                {wildSurgeVisible[surgeKey] && (
                                                                    <div className="wild-surge-content">
                                                                        <p><strong>Description:</strong> {surge.description}</p>
                                                                        <p className="echo-asc"><strong>Echo Of Ascendance:</strong> {surge["echo of ascendance"]}</p>
                                                                        <p className="echo-ruin"><strong>Echo Of Ruin:</strong> {surge["echo of ruin"]}</p>
                                                                        <p className="worldshift"><strong>Worldshift Trait:</strong> {surge["worldshift trait"]}</p>
                                                                    </div>
                                                                )}
                                                            </div>
                                                        </li>
                                                    );
                                                })}
                                            </ol>
                                        )}
                                    </section>
                                )}

                                {(() => {
                                    const term = searchTerm.toLowerCase().trim();
                                    const renderedCycles = (session.run.data.cycles || []).map((cycle) => {
                                        const grouped = groupCycleMonsters(cycle.monsters || [], cycle.cycle);

                                        // Filter monsters inside each group based on visibility and search
                                        const filteredGroups = grouped.map(group => {
                                            const visibleMonsters = group.monsters.filter(monster => {
                                                const isVisible = isDM || monster._isCompleted;
                                                if (!isVisible) return false;
                                                if (!term) return true;
                                                const nameMatch = monster.name?.toLowerCase().includes(term);
                                                const crMatch = monster.cr?.toLowerCase().includes(term);
                                                const noteMatch = (monster.encounter_note || "").toLowerCase().includes(term);
                                                const itemMatch = getDisplayItemName(monster.item).toLowerCase().includes(term);
                                                return nameMatch || crMatch || noteMatch || itemMatch;
                                            });
                                            return {
                                                ...group,
                                                monsters: visibleMonsters
                                            };
                                        }).filter(group => group.monsters.length > 0);

                                        const shopMatchesSearch = !term || (cycle.shop && (
                                            (cycle.shop.type || "").toLowerCase().includes(term) ||
                                            (cycle.shop.rest || "").toLowerCase().includes(term) ||
                                            (cycle.shop.items_by_category && Object.values(cycle.shop.items_by_category).flat().some(item => getDisplayItemName(item).toLowerCase().includes(term)))
                                        ));

                                        const activeCycleShop = session.shop_state?.cycle_shop
                                            && Number(session.shop_state.cycle) === Number(cycle.cycle);

                                        const shouldShowCycle = isDM
                                            ? (!term || filteredGroups.length > 0 || (cycle.shop && shopMatchesSearch))
                                            : (filteredGroups.length > 0 || (cycle.shop && activeCycleShop && shopMatchesSearch));

                                        if (!shouldShowCycle) return null;

                                        return (
                                            <div key={cycle.cycle} className="endless-cycle-card">
                                                <div className="endless-cycle-header">
                                                    <h3>{cycle.name}</h3>
                                                    {cycle.shop && (isDM || activeCycleShop) && (
                                                        <span className="shop-badge"><i className="fa-solid fa-shop"></i> Shop</span>
                                                    )}
                                                </div>

                                                <div className="cycle-rules">
                                                    {cycle.rules.map((rule, index) => (
                                                        <div key={index} className="rule-line">• {rule}</div>
                                                    ))}
                                                </div>

                                                <div className="cycle-encounters">
                                                    {filteredGroups.map(({ encounterNumber, monsters }) => (
                                                        <section key={`${cycle.cycle}-${encounterNumber}`} className="cycle-encounter-group">
                                                            <div className="cycle-encounter-heading">
                                                                <h4>Encounter {encounterNumber}</h4>
                                                                {monsters[0]?.encounter_note && (
                                                                    <span>{monsters[0].encounter_note}</span>
                                                                )}
                                                            </div>
                                                            <div className="cycle-monster-list">
                                                                {monsters.map((monster) => (
                                                                    <div
                                                                        key={monster._id}
                                                                        className={`cycle-monster-row ${monster._isCompleted ? 'completed' : ''}`}
                                                                    >
                                                                        <span className="monster-name">
                                                                            {monster.name}
                                                                            {monster._isCompleted && (
                                                                                <span className="monster-completed-tag">
                                                                                    <i className="fa-solid fa-check"></i> Defeated
                                                                                </span>
                                                                            )}
                                                                        </span>
                                                                        <span className="monster-meta">CR {monster.cr}</span>
                                                                        {monster.xp != null && (
                                                                            <span className="monster-meta monster-xp">{monster.xp.toLocaleString()} XP</span>
                                                                        )}
                                                                        {monster.gold != null && (
                                                                            <span className="monster-meta monster-gold">{monster.gold.toLocaleString()} GP</span>
                                                                        )}
                                                                        {monster.item ? (
                                                                            <span className="monster-item">{getDisplayItemName(monster.item)}</span>
                                                                        ) : (
                                                                            <span className="monster-item empty">—</span>
                                                                        )}
                                                                        {isDM && (
                                                                            <button
                                                                                className="complete-btn monster-complete-btn"
                                                                                onClick={(e) => {
                                                                                    e.stopPropagation();
                                                                                    handleCompleteMonster(cycle.cycle, monster._globalIndex, monster);
                                                                                }}
                                                                                title={monster._isCompleted ? "Completed" : "Complete Monster"}
                                                                                disabled={monster._isCompleted}
                                                                                style={monster._isCompleted ? { background: 'var(--success)', color: 'white' } : {}}
                                                                            >
                                                                                <i className="fa-solid fa-check"></i>
                                                                            </button>
                                                                        )}
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </section>
                                                    ))}
                                                </div>

                                                {cycle.shop && (isDM || activeCycleShop) && shopMatchesSearch && (
                                                    activeCycleShop ? (
                                                        renderInteractiveShop(cycle.cycle)
                                                    ) : (
                                                        <div className="cycle-shop-box">
                                                            <div className="cycle-shop-heading">
                                                                <h4><i className="fa-solid fa-shop"></i> Cycle Shop Preview</h4>
                                                                <span>{cycle.shop.rest} · {cycle.shop.total_gold?.toLocaleString()} GP</span>
                                                            </div>
                                                            {cycle.shop.rarity_mix && (
                                                                <div className="cycle-shop-rarity-mix">
                                                                    {Object.entries(cycle.shop.rarity_mix).map(([rarity, count]) => (
                                                                        <span key={rarity} className={`rarity-tag ${rarity.replace(/\s+/g, '-')}`}>
                                                                            {rarity}: {count}
                                                                        </span>
                                                                    ))}
                                                                </div>
                                                            )}
                                                            {cycle.shop.items_by_category && Object.entries(cycle.shop.items_by_category).map(([category, items]) => (
                                                                <div key={category} className="cycle-shop-category">
                                                                    <strong>{category}</strong>
                                                                    <div className="cycle-shop-items">
                                                                        {items.map((item, idx) => (
                                                                            <span key={idx}>{getDisplayItemName(item)}</span>
                                                                        ))}
                                                                    </div>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    )
                                                )}
                                            </div>
                                        );
                                    }).filter(Boolean);

                                    if (renderedCycles.length === 0) {
                                        return (
                                            <div className="empty-trials-note">
                                                <p>{term ? "No monsters match your search." : (!isDM ? "No monsters have been defeated yet. The trial awaits!" : "No cycles found.")}</p>
                                            </div>
                                        );
                                    }

                                    return renderedCycles;
                                })()}
                            </div>
                        ) : (
                            <div className="encounters-timeline">
                                {(session.run.data.encounters || [])
                                    .filter(([num, enc]) => isDM || session.completed_encounters.includes(String(num)))
                                    .filter(([num, enc]) => {
                                        if (!searchTerm) return true;
                                        const term = searchTerm.toLowerCase();
                                        const monstersMatch = enc.monsters?.some(m => m.toLowerCase().includes(term)) || false;
                                        const typeMatch = (enc.type?.toLowerCase() || "").includes(term);
                                        const noteMatch = (enc.note?.toLowerCase() || "").includes(term);
                                        const itemMatch = enc.magic_items?.some(i => {
                                            const itemName = typeof i === 'string' ? i : i.name;
                                            return (itemName?.toLowerCase() || "").includes(term);
                                        }) || false;
                                        const shopItemMatch = enc.items_by_category ? Object.values(enc.items_by_category).flat().some(i => {
                                            const itemName = typeof i === 'string' ? i : i.name;
                                            return (itemName?.toLowerCase() || "").includes(term);
                                        }) : false;
                                        return monstersMatch || typeMatch || noteMatch || itemMatch || shopItemMatch;
                                    })
                                    .map(([num, enc]) => (
                                        <div key={num} className={`timeline-node ${expandedEncounters[num] ? 'expanded' : ''}`}>
                                            <div className="node-header" onClick={() => toggleEncounter(num)}>
                                                <div className="node-marker">{num}</div>
                                                <div className="node-content">
                                                    <h4>{enc.type}</h4>
                                                    {!expandedEncounters[num] && (
                                                        <p>{enc.monsters?.join(', ') || enc.note || 'Exploration Encounter'}</p>
                                                    )}
                                                </div>
                                                <div className="expand-icon">
                                                    <i className={`fa-solid fa-chevron-${expandedEncounters[num] ? 'up' : 'down'}`}></i>
                                                </div>
                                                {isDM && (
                                                    <button
                                                        className="complete-btn"
                                                        onClick={(e) => { e.stopPropagation(); handleCompleteEncounter(num); }}
                                                        title={session.completed_encounters.includes(String(num)) ? "Completed" : "Complete Encounter"}
                                                        disabled={session.completed_encounters.includes(String(num))}
                                                        style={session.completed_encounters.includes(String(num)) ? { background: 'var(--success)', color: 'white' } : {}}
                                                    >
                                                        <i className="fa-solid fa-check"></i>
                                                    </button>
                                                )}
                                            </div>
                                            {expandedEncounters[num] && renderEncounterContent(num, enc)}
                                        </div>
                                    ))}
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'party' && (
                    <div className="party-view">
                        <div className="participants-grid">
                            {session.participants.map(p => (
                                <div key={p.user_id} className={`participant-card ${p.role === 'DM' ? 'dm' : ''} ${p.user_id === currentUser?.id ? 'is-me' : ''}`}>
                                    <div className="p-header">
                                        <div className="p-avatar">
                                            {p.username.substring(0, 2).toUpperCase()}
                                        </div>
                                        <div className="p-names">
                                            <strong>{p.username}</strong>
                                            <span>{p.role}</span>
                                        </div>
                                    </div>
                                    {p.character ? (
                                        <div className="p-char-preview">
                                            <p className="char-name">
                                                {p.character.name}
                                                {p.character.data?.level_up_pending && (
                                                    <span className="level-up-badge-small" title="Level Up Pending!">✧</span>
                                                )}
                                            </p>
                                            <p className="char-stats">Level {p.character.level || p.character.data?.level} {p.character.class_name || p.character.data?.class_name}</p>
                                            <div className="hp-bar">
                                                <div className="hp-fill" style={{ width: `${((p.character.data?.hp_current || 0) / ((p.character.data?.hp_max_base || 1) + (p.character.data?.hp_modifier || 0))) * 100}%` }}></div>
                                                <span>HP: {p.character.data?.hp_current || 0}/{(p.character.data?.hp_max_base || 0) + (p.character.data?.hp_modifier || 0)}</span>
                                            </div>
                                            <div className="char-card-actions">
                                                <button className="view-sheet-btn" onClick={() => navigate(`/characters/${p.character.id}`)}>
                                                    View Sheet
                                                </button>
                                                {p.character.data?.level_up_pending && p.user_id === currentUser.id && (
                                                    <div className="level-up-reminder-party">
                                                        PENDING UPDATE
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="p-char-missing">
                                            {(p.user_id === currentUser.id && !isDM) ? (
                                                <button className="pick-char-btn" onClick={() => setShowCharPicker(true)}>Pick Character</button>
                                            ) : (
                                                <p>{p.role === 'DM' ? 'Overseeing the Trial' : 'Choosing character...'}</p>
                                            )}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === 'inventory' && (
                    <div className="inventory-tab-container">
                        <div className="search-wrapper" style={{ maxWidth: '100%', marginBottom: '20px' }}>
                            <input
                                type="text"
                                className="search-input"
                                placeholder="Search the Vault for items or gold sources..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <i className="fa-solid fa-magnifying-glass"></i>
                        </div>
                        <div className="inventory-view">
                            <section className="vault-section">
                                <h3><i className="fa-solid fa-box-open"></i> Available Spoils</h3>
                                <div className="vault-grid">
                                    {session.vault_gold && session.vault_gold.length > 0 &&
                                        session.vault_gold
                                            .filter(share => !searchTerm || share.source.toLowerCase().includes(searchTerm.toLowerCase()) || "gold".includes(searchTerm.toLowerCase()))
                                            .map((share, idx) => (
                                                <div key={`gold-${idx}`} className="vault-item gold-share">
                                                    <div className="item-info">
                                                        <i className="fa-solid fa-coins" style={{ color: '#ffd700' }}></i>
                                                        <span className="item-name">{share.count}x {share.amount} Gold Shares</span>
                                                        <small style={{ display: 'block', color: 'var(--text-dim)', fontSize: '0.7rem' }}>Source: {share.source}</small>
                                                    </div>
                                                    {!isDM && (
                                                        <button className="claim-btn gold" onClick={() => handleClaimGold(idx)}>
                                                            Claim 1x
                                                        </button>
                                                    )}
                                                </div>
                                            ))
                                    }
                                    {session.party_inventory.length > 0 ? (
                                        session.party_inventory
                                            .filter(item => {
                                                const itemName = typeof item === 'string' ? item : item.name;
                                                return !searchTerm || itemName.toLowerCase().includes(searchTerm.toLowerCase());
                                            })
                                            .map((item, idx) => (
                                                <div key={`item-${idx}`} className="vault-item">
                                                    <span className="item-name">{typeof item === 'string' ? item : item.name}</span>
                                                    {!isDM && (
                                                        <button className="claim-btn" onClick={() => handleClaimItem(idx)}>
                                                            <i className="fa-solid fa-hand-holding-dollar"></i> Claim
                                                        </button>
                                                    )}
                                                </div>
                                            ))
                                    ) : (
                                        (!session.vault_gold || session.vault_gold.length === 0) && (
                                            <div className="empty-vault">
                                                <p>No available items in the vault.</p>
                                            </div>
                                        )
                                    )}
                                </div>
                            </section>

                            <section className="vault-section claimed">
                                <h3><i className="fa-solid fa-circle-check"></i> Claimed Rewards</h3>
                                <div className="vault-grid">
                                    {(session.claimed_items && session.claimed_items.length > 0) ? (
                                        session.claimed_items
                                            .filter(entry => {
                                                const itemName = typeof entry.item === 'string' ? entry.item : entry.item.name;
                                                return !searchTerm || itemName.toLowerCase().includes(searchTerm.toLowerCase()) || entry.character_name.toLowerCase().includes(searchTerm.toLowerCase());
                                            })
                                            .map((entry, idx) => (
                                                <div key={idx} className="vault-item claimed">
                                                    <span className="item-name">{typeof entry.item === 'string' ? entry.item : entry.item.name}</span>
                                                    <div className="claimed-by">
                                                        <i className="fa-solid fa-user-tag"></i> {entry.character_name}
                                                    </div>
                                                </div>
                                            ))
                                    ) : (
                                        <div className="empty-vault">
                                            <p>No items have been claimed yet.</p>
                                        </div>
                                    )}
                                </div>
                            </section>
                        </div>
                    </div>
                )}
            </main>

            {showCharPicker && (
                <div className="modal-overlay">
                    <div className="char-picker-modal">
                        <h2>Select Your Champion</h2>
                        <div className="char-list">
                            {userCharacters
                                .filter(char => char.user_id === currentUser?.id && (!char.active_run_id || char.active_run_id === parseInt(id)))
                                .map(char => (
                                    <div key={char.id} className="char-option" onClick={() => handleLinkCharacter(char.id)}>
                                        <strong>{char.name}</strong>
                                        <span>Level {char.level} {char.class_name}</span>
                                    </div>
                                ))}
                            {userCharacters.filter(char => char.user_id === currentUser?.id && (!char.active_run_id || char.active_run_id === parseInt(id))).length === 0 && (
                                <p>No eligible characters found. Characters already participating in another Run cannot be selected.</p>
                            )}
                        </div>
                        <button className="close-modal" onClick={() => setShowCharPicker(false)}>Cancel</button>
                    </div>
                </div>
            )}

            {shopConfirm && (() => {
                const myParticipant = session.participants.find(p => p.user_id === currentUser.id);
                const currentGold = myParticipant?.character?.data?.gold || 0;
                const charInventoryRaw = myParticipant?.character?.data?.inventory || [];
                const charInventory = charInventoryRaw.map(it =>
                    typeof it === 'string' ? { name: it, rarity: 'common', category: 'Other' } : it
                );

                const RARITY_VALS = { 'common': 50, 'uncommon': 400, 'rare': 4000, 'very rare': 40000, 'legendary': 400000 };
                const getItemVal = (it) => {
                    const r = it.rarity?.toLowerCase() || 'common';
                    const base = RARITY_VALS[r] || 0;
                    return it.category === 'Wondrous' ? base * 2 : base;
                };

                const itemToBuy = shopConfirm.item;
                const isWondrous = shopConfirm.category === 'Wondrous';
                const baseCost = itemToBuy.cost;

                // Calculate discount from selected trade-ins
                const selectedIndices = shopConfirm.tradeIns || [];
                const totalDiscount = selectedIndices.reduce((acc, idx) => acc + getItemVal(charInventory[idx]), 0);
                const finalCost = Math.max(0, baseCost - totalDiscount);
                const remainingGold = currentGold - finalCost;

                // Find eligible items for trade-in (same rarity)
                const eligibleItems = isWondrous ? charInventory.map((it, idx) => ({ ...it, originalIndex: idx }))
                    .filter(it => it.rarity && it.rarity.toLowerCase() === itemToBuy.rarity?.toLowerCase()) : [];

                const toggleTradeIn = (idx) => {
                    const newTradeIns = selectedIndices.includes(idx)
                        ? selectedIndices.filter(i => i !== idx)
                        : [...selectedIndices, idx];
                    setShopConfirm({ ...shopConfirm, tradeIns: newTradeIns });
                };

                return (
                    <div className="modal-overlay">
                        <div className="shop-confirm-modal">
                            <h2>Confirm Purchase</h2>
                            <div className="shop-modal-body">
                                <div className="sq-header">
                                    <p className="sq-item-name">{itemToBuy.name}</p>
                                    <span className={`rarity-tag ${itemToBuy.rarity?.toLowerCase()}`}>{itemToBuy.rarity}</span>
                                </div>

                                {isWondrous && (
                                    <div className="trade-in-section">
                                        <h4><i className="fa-solid fa-arrows-rotate"></i> Trade-in Options</h4>
                                        <p className="trade-in-hint">Trade items of the same rarity to reduce the price.</p>
                                        <div className="trade-in-grid">
                                            {eligibleItems.length > 0 ? (
                                                eligibleItems.map((it) => (
                                                    <div
                                                        key={it.originalIndex}
                                                        className={`trade-in-item ${selectedIndices.includes(it.originalIndex) ? 'selected' : ''}`}
                                                        onClick={() => toggleTradeIn(it.originalIndex)}
                                                    >
                                                        <div className="tii-info">
                                                            <span className="tii-name">{it.name}</span>
                                                            <span className="tii-rarity">{it.rarity} {it.category}</span>
                                                        </div>
                                                        <div className="tii-value">
                                                            -{getItemVal(it)} gp
                                                        </div>
                                                    </div>
                                                ))
                                            ) : (
                                                <div className="trade-in-empty">No items of {itemToBuy.rarity} rarity available for trade.</div>
                                            )}
                                        </div>
                                        {totalDiscount > 0 && (
                                            <div className="trade-in-summary">
                                                <span className="tis-label">Total Trade-in Value:</span>
                                                <span className="tis-value">-{totalDiscount} gp</span>
                                            </div>
                                        )}
                                    </div>
                                )}

                                <div className="shop-gold-summary">
                                    <div className="sgs-row">
                                        <span>Current Gold:</span>
                                        <span>{currentGold} <i className="fa-solid fa-coins"></i></span>
                                    </div>
                                    <div className="sgs-row cost">
                                        <span>{isWondrous ? 'Final Cost:' : 'Cost:'}</span>
                                        <span className={totalDiscount > 0 ? 'discounted' : ''}>
                                            - {finalCost} <i className="fa-solid fa-coins"></i>
                                        </span>
                                    </div>
                                    <hr />
                                    <div className={`sgs-row remaining ${remainingGold < 0 ? 'insufficient' : ''}`}>
                                        <span>Remaining:</span>
                                        <span>{remainingGold} <i className="fa-solid fa-coins"></i></span>
                                    </div>
                                </div>
                            </div>
                            <div className="shop-modal-actions">
                                <button
                                    className="confirm-btn gold"
                                    onClick={handleBuyItem}
                                    disabled={remainingGold < 0}
                                >
                                    <i className="fa-solid fa-hand-holding-dollar"></i> Confirm & Buy
                                </button>
                                <button className="close-modal" onClick={() => setShopConfirm(null)}>Cancel</button>
                            </div>
                        </div>
                    </div>
                );
            })()}
            {showSellModal && (() => {
                const myParticipant =
                    session.participants.find(
                        p => p.user_id === currentUser.id
                    );
                const inventory =
                    myParticipant?.character?.data?.inventory || [];
                const normalized =
                    inventory.map((it, idx) => {
                        if (typeof it === "string") {
                            return {
                                name: it,
                                rarity: "common",
                                category: "Other",
                                originalIndex: idx
                            };
                        }
                        return {
                            ...it,
                            originalIndex: idx
                        };
                    });
                const total = Object.entries(selectedSellItems)
                    .reduce(
                        (sum, [index, quantity]) =>
                            sum + ((sellPrices[index] || 0) / (normalized[index]?.quantity || 1)) * quantity,
                        0
                    );

                return (
                    <div className="modal-overlay">
                        <div className="shop-confirm-modal sell-items-modal">
                            <h2>Sell Items</h2>
                            <div className="shop-modal-body">
                                <div className="trade-in-grid">
                                    {
                                        normalized.map((item, index) => (
                                            <div
                                                key={index}
                                                className={
                                                    `trade-in-item ${selectedSellItems[index]
                                                        ? "selected"
                                                        : ""
                                                    }`
                                                }
                                                onClick={() => {
                                                    setSelectedSellItems(prev => {
                                                        const next = { ...prev };
                                                        if (next[index]) {
                                                            delete next[index];
                                                        }
                                                        else {
                                                            next[index] = item.quantity || 1;
                                                        }
                                                        return next;
                                                    });
                                                }}
                                            >
                                                <div className="tii-info">
                                                    <span className="tii-name">
                                                        {item.name}
                                                        {item.quantity > 1 && ` ×${item.quantity}`}
                                                    </span>
                                                    <span className="tii-rarity">
                                                        {item.rarity} • {item.category}
                                                    </span>
                                                </div>
                                                <div className="tii-value">
                                                    {item.quantity > 1 && (
                                                        <>
                                                            <button
                                                                type="button"
                                                                className="sell-quantity-btn"
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    setSelectedSellItems(prev => {
                                                                        const next = { ...prev };
                                                                        if (!next[index]) {
                                                                            next[index] = item.quantity;
                                                                        }
                                                                        next[index] = Math.max(
                                                                            1,
                                                                            next[index] - 1
                                                                        );
                                                                        return next;
                                                                    });
                                                                }}
                                                            >
                                                                -
                                                            </button>
                                                            <input
                                                                className="sell-quantity-input"
                                                                type="number"
                                                                min="1"
                                                                max={item.quantity}
                                                                value={
                                                                    selectedSellItems[index] || item.quantity
                                                                }
                                                                onClick={(e) => e.stopPropagation()}
                                                                onChange={(e) => {
                                                                    const value = Math.min(
                                                                        item.quantity,
                                                                        Math.max(1, Number(e.target.value))
                                                                    );
                                                                    setSelectedSellItems(prev => ({
                                                                        ...prev,
                                                                        [index]: value
                                                                    }));
                                                                }}
                                                            />
                                                            <button
                                                                type="button"
                                                                className="sell-quantity-btn"
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    setSelectedSellItems(prev => {
                                                                        const next = { ...prev };
                                                                        if (!next[index]) {
                                                                            next[index] = item.quantity;
                                                                        }
                                                                        next[index] = Math.min(
                                                                            item.quantity,
                                                                            next[index] + 1
                                                                        );
                                                                        return next;
                                                                    });
                                                                }}
                                                            >
                                                                +
                                                            </button>
                                                        </>
                                                    )}
                                                    +{
                                                        Math.floor(
                                                            (sellPrices[index] / (item.quantity || 1))
                                                            *
                                                            (selectedSellItems[index] || item.quantity || 1)
                                                        )
                                                    } gp
                                                </div>
                                            </div>
                                        ))
                                    }
                                </div>
                                <div className="shop-gold-summary">
                                    <div className="sgs-row">
                                        <span>
                                            Total:
                                        </span>
                                        <span>
                                            {total}
                                            <i className="fa-solid fa-coins" />
                                        </span>
                                    </div>
                                </div>
                                <div className="shop-modal-actions">
                                    <button
                                        className="confirm-btn gold"
                                        disabled={Object.keys(selectedSellItems).length === 0}
                                        onClick={handleSellItems}
                                    >
                                        <i className="fa-solid fa-hand-holding-dollar"></i>
                                        Confirm Sale
                                    </button>
                                    <button
                                        className="close-modal"
                                        onClick={() => {
                                            setShowSellModal(false)
                                            setSelectedSellItems({})
                                        }}
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })()}
            {levelUpReveal && (
                <div className="modal-overlay level-up-reveal-overlay">
                    <div className="level-up-reveal-card animated fadeIn">
                        <div className="reveal-sparkles"></div>
                        <div className="reveal-content">
                            <span className="reveal-subtitle">Achievement Unlocked</span>
                            <h2 className="reveal-title">LEVEL UP!</h2>
                            <div className="reveal-char-info">
                                <p className="reveal-name">{levelUpReveal.name}</p>
                                <p className="reveal-level">Reached Level {levelUpReveal.level}</p>
                            </div>
                            <p className="reveal-desc">New features and Greater Power await in your character sheet.</p>
                            <div className="reveal-actions">
                                <button className="reveal-confirm-btn" onClick={() => navigate(`/characters/${levelUpReveal.id}/edit`)}>
                                    Update Character Now
                                </button>
                                <button className="reveal-dismiss-btn" onClick={handleDismissLevelUpReveal}>
                                    Dismiss
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
            <BackToTop containerSelector=".session-content" />
        </div>
    );
};

export default HostedRunPage;
