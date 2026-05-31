import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../styles/Auth.css';

const RecoveryRequest = () => {
    const [activeTab, setActiveTab] = useState('self_service'); // 'self_service', 'manual', 'code'
    
    // Self Service State
    const [selfUsername, setSelfUsername] = useState('');
    const [question, setQuestion] = useState('');
    const [selfAnswer, setSelfAnswer] = useState('');
    const [fetchingQuestion, setFetchingQuestion] = useState(false);
    
    // Manual Request State
    const [manualUsername, setManualUsername] = useState('');
    const [requestType, setRequestType] = useState('password');
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    // Code Redemption State
    const [codeUsername, setCodeUsername] = useState('');
    const [recoveryCode, setRecoveryCode] = useState('');
    const [redeeming, setRedeeming] = useState(false);
    
    const [status, setStatus] = useState({ type: '', message: '' });
    const { requestRecovery } = useAuth();
    const navigate = useNavigate();

    const fetchQuestion = async (e) => {
        e.preventDefault();
        if (!selfUsername.trim()) return;
        setFetchingQuestion(true);
        setStatus({ type: '', message: '' });
        try {
            const response = await fetch(`/api/auth/security-question?username=${encodeURIComponent(selfUsername.trim())}`);
            const data = await response.json();
            if (response.ok) {
                setQuestion(data.security_question);
            } else {
                setStatus({ type: 'error', message: data.error || 'User not found.' });
            }
        } catch (err) {
            setStatus({ type: 'error', message: 'Failed to fetch security question.' });
        } finally {
            setFetchingQuestion(false);
        }
    };

    const handleSelfServiceSubmit = async (e) => {
        e.preventDefault();
        if (!selfUsername.trim() || !selfAnswer.trim()) return;
        setIsSubmitting(true);
        setStatus({ type: '', message: '' });
        try {
            const response = await fetch('/api/auth/verify-security-answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: selfUsername.trim(),
                    security_answer: selfAnswer.trim()
                })
            });
            const data = await response.json();
            if (response.ok) {
                setStatus({ type: 'success', message: 'Identity verified!' });
                setTimeout(() => {
                    navigate('/reset-credentials', { state: { resetToken: data.reset_token } });
                }, 1000);
            } else {
                setStatus({ type: 'error', message: data.error || 'Incorrect security answer.' });
            }
        } catch (err) {
            setStatus({ type: 'error', message: 'Magic interference occurred.' });
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleManualSubmit = async (e) => {
        e.preventDefault();
        if (!manualUsername.trim()) return;

        setIsSubmitting(true);
        setStatus({ type: '', message: '' });

        try {
            const data = await requestRecovery(manualUsername, requestType);
            if (data.success) {
                setStatus({ 
                    type: 'success', 
                    message: 'Your request has been submitted to the Archive of the Trials. Please contact the Admin directly on Discord to verify your identity using your Discord ID.' 
                });
                setManualUsername('');
            } else {
                setStatus({ type: 'error', message: data.error || 'Failed to submit request.' });
            }
        } catch (error) {
            setStatus({ type: 'error', message: 'A magical interference occurred. Please try again later.' });
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleCodeRedemption = async (e) => {
        e.preventDefault();
        if (!codeUsername.trim() || !recoveryCode.trim()) return;

        setRedeeming(true);
        setStatus({ type: '', message: '' });

        try {
            const response = await fetch('/api/auth/redeem-recovery', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: codeUsername.trim(),
                    recovery_code: recoveryCode.trim().toUpperCase()
                })
            });
            const data = await response.json();
            if (response.ok) {
                setStatus({ type: 'success', message: 'Recovery Code accepted!' });
                setTimeout(() => {
                    navigate('/reset-credentials', { state: { resetToken: data.reset_token } });
                }, 1000);
            } else {
                setStatus({ type: 'error', message: data.error || 'Invalid or expired recovery code.' });
            }
        } catch (err) {
            setStatus({ type: 'error', message: 'Connection failed.' });
        } finally {
            setRedeeming(false);
        }
    };

    return (
        <div className="auth-container dnd-theme">
            <Link to="/" className="back-home-btn">
                <i className="fas fa-home"></i>
            </Link>

            <div className="auth-card" style={{ maxWidth: '550px' }}>
                <div className="auth-header">
                    <h2>Account Recovery</h2>
                    <p>Unlock your trial credentials</p>
                </div>

                <div className="recovery-tabs" style={{ display: 'flex', borderBottom: '1px solid rgba(142, 68, 173, 0.3)', marginBottom: '20px' }}>
                    <button 
                        onClick={() => { setActiveTab('self_service'); setStatus({ type: '', message: '' }); }}
                        style={{ flex: 1, padding: '12px 6px', background: 'none', border: 'none', borderBottom: activeTab === 'self_service' ? '3px solid #8e44ad' : 'none', color: activeTab === 'self_service' ? '#c4a7e7' : '#999', cursor: 'pointer', fontWeight: 'bold' }}
                    >
                        Self-Service
                    </button>
                    <button 
                        onClick={() => { setActiveTab('manual'); setStatus({ type: '', message: '' }); }}
                        style={{ flex: 1, padding: '12px 6px', background: 'none', border: 'none', borderBottom: activeTab === 'manual' ? '3px solid #8e44ad' : 'none', color: activeTab === 'manual' ? '#c4a7e7' : '#999', cursor: 'pointer', fontWeight: 'bold' }}
                    >
                        Ask Admin
                    </button>
                    <button 
                        onClick={() => { setActiveTab('code'); setStatus({ type: '', message: '' }); }}
                        style={{ flex: 1, padding: '12px 6px', background: 'none', border: 'none', borderBottom: activeTab === 'code' ? '3px solid #8e44ad' : 'none', color: activeTab === 'code' ? '#c4a7e7' : '#999', cursor: 'pointer', fontWeight: 'bold' }}
                    >
                        Use Code
                    </button>
                </div>

                {status.message && (
                    <div className={status.type === 'success' ? 'security-challenge-notice' : 'auth-error'} style={{ marginBottom: '15px' }}>
                        {status.type === 'success' && <i className="fas fa-check-circle" style={{ marginRight: '8px' }}></i>}
                        {status.message}
                    </div>
                )}

                {activeTab === 'self_service' && status.type !== 'success' && (
                    <form onSubmit={question ? handleSelfServiceSubmit : fetchQuestion}>
                        <div className="form-group">
                            <label>Your Username</label>
                            <input
                                type="text"
                                value={selfUsername}
                                onChange={(e) => setSelfUsername(e.target.value)}
                                placeholder="Enter your username"
                                required
                                disabled={!!question || fetchingQuestion}
                            />
                        </div>

                        {question && (
                            <div className="security-question-step" style={{ marginTop: '15px' }}>
                                <label className="security-label" style={{ color: '#c4a7e7', fontStyle: 'italic' }}>Security Challenge Question:</label>
                                <p style={{ fontSize: '1.05rem', margin: '8px 0 12px', color: '#fff' }}>"{question}"</p>
                                <div className="form-group">
                                    <label>Your Security Answer</label>
                                    <input
                                        type="text"
                                        value={selfAnswer}
                                        onChange={(e) => setSelfAnswer(e.target.value)}
                                        placeholder="Type your security answer..."
                                        required
                                        autoFocus
                                        disabled={isSubmitting}
                                    />
                                </div>
                            </div>
                        )}

                        <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                            {question && (
                                <button 
                                    type="button" 
                                    className="auth-btn" 
                                    onClick={() => { setQuestion(''); setSelfAnswer(''); }}
                                    style={{ background: 'rgba(255, 255, 255, 0.1)', flex: 1 }}
                                >
                                    Change User
                                </button>
                            )}
                            <button 
                                type="submit" 
                                className="auth-btn" 
                                disabled={fetchingQuestion || isSubmitting}
                                style={{ flex: 2 }}
                            >
                                {fetchingQuestion ? 'Consulting Question...' : isSubmitting ? 'Verifying Answer...' : question ? 'Verify Answer' : 'Get Security Question'}
                            </button>
                        </div>
                    </form>
                )}

                {activeTab === 'manual' && status.type !== 'success' && (
                    <form onSubmit={handleManualSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">Your Username</label>
                            <input
                                id="username"
                                type="text"
                                value={manualUsername}
                                onChange={(e) => setManualUsername(e.target.value)}
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
                                    cursor: 'pointer',
                                    width: '100%'
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
                            disabled={isSubmitting || !manualUsername.trim()}
                            style={{ marginTop: '20px' }}
                        >
                            {isSubmitting ? 'Sending Scroll...' : 'Request Assistance'}
                        </button>
                    </form>
                )}

                {activeTab === 'code' && status.type !== 'success' && (
                    <form onSubmit={handleCodeRedemption}>
                        <div className="form-group">
                            <label>Your Username</label>
                            <input
                                type="text"
                                value={codeUsername}
                                onChange={(e) => setCodeUsername(e.target.value)}
                                placeholder="Enter your username"
                                required
                                disabled={redeeming}
                            />
                        </div>

                        <div className="form-group" style={{ marginTop: '15px' }}>
                            <label>One-Time Recovery Code</label>
                            <input
                                type="text"
                                value={recoveryCode}
                                onChange={(e) => setRecoveryCode(e.target.value)}
                                placeholder="e.g. A4C29E6B"
                                maxLength="10"
                                required
                                disabled={redeeming}
                                style={{ letterSpacing: '2px', textTransform: 'uppercase', fontSize: '1.2rem', textAlign: 'center' }}
                            />
                        </div>

                        <button 
                            type="submit" 
                            className="auth-btn" 
                            disabled={redeeming || !codeUsername.trim() || !recoveryCode.trim()}
                            style={{ marginTop: '20px' }}
                        >
                            {redeeming ? 'Redeeming Scroll...' : 'Redeem Code'}
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

