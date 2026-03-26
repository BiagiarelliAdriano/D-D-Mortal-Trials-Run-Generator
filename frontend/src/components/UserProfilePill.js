import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/UserProfilePill.css';

const UserProfilePill = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    if (!user) return null;

    return (
        <div
            className="user-profile-pill clickable"
            title="View your ascendant's profile"
            onClick={() => navigate(`/profile/${user?.id}`)}
        >
            <div className="user-avatar-small">
                {user?.avatar && (user.avatar.startsWith('/') || user.avatar.startsWith('data:')) ? (
                    <img src={user.avatar.startsWith('/') ? `http://127.0.0.1:5000${user.avatar}` : user.avatar} alt="P" className="user-avatar-img" />
                ) : (
                    user?.username?.substring(0, 2).toUpperCase()
                )}
            </div>
            <span className="user-name-display">{user?.username}</span>
            <button className="logout-button" onClick={(e) => { e.stopPropagation(); logout(); }}>Sign Out</button>
        </div>
    );
};

export default UserProfilePill;
