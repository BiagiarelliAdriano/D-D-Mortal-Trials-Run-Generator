import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useNotification } from '../../context/NotificationContext';
import BackToTop from '../common/BackToTop';
import UserProfilePill from '../UserProfilePill';
import '../../styles/HostHub.css';
import API_BASE_URL from '../../config';

const HostHub = () => {
    const navigate = useNavigate();
    const { token, hasUnlimitedAccess } = useAuth();
    const { addAlert, confirm } = useNotification();
    const [activeGames, setActiveGames] = useState([]);
    const [joinCode, setJoinCode] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [copiedCode, setCopiedCode] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");

    const fetchGames = useCallback(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/active`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Failed to fetch trials');
            const data = await response.json();
            setActiveGames(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [token]);

    useEffect(() => {
        fetchGames();
    }, [fetchGames]);

    // Limit calculations
    const myHostedCount = activeGames.filter(g => g.role === 'DM').length;
    const myJoinedCount = activeGames.filter(g => g.role === 'Ascendant').length;
    const dmLimitReached = !hasUnlimitedAccess && myHostedCount >= 1;
    const joinLimitReached = !hasUnlimitedAccess && myJoinedCount >= 5;

    // Partition and Sort trials with search filtering
    const { myTrials, communityTrials } = useMemo(() => {
        const term = searchTerm.toLowerCase();
        const filtered = activeGames.filter(g =>
            (g.run_title?.toLowerCase() || "").includes(term) ||
            (g.dm_name?.toLowerCase() || "").includes(term)
        );

        const mine = filtered.filter(g => g.role !== 'Visitor');
        const community = filtered.filter(g => g.role === 'Visitor');

        // community already sorted by dm_name from backend, but ensuring here
        community.sort((a, b) => a.dm_name.localeCompare(b.dm_name));

        return { myTrials: mine, communityTrials: community };
    }, [activeGames, searchTerm]);

    const handleJoin = async () => {
        if (joinCode.length !== 6) {
            addAlert('Invite code must be 6 digits', 'error');
            return;
        }

        // If user is already in this game, let them in without limit check
        const alreadyInGame = activeGames.some(g => g.invite_code === joinCode && g.can_enter);
        if (!alreadyInGame && joinLimitReached) {
            addAlert('Free accounts can join up to 5 active Trials as a player. Leave an active trial, or subscribe to Patreon for unlimited access.', 'error');
            return;
        }

        setError('');
        try {
            const response = await fetch(`${API_BASE_URL}/api/host/join`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ invite_code: joinCode })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to join trial');

            addAlert('Joined trial successfully!', 'success');
            navigate(`/hosting/${data.session_id}`);
        } catch (err) {
            setError(err.message);
            addAlert(err.message, 'error');
        }
    };

    const handleLeaveTrial = async (e, sessionId) => {
        e.stopPropagation();
        if (!(await confirm('Are you sure you want to leave this trial?'))) return;

        try {
            const response = await fetch(`${API_BASE_URL}/api/host/${sessionId}/leave`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to leave trial');

            addAlert('Left trial successfully', 'success');
            fetchGames();
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const handleCopyCode = (e, code) => {
        e.stopPropagation();
        navigator.clipboard.writeText(code);
        setCopiedCode(code);
        setTimeout(() => setCopiedCode(null), 2000);
    };

    const renderTrialCard = (game) => (
        <div
            key={game.id}
            className={`trial-card ${!game.can_enter ? 'visitor-card' : ''}`}
            onClick={() => game.can_enter && navigate(`/hosting/${game.id}`)}
        >
            <div className="card-top">
                <div className="role-icon">
                    {game.role === 'DM' ?
                        <i className="fa-solid fa-crown" title="Dungeon Master"></i> :
                        game.role === 'Visitor' ?
                            <i className="fa-solid fa-eye" title="Visitor"></i> :
                            <i className="fa-solid fa-shield-halved" title="Player"></i>
                    }
                </div>
                <div className="trial-title">
                    <h3>{game.run_title}</h3>
                    <span className="owner-name">Hosted by: {game.dm_name}</span>
                </div>
            </div>

            <div className="card-middle">
                <div className="participant-stats">
                    <div className="stat-label">
                        <span><i className="fa-solid fa-users"></i> Party Size</span>
                        <span>{game.participant_count} / 5</span>
                    </div>
                    <div className="party-progress-bar">
                        <div
                            className="party-progress-fill"
                            style={{ width: `${(game.participant_count / 5) * 100}%` }}
                        ></div>
                    </div>
                </div>
            </div>

            <div className="card-bottom">
                {game.can_enter ? (
                    <>
                        <div
                            className={`invite-code-pill ${copiedCode === game.invite_code ? 'copied' : ''}`}
                            onClick={(e) => handleCopyCode(e, game.invite_code)}
                            title="Click to copy code"
                        >
                            <small>{copiedCode === game.invite_code ? 'COPIED!' : 'CODE'}</small>
                            <strong>{game.invite_code}</strong>
                        </div>
                        <div className="card-action-buttons">
                            {game.role === 'Ascendant' && (
                                <button
                                    className="leave-trial-btn"
                                    onClick={(e) => handleLeaveTrial(e, game.id)}
                                    title="Leave Trial"
                                >
                                    <i className="fa-solid fa-right-from-bracket"></i> Leave
                                </button>
                            )}
                            <button className="enter-trial-btn">
                                Enter Spire <i className="fa-solid fa-arrow-right"></i>
                            </button>
                        </div>
                    </>
                ) : (
                    <div className="card-visitor-badge">
                        <i className="fa-solid fa-lock"></i> Requires Participant Code
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div className="host-hub-container">
            <div className="host-hub-card">
                <div className="hub-nav-group">
                    <button className="spire-back-btn" onClick={() => navigate('/')}>
                        <i className="fa-solid fa-house"></i> Home Spire
                    </button>
                    <UserProfilePill />
                </div>
                <div className="host-header">
                    <h1>The Hosting Spire</h1>
                    <p>Manage your trials or join an existing ascent.</p>
                    <div className="search-wrapper" style={{ margin: '20px auto' }}>
                        <input
                            type="text"
                            className="search-input"
                            placeholder="Look for a Run within the Tower..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                        <i className="fa-solid fa-magnifying-glass"></i>
                    </div>
                </div>

                <div className="host-actions">
                    <button
                        className={`host-primary-btn ${dmLimitReached ? 'host-limit-reached' : ''}`}
                        onClick={() => {
                            if (dmLimitReached) {
                                addAlert(
                                    "Free accounts are limited to 1 active Hosted Run as Dungeon Master. Complete or delete your existing session, or subscribe to Patreon for unlimited hosting.",
                                    "error"
                                );
                                return;
                            }
                            navigate('/run-generator?host=true');
                        }}
                    >
                        <i className={dmLimitReached ? "fa-solid fa-lock" : "fa-solid fa-plus-circle"}></i>
                        {dmLimitReached ? "✧ Hosted Run Limit Reached" : "Host New Run"}
                    </button>

                    <div className="join-code-section">
                        <input
                            type="text"
                            placeholder="6-Digit Invite Code"
                            maxLength="6"
                            value={joinCode}
                            onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                        />
                        <button className="join-btn" onClick={handleJoin}>Join Run</button>
                    </div>
                    {error && <p className="error-text">{error}</p>}
                </div>

                <div className="host-sections">
                    {/* Section 1: Your Active Trials */}
                    <section className="hub-section">
                        <h2 className="hub-section-title">✧ Your Active Trials ✧</h2>
                        <div className="hosting-limits-bar">
                            <div className="hosting-limit-pill">
                                <i className="fa-solid fa-crown"></i>
                                <span>
                                    {hasUnlimitedAccess
                                        ? "Unlimited Hosted Trials"
                                        : `Hosted Trials: ${myHostedCount} / 1`}
                                </span>
                            </div>
                            <div className="hosting-limit-pill">
                                <i className="fa-solid fa-shield-halved"></i>
                                <span>
                                    {hasUnlimitedAccess
                                        ? "Unlimited Joined Trials"
                                        : `Joined Trials: ${myJoinedCount} / 5`}
                                </span>
                            </div>
                        </div>

                        {loading ? (
                            <div className="loading-mini">Seeking your path...</div>
                        ) : myTrials.length > 0 ? (
                            <div className="active-trials-grid">
                                {myTrials.map(game => renderTrialCard(game))}
                            </div>
                        ) : (
                            <div className="empty-state">
                                <p>You are not currently participating in any active trials.</p>
                            </div>
                        )}
                    </section>

                    {/* Section 2: The Ethereal Spire (Community) */}
                    <section className="hub-section community-section">
                        <h2 className="hub-section-title">✧ The Ethereal Spire ✧</h2>
                        {loading ? (
                            <div className="loading-mini">Seeking others' paths...</div>
                        ) : communityTrials.length > 0 ? (
                            <div className="active-trials-grid">
                                {communityTrials.map(game => renderTrialCard(game))}
                            </div>
                        ) : (
                            <div className="empty-state">
                                <p>No other active trials found in the spire.</p>
                            </div>
                        )}
                    </section>
                </div>
            </div>
            <BackToTop />
        </div>
    );
};

export default HostHub;
