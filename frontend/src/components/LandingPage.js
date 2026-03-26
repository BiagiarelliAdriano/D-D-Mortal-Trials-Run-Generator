import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import UserProfilePill from './UserProfilePill';
import '../styles/LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();
    const { token } = useAuth();

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

            <header className="landing-header">
                <div className="header-top-nav">
                    {token && (
                        <UserProfilePill />
                    )}
                </div>
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

            <footer className="landing-footer">
                <p className="copyright-text">© {new Date().getFullYear()} The Mortal Trials. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default LandingPage;
