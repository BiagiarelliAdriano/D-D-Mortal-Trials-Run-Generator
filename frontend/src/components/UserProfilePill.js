import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/UserProfilePill.css';

const UserProfilePill = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    if (!user) {
        return (
            <div className="user-profile-pill guest" onClick={() => navigate('/login')}>
                <div className="user-avatar-small guest">
                    <i className="fa-solid fa-user-secret"></i>
                </div>
                <div className="guest-text">
                    <span className="welcome">Welcome, Ascendant</span>
                    <div className="auth-links">
                        <span className="auth-link">Log In</span>
                        <span className="separator">|</span>
                        <span className="auth-link" onClick={(e) => { e.stopPropagation(); navigate('/register'); }}>Register</span>
                    </div>
                </div>
            </div>
        );
    }

    let tierClass = "free-tier";
    if (user?.patreon_connected && user?.patreon_tier) {
        const tierLower = user.patreon_tier.toLowerCase();
        if (tierLower.includes("warden")) tierClass = "tier-warden";
        else if (tierLower.includes("ascended")) tierClass = "tier-ascended";
        else if (tierLower.includes("chosen")) tierClass = "tier-chosen";
        else tierClass = "tier-supporter";
    }

    return (
        <div
            className="user-profile-pill clickable"
            title="View your ascendant's profile"
            onClick={() => navigate(`/profile/${user?.id}`)}
        >
            <div className={`user-avatar-small ${tierClass}`}>
                {user?.avatar ? (
                    <img
                        src={user.avatar}
                        alt="Profile"
                        className="user-avatar-img"
                    />
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
