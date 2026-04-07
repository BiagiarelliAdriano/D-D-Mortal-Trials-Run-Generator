import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import BackToTop from './common/BackToTop';
import '../styles/RunGenerator.css';

const RunGenerator = () => {
    const { token } = useAuth();
    const location = useLocation();
    const [runData, setRunData] = useState(location.state?.savedRunData || null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [expandedEncounters, setExpandedEncounters] = useState({});
    const [wildSurgeVisible, setWildSurgeVisible] = useState({});
    const navigate = useNavigate();

    // Reset expanded states if a saved run is loaded
    useEffect(() => {
        if (location.state?.savedRunData) {
            setRunData(location.state.savedRunData);
            setExpandedEncounters({ 1: true, 2: true, 3: true });
        }
    }, [location.state]);

    const generateRun = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('/api/run/generate');
            if (!response.ok) throw new Error('Failed to generate run');
            const data = await response.json();
            setRunData(data);
            // Auto-expand first 3 encounters for better UX
            setExpandedEncounters({ 1: true, 2: true, 3: true });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const toggleEncounter = (id) => {
        setExpandedEncounters(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const toggleWildSurge = (e, id) => {
        e.stopPropagation();
        setWildSurgeVisible(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const renderEncounterContent = (id, encounter) => {
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
                            className={`wild-surge-toggle ${wildSurgeVisible[id] ? 'active' : ''}`}
                            onClick={(e) => toggleWildSurge(e, id)}
                        >
                            <i className="fa-solid fa-bolt"></i> {encounter.wild_surge.name}
                        </button>
                        {wildSurgeVisible[id] && (
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

    const handlePrint = () => {
        // Save current expanded state
        const originalExpanded = { ...expandedEncounters };
        const originalWildSurge = { ...wildSurgeVisible };

        // Expand everything for print
        const allExpanded = {};
        const allWildSurge = {};
        runData.encounters.forEach(([num]) => {
            allExpanded[num] = true;
            allWildSurge[num] = true;
        });

        setExpandedEncounters(allExpanded);
        setWildSurgeVisible(allWildSurge);

        // Wait for state to apply and DOM to render
        setTimeout(() => {
            window.print();
            // Restore original state
            setExpandedEncounters(originalExpanded);
            setWildSurgeVisible(originalWildSurge);
        }, 500);
    };

    const saveRun = async (silent = false) => {
        let title = "";
        if (!silent) {
            title = prompt("Enter a name for this Run (max 24 characters):");
            if (title === null) return null; // Cancelled
            if (title.length > 24) {
                alert("Run name must be 24 characters or less. Truncating to 24 characters.");
                title = title.substring(0, 24);
            }
            const now = new Date();
            if (!title.trim()) {
                title = `Trial ${now.toLocaleDateString()} ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
            }
        } else {
            const now = new Date();
            title = `Trial ${now.toLocaleDateString()} ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
        }

        try {
            const response = await fetch('/api/runs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : ''
                },
                body: JSON.stringify({
                    title,
                    data: runData
                })
            });

            if (!response.ok) throw new Error('Failed to save run');
            const result = await response.json();
            if (!silent) alert('Run saved successfully!');
            return result.id;
        } catch (err) {
            alert('Error saving run: ' + err.message);
            return null;
        }
    };

    const handleStartHosting = async () => {
        setLoading(true);
        try {
            // 1. Save the run first to get a run_id
            const runId = await saveRun(true);
            if (!runId) return;

            // 2. Create the hosted session
            const response = await fetch('/api/host/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ run_id: runId })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to create host session');

            // 3. Navigate to the session page
            navigate(`/hosting/${data.session_id}`);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const isHostMode = new URLSearchParams(location.search).get('host') === 'true';

    return (
        <div className="generator-container">
            <header className="generator-header">
                <div className="nav-group">
                    <button className="back-btn" onClick={() => navigate('/')}>
                        <i className="fa-solid fa-arrow-left"></i> Home
                    </button>
                    {token && (
                        <button className="back-btn secondary" onClick={() => navigate('/saved-runs')}>
                            <i className="fa-solid fa-list-ul"></i> My Saved Runs
                        </button>
                    )}
                </div>
                <h1 className="serif-text">Run Generator</h1>
                <div className="header-actions">
                    <button className="action-btn primary" onClick={generateRun} disabled={loading}>
                        {loading ? <i className="fa-solid fa-spinner fa-spin"></i> : <i className="fa-solid fa-dice"></i>}
                        {runData ? 'Generate New Run' : 'Generate Run'}
                    </button>
                    {runData && (
                        <>
                            {token && (
                                isHostMode ? (
                                    <button className="action-btn host-btn" onClick={handleStartHosting} disabled={loading}>
                                        <i className="fa-solid fa-tower-observation"></i> Start Hosting Trial
                                    </button>
                                ) : (
                                    <button className="action-btn success" onClick={() => saveRun()}>
                                        <i className="fa-solid fa-floppy-disk"></i> Save Run
                                    </button>
                                )
                            )}
                            <button className="action-btn secondary" onClick={handlePrint}>
                                <i className="fa-solid fa-print"></i> Print / Download Run
                            </button>
                        </>
                    )}
                </div>
            </header>

            {error && <div className="error-message">{error}</div>}

            {!runData && !loading && (
                <div className="empty-state">
                    <i className="fa-solid fa-scroll"></i>
                    <p>Begin your trial. Generate a new run to see your destiny.</p>
                </div>
            )}

            {runData && (
                <main className="run-results">
                    {runData.divine_blessing && (
                        <section className={`blessing-card blessing-${runData.divine_blessing.name.toLowerCase().replace(/\s+/g, '-')}`}>
                            <div className="blessing-icon">
                                <i className="fa-solid fa-sun"></i>
                            </div>
                            <div className="blessing-content">
                                <h2>Divine Blessing: {runData.divine_blessing.name}</h2>
                                <p className="blessing-title"><em>{runData.divine_blessing.title}</em></p>
                                <p className="blessing-desc">{runData.divine_blessing.description}</p>
                                <div className="blessing-effect">
                                    <strong>Grace:</strong> {runData.divine_blessing.blessing}
                                </div>
                            </div>
                        </section>
                    )}

                    <div className="encounters-list">
                        {runData.encounters.map(([num, encounter]) => (
                            <div
                                key={num}
                                className={`encounter-card ${expandedEncounters[num] ? 'expanded' : ''} ${encounter.type === "Shop Encounter" ? 'shop' : 'combat'}`}
                                onClick={() => toggleEncounter(num)}
                            >
                                <div className="encounter-header">
                                    <div className="encounter-num">{num}</div>
                                    <h3>{encounter.type || `Encounter ${num}`}</h3>
                                    <div className="expand-icon">
                                        <i className={`fa-solid fa-chevron-${expandedEncounters[num] ? 'up' : 'down'}`}></i>
                                    </div>
                                </div>
                                {expandedEncounters[num] && renderEncounterContent(num, encounter)}
                            </div>
                        ))}
                    </div>
                </main>
            )}
            <BackToTop />
        </div>
    );
};

export default RunGenerator;
