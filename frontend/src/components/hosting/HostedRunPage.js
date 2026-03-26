import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/HostedRunPage.css';

const HostedRunPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user: currentUser, token } = useAuth();
    
    const [userCharacters, setUserCharacters] = useState([]);
    const [showCharPicker, setShowCharPicker] = useState(false);
    const [session, setSession] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [activeTab, setActiveTab] = useState('trial');
    const [isEditingTitle, setIsEditingTitle] = useState(false);
    const [runTitleInput, setRunTitleInput] = useState('');
    const [expandedEncounters, setExpandedEncounters] = useState({});
    const [wildSurgeVisible, setWildSurgeVisible] = useState({});

    const fetchSessionDetails = useCallback(async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/host/details/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Failed to fetch session details');
            const data = await response.json();
            setSession(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [id, token]);

    const fetchUserCharacters = useCallback(async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/characters', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setUserCharacters(data);
            }
        } catch (err) {
            console.error('Failed to fetch characters:', err);
        }
    }, [token]);

    useEffect(() => {
        fetchSessionDetails();
        fetchUserCharacters();
        const interval = setInterval(fetchSessionDetails, 5000); // Polling every 5s
        return () => clearInterval(interval);
    }, [fetchSessionDetails, fetchUserCharacters]);

    const handleLinkCharacter = async (charId) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/host/${id}/link-character`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ character_id: charId })
            });
            if (!response.ok) throw new Error('Failed to link character');
            setShowCharPicker(false);
            fetchSessionDetails();
        } catch (err) {
            alert(err.message);
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
            const response = await fetch(`http://127.0.0.1:5000/api/host/${id}/rename`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title: runTitleInput.trim() })
            });
            if (!response.ok) throw new Error('Failed to rename run');
            setIsEditingTitle(false);
            fetchSessionDetails();
        } catch (err) {
            alert(err.message);
        }
    };

    const handleCompleteEncounter = async (num) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/host/${id}/complete-encounter`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ encounter_num: num })
            });
            if (response.ok) fetchSessionDetails();
        } catch (err) {
            alert(err.message);
        }
    };

    const handleClaimItem = async (index) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/host/${id}/claim-item`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ item_index: index })
            });
            if (response.ok) fetchSessionDetails();
        } catch (err) {
            alert(err.message);
        }
    };

    const toggleEncounter = (num) => {
        setExpandedEncounters(prev => ({ ...prev, [num]: !prev[num] }));
    };

    const toggleWildSurge = (e, num) => {
        e.stopPropagation();
        setWildSurgeVisible(prev => ({ ...prev, [num]: !prev[num] }));
    };

    const renderEncounterContent = (num, encounter) => {
        if (encounter.type === "Shop Encounter") {
            return (
                <div className="encounter-details">
                    <div className="detail-section highlight">
                        <h4><i className="fa-solid fa-gem"></i> Item Rarity Mix</h4>
                        <div className="rarity-grid">
                            {Object.entries(encounter.rarity_mix).map(([rarity, count]) => (
                                <div key={rarity} className={`rarity-tag ${rarity.toLowerCase()}`}>
                                    {rarity}: {count}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="detail-section">
                        <h4><i className="fa-solid fa-shop"></i> Shop Inventory</h4>
                        {Object.entries(encounter.items_by_category).map(([category, items]) => (
                            <div key={category} className="item-category">
                                <h5>{category}</h5>
                                <ul>
                                    {items.map((item, idx) => <li key={idx}>{item}</li>)}
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
                            {encounter.magic_items.map((item, i) => <li key={i}>{item}</li>)}
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
    if (error) return <div className="hosted-page-container"><div className="error-card">{error}</div></div>;
    if (!session) return null;

    const isDM = currentUser.id === session.dm_id;

    return (
        <div className="hosted-page-container">
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
                            {isDM && (
                                <button className="edit-title-btn" onClick={startEditingTitle} title="Rename Run">
                                    <i className="fa-solid fa-pen-to-square"></i>
                                </button>
                            )}
                        </h1>
                    )}
                    <div className="invite-badge">
                        CODE: <span>{session.invite_code}</span>
                    </div>
                </div>
                
                <nav className="session-tabs">
                    <button className={activeTab === 'trial' ? 'active' : ''} onClick={() => setActiveTab('trial')}>Trial</button>
                    <button className={activeTab === 'party' ? 'active' : ''} onClick={() => setActiveTab('party')}>Party</button>
                    <button className={activeTab === 'inventory' ? 'active' : ''} onClick={() => setActiveTab('inventory')}>Vault</button>
                </nav>
            </header>

            <main className="session-content">
                {activeTab === 'trial' && (
                    <div className="trial-view">
                        <section className="blessing-banner">
                            <h3>Divine Blessing: {session.run.data.divine_blessing?.name}</h3>
                            <p>{session.run.data.divine_blessing?.blessing}</p>
                        </section>

                        {!isDM && (
                            <div className="player-info-note">
                                <i className="fa-solid fa-circle-info"></i>
                                Completed trial encounters and their rewards will appear below as you progress.
                            </div>
                        )}
                        
                        <div className="encounters-timeline">
                            {session.run.data.encounters
                                .filter(([num, enc]) => isDM || session.completed_encounters.includes(String(num)))
                                .map(([num, enc]) => (
                                    <div key={num} className={`timeline-node ${expandedEncounters[num] ? 'expanded' : ''}`} onClick={() => toggleEncounter(num)}>
                                        <div className="node-header">
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
                                                    style={session.completed_encounters.includes(String(num)) ? {background: 'var(--success)', color: 'white'} : {}}
                                                >
                                                    <i className="fa-solid fa-check"></i>
                                                </button>
                                            )}
                                        </div>
                                        {expandedEncounters[num] && renderEncounterContent(num, enc)}
                                    </div>
                                ))}
                        </div>
                    </div>
                )}

                {activeTab === 'party' && (
                    <div className="party-view">
                        <div className="participants-grid">
                            {session.participants.map(p => (
                                <div key={p.user_id} className={`participant-card ${p.role === 'DM' ? 'dm' : ''}`}>
                                    <div className="p-header">
                                        <div className="p-avatar">
                                            {p.username.substring(0,2).toUpperCase()}
                                        </div>
                                        <div className="p-names">
                                            <strong>{p.username}</strong>
                                            <span>{p.role}</span>
                                        </div>
                                    </div>
                                    {p.character ? (
                                        <div className="p-char-preview">
                                            <p className="char-name">{p.character.name}</p>
                                            <p className="char-stats">Level {p.character.level || p.character.data?.level} {p.character.class_name || p.character.data?.class_name}</p>
                                            <div className="hp-bar">
                                                <div className="hp-fill" style={{width: `${((p.character.data?.hp_current || 0) / ((p.character.data?.hp_max_base || 1) + (p.character.data?.hp_modifier || 0))) * 100}%`}}></div>
                                                <span>HP: {p.character.data?.hp_current || 0}/{ (p.character.data?.hp_max_base || 0) + (p.character.data?.hp_modifier || 0) }</span>
                                            </div>
                                            <button className="view-sheet-btn" onClick={() => navigate(`/characters/${p.character.id}`)}>
                                                View Sheet
                                            </button>
                                        </div>
                                    ) : (
                                        <div className="p-char-missing">
                                            {p.user_id === currentUser.id ? (
                                                <button className="pick-char-btn" onClick={() => setShowCharPicker(true)}>Pick Character</button>
                                            ) : (
                                                <p>Choosing character...</p>
                                            )}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === 'inventory' && (
                    <div className="inventory-view">
                        <h3>Party Vault</h3>
                        <div className="vault-grid">
                            {session.party_inventory.length > 0 ? (
                                session.party_inventory.map((item, idx) => (
                                    <div key={idx} className="vault-item">
                                        <span>{item}</span>
                                        <button className="claim-btn" onClick={() => handleClaimItem(idx)}>Claim</button>
                                    </div>
                                ))
                            ) : (
                                <div className="empty-vault">
                                    <p>The vault is empty. Complete encounters to find rewards.</p>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </main>

            {showCharPicker && (
                <div className="modal-overlay">
                    <div className="char-picker-modal">
                        <h2>Select Your Champion</h2>
                        <div className="char-list">
                            {userCharacters.map(char => (
                                <div key={char.id} className="char-option" onClick={() => handleLinkCharacter(char.id)}>
                                    <strong>{char.name}</strong>
                                    <span>Level {char.level} {char.class_name}</span>
                                </div>
                            ))}
                            {userCharacters.length === 0 && <p>No characters found. Create one first!</p>}
                        </div>
                        <button className="close-modal" onClick={() => setShowCharPicker(false)}>Cancel</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HostedRunPage;
