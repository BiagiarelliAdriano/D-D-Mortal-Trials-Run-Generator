import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { needsSecurityChallenge } from '../../utils/deviceFingerprint';
import '../../styles/Auth.css';
import API_BASE_URL from '../../config';

const Login = () => {
    const [step, setStep] = useState(1); // 1 = credentials, 2 = security challenge
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [securityQuestion, setSecurityQuestion] = useState('');
    const [securityAnswer, setSecurityAnswer] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    // Final login request — sends credentials and optionally a security answer
    const submitLogin = async (secAnswer = null) => {
        setError('');
        setLoading(true);
        try {
            const body = { username, password };
            if (secAnswer !== null) {
                body.security_answer = secAnswer;
            }

            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            const data = await response.json();

            if (response.ok) {
                login(data.token, data.user);
                navigate('/');
            } else {
                setError(data.error || 'Login failed');
            }
        } catch (err) {
            setError('Could not connect to the server.');
        } finally {
            setLoading(false);
        }
    };

    // Step 1: Check whether a security challenge is needed, then either
    // proceed directly or fetch the question and advance to step 2.
    const handleStep1Submit = async (e) => {
        e.preventDefault();
        setError('');

        if (needsSecurityChallenge()) {
            // New device or expired session — fetch the security question before
            // verifying credentials so the user sees the correct question text.
            setLoading(true);
            try {
                const res = await fetch(
                    `${API_BASE_URL}/api/auth/security-question?username=${encodeURIComponent(username.trim())}`
                );
                if (!res.ok) {
                    // Username doesn't exist — show a generic error to avoid enumeration
                    setError('Invalid username or password');
                    return;
                }
                const data = await res.json();
                setSecurityQuestion(data.security_question);
                setStep(2);
            } catch (err) {
                setError('Could not connect to the server.');
            } finally {
                setLoading(false);
            }
        } else {
            // Trusted device — login without the security question
            await submitLogin();
        }
    };

    // Step 2: Submit credentials + security answer together
    const handleStep2Submit = async (e) => {
        e.preventDefault();
        await submitLogin(securityAnswer);
    };

    const handleBackToStep1 = () => {
        setStep(1);
        setSecurityAnswer('');
        setError('');
    };

    return (
        <div className="auth-container dnd-theme">
            <div className="auth-card">
                <button
                    className="back-home-btn"
                    onClick={() => navigate('/')}
                    title="Return to Tower Entrance"
                >
                    <i className="fa-solid fa-house"></i>
                </button>

                <div className="auth-header">
                    <h2>The Mortal Trials</h2>
                    {step === 1
                        ? <p>Enter your credentials to access your characters.</p>
                        : <p>Verify your identity to continue.</p>
                    }
                </div>

                {error && <div className="auth-error">{error}</div>}

                {/* ── Step 1: Credentials ── */}
                {step === 1 && (
                    <form onSubmit={handleStep1Submit} className="auth-form">
                        <div className="form-group">
                            <label>Ascendant Name</label>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                                autoFocus
                                placeholder="Enter username..."
                            />
                        </div>

                        <div className="form-group">
                            <label>Secret Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                placeholder="Enter password..."
                            />
                        </div>

                        <button type="submit" className="auth-btn" disabled={loading}>
                            {loading ? 'Checking...' : 'Continue'}
                        </button>

                        <div className="auth-footer">
                            <p style={{ marginBottom: '10px' }}>
                                Don't have an account?{' '}
                                <button type="button" className="text-link" onClick={() => navigate('/register')}>
                                    Join the Trials
                                </button>
                            </p>
                            <p>
                                <button type="button" className="text-link" onClick={() => navigate('/recovery-request')} style={{ fontSize: '0.85rem', opacity: 0.8 }}>
                                    Forgotten your account info?
                                </button>
                            </p>
                        </div>
                    </form>
                )}

                {/* ── Step 2: Security Challenge ── */}
                {step === 2 && (
                    <form onSubmit={handleStep2Submit} className="auth-form">
                        <div className="security-challenge-notice">
                            <i className="fa-solid fa-shield-halved"></i>
                            <span>
                                New device or expired session detected.
                                Please answer your security question to verify your identity.
                            </span>
                        </div>

                        <div className="form-group security-box">
                            <label className="security-label">Security Question</label>
                            <p className="security-question-text">
                                <em>"{securityQuestion}"</em>
                            </p>
                            <input
                                type="text"
                                value={securityAnswer}
                                onChange={(e) => setSecurityAnswer(e.target.value)}
                                required
                                autoFocus
                                placeholder="Your answer..."
                                autoComplete="off"
                            />
                        </div>

                        <button type="submit" className="auth-btn" disabled={loading}>
                            {loading ? 'Verifying...' : 'Enter the Trials'}
                        </button>

                        <button
                            type="button"
                            className="back-step-btn"
                            onClick={handleBackToStep1}
                            disabled={loading}
                        >
                            ← Back to Credentials
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};

export default Login;
