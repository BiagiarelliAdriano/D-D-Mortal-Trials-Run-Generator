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
    const [generatedCodes, setGeneratedCodes] = useState({});

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

    const handleAction = async (requestId, action) => {
        const msg = action === 'deny' 
            ? "Are you sure you want to DENY this recovery request?" 
            : "Are you sure you want to APPROVE this request and generate a Recovery Code?";
        if (!await confirm(msg)) return;

        try {
            const data = await resolveRecovery(requestId, action, masterKey);
            if (data.success) {
                if (action === 'approve') {
                    addAlert(`Request approved! Code generated successfully.`, "success");
                    setGeneratedCodes(prev => ({ ...prev, [requestId]: data.recovery_code }));
                } else {
                    addAlert(`Request denied successfully.`, "success");
                    fetchRequests();
                }
            } else {
                addAlert(data.error || "Failed to resolve request.", "error");
            }
        } catch (err) {
            addAlert("Magic failure: " + err.message, "error");
        }
    };

    const handleCopy = (code) => {
        navigator.clipboard.writeText(code);
        addAlert("Recovery code copied to clipboard!", "success");
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
                                        <div className="info-row highlight" style={{ backgroundColor: '#2d1b4e', padding: '10px', borderRadius: '4px', border: '1px solid #5b3e96', marginTop: '10px' }}>
                                            <label style={{ color: '#c4a7e7', display: 'block', marginBottom: '4px' }}>Discord ID:</label>
                                            <strong style={{ fontSize: '1.1rem', color: '#fff', letterSpacing: '0.5px' }}>
                                                {req.user_info.discord_id || "No Discord ID Linked"}
                                            </strong>
                                            <small style={{ display: 'block', opacity: 0.7, marginTop: '4px', fontSize: '0.75rem', lineHeight: '1.2' }}>
                                                Verify the Discord account matches this ID before sending the code!
                                            </small>
                                        </div>
                                        <div className="info-row" style={{ marginTop: '10px' }}>
                                            <label>Security Question:</label>
                                            <p className="q-text" style={{ margin: '4px 0 0' }}>{req.user_info.security_question || "No security question configured"}</p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="user-not-found-warning">
                                        <i className="fas fa-exclamation-triangle"></i>
                                        <span>No matching account found for this username.</span>
                                    </div>
                                )}

                                {generatedCodes[req.id] && (
                                    <div className="generated-code-box" style={{ marginTop: '15px', padding: '12px', background: '#1c3d27', border: '1px solid #27a243', borderRadius: '4px', textAlign: 'center' }}>
                                        <label style={{ display: 'block', color: '#a3f3b9', fontWeight: 'bold', marginBottom: '5px' }}>ONE-TIME RECOVERY CODE</label>
                                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                                            <code style={{ fontSize: '1.4rem', color: '#fff', fontWeight: 'bold', letterSpacing: '2px' }}>{generatedCodes[req.id]}</code>
                                            <button 
                                                className="action-btn copy" 
                                                onClick={() => handleCopy(generatedCodes[req.id])}
                                                style={{ background: '#27a243', border: 'none', color: '#fff', padding: '4px 8px', borderRadius: '3px', cursor: 'pointer' }}
                                            >
                                                <i className="fas fa-copy"></i> Copy
                                            </button>
                                        </div>
                                        <p style={{ margin: '5px 0 0', fontSize: '0.75rem', color: '#a3f3b9', opacity: 0.8 }}>Send this code to the user via Discord. Expires in 24 hours.</p>
                                    </div>
                                )}
                            </div>

                            <div className="req-actions">
                                {!generatedCodes[req.id] && req.user_info && (
                                    <button className="action-btn reset" style={{ background: '#5b3e96' }} onClick={() => handleAction(req.id, 'approve')}>
                                        <i className="fas fa-check-circle"></i> Approve & Generate Code
                                    </button>
                                )}
                                {!generatedCodes[req.id] && (
                                    <button className="action-btn deny" onClick={() => handleAction(req.id, 'deny')}>
                                        <i className="fas fa-times"></i> Deny
                                    </button>
                                )}
                                {generatedCodes[req.id] && (
                                    <button className="action-btn complete" onClick={fetchRequests}>
                                        <i className="fas fa-check"></i> Done
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default AdminRecovery;

