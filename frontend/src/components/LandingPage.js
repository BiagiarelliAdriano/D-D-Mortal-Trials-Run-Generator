import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import UserProfilePill from './UserProfilePill';
import '../styles/LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();
    const { token, user } = useAuth();

    const handleCharacterManagerClick = () => {
        if (token) {
            navigate('/characters');
        } else {
            navigate('/login');
        }
    };

    return (
        <div className="landing-container">
            <div className="landing-overlay"></div>

            <div className="header-top-nav">
                {user?.is_admin && (
                    <button className="admin-link-btn" onClick={() => navigate('/admin')}>
                        <i className="fa-solid fa-crown"></i> Creator's Hub
                    </button>
                )}
                <UserProfilePill />
            </div>

            <header className="landing-header">
                <img
                    src="/static/assets/images/themortaltrialslogo.webp"
                    alt="The Mortal Trials Logo"
                    className="landing-logo"
                />
            </header>

            <main className="landing-content">
                <section className="description-card">
                    <h1 className="serif-text">Step into the Tower</h1>
                    <p className="recap-text">
                        The Mortal Trials is a fan-made, roguelike D&D experience focused on tactical combat and structured growth.
                        Every Run features random encounters, meaningful rewards, and a complete story shared with friends. <br />
                        Experiment boldly, climb the Tower, and enjoy the Trials.
                    </p>
                    <p className="features-text">
                        <strong>Run Generation</strong> • <strong>Character Management</strong> • <strong>Run Hosting</strong>
                    </p>
                </section>

                <div className="cta-buttons">
                    <button
                        className="cta-button primary-btn"
                        onClick={() => navigate('/run-generator')}
                    >
                        <i className="fa-solid fa-dice-d20"></i>
                        <span>Run Generator</span>
                    </button>
                    <button
                        className="cta-button secondary-btn"
                        onClick={() => navigate('/hosting')}
                    >
                        <i className="fa-solid fa-tower-observation"></i>
                        <span>Look for Game</span>
                    </button>
                    <button
                        className="cta-button secondary-btn"
                        onClick={handleCharacterManagerClick}
                    >
                        <i className="fa-solid fa-users"></i>
                        <span>Character Manager</span>
                    </button>
                </div>
            </main>
        </div>
    );
};

export default LandingPage;
