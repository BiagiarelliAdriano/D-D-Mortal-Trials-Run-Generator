import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/Auth.css';

const avatarOptions = [
    "artificer", "barbarian", "bard", "cleric",
    "druid", "fighter", "monk", "paladin",
    "ranger", "rogue", "sorcerer", "warlock", "wizard"
];

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [avatar, setAvatar] = useState('fighter');
    const [securityAnswer, setSecurityAnswer] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }

        if (password.length < 12) {
            setError("Password must be at least 12 characters long.");
            return;
        }

        if (!securityAnswer.trim()) {
            setError("Security question answer is required.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username,
                    password,
                    avatar,
                    security_answer: securityAnswer
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Auto-login upon successful registration
                login(data.token, data.user);
                navigate('/');
            } else {
                setError(data.error || 'Registration failed');
            }
        } catch (err) {
            setError('Could not connect to the server.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container dnd-theme">
            <div className="auth-card register-card">
                <button className="back-home-btn" onClick={() => navigate('/')} title="Return to Tower Entrance">
                    <i className="fa-solid fa-house"></i>
                </button>
                <div className="auth-header">
                    <h2>Join The Mortal Trials</h2>
                    <p>Forge your legacy by creating a new account.</p>
                </div>

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form two-col-form">

                    <div className="auth-col left-col">
                        <div className="form-group">
                            <label>Ascendant Name</label>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                                autoFocus
                                placeholder="Unique Name..."
                                maxLength="80"
                            />
                        </div>

                        <div className="form-group">
                            <label>Secret Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                placeholder="Create password..."
                            />
                        </div>

                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                placeholder="Repeat password..."
                            />
                        </div>

                        <div className="form-group security-box">
                            <label className="security-label">Security Question</label>
                            <p className="security-question-text">
                                <em>"What is the name of your very first Dungeons & Dragons character?"</em>
                            </p>
                            <input
                                type="text"
                                value={securityAnswer}
                                onChange={(e) => setSecurityAnswer(e.target.value)}
                                required
                                placeholder="Answer here to recover account..."
                            />
                        </div>
                    </div>

                    <div className="auth-col right-col">
                        <label className="avatar-label">Choose your Class Avatar</label>
                        <div className="avatar-grid">
                            {avatarOptions.map(opt => (
                                <div
                                    key={opt}
                                    className={`avatar-option ${avatar === opt ? 'selected' : ''}`}
                                    onClick={() => setAvatar(opt)}
                                    title={opt.charAt(0).toUpperCase() + opt.slice(1)}
                                >
                                    {/* Placeholder styling for SVG/Image, using letters for now */}
                                    {opt.substring(0, 2).toUpperCase()}
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="form-actions full-width">
                        <button type="submit" className="auth-btn" disabled={loading}>
                            {loading ? 'Forging Account...' : 'Register'}
                        </button>

                        <div className="auth-footer">
                            <span>Already have an account? </span>
                            <button type="button" className="text-link" onClick={() => navigate('/login')}>
                                Log in
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
