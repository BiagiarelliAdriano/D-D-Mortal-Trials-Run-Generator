import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/HostHub.css';

const HostHub = () => {
    const navigate = useNavigate();
    const { token } = useAuth();
    const [activeGames, setActiveGames] = useState([]);
    const [joinCode, setJoinCode] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchGames = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/host/active', {
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
        };
        fetchGames();
    }, [token]);

    const handleJoin = async () => {
        if (joinCode.length !== 6) {
            setError('Invite code must be 6 digits');
            return;
        }
        setError('');
        try {
            const response = await fetch('http://127.0.0.1:5000/api/host/join', {
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

    return (
        <div className="host-hub-container">
            <div className="host-hub-card">
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
                            placeholder="Enter 6-Digit Code" 
                            maxLength="6" 
                            value={joinCode}
                            onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                        />
                        <button className="join-btn" onClick={handleJoin}>Join Run</button>
                    </div>
                    {error && <p className="error-text">{error}</p>}
                </div>

                <div className="games-list-section">
                    <h2>Your Active Trials</h2>
                    {loading ? (
                        <div className="loading-mini">Seeking your path...</div>
                    ) : activeGames.length > 0 ? (
                        <div className="active-trials-grid">
                            {activeGames.map(game => (
                                <div key={game.id} className="trial-item" onClick={() => navigate(`/hosting/${game.id}`)}>
                                    <div className="trial-info">
                                        <h3>{game.run_title}</h3>
                                        <p>Hosted by {game.dm_name}</p>
                                    </div>
                                    <div className="trial-meta">
                                        <span className={`role-badge ${game.role.toLowerCase()}`}>{game.role}</span>
                                        <span className="participants-count">
                                            <i className="fa-solid fa-users"></i> {game.participant_count}/5
                                        </span>
                                        <span className="invite-code-display">{game.invite_code}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="empty-state">
                            <p>No active trials found. Be the first to host one!</p>
                        </div>
                    )}
                </div>
                
                <button className="back-btn" onClick={() => navigate('/')}>
                    <i className="fa-solid fa-arrow-left"></i> Back to Home
                </button>
            </div>
        </div>
    );
};

export default HostHub;
