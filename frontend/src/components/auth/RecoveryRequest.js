import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/Auth.css';

const RecoveryRequest = () => {
    const [username, setUsername] = useState('');
    const [requestType, setRequestType] = useState('password');
    const [status, setStatus] = useState({ type: '', message: '' });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { requestRecovery } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!username.trim()) return;

        setIsSubmitting(true);
        setStatus({ type: '', message: '' });

        try {
            const data = await requestRecovery(username, requestType);
            if (data.success) {
                setStatus({ 
                    type: 'success', 
                    message: 'Your request has been submitted to the Archive of the Trials. Please contact the Admin directly to verify your identity and finalize recovery.' 
                });
                setUsername('');
            } else {
                setStatus({ type: 'error', message: data.error || 'Failed to submit request.' });
            }
        } catch (error) {
            setStatus({ type: 'error', message: 'A magical interference occurred. Please try again later.' });
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="auth-container dnd-theme">
            <Link to="/" className="back-home-btn">
                <i className="fas fa-home"></i>
            </Link>

            <div className="auth-card">
                <div className="auth-header">
                    <h2>Account Recovery</h2>
                    <p>Contact the Archive to regain your access</p>
                </div>

                {status.message && (
                    <div className={status.type === 'success' ? 'security-challenge-notice' : 'auth-error'}>
                        {status.type === 'success' && <i className="fas fa-check-circle"></i>}
                        {status.message}
                    </div>
                )}

                {status.type !== 'success' && (
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">Your Username</label>
                            <input
                                id="username"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Enter the username you remember"
                                required
                                disabled={isSubmitting}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="requestType">What do you need help with?</label>
                            <select
                                id="requestType"
                                value={requestType}
                                onChange={(e) => setRequestType(e.target.value)}
                                style={{
                                    background: 'rgba(0, 0, 0, 0.3)',
                                    border: '1px solid rgba(142, 68, 173, 0.3)',
                                    color: 'white',
                                    padding: '12px 15px',
                                    borderRadius: '6px',
                                    fontSize: '1rem',
                                    cursor: 'pointer'
                                }}
                                disabled={isSubmitting}
                            >
                                <option value="password">Forgotten Password</option>
                                <option value="username">Forgotten Username</option>
                                <option value="security_answer">Forgotten Security Answer</option>
                            </select>
                        </div>

                        <button 
                            type="submit" 
                            className="auth-btn" 
                            disabled={isSubmitting || !username.trim()}
                        >
                            {isSubmitting ? 'Sending Scroll...' : 'Request Assistance'}
                        </button>
                    </form>
                )}

                <div className="auth-footer">
                    <p>
                        Remembered your details?{' '}
                        <button className="text-link" onClick={() => navigate('/login')}>
                            Back to Login
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default RecoveryRequest;
