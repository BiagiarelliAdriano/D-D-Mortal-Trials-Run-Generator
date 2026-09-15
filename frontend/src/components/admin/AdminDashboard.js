import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useNotification } from '../../context/NotificationContext';
import UserProfilePill from '../UserProfilePill';
import AdminRecovery from './AdminRecovery';
import AdminReports from './AdminReports';
import '../../styles/Auth.css'; // Reuse some base auth styles
import '../../styles/Admin.css';
import API_BASE_URL from '../../config';

const AdminDashboard = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [expandedUser, setExpandedUser] = useState(null);
    const [editData, setEditData] = useState({});
    const [updatingUser, setUpdatingUser] = useState(null);
    const [activeTab, setActiveTab] = useState('command');
    const [userQuery, setUserQuery] = useState('');
    const { token, user } = useAuth();
    const { addAlert, confirm } = useNotification();
    const navigate = useNavigate();

    const fetchStats = useCallback(() => {
        setLoading(true);
        fetch(`${API_BASE_URL}/api/admin/system`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(res => {
                if (!res.ok) throw new Error('Failed to fetch admin data');
                return res.json();
            })
            .then(data => {
                setStats(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, [token]);

    useEffect(() => {
        if (!user?.is_admin) {
            navigate('/');
            return;
        }
        fetchStats();
    }, [user, navigate, fetchStats]);

    const handleDeleteCharacter = async (charId, e) => {
        if (e) e.stopPropagation();
        if (!await confirm("Are you sure you want to PERMANENTLY delete this character? This action cannot be undone.")) return;

        try {
            const res = await fetch(`${API_BASE_URL}/api/characters/${charId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (res.ok) {
                fetchStats();
                addAlert("Character deleted successfully.", "success");
            } else {
                addAlert("Failed to delete character.", "error");
            }
        } catch (err) {
            addAlert("Error deleting character: " + err.message, "error");
        }
    };

    const toggleExpand = (u) => {
        if (expandedUser === u.id) {
            setExpandedUser(null);
            setEditData({});
        } else {
            setExpandedUser(u.id);
            setEditData({
                username: u.username,
                avatar: u.avatar,
                is_admin: u.is_admin,
                patreon_connected: u.patreon_connected,
                patreon_tier: u.patreon_tier || ''
            });
        }
    };

    const handleFieldChange = (field, value) => {
        setEditData(prev => ({ ...prev, [field]: value }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setEditData(prev => ({ ...prev, avatar_file: file }));
        }
    };

    const handleSaveProfile = async (userId) => {
        setUpdatingUser(userId);
        const formData = new FormData();
        if (editData.username) formData.append('username', editData.username);
        if (editData.is_admin !== undefined) formData.append('is_admin', String(editData.is_admin));
        formData.append('patreon_tier', editData.patreon_tier || '');
        formData.append('patreon_connected', String(!!editData.patreon_connected));
        if (editData.avatar_file) formData.append('avatar_file', editData.avatar_file);

        try {
            const res = await fetch(`${API_BASE_URL}/api/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || 'Failed to update profile');
            }

            fetchStats();
            addAlert("Profile updated successfully!", "success");
        } catch (err) {
            addAlert(err.message, "error");
        } finally {
            setUpdatingUser(null);
        }
    };

    const handleDeleteUser = async (userId, username) => {
        if (!await confirm(`DANGER: You are about to PERMANENTLY delete the account of "${username}" and ALL their characters and runs. This action is irreversible. Proceed?`)) return;

        try {
            const res = await fetch(`${API_BASE_URL}/api/admin/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || 'Failed to delete user');
            }

            setExpandedUser(null);
            fetchStats();
            addAlert("User deleted successfully.", "success");
        } catch (err) {
            addAlert(err.message, "error");
        }
    };

    const handleDeleteRun = async (runId, title) => {
        if (!await confirm(`Delete the saved run "${title}" permanently?`)) return;
        try {
            const res = await fetch(`${API_BASE_URL}/api/runs/${runId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.error || 'Failed to delete run');
            addAlert('Saved run deleted.', 'success');
            fetchStats();
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const handleDeleteSession = async (sessionId, title) => {
        if (!await confirm(`Delete the hosted trial "${title}" and its session data permanently?`)) return;
        try {
            const res = await fetch(`${API_BASE_URL}/api/host/${sessionId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.error || 'Failed to delete session');
            addAlert('Hosted trial deleted.', 'success');
            fetchStats();
        } catch (err) {
            addAlert(err.message, 'error');
        }
    };

    const openRun = (run) => {
        if (run.hosted_session_id) {
            window.open(`/hosting/${run.hosted_session_id}`, '_blank', 'noopener,noreferrer');
            return;
        }
        window.open(`/run-generator?runId=${run.id}`, '_blank', 'noopener,noreferrer');
    };

    if (loading) return <div className="admin-loading">Ascertaining system equilibrium...</div>;
    if (error) return <div className="admin-error">Error: {error}</div>;

    return (
        <div className="admin-container dnd-theme">
            <header className="admin-header">
                <button className="back-btn" onClick={() => navigate('/')}>← Back to Hub</button>
                <h1>The Creator's Domain</h1>
                <UserProfilePill />
            </header>

            <main className="admin-content">
                <section className="stats-overview">
                    <div className="stat-card">
                        <span className="stat-label">Total Ascendants</span>
                        <span className="stat-value">{stats?.total_users}</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-label">Global Characters</span>
                        <span className="stat-value">{stats?.total_characters}</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-label">Saved Trials</span>
                        <span className="stat-value">{stats?.total_runs}</span>
                    </div>
                    <div className="stat-card live-stat">
                        <span className="stat-label">Live Sessions</span>
                        <span className="stat-value">{stats?.active_sessions}</span>
                    </div>
                    <div className="stat-card">
                        <span className="stat-label">Needs Attention</span>
                        <span className="stat-value">{(stats?.pending_reports || 0) + (stats?.pending_recovery_requests || 0)}</span>
                        <span className="stat-note">{stats?.pending_reports || 0} reports · {stats?.pending_recovery_requests || 0} recovery</span>
                    </div>
                </section>

                <nav className="admin-tabs">
                    <button 
                        className={`tab-btn ${activeTab === 'command' ? 'active' : ''}`}
                        onClick={() => setActiveTab('command')}
                    >
                        <i className="fas fa-gauge-high"></i> Command
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
                        onClick={() => setActiveTab('users')}
                    >
                        <i className="fas fa-users"></i> Ascendants
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'recovery' ? 'active' : ''}`}
                        onClick={() => setActiveTab('recovery')}
                    >
                        <i className="fas fa-key"></i> Recovery Requests
                    </button>
                    <button 
                        className={`tab-btn ${activeTab === 'reports' ? 'active' : ''}`}
                        onClick={() => setActiveTab('reports')}
                    >
                        <i className="fa-solid fa-bug"></i> Reports
                    </button>
                </nav>

                {activeTab === 'command' ? (
                    <section className="command-center">
                        <div className="section-heading-row">
                            <div>
                                <span className="eyebrow">Creator control</span>
                                <h2>System Operations</h2>
                                <p>See the live shape of the server and reach the records that need your attention.</p>
                            </div>
                            <button className="refresh-btn" onClick={fetchStats}><i className="fas fa-arrows-rotate"></i> Refresh</button>
                        </div>
                        <div className="operations-grid">
                            <div className="operation-panel">
                                <div className="panel-title"><i className="fas fa-dice-d20"></i><span>Recent Saved Trials</span></div>
                                {stats?.recent_runs?.length ? stats.recent_runs.map(run => (
                                    <div className="operation-row" key={run.id}>
                                        <div className="operation-main">
                                            <button className="operation-link" onClick={() => openRun(run)}>{run.title}</button>
                                            <small>{run.owner} · {new Date(run.created_at).toLocaleDateString()} · {run.hosted_session_id ? 'Hosted' : 'Saved'}</small>
                                        </div>
                                        <button className="admin-btn delete" onClick={() => handleDeleteRun(run.id, run.title)} title="Delete saved run"><i className="fas fa-trash"></i></button>
                                    </div>
                                )) : <p className="empty-state">No saved trials in the archive.</p>}
                            </div>
                            <div className="operation-panel">
                                <div className="panel-title"><i className="fas fa-tower-broadcast"></i><span>Hosted Sessions</span></div>
                                {stats?.recent_sessions?.length ? stats.recent_sessions.map(session => (
                                    <div className="operation-row" key={session.id}>
                                        <div className="operation-main"><button className="operation-link" onClick={() => window.open(`/hosting/${session.id}`, '_blank', 'noopener,noreferrer')}>{session.title}</button><small>{session.dm_name} · {session.participant_count} participants</small></div>
                                        <div className="operation-actions">
                                            <button className="admin-btn view" onClick={() => navigate(`/hosting/${session.id}`)} title="Inspect session"><i className="fas fa-eye"></i></button>
                                            <button className="admin-btn delete" onClick={() => handleDeleteSession(session.id, session.title)} title="Delete session"><i className="fas fa-trash"></i></button>
                                        </div>
                                    </div>
                                )) : <p className="empty-state">No hosted sessions found.</p>}
                            </div>
                        </div>
                    </section>
                ) : activeTab === 'users' ? (
                    <section className="user-table-section">
                        <div className="section-heading-row">
                            <div><span className="eyebrow">Identity and access</span><h2>Registered Ascendants</h2></div>
                            <input className="admin-search" type="search" placeholder="Search users..." value={userQuery} onChange={(e) => setUserQuery(e.target.value)} />
                        </div>
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>Avatar</th>
                                    <th>Name</th>
                                    <th>Status</th>
                                    <th>Characters</th>
                                    <th>Joined</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {stats?.users.filter(u => u.username.toLowerCase().includes(userQuery.toLowerCase())).map(u => (
                                    <React.Fragment key={u.id}>
                                        <tr className={`${u.is_admin ? 'admin-row' : ''} ${expandedUser === u.id ? 'expanded-row' : ''}`} onClick={() => toggleExpand(u)}>
                                            <td className="center">
                                                {u.avatar ? (
                                                    <img 
                                                        src={u.avatar} 
                                                        alt="Avatar" 
                                                        className="admin-avatar-mini"
                                                        onError={(e) => {
                                                            e.target.onerror = null;
                                                            e.target.style.display = 'none';
                                                            e.target.parentNode.innerHTML = `<div class="admin-avatar-mini">${u.username.substring(0, 2).toUpperCase()}</div>`;
                                                        }}
                                                    />
                                                ) : (
                                                    <div className="admin-avatar-mini">
                                                        {u.username.substring(0, 2).toUpperCase()}
                                                    </div>
                                                )}
                                            </td>
                                            <td>{u.username}</td>
                                            <td>
                                                <span className={`status-badge ${u.is_admin ? 'admin' : 'user'}`}>
                                                    {u.is_admin ? 'Creator' : 'Ascendant'}
                                                </span>
                                            </td>
                                            <td className="center">{u.character_count}</td>
                                            <td>{new Date(u.created_at).toLocaleDateString()}</td>
                                            <td className="center">
                                                <button className="admin-expand-btn">
                                                    {expandedUser === u.id ? '▲ Hide' : '▼ Manage'}
                                                </button>
                                            </td>
                                        </tr>
                                        {expandedUser === u.id && (
                                            <tr className="character-sub-row">
                                                <td colSpan="6">
                                                    <div className="admin-user-management">
                                                        <div className="management-header">
                                                            <div className="user-profile-preview">
                                                                {u.avatar ? (
                                                                    <img 
                                                                        src={u.avatar} 
                                                                        alt="Avatar Large" 
                                                                        className="admin-avatar-large"
                                                                        onError={(e) => {
                                                                            e.target.onerror = null;
                                                                            e.target.style.display = 'none';
                                                                            e.target.parentNode.innerHTML = `<div class="admin-avatar-large">${u.username.substring(0, 2).toUpperCase()}</div>`;
                                                                        }}
                                                                    />
                                                                ) : (
                                                                    <div className="admin-avatar-large">{u.username.substring(0, 2).toUpperCase()}</div>
                                                                )}
                                                                <div className="user-meta-info">
                                                                    <h3>Manage {u.username}</h3>
                                                                    <span className="joined-date">Joined on {new Date(u.created_at).toLocaleDateString()}</span>
                                                                    <span className="security-q">Security Question: <strong>{u.security_question || 'None set'}</strong></span>
                                                                </div>
                                                            </div>
                                                        </div>

                                                        <div className="edit-actions-form">
                                                            <div className="form-group">
                                                                <label>Username</label>
                                                                <input 
                                                                    type="text" 
                                                                    value={editData.username || ''} 
                                                                    onChange={(e) => handleFieldChange('username', e.target.value)}
                                                                />
                                                            </div>
                                                            <div className="form-group">
                                                                <label>New Profile Image</label>
                                                                <input 
                                                                    type="file" 
                                                                    accept="image/*"
                                                                    onChange={handleFileChange}
                                                                />
                                                            </div>
                                                            <label className="admin-access-toggle">
                                                                <input
                                                                    type="checkbox"
                                                                    checked={!!editData.is_admin}
                                                                    disabled={u.id === user?.id}
                                                                    onChange={(e) => handleFieldChange('is_admin', e.target.checked)}
                                                                />
                                                                <span>Administrator access</span>
                                                                {u.id === user?.id && <small> Your own access cannot be changed here.</small>}
                                                            </label>
                                                            <div className="patreon-access-control">
                                                                <label htmlFor={`patreon-tier-${u.id}`}>Patreon role</label>
                                                                <input
                                                                    id={`patreon-tier-${u.id}`}
                                                                    type="text"
                                                                    value={editData.patreon_tier || ''}
                                                                    placeholder="No active Patreon role"
                                                                    onChange={(e) => handleFieldChange('patreon_tier', e.target.value)}
                                                                />
                                                                <label className="patreon-connected-toggle">
                                                                    <input
                                                                        type="checkbox"
                                                                        checked={!!editData.patreon_connected}
                                                                        onChange={(e) => handleFieldChange('patreon_connected', e.target.checked)}
                                                                    />
                                                                    Active access
                                                                </label>
                                                                <small>Enter the tier name shown to the user. Clearing the tier removes Patreon access.</small>
                                                            </div>
                                                            <button 
                                                                className="save-profile-btn"
                                                                onClick={() => handleSaveProfile(u.id)}
                                                                disabled={updatingUser === u.id}
                                                            >
                                                                {updatingUser === u.id ? 'Saving Changes...' : 'Save Profile Changes'}
                                                            </button>
                                                            <hr className="admin-hr" />
                                                            <button 
                                                                className="delete-user-btn"
                                                                onClick={() => handleDeleteUser(u.id, u.username)}
                                                                disabled={updatingUser === u.id}
                                                            >
                                                                Delete Ascendant Account
                                                            </button>
                                                        </div>
                                                    </div>

                                                    <div className="admin-char-list">
                                                        <h4>Characters of {u.username}</h4>
                                                        {u.characters.length === 0 ? (
                                                            <p className="no-chars">This ascendant has not yet forged any characters.</p>
                                                        ) : (
                                                            <div className="admin-char-grid">
                                                                {u.characters.map(c => (
                                                                    <div key={c.id} className="admin-char-card">
                                                                        <div className="admin-char-info">
                                                                            <span className="admin-char-name">{c.name}</span>
                                                                            <span className="admin-char-details">Lvl {c.level} {c.class_name}</span>
                                                                        </div>
                                                                        <div className="admin-char-actions">
                                                                            <button onClick={() => navigate(`/characters/${c.id}`)} className="admin-btn view">View</button>
                                                                            <button onClick={() => navigate(`/characters/${c.id}/edit`)} className="admin-btn edit">Edit</button>
                                                                            <button onClick={(e) => handleDeleteCharacter(c.id, e)} className="admin-btn delete">Delete</button>
                                                                        </div>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        )}
                                                    </div>
                                                </td>
                                            </tr>
                                        )}
                                    </React.Fragment>
                                ))}
                            </tbody>
                        </table>
                    </section>
                ) : activeTab === 'recovery' ? (
                    <AdminRecovery />
                ) : (
                    <AdminReports />
                )}
            </main>
        </div>
    );
};

export default AdminDashboard;
