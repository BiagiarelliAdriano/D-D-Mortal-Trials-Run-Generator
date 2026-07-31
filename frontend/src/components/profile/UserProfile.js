import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/Profile.css';
import API_BASE_URL from '../../config';

const UserProfile = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user: currentUser, token, login } = useAuth();

    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [editMode, setEditMode] = useState(false);

    // Edit form states
    const [newUsername, setNewUsername] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [avatarFile, setAvatarFile] = useState(null);
    const [avatarPreview, setAvatarPreview] = useState(null);
    const [saving, setSaving] = useState(false);

    const fetchProfile = useCallback(async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/users/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Failed to fetch profile');
            const data = await response.json();
            setProfileData(data);
            setNewUsername(data.username);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [id, token]);

    useEffect(() => {
        fetchProfile();
    }, [fetchProfile]);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setAvatarFile(file);
            const reader = new FileReader();
            reader.onloadend = () => setAvatarPreview(reader.result);
            reader.readAsDataURL(file);
        }
    };

    const handleSave = async (e) => {
        e.preventDefault();
        setSaving(true);
        setError('');

        const formData = new FormData();
        if (newUsername !== profileData.username) formData.append('username', newUsername);
        if (newPassword) formData.append('password', newPassword);
        if (avatarFile) formData.append('avatar_file', avatarFile);

        try {
            const response = await fetch(`${API_BASE_URL}/api/users/${id}`, {
                method: 'PUT',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Failed to update profile');

            setProfileData({ ...profileData, ...result.user });
            setEditMode(false);
            setAvatarFile(null);
            setAvatarPreview(null);
            setNewPassword('');

            // If updating self, refresh AuthContext
            if (currentUser.id === parseInt(id)) {
                login(token, result.user);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div className="profile-container"><div className="loading-screen">Seeking the Ascendant...</div></div>;
    if (error) return <div className="profile-container"><div className="auth-error">{error}</div></div>;
    if (!profileData) return null;

    const isOwner = currentUser?.id === profileData.id;
    const isAdmin = currentUser?.is_admin;
    const canEdit = isOwner || isAdmin;

    const getAvatarDisplay = () => {
        const avatar = avatarPreview || profileData.avatar;
        if (avatar) {
            return (
                <img
                    src={avatar}
                    alt="Profile"
                    className="profile-avatar"
                />
            );
        }
        return (
            <div className="profile-avatar">
                {profileData.username.substring(0, 2).toUpperCase()}
            </div>
        );
    };

    return (
        <div className="profile-container">
            <div className="profile-card">
                <div className="profile-header">
                    <div className="profile-avatar-container">
                        {getAvatarDisplay()}
                    </div>
                    <div className="profile-info">
                        <h1>{profileData.username}</h1>
                        <p className="profile-meta">Joined the Trials on {new Date(profileData.created_at).toLocaleDateString()}</p>
                        {profileData.is_admin && <span className="level-tag">Creator</span>}
                    </div>
                    {canEdit && !editMode && (
                        <button className="edit-profile-btn" onClick={() => setEditMode(true)}>
                            ⚙ Edit Profile
                        </button>
                    )}
                </div>

                {!editMode && (
                    <div className="profile-navigation">
                        <button className="nav-btn" onClick={() => navigate('/run-generator')}>
                            <i className="fa-solid fa-dice-d20"></i> Run Generator
                        </button>
                        <button className="nav-btn" onClick={() => navigate('/characters')}>
                            <i className="fa-solid fa-users"></i> Characters Hub
                        </button>
                        <button className="nav-btn" onClick={() => navigate('/hosting')}>
                            <i className="fa-solid fa-tower-observation"></i> Look for Game
                        </button>
                        <button className="nav-btn" onClick={() => navigate('/')}>
                            <i className="fa-solid fa-house"></i> Home
                        </button>
                    </div>
                )}

                {editMode && (
                    <form className="edit-form" onSubmit={handleSave}>
                        <div className="edit-form-group">
                            <label>Ascendant Name</label>
                            <input
                                type="text"
                                value={newUsername}
                                onChange={(e) => setNewUsername(e.target.value)}
                                placeholder="Change your name..."
                            />
                        </div>
                        <div className="edit-form-group">
                            <label>New Secret Password</label>
                            <input
                                type="password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                placeholder="Leave empty to keep current..."
                            />
                        </div>
                        <div className="edit-form-group">
                            <label>Update Avatar</label>
                            <div className="file-input-wrapper">
                                <input
                                    type="file"
                                    id="avatar-upload"
                                    hidden
                                    onChange={handleFileChange}
                                    accept="image/*"
                                />
                                <label htmlFor="avatar-upload" className="upload-btn">
                                    {avatarFile ? 'Change Image' : 'Upload New Image'}
                                </label>
                                {avatarFile && <span className="file-name">{avatarFile.name}</span>}
                            </div>
                        </div>
                        <div className="edit-actions">
                            <button type="submit" className="save-btn" disabled={saving}>
                                {saving ? 'Saving...' : 'Save Changes'}
                            </button>
                            <button type="button" className="cancel-btn" onClick={() => {
                                setEditMode(false);
                                setAvatarPreview(null);
                                setAvatarFile(null);
                            }}>
                                Cancel
                            </button>
                        </div>
                        {error && <div className="auth-error" style={{ marginTop: '10px' }}>{error}</div>}
                    </form>
                )}

                <div className="profile-content-scroll">
                    <h2 className="profile-section-title">
                        Characters
                    </h2>

                    {profileData.characters.length > 0 ? (
                        <div className="profile-char-grid">
                            {profileData.characters.map(char => (
                                <div
                                    key={char.id}
                                    className="character-card"
                                    onClick={() => window.open(`/characters/${char.id}`, '_blank')}
                                >
                                    <div className="card-header">
                                        <h3>{char.name}</h3>
                                        <span className="level-tag">Lvl {char.level}</span>
                                    </div>
                                    <div className="card-info">
                                        <span>{char.class_name}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="empty-state">
                            <h3>No characters found.</h3>
                            <p>This Ascendant has yet to forge their first destiny.</p>
                            {isOwner && (
                                <button className="create-button" onClick={() => navigate('/characters/create')} style={{ marginTop: '20px' }}>
                                    ✧ Create First Character
                                </button>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
