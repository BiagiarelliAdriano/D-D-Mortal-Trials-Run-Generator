import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import UserProfilePill from '../UserProfilePill';
import '../../styles/Auth.css'; // Reuse some base auth styles
import '../../styles/Admin.css';

const AdminDashboard = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [expandedUser, setExpandedUser] = useState(null);
    const [editData, setEditData] = useState({});
    const [updatingUser, setUpdatingUser] = useState(null);
    const { token, user } = useAuth();
    const navigate = useNavigate();

    const fetchStats = useCallback(() => {
        setLoading(true);
        fetch('/api/admin/system', {
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

    const handleDeleteCharacter = (charId, e) => {
        e.stopPropagation();
        if (!window.confirm("Are you sure you want to PERMANENTLY delete this character? This action cannot be undone.")) return;

        fetch(`/api/characters/${charId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(res => {
                if (res.ok) {
                    fetchStats(); // Refresh data
                } else {
                    alert("Failed to delete character.");
                }
            })
            .catch(err => console.error("Error deleting character:", err));
    };

    const toggleExpand = (u) => {
        if (expandedUser === u.id) {
            setExpandedUser(null);
            setEditData({});
        } else {
            setExpandedUser(u.id);
            setEditData({
                username: u.username,
                avatar: u.avatar
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
        if (editData.avatar_file) formData.append('avatar_file', editData.avatar_file);

        try {
            const res = await fetch(`/api/users/${userId}`, {
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

            fetchStats(); // Refresh list
            setUpdatingUser(null);
            alert("Profile updated successfully!");
        } catch (err) {
            alert(err.message);
            setUpdatingUser(null);
        }
    };

    const handleDeleteUser = async (userId, username) => {
        if (!window.confirm(`DANGER: You are about to PERMANENTLY delete the account of "${username}" and ALL their characters and runs. This action is irreversible. Proceed?`)) return;

        try {
            const res = await fetch(`/api/admin/users/${userId}`, {
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
            fetchStats(); // Refresh list
            alert("User deleted successfully.");
        } catch (err) {
            alert(err.message);
        }
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
                </section>
                <section className="user-table-section">
                    <h2>Registered Ascendants</h2>
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
                            {stats?.users.map(u => (
                                <React.Fragment key={u.id}>
                                    <tr className={`${u.is_admin ? 'admin-row' : ''} ${expandedUser === u.id ? 'expanded-row' : ''}`} onClick={() => toggleExpand(u)}>
                                        <td className="center">
                                            {u.avatar.startsWith('static/') || u.avatar.startsWith('/') ? (
                                                <img 
                                                    src={`${u.avatar}`} 
                                                    alt="Avatar" 
                                                    className="admin-avatar-mini"
                                                    onError={(e) => {
                                                        e.target.onerror = null;
                                                        e.target.src = '';
                                                        e.target.innerText = u.username.substring(0, 2).toUpperCase();
                                                    }}
                                                />
                                            ) : (
                                                <div className="admin-avatar-mini" title={u.avatar}>
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
                                                            {u.avatar.startsWith('/') ? (
                                                                <img src={`${u.avatar}`} alt="Avatar Large" className="admin-avatar-large" />
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
            </main>
        </div>
    );
};

export default AdminDashboard;
