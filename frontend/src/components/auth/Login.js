import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/Auth.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
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

    return (
        <div className="auth-container dnd-theme">
            <div className="auth-card">
                <button className="back-home-btn" onClick={() => navigate('/')} title="Return to Tower Entrance">
                    <i className="fa-solid fa-house"></i>
                </button>
                <div className="auth-header">
                    <h2>The Mortal Trials</h2>
                    <p>Enter your credentials to access your characters.</p>
                </div>

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
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
                        {loading ? 'Entering Realm...' : 'Log In'}
                    </button>

                    <div className="auth-footer">
                        <span>A new Ascendant? </span>
                        <button type="button" className="text-link" onClick={() => navigate('/register')}>
                            Create Account
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
