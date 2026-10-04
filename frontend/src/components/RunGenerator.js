import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import BackToTop from './common/BackToTop';
import UserProfilePill from './UserProfilePill';
import '../styles/RunGenerator.css';
import API_BASE_URL from '../config';

const RunGenerator = () => {
    const {
        token,
        autoSaveGeneratedRuns,
        toggleAutoSaveGeneratedRuns
    } = useAuth();
    const { addAlert, prompt } = useNotification();
    const location = useLocation();
    const [runData, setRunData] = useState(location.state?.savedRunData || null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [generationLimit, setGenerationLimit] = useState(null);
    const [resetDate, setResetDate] = useState(null);
    const [unlimitedAccess, setUnlimitedAccess] = useState(false);
    const [timeUntilReset, setTimeUntilReset] = useState(null);
    const [expandedEncounters, setExpandedEncounters] = useState({});
    const [wildSurgeVisible, setWildSurgeVisible] = useState({});
    const [wildSurgesExpanded, setWildSurgesExpanded] = useState(false);
    const [selectedMode, setSelectedMode] = useState('mortal_trials');
    // Host-mode saved run picker
    const [selectedSavedRunId, setSelectedSavedRunId] = useState(null);
    const [savedRuns, setSavedRuns] = useState([]);
    const [savedRunsLoading, setSavedRunsLoading] = useState(false);
    const [showSavedRunPicker, setShowSavedRunPicker] = useState(false);
    const navigate = useNavigate();

    // Reset expanded states if a saved run is loaded
    useEffect(() => {
        if (location.state?.savedRunData) {
            setRunData(location.state.savedRunData);
            setExpandedEncounters({ 1: true, 2: true, 3: true });
        }
    }, [location.state]);

    useEffect(() => {
        const runId = new URLSearchParams(location.search).get('runId');
        if (!runId || location.state?.savedRunData || !token) return;

        const fetchSavedRun = async () => {
            setLoading(true);
            try {
                const response = await fetch(`${API_BASE_URL}/api/runs/${runId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Failed to load saved run');
                setRunData(data.data);
                setExpandedEncounters({ 1: true, 2: true, 3: true });
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchSavedRun();
    }, [location.search, location.state, token]);

    useEffect(() => {
        // No countdown is needed for unlimited users.
        if (unlimitedAccess || !resetDate) {
            setTimeUntilReset(null);
            return;
        }

        const updateCountdown = () => {
            const now = new Date();

            // The backend gives us the date on which the daily limit resets.
            // The reset happens at the start of that date.
            const reset = new Date(`${resetDate}T00:00:00Z`);
            let difference = reset.getTime() - now.getTime();

            // If the reset date has already passed, the next reset is tomorrow.
            if (difference <= 0) {
                const nextReset = new Date(reset);
                nextReset.setDate(nextReset.getDate() + 1);
                difference = nextReset.getTime() - now.getTime();
            }
            const totalSeconds = Math.max(0, Math.floor(difference / 1000));
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;
            setTimeUntilReset({
                hours,
                minutes,
                seconds
            });
        };

        // Calculate immediately instead of waiting one second.
        updateCountdown();

        // Keep the countdown updated every second.
        const timer = setInterval(updateCountdown, 1000);

        // Clean up the interval when the component unmounts
        // or when the reset date/access level changes.
        return () => clearInterval(timer);
    }, [resetDate, unlimitedAccess]);

    // Fetch daily run limit status on mount
    useEffect(() => {
        if (!token) return;
        const fetchStatus = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/run/status`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    setUnlimitedAccess(data.unlimited_access);
                    setResetDate(data.reset_date);
                    setGenerationLimit({
                        remaining: data.generations_remaining,
                        dailyLimit: data.daily_limit,
                        unlimited: data.unlimited_access,
                        resetDate: data.reset_date
                    });
                }
            } catch (err) {
                console.error('Failed to fetch run status:', err);
            }
        };
        fetchStatus();
    }, [token]);

    const isHostMode = new URLSearchParams(location.search).get('host') === 'true';

    // In host mode, fetch the user's saved runs so they can pick one to host
    const fetchSavedRuns = async () => {
        if (!token) return;
        setSavedRunsLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/runs`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setSavedRuns(data);
            }
        } catch (err) {
            console.error('Failed to fetch saved runs:', err);
        } finally {
            setSavedRunsLoading(false);
        }
    };

    // When in host mode and limit is known, pre-load saved runs for the picker
    useEffect(() => {
        if (isHostMode && token) {
            fetchSavedRuns();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isHostMode, token]);

    const handlePickSavedRun = (run) => {
        setSelectedSavedRunId(run.id);
        setRunData(run.data);
        setExpandedEncounters({ 1: true, 2: true, 3: true });
        setShowSavedRunPicker(false);
        setError(null);
    };

    const generateRun = async () => {
        // ── Guest path: allow one free run per browser session ────────────────
        if (!token) {
            const alreadyUsed = sessionStorage.getItem('guest_run_used') === 'true';
            if (alreadyUsed) {
                addAlert(
                    'You\'ve used your free preview run! Create a free account to get 3 runs per day, save your trials, and more.',
                    'info'
                );
                return;
            }
        }

        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/api/run/generate?mode=${encodeURIComponent(selectedMode)}`, {
                method: 'GET',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });
            const data = await response.json();
            if (!response.ok) {
                const error = new Error(data.error || 'Failed to generate run');
                error.responseData = data;
                throw error;
            }
            setRunData(data);

            // If this was a guest generation, mark it used and show the upsell
            if (!token) {
                sessionStorage.setItem('guest_run_used', 'true');
                setGenerationLimit({ remaining: 0, dailyLimit: 1, unlimited: false, resetDate: null });
            }

            // Store the current Run generation limit information.
            setUnlimitedAccess(data.unlimited_access);
            setResetDate(data.reset_date);

            setGenerationLimit({
                remaining: data.generations_remaining,
                dailyLimit: data.daily_limit,
                unlimited: data.unlimited_access,
                resetDate: data.reset_date
            });

            // Auto-expand first 3 encounters for better UX
            setExpandedEncounters({ 1: true, 2: true, 3: true });
        } catch (err) {
            setError(err.message);

            // If the daily generation limit was reached,
            // refresh the limit information from the backend response.
            if (err.responseData) {
                setGenerationLimit({
                    remaining: err.responseData.generations_remaining,
                    dailyLimit: err.responseData.daily_limit,
                    unlimited: err.responseData.unlimited_access,
                    resetDate: err.responseData.reset_date
                });
            }
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

    const getDisplayItemName = (item) => {
        if (!item) return 'No item';
        if (typeof item === 'string') return item;
        if (typeof item.name === 'string') return item.name;
        if (item.name && typeof item.name === 'object' && typeof item.name.name === 'string') return item.name.name;
        return 'Unknown item';
    };

    const groupCycleMonsters = (monsters) => {
        const groups = [];
        monsters.forEach(monster => {
            const encounterNumber = monster.encounter_number ?? 1;
            let group = groups[groups.length - 1];
            if (!group || group.encounterNumber !== encounterNumber) {
                group = { encounterNumber, monsters: [] };
                groups.push(group);
            }
            group.monsters.push(monster);
        });
        return groups;
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
                            {encounter.monsters.map((m, i) => <li key={i}>{typeof m === 'string' ? m : `${m.name} — ${m.cr} CR — ${m.xp} XP — ${m.gold}g — ${m.item?.name || 'No item'}`}</li>)}
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
        if (!runData) return;

        const originalExpanded = { ...expandedEncounters };
        const originalWildSurge = { ...wildSurgeVisible };

        if (runData.encounters) {
            const allExpanded = {};
            const allWildSurge = {};
            runData.encounters.forEach(([num]) => {
                allExpanded[num] = true;
                allWildSurge[num] = true;
            });

            setExpandedEncounters(allExpanded);
            setWildSurgeVisible(allWildSurge);
        }

        setTimeout(() => {
            window.print();
            setExpandedEncounters(originalExpanded);
            setWildSurgeVisible(originalWildSurge);
        }, 500);
    };

    const saveRun = async (silent = false) => {
        let title = "";

        if (!silent) {
            title = await prompt("Enter a name for this Run (max 24 characters):");
            if (!title) return null; // Cancelled or empty

            if (title.length > 24) {
                addAlert(
                    "Run name must be 24 characters or less. Truncating to 24 characters.",
                    "warning"
                );
                title = title.substring(0, 24);
            }

            const now = new Date();

            if (!title.trim()) {
                title = `Trial ${now.toLocaleDateString()} ${now.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                })}`;
            }
        } else {
            const now = new Date();

            title = `Trial ${now.toLocaleDateString()} ${now.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            })}`;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/runs`, {
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

            const data = await response.json();

            if (response.ok) {
                if (!silent) addAlert('Run saved successfully!', 'success');
                return data.id;
            } else {
                addAlert(
                    'Error saving run: ' + (data.error || 'Unknown error'),
                    'error'
                );
                return null;
            }
        } catch (err) {
            addAlert('Error saving run: ' + err.message, 'error');
            return null;
        }
    };

    const handleStartHosting = async () => {
        setLoading(true);
        try {
            let runId;

            if (selectedSavedRunId) {
                // User picked an existing saved run — no need to save a new copy
                runId = selectedSavedRunId;
            } else {
                // Freshly generated run — save it first to get an ID
                runId = await saveRun(true);
                if (!runId) return;
            }

            // Create the hosted session
            const response = await fetch(`${API_BASE_URL}/api/host/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ run_id: runId })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to create host session');

            // Navigate to the session page
            navigate(`/hosting/${data.session_id}`);
        } catch (err) {
            setError(err.message);
            addAlert(err.message, 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="generator-container">
            <header className="generator-header">
                <div className="nav-group">
                    <button className="back-btn" onClick={() => navigate(-1)}>
                        <i className="fa-solid fa-arrow-left"></i> Back
                    </button>
                    {token && (
                        <button className="back-btn secondary" onClick={() => navigate('/saved-runs')}>
                            <i className="fa-solid fa-list-ul"></i> My Saved Runs
                        </button>
                    )}

                    {token && (
                        <button
                            className={`auto-save-btn ${autoSaveGeneratedRuns ? 'active' : ''}`}
                            onClick={async () => {
                                const newValue = !autoSaveGeneratedRuns;

                                try {
                                    await toggleAutoSaveGeneratedRuns();

                                    addAlert(
                                        newValue
                                            ? 'Auto-save generated Runs enabled.'
                                            : 'Auto-save generated Runs disabled.',
                                        'success'
                                    );
                                } catch (err) {
                                    addAlert(
                                        'Could not update auto-save preference.',
                                        'error'
                                    );
                                }
                            }}
                            title={
                                autoSaveGeneratedRuns
                                    ? 'Automatically save generated Runs - ON'
                                    : 'Automatically save generated Runs - OFF'
                            }
                        >
                            <i className={"fa-solid fa-floppy-disk"}></i>
                            Auto-save Generated Runs
                            <span className="auto-save-status">
                                {autoSaveGeneratedRuns ? 'ON' : 'OFF'}
                            </span>
                        </button>
                    )}
                </div>
                <h1 className="serif-text">Run Generator</h1>
                <div className="header-actions">
                    <button
                        className="action-btn primary"
                        onClick={generateRun}
                        disabled={loading || (generationLimit && !generationLimit.unlimited && generationLimit.remaining <= 0)}
                    >
                        {loading ? <i className="fa-solid fa-spinner fa-spin"></i> : <i className="fa-solid fa-dice"></i>}
                        {generationLimit &&
                            generationLimit.remaining <= 0 &&
                            !generationLimit.unlimited
                            ? (!token ? 'Free Preview Used' : 'Daily Limit Reached')
                            : runData
                                ? 'Generate New Run'
                                : 'Generate Run'
                        }
                    </button>
                    {/* In host mode, offer the option to pick a saved run instead */}
                    {isHostMode && token && (
                        <button
                            className="action-btn saved-run-pick-btn"
                            onClick={() => setShowSavedRunPicker(v => !v)}
                            disabled={loading}
                            title="Use one of your saved runs to start hosting"
                        >
                            <i className="fa-solid fa-list-ul"></i>
                            {showSavedRunPicker ? 'Hide Saved Runs' : 'Use a Saved Run'}
                        </button>
                    )}
                    <UserProfilePill />
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

            <div className="mode-selector-panel">
                <div className="mode-selector-header">
                    <span className="mode-selector-label">Game Mode</span>
                </div>
                <div className="mode-toggle-group" role="tablist" aria-label="Run mode selector">
                    <button
                        type="button"
                        className={`mode-toggle-btn ${selectedMode === 'mortal_trials' ? 'active' : ''}`}
                        onClick={() => setSelectedMode('mortal_trials')}
                    >
                        <span className="mode-title">The Mortal Trials</span>
                        <span className="mode-subtitle">Classic progression</span>
                    </button>
                    <button
                        type="button"
                        className={`mode-toggle-btn ${selectedMode === 'endless_trials' ? 'active' : ''}`}
                        onClick={() => setSelectedMode('endless_trials')}
                    >
                        <span className="mode-title">The Endless Trials</span>
                        <span className="mode-subtitle">Endless waves • stacked hazards</span>
                    </button>
                </div>
            </div>

            {generationLimit && !generationLimit.unlimited && (
                <div className="generation-limit-bar">
                    <div className="generation-limit-info">
                        <i className="fa-solid fa-dice"></i>
                        <span>
                            {!token
                                ? <><strong>Free preview</strong> — 1 run per session</>
                                : <><strong>{generationLimit.remaining}</strong> of {generationLimit.dailyLimit} Run generations remaining today</>
                            }
                        </span>
                    </div>
                    {generationLimit.resetDate && timeUntilReset && (
                        <div className="generation-limit-reset">
                            <i className="fa-solid fa-clock"></i>
                            {generationLimit.remaining <= 0 ? (
                                <span>
                                    New Runs available in{' '}
                                    <strong>
                                        {String(timeUntilReset.hours).padStart(2, '0')}:
                                        {String(timeUntilReset.minutes).padStart(2, '0')}:
                                        {String(timeUntilReset.seconds).padStart(2, '0')}
                                    </strong>
                                </span>
                            ) : (
                                <span>
                                    Limit resets in{' '}
                                    <strong>
                                        {String(timeUntilReset.hours).padStart(2, '0')}:
                                        {String(timeUntilReset.minutes).padStart(2, '0')}:
                                        {String(timeUntilReset.seconds).padStart(2, '0')}
                                    </strong>
                                </span>
                            )}
                        </div>
                    )}
                </div>
            )}

            {/* Guest upsell banner — shown after the free preview run is used */}
            {!token && generationLimit && generationLimit.remaining <= 0 && (
                <div className="guest-upsell-banner">
                    <div className="guest-upsell-icon">
                        <i className="fa-solid fa-tower-observation"></i>
                    </div>
                    <div className="guest-upsell-content">
                        <strong>Want more trials?</strong>
                        <p>
                            Create a free account to get <strong>3 runs per day</strong>, save your favourite trials, build characters, and join Hosted Runs — or subscribe to our Patreon for unlimited access!
                        </p>
                    </div>
                    <div className="guest-upsell-actions">
                        <button className="action-btn primary" onClick={() => navigate('/register')}>
                            <i className="fa-solid fa-user-plus"></i> Create Free Account
                        </button>
                        <button className="action-btn secondary" onClick={() => navigate('/login')}>
                            <i className="fa-solid fa-right-to-bracket"></i> Log In
                        </button>
                    </div>
                </div>
            )}

            {/* Saved run picker panel (host mode only) */}
            {isHostMode && showSavedRunPicker && (
                <div className="saved-run-picker">
                    <div className="saved-run-picker-header">
                        <h2 className="serif-text">
                            <i className="fa-solid fa-scroll"></i> Choose a Saved Trial to Host
                        </h2>
                        <p>Select one of your saved runs below. It will be loaded as the run for your new Hosted Trial.</p>
                    </div>
                    {savedRunsLoading ? (
                        <div className="saved-run-picker-loading">
                            <i className="fa-solid fa-spinner fa-spin"></i>
                            <span>Retrieving your trials...</span>
                        </div>
                    ) : savedRuns.length === 0 ? (
                        <div className="saved-run-picker-empty">
                            <i className="fa-solid fa-box-open"></i>
                            <p>You have no saved runs yet. Generate a run first to save it.</p>
                        </div>
                    ) : (
                        <div className="saved-run-picker-grid">
                            {savedRuns.map(run => (
                                <button
                                    key={run.id}
                                    className={`saved-run-picker-card ${selectedSavedRunId === run.id ? 'selected' : ''}`}
                                    onClick={() => handlePickSavedRun(run)}
                                >
                                    <div className="picker-card-title">
                                        <i className="fa-solid fa-scroll"></i>
                                        <span>{run.title}</span>
                                        {selectedSavedRunId === run.id && (
                                            <i className="fa-solid fa-circle-check picker-selected-icon"></i>
                                        )}
                                    </div>
                                    <div className="picker-card-meta">
                                        <span>
                                            <i className="fa-solid fa-calendar-days"></i>{' '}
                                            {new Date(run.created_at).toLocaleDateString()}
                                        </span>
                                        <span>
                                            <i className="fa-solid fa-skull"></i>{' '}
                                            {run.data.mode === 'The Endless Trials' ? `${run.data.total_cycles || run.data.cycles?.length || 4} Cycles` : `${run.data.encounters?.length || 0} Encounters`}
                                        </span>
                                        {run.data.divine_blessing && (
                                            <span>
                                                <i className="fa-solid fa-sun"></i>{' '}
                                                {run.data.divine_blessing.name}
                                            </span>
                                        )}
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {!runData && !loading && !showSavedRunPicker && (
                <div className="generator-empty-state">
                    <i className="fa-solid fa-scroll"></i>
                    <p>
                        {isHostMode
                            ? 'Generate a new run or choose a saved run above to begin hosting your trial.'
                            : 'Begin your trial. Generate a new run to see your destiny.'
                        }
                    </p>
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

                    {runData.mode === 'The Endless Trials' ? (
                        <div className="endless-trials-results">
                            <div className="endless-trials-summary">
                                <div className="summary-badge">{runData.mode}</div>
                            </div>

                            {runData.wild_surges && (
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
                                            {runData.wild_surges.map((surge, index) => (
                                                <li key={surge.id || index}>
                                                    <div className="wild-surge-box">
                                                        <button
                                                            className={`wild-surge-toggle ${wildSurgeVisible[`endless-${surge.id || index}`] ? 'active' : ''}`}
                                                            onClick={(e) => toggleWildSurge(e, `endless-${surge.id || index}`)}
                                                            aria-expanded={!!wildSurgeVisible[`endless-${surge.id || index}`]}
                                                        >
                                                            <i className="fa-solid fa-bolt"></i> {surge.name}
                                                        </button>
                                                        {wildSurgeVisible[`endless-${surge.id || index}`] && (
                                                            <div className="wild-surge-content">
                                                                <p><strong>Description:</strong> {surge.description}</p>
                                                                <p className="echo-asc"><strong>Echo Of Ascendance:</strong> {surge["echo of ascendance"]}</p>
                                                                <p className="echo-ruin"><strong>Echo Of Ruin:</strong> {surge["echo of ruin"]}</p>
                                                                <p className="worldshift"><strong>Worldshift Trait:</strong> {surge["worldshift trait"]}</p>
                                                            </div>
                                                        )}
                                                    </div>
                                                </li>
                                            ))}
                                        </ol>
                                    )}
                                </section>
                            )}

                            {runData.cycles.map((cycle) => (
                                <div key={cycle.cycle} className="endless-cycle-card">
                                    <div className="endless-cycle-header">
                                        <h3>{cycle.name}</h3>
                                        {cycle.shop && (
                                            <span className="shop-badge"><i className="fa-solid fa-shop"></i> Shop</span>
                                        )}
                                    </div>

                                    <div className="cycle-rules">
                                        {cycle.rules.map((rule, index) => (
                                            <div key={index} className="rule-line">• {rule}</div>
                                        ))}
                                    </div>

                                    <div className="cycle-encounters">
                                        {groupCycleMonsters(cycle.monsters).map(({ encounterNumber, monsters }) => (
                                            <section key={`${cycle.cycle}-${encounterNumber}`} className="cycle-encounter-group">
                                                <div className="cycle-encounter-heading">
                                                    <h4>Encounter {encounterNumber}</h4>
                                                    {monsters[0]?.encounter_note && (
                                                        <span>{monsters[0].encounter_note}</span>
                                                    )}
                                                </div>
                                                <div className="cycle-monster-list">
                                                    {monsters.map((monster, index) => (
                                                        <div key={`${cycle.cycle}-${encounterNumber}-${index}`} className="cycle-monster-row">
                                                            <span className="monster-name">{monster.name}</span>
                                                            <span className="monster-meta">CR {monster.cr}</span>
                                                            {monster.xp != null && <span className="monster-meta">{monster.xp.toLocaleString()} XP</span>}
                                                            {monster.gold != null && <span className="monster-meta">{monster.gold.toLocaleString()} GP</span>}
                                                            {monster.item && <span className="monster-item">{getDisplayItemName(monster.item)}</span>}
                                                        </div>
                                                    ))}
                                                </div>
                                            </section>
                                        ))}
                                    </div>

                                    {cycle.shop && (
                                        <div className="cycle-shop-box">
                                            <div className="cycle-shop-heading">
                                                <h4><i className="fa-solid fa-shop"></i> Cycle Shop</h4>
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
                                            {Object.entries(cycle.shop.items_by_category).map(([category, items]) => (
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
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
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
                    )}
                </main>
            )}
            <BackToTop />
        </div>
    );
};

export default RunGenerator;
