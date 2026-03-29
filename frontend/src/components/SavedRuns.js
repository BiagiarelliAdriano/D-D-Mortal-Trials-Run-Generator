import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import BackToTop from './common/BackToTop';
import '../styles/SavedRuns.css';

const SavedRuns = () => {
    const [runs, setRuns] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchRuns();
    }, []);

    const fetchRuns = async () => {
        setLoading(true);
        try {
            const token = sessionStorage.getItem('token');
            const response = await fetch('/api/runs', {
                headers: {
                    'Authorization': token ? `Bearer ${token}` : ''
                }
            });
            if (!response.ok) throw new Error('Failed to fetch saved runs');
            const data = await response.json();
            setRuns(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const deleteRun = async (e, id) => {
        e.stopPropagation();
        if (!window.confirm('Are you sure you want to delete this run?')) return;

        try {
            const token = sessionStorage.getItem('token');
            const response = await fetch(`/api/runs/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': token ? `Bearer ${token}` : ''
                }
            });
            if (!response.ok) throw new Error('Failed to delete run');
            setRuns(runs.filter(r => r.id !== id));
        } catch (err) {
            alert('Error deleting run: ' + err.message);
        }
    };

    const viewRun = (run) => {
        // We could either navigate to a specific view or store it in state
        // For now, let's navigate to RunGenerator with this data
        // But the RunGenerator usually fetches new ones. 
        // We'll update RunGenerator to accept data via state
        navigate('/run-generator', { state: { savedRunData: run.data } });
    };

    return (
        <div className="saved-runs-container">
            <header className="saved-runs-header">
                <button className="back-btn" onClick={() => navigate('/run-generator')}>
                    <i className="fa-solid fa-arrow-left"></i> Back to Generator
                </button>
                <h1 className="serif-text">My Saved Trials</h1>
            </header>

            {loading && (
                <div className="loading-state">
                    <i className="fa-solid fa-spinner fa-spin"></i>
                    <p>Retrieving your destiny...</p>
                </div>
            )}

            {error && <div className="error-message">{error}</div>}

            {!loading && runs.length === 0 && (
                <div className="empty-state">
                    <i className="fa-solid fa-ghost"></i>
                    <p>No runs found. Go forth and generate your first trial!</p>
                </div>
            )}

            <div className="runs-grid">
                {runs.map(run => (
                    <div key={run.id} className="run-summary-card" onClick={() => viewRun(run)}>
                        <div className="run-card-header">
                            <h3>{run.title}</h3>
                            <button className="delete-btn" onClick={(e) => deleteRun(e, run.id)} title="Delete Run">
                                <i className="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                        <div className="run-card-meta">
                            <span><i className="fa-solid fa-calendar-days"></i> {new Date(run.created_at).toLocaleDateString()}</span>
                            <span><i className="fa-solid fa-skull"></i> {run.data.encounters?.length || 0} Encounters</span>
                        </div>
                        <div className="run-card-preview">
                            {run.data.divine_blessing && (
                                <div className="blessing-preview">
                                    <strong>Blessing:</strong> {run.data.divine_blessing.name}
                                </div>
                            )}
                        </div>
                        <div className="view-overlay">
                            <span>Load Trial</span>
                        </div>
                    </div>
                ))}
            </div>
            <BackToTop />
        </div>
    );
};

export default SavedRuns;
