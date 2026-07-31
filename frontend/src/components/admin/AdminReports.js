import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNotification } from '../../context/NotificationContext';
import '../../styles/Admin.css'; // Assuming we reuse existing admin styles
import API_BASE_URL from '../../config';

const AdminReports = () => {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [expandedReport, setExpandedReport] = useState(null);
    const [replyMessage, setReplyMessage] = useState('');
    const [resolvingId, setResolvingId] = useState(null);

    const { token } = useAuth();
    const { addAlert, confirm } = useNotification();

    const fetchReports = useCallback(async () => {
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/api/admin/reports`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!res.ok) throw new Error('Failed to fetch reports');
            const data = await res.json();
            setReports(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [token]);

    useEffect(() => {
        fetchReports();
    }, [fetchReports]);

    const handleResolve = async (reportId) => {
        if (!replyMessage.trim()) {
            addAlert('Please enter a reply message for the user.', 'error');
            return;
        }

        if (!await confirm('Resolve this report and send the notification to the user?')) return;

        setResolvingId(reportId);
        try {
            const res = await fetch(`${API_BASE_URL}/api/admin/reports/${reportId}/resolve`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message: replyMessage })
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.error || 'Failed to resolve report');
            }

            addAlert('Report resolved and user notified.', 'success');
            setReplyMessage('');
            setExpandedReport(null);
            fetchReports();
        } catch (err) {
            addAlert(err.message, 'error');
        } finally {
            setResolvingId(null);
        }
    };

    if (loading) return <div className="admin-loading">Fetching reports...</div>;
    if (error) return <div className="admin-error">Error: {error}</div>;

    const pendingReports = reports.filter(r => r.status === 'pending');
    const resolvedReports = reports.filter(r => r.status === 'resolved');

    return (
        <section className="admin-reports-section">
            <h2>Feedback & Bug Reports</h2>
            
            <div className="reports-stats">
                <p>Pending: {pendingReports.length} | Resolved: {resolvedReports.length}</p>
            </div>

            {reports.length === 0 ? (
                <p>No reports found.</p>
            ) : (
                <table className="admin-table">
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>User</th>
                            <th>Date</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reports.map(r => (
                            <React.Fragment key={r.id}>
                                <tr className={expandedReport === r.id ? 'expanded-row' : ''}>
                                    <td>
                                        <span className={`status-badge ${r.report_type === 'Bug' ? 'admin' : 'user'}`}>
                                            {r.report_type}
                                        </span>
                                    </td>
                                    <td>{r.username}</td>
                                    <td>{new Date(r.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <span className={`status-badge ${r.status === 'resolved' ? 'user' : 'pending'}`} style={r.status === 'pending' ? {background: '#FF9800', color: '#fff'} : {}}>
                                            {r.status}
                                        </span>
                                    </td>
                                    <td className="center">
                                        <button 
                                            className="admin-expand-btn"
                                            onClick={() => {
                                                if (expandedReport === r.id) {
                                                    setExpandedReport(null);
                                                    setReplyMessage('');
                                                } else {
                                                    setExpandedReport(r.id);
                                                    setReplyMessage('');
                                                }
                                            }}
                                        >
                                            {expandedReport === r.id ? '▲ Hide' : '▼ View'}
                                        </button>
                                    </td>
                                </tr>
                                {expandedReport === r.id && (
                                    <tr className="character-sub-row">
                                        <td colSpan="5">
                                            <div className="report-details" style={{ padding: '20px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                                                {r.report_type === 'Bug' && (
                                                    <div style={{ marginBottom: '15px' }}>
                                                        <h4>Malfunctioning Feature:</h4>
                                                        <p style={{ background: 'rgba(255,255,255,0.05)', padding: '10px', borderRadius: '4px', wordBreak: 'break-word' }}>{r.feature || 'N/A'}</p>
                                                    </div>
                                                )}
                                                
                                                <div style={{ marginBottom: '15px' }}>
                                                    <h4>Description:</h4>
                                                    <p style={{ background: 'rgba(255,255,255,0.05)', padding: '10px', borderRadius: '4px', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{r.description}</p>
                                                </div>

                                                {r.report_type === 'Bug' && r.reproduction_steps && (
                                                    <div style={{ marginBottom: '15px' }}>
                                                        <h4>Steps to Reproduce:</h4>
                                                        <p style={{ background: 'rgba(255,255,255,0.05)', padding: '10px', borderRadius: '4px', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{r.reproduction_steps}</p>
                                                    </div>
                                                )}

                                                {r.status === 'pending' ? (
                                                    <div className="resolve-report-form" style={{ marginTop: '20px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px' }}>
                                                        <h4>Resolve Report</h4>
                                                        <p style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '10px' }}>
                                                            Write a completion message. This will be sent as a notification to <strong>{r.username}</strong> the next time they open the app.
                                                        </p>
                                                        <textarea 
                                                            value={replyMessage}
                                                            onChange={(e) => setReplyMessage(e.target.value)}
                                                            placeholder={`Thank you for reporting this...`}
                                                            style={{ width: '100%', minHeight: '80px', background: 'rgba(0,0,0,0.5)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', padding: '10px', borderRadius: '4px', marginBottom: '10px' }}
                                                        />
                                                        <button 
                                                            className="save-profile-btn"
                                                            onClick={() => handleResolve(r.id)}
                                                            disabled={resolvingId === r.id}
                                                            style={{ background: '#4CAF50' }}
                                                        >
                                                            {resolvingId === r.id ? 'Resolving...' : 'Mark as Resolved & Send Reply'}
                                                        </button>
                                                    </div>
                                                ) : (
                                                    <div style={{ marginTop: '15px', color: '#4CAF50' }}>
                                                        ✓ Resolved on {new Date(r.resolved_at).toLocaleString()}
                                                    </div>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                )}
                            </React.Fragment>
                        ))}
                    </tbody>
                </table>
            )}
        </section>
    );
};

export default AdminReports;
