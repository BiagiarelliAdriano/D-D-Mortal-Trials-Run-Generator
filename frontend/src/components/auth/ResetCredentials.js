import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../../styles/Auth.css';
import API_BASE_URL from '../../config';

const ResetCredentials = () => {
    const location = useLocation();
    const navigate = useNavigate();
    
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [securityQuestion, setSecurityQuestion] = useState("What is the name of your very first Dungeons & Dragons character?");
    const [securityAnswer, setSecurityAnswer] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    
    const resetToken = location.state?.resetToken;
    
    useEffect(() => {
        if (!resetToken) {
            navigate('/login');
        }
    }, [resetToken, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

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
            const response = await fetch(`${API_BASE_URL}/api/auth/reset-credentials`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${resetToken}`
                },
                body: JSON.stringify({
                    new_password: password,
                    new_security_question: securityQuestion.trim(),
                    new_security_answer: securityAnswer.trim()
                })
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess('Your trial credentials have been successfully reforged! Redirecting to login...');
                setTimeout(() => {
                    navigate('/login');
                }, 3000);
            } else {
                setError(data.error || 'Failed to reset credentials.');
            }
        } catch (err) {
            setError('Could not connect to the server.');
        } finally {
            setLoading(false);
        }
    };

    if (!resetToken) {
        return null;
    }

    return (
        <div className="auth-container dnd-theme">
            <div className="auth-card" style={{ maxWidth: '500px' }}>
                <div className="auth-header">
                    <h2>Reforge Credentials</h2>
                    <p>Forge your new secret passcode and security sign</p>
                </div>

                {error && <div className="auth-error">{error}</div>}
                {success && <div className="security-challenge-notice"><i className="fas fa-check-circle" style={{ marginRight: '8px' }}></i>{success}</div>}

                {!success && (
                    <form onSubmit={handleSubmit} className="auth-form">
                        <div className="form-group">
                            <label>New Secret Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                placeholder="Create new password (min 12 chars)..."
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                placeholder="Repeat new password..."
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group security-box" style={{ marginTop: '15px' }}>
                            <label className="security-label">Security Question</label>
                            <select
                                value={securityQuestion}
                                onChange={(e) => setSecurityQuestion(e.target.value)}
                                style={{
                                    background: 'rgba(0, 0, 0, 0.3)',
                                    border: '1px solid rgba(142, 68, 173, 0.3)',
                                    color: 'white',
                                    padding: '12px 15px',
                                    borderRadius: '6px',
                                    fontSize: '1rem',
                                    cursor: 'pointer',
                                    width: '100%',
                                    marginBottom: '10px'
                                }}
                                disabled={loading}
                            >
                                <option value="What is the name of your very first Dungeons & Dragons character?">
                                    What is the name of your very first Dungeons & Dragons character?
                                </option>
                                <option value="What was the name of your first pet?">
                                    What was the name of your first pet?
                                </option>
                                <option value="In what city or town did your mother and father meet?">
                                    In what city or town did your mother and father meet?
                                </option>
                            </select>

                            <label>Your New Security Answer</label>
                            <input
                                type="text"
                                value={securityAnswer}
                                onChange={(e) => setSecurityAnswer(e.target.value)}
                                required
                                placeholder="Type answer here..."
                                disabled={loading}
                            />
                        </div>

                        <button type="submit" className="auth-btn" disabled={loading} style={{ marginTop: '20px' }}>
                            {loading ? 'Reforging...' : 'Reforge Credentials'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};

export default ResetCredentials;
