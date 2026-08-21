import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from "../context/AuthContext";
import { useNotification } from "../context/NotificationContext";
import BackToTop from './common/BackToTop';
import UserProfilePill from './UserProfilePill';
import '../styles/SavedRuns.css';
import API_BASE_URL from '../config';

const SavedRuns = () => {
    const [runs, setRuns] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { token } = useAuth();
    const { addAlert, confirm } = useNotification();
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState("");
    const [editMode, setEditMode] = useState(false);
    const [editingTitles, setEditingTitles] = useState({});
    const [savingTitles, setSavingTitles] = useState({});

    const fetchRuns = useCallback(async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/runs`, {
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
    }, [token]);

    useEffect(() => {
        fetchRuns();
    }, [fetchRuns]);

    const deleteRun = async (e, id) => {
        e.stopPropagation();
        if (!(await confirm('Are you sure you want to delete this run?'))) return;

        try {
            const response = await fetch(`${API_BASE_URL}/api/runs/${id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': token ? `Bearer ${token}` : ''
                }
            });
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.error || 'Failed to delete run');
            }
            setRuns(runs.filter(r => r.id !== id));
            addAlert('Run deleted successfully', 'success');
        } catch (err) {
            addAlert('Error deleting run: ' + err.message, 'error');
        }
    };

    const updateRunTitle = async (id) => {
        const newTitle = editingTitles[id]?.trim();
        if (!newTitle) {
            addAlert('Run title cannot be empty.', 'error');
            return;
        }
        if (newTitle.length > 24) {
            addAlert('Run title cannot be longer than 24 characters.', 'error');
            return;
        }
        const currentRun = runs.find(run => run.id === id);

        // Nothing changed, so there is nothing to save.
        if (currentRun && currentRun.title === newTitle) {
            setEditingTitles(prev => {
                const updated = { ...prev };
                delete updated[id];
                return updated;
            });
            return;
        }
        setSavingTitles(prev => ({
            ...prev,
            [id]: true
        }));

        try {
            const response = await fetch(`${API_BASE_URL}/api/runs/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : ''
                },
                body: JSON.stringify({
                    title: newTitle
                })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Failed to rename run');
            }

            setRuns(prevRuns =>
                prevRuns.map(run =>
                    run.id === id
                        ? { ...run, title: data.title }
                        : run
                )
            );

            setEditingTitles(prev => {
                const updated = { ...prev };
                delete updated[id];
                return updated;
            });
            addAlert('Run renamed successfully.', 'success');
        } catch (err) {
            addAlert(err.message, 'error');
        } finally {
            setSavingTitles(prev => {
                const updated = { ...prev };
                delete updated[id];
                return updated;
            });
        }
    };

    const handleTitleChange = (id, value) => {
        const currentRun = runs.find(run => run.id === id);
        setEditingTitles(prev => {
            const updated = { ...prev };

            // If the user changed the title back to its original value,
            // there is no longer an unsaved change for this Run.
            if (currentRun && value === currentRun.title) {
                delete updated[id];
            } else {
                updated[id] = value;
            }

            return updated;
        });
    };

    const cancelTitleEdit = (id) => {
        setEditingTitles(prev => {
            const updated = { ...prev };
            delete updated[id];
            return updated;
        });
    };

    const handleEditModeToggle = async () => {
        // If we're currently editing, simply enter Edit Mode.
        if (!editMode) {
            setEditMode(true);
            return;
        }

        // Check whether there are any unsaved title changes.
        const hasUnsavedChanges = Object.keys(editingTitles).length > 0;

        // No unsaved changes, so we can safely leave Edit Mode.
        if (!hasUnsavedChanges) {
            setEditMode(false);
            return;
        }

        // Ask the user whether they want to discard their unsaved changes.
        const shouldDiscard = await confirm(
            'Oops! Looks like you have some unsaved changes. Would you still like to leave Edit Mode and discard them?'
        );

        // User chose to keep editing.
        if (!shouldDiscard) {
            return;
        }

        // User chose to discard the unsaved changes.
        setEditingTitles({});
        setEditMode(false);
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
                <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                    <button className="back-btn" onClick={() => navigate(-1)}>
                        <i className="fa-solid fa-arrow-left"></i> Back
                    </button>
                    <UserProfilePill />
                    <button
                        className={`edit-runs-btn ${editMode ? 'active' : ''}`}
                        onClick={handleEditModeToggle}
                    >
                        <i className={`fa-solid ${editMode ? 'fa-check' : 'fa-pen-to-square'}`}></i>
                        {editMode ? 'Done Editing' : 'Edit Runs'}
                    </button>
                </div>
                <h1 className="serif-text">My Saved Trials</h1>
                <div className="search-wrapper" style={{ margin: '10px 0', maxWidth: '300px' }}>
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Recall a legend..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <i className="fa-solid fa-magnifying-glass"></i>
                </div>
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
                {runs
                    .filter(run => !searchTerm || run.title.toLowerCase().includes(searchTerm.toLowerCase()))
                    .map(run => (
                        <div
                            key={run.id}
                            className={`run-summary-card ${editMode ? 'editing' : ''}`}
                            onClick={() => {
                                if (!editMode) {
                                    viewRun(run);
                                }
                            }}
                        >
                            <div className="run-card-header">
                                {editMode ? (
                                    <div className="run-title-editor">
                                        <input
                                            type="text"
                                            value={
                                                editingTitles[run.id] !== undefined
                                                    ? editingTitles[run.id]
                                                    : run.title
                                            }
                                            maxLength={24}
                                            onChange={(e) => handleTitleChange(run.id, e.target.value)}
                                            onClick={(e) => e.stopPropagation()}
                                            onKeyDown={(e) => {
                                                if (e.key === 'Enter') {
                                                    e.preventDefault();
                                                    updateRunTitle(run.id);
                                                }

                                                if (e.key === 'Escape') {
                                                    e.preventDefault();
                                                    cancelTitleEdit(run.id);
                                                }
                                            }}
                                            className="run-title-input"
                                            disabled={savingTitles[run.id]}
                                        />

                                        <button
                                            className="save-title-btn"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                updateRunTitle(run.id);
                                            }}
                                            disabled={
                                                savingTitles[run.id] ||
                                                !editingTitles[run.id]?.trim()
                                            }
                                            title="Save title"
                                        >
                                            {savingTitles[run.id] ? (
                                                <i className="fa-solid fa-spinner fa-spin"></i>
                                            ) : (
                                                <i className="fa-solid fa-floppy-disk"></i>
                                            )}
                                        </button>
                                    </div>
                                ) : (
                                    <h3>{run.title}</h3>
                                )}

                                <button
                                    className="delete-btn"
                                    onClick={(e) => deleteRun(e, run.id)}
                                    title="Delete Run"
                                >
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
                            {!editMode && (
                                <div className="view-overlay">
                                    <span>Load Trial</span>
                                </div>
                            )}
                        </div>
                    ))}
            </div>
            <BackToTop />
        </div>
    );
};

export default SavedRuns;
