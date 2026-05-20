import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import '../styles/ReportPage.css';

const ReportPage = () => {
    const [reportType, setReportType] = useState('Feedback');
    const [feature, setFeature] = useState('');
    const [description, setDescription] = useState('');
    const [reproductionSteps, setReproductionSteps] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    const { token } = useAuth();
    const { addAlert } = useNotification();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        const payload = {
            report_type: reportType,
            description: description,
            feature: reportType === 'Bug' ? feature : null,
            reproduction_steps: reportType === 'Bug' ? reproductionSteps : null
        };

        try {
            const response = await fetch('/api/reports', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.error || 'Failed to submit report');
            }

            addAlert(`${reportType} submitted successfully! Thank you.`, "success");
            // Clear form
            setDescription('');
            setFeature('');
            setReproductionSteps('');
        } catch (err) {
            addAlert(err.message, "error");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="report-page-container dnd-theme">
            <header className="report-header">
                <button className="close-window-btn" onClick={() => window.close()}>
                    <i className="fa-solid fa-xmark"></i> Close Window
                </button>
                <h1>Help Us Improve</h1>
                <p>Share your thoughts or let us know if something isn't working as intended.</p>
            </header>

            <main className="report-content">
                <div className="report-type-toggle">
                    <button 
                        className={`toggle-btn ${reportType === 'Feedback' ? 'active' : ''}`}
                        onClick={() => setReportType('Feedback')}
                        type="button"
                    >
                        <i className="fa-regular fa-comment"></i> Submit Feedback
                    </button>
                    <button 
                        className={`toggle-btn ${reportType === 'Bug' ? 'active' : ''}`}
                        onClick={() => setReportType('Bug')}
                        type="button"
                    >
                        <i className="fa-solid fa-bug"></i> Report a Bug
                    </button>
                </div>

                <form className="report-form" onSubmit={handleSubmit}>
                    {reportType === 'Bug' && (
                        <div className="form-group">
                            <label>Feature Malfunctioning <span className="required">*</span></label>
                            <input 
                                type="text" 
                                value={feature}
                                onChange={(e) => setFeature(e.target.value)}
                                placeholder="e.g., Character Sheet Level Up, Run Generator"
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>{reportType === 'Feedback' ? 'Your Feedback' : 'Bug Description'} <span className="required">*</span></label>
                        <textarea 
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder={reportType === 'Feedback' 
                                ? "What do you like? What could be better? Any new feature ideas?" 
                                : "Describe what happened versus what you expected to happen."}
                            rows={5}
                            required
                        />
                    </div>

                    {reportType === 'Bug' && (
                        <div className="form-group">
                            <label>Steps to Reproduce <span className="required">*</span></label>
                            <textarea 
                                value={reproductionSteps}
                                onChange={(e) => setReproductionSteps(e.target.value)}
                                placeholder="1. Go to...\n2. Click on...\n3. See error..."
                                rows={5}
                                required
                            />
                        </div>
                    )}

                    <button 
                        type="submit" 
                        className="submit-report-btn"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Submitting...' : `Submit ${reportType}`}
                    </button>
                </form>
            </main>
        </div>
    );
};

export default ReportPage;
