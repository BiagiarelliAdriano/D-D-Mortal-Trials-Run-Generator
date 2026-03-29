import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import BackToTop from '../common/BackToTop';
import '../../styles/HostHub.css';

const HostHub = () => {
    const navigate = useNavigate();
    const { token } = useAuth();
    const [activeGames, setActiveGames] = useState([]);
    const [joinCode, setJoinCode] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [copiedCode, setCopiedCode] = useState(null);

    const fetchGames = useCallback(async () => {
        try {
            const response = await fetch('/api/host/active', {
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

    // Partition and Sort trials
    const { myTrials, communityTrials } = useMemo(() => {
        const mine = activeGames.filter(g => g.role !== 'Visitor');
        const community = activeGames.filter(g => g.role === 'Visitor');

        // community already sorted by dm_name from backend, but ensuring here
        community.sort((a, b) => a.dm_name.localeCompare(b.dm_name));

        return { myTrials: mine, communityTrials: community };
    }, [activeGames]);

    const handleJoin = async () => {
        if (joinCode.length !== 6) {
            setError('Invite code must be 6 digits');
            return;
        }
        setError('');
        try {
            const response = await fetch('/api/host/join', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ invite_code: joinCode })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to join trial');
            
            navigate(`/hosting/${data.session_id}`);
        } catch (err) {
            setError(err.message);
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
                        <button className="enter-trial-btn">
                            Enter Spire <i className="fa-solid fa-arrow-right"></i>
                        </button>
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
                <button className="spire-back-btn" onClick={() => navigate('/')}>
                    <i className="fa-solid fa-house"></i> Home Spire
                </button>
                <div className="host-header">
                    <h1>The Hosting Spire</h1>
                    <p>Manage your trials or join an existing ascent.</p>
                </div>

                <div className="host-actions">
                    <button className="host-primary-btn" onClick={() => navigate('/run-generator?host=true')}>
                        <i className="fa-solid fa-plus-circle"></i> Host New Run
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
