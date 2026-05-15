import React, { useState, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNotification } from '../../context/NotificationContext';
import '../../styles/Admin.css';

const AdminRecovery = () => {
    const { getRecoveryRequests, resolveRecovery } = useAuth();
    const { addAlert, confirm } = useNotification();
    const [masterKey, setMasterKey] = useState('');
    const [isUnlocked, setIsUnlocked] = useState(false);
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(false);
    const [unlocking, setUnlocking] = useState(false);
    const [resettingId, setResettingId] = useState(null);
    const [newPasswords, setNewPasswords] = useState({});

    const handleUnlock = async (e) => {
        if (e) e.preventDefault();
        setUnlocking(true);
        try {
            const data = await getRecoveryRequests(masterKey);
            if (data.error) {
                addAlert(data.error, "error");
            } else {
                setRequests(data);
                setIsUnlocked(true);
            }
        } catch (err) {
            addAlert("Failed to communicate with the Archive.", "error");
        } finally {
            setUnlocking(false);
        }
    };

    const fetchRequests = useCallback(async () => {
        if (!isUnlocked) return;
        setLoading(true);
        try {
            const data = await getRecoveryRequests(masterKey);
            if (!data.error) {
                setRequests(data);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [isUnlocked, masterKey, getRecoveryRequests]);

    const handleAction = async (requestId, action, extraData = {}) => {
        const msg = action === 'deny' ? "Deny this recovery request?" : "Mark this request as resolved?";
        if (!await confirm(msg)) return;

        try {
            const data = await resolveRecovery(requestId, action, masterKey, extraData);
            if (data.success) {
                addAlert(`Request ${action === 'deny' ? 'denied' : 'resolved'} successfully.`, "success");
                fetchRequests();
                if (action === 'reset_password') setResettingId(null);
            } else {
                addAlert(data.error || "Failed to resolve request.", "error");
            }
        } catch (err) {
            addAlert("Magic failure: " + err.message, "error");
        }
    };

    const handlePasswordChange = (requestId, val) => {
        setNewPasswords(prev => ({ ...prev, [requestId]: val }));
    };

    if (!isUnlocked) {
        return (
            <div className="recovery-unlock-container">
                <div className="unlock-card">
                    <i className="fas fa-lock-alt unlock-icon"></i>
                    <h3>Archive Sealed</h3>
                    <p>Enter the Master Key to access account recovery records.</p>
                    <form onSubmit={handleUnlock}>
                        <input 
                            type="password" 
                            value={masterKey}
                            onChange={(e) => setMasterKey(e.target.value)}
                            placeholder="Master Recovery Key"
                            className="master-key-input"
                            autoFocus
                        />
                        <button type="submit" className="unlock-btn" disabled={unlocking || !masterKey}>
                            {unlocking ? 'Unsealing...' : 'Unseal Records'}
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    return (
        <div className="admin-recovery-section">
            <div className="section-header">
                <h2>Pending Recovery Requests</h2>
                <button onClick={fetchRequests} className="refresh-btn" disabled={loading}>
                    <i className={`fas fa-sync-alt ${loading ? 'fa-spin' : ''}`}></i> Refresh
                </button>
            </div>

            {requests.length === 0 ? (
                <div className="no-requests-msg">
                    <i className="fas fa-scroll"></i>
                    <p>The Archive is clear. No pending recovery requests.</p>
                </div>
            ) : (
                <div className="recovery-grid">
                    {requests.map(req => (
                        <div key={req.id} className={`recovery-card ${req.user_info ? 'found' : 'not-found'}`}>
                            <div className="req-header">
                                <span className="req-type">{req.request_type.replace('_', ' ')}</span>
                                <span className="req-date">{new Date(req.created_at).toLocaleString()}</span>
                            </div>

                            <div className="req-body">
                                <div className="provided-info">
                                    <label>Provided Username:</label>
                                    <strong>{req.provided_username}</strong>
                                </div>

                                {req.user_info ? (
                                    <div className="found-user-info">
                                        <div className="info-row">
                                            <label>Matched User:</label>
                                            <span>{req.user_info.username} (ID: {req.user_info.id})</span>
                                        </div>
                                        <div className="info-row">
                                            <label>Security Question:</label>
                                            <p className="q-text">{req.user_info.security_question}</p>
                                        </div>
                                        <div className="info-row highlight">
                                            <label>Security Answer:</label>
                                            <p className="a-text">{req.user_info.security_answer}</p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="user-not-found-warning">
                                        <i className="fas fa-exclamation-triangle"></i>
                                        <span>No matching account found for this username.</span>
                                    </div>
                                )}
                            </div>

                            <div className="req-actions">
                                {req.user_info && req.request_type === 'password' && (
                                    <>
                                        {resettingId === req.id ? (
                                            <div className="reset-password-form">
                                                <input 
                                                    type="text" 
                                                    placeholder="New Password"
                                                    value={newPasswords[req.id] || ''}
                                                    onChange={(e) => handlePasswordChange(req.id, e.target.value)}
                                                />
                                                <div className="form-buttons">
                                                    <button 
                                                        className="confirm-reset"
                                                        onClick={() => handleAction(req.id, 'reset_password', { new_password: newPasswords[req.id] })}
                                                        disabled={!newPasswords[req.id] || newPasswords[req.id].length < 12}
                                                    >
                                                        Confirm
                                                    </button>
                                                    <button className="cancel-reset" onClick={() => setResettingId(null)}>Cancel</button>
                                                </div>
                                            </div>
                                        ) : (
                                            <button className="action-btn reset" onClick={() => setResettingId(req.id)}>
                                                <i className="fas fa-key"></i> Reset Password
                                            </button>
                                        )}
                                    </>
                                )}

                                <button className="action-btn complete" onClick={() => handleAction(req.id, 'complete')}>
                                    <i className="fas fa-check"></i> Resolved
                                </button>
                                <button className="action-btn deny" onClick={() => handleAction(req.id, 'deny')}>
                                    <i className="fas fa-times"></i> Deny
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default AdminRecovery;
