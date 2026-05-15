import React from 'react';
import '../../styles/NotificationHub.css';

const NotificationHub = ({ notifications, removeAlert, confirmData, onConfirmResponse }) => {
    const [inputValue, setInputValue] = React.useState('');

    // Reset input value when modal opens/closes
    React.useEffect(() => {
        if (confirmData?.isPrompt) {
            setInputValue(confirmData.defaultValue || '');
        }
    }, [confirmData]);

    const handleConfirm = () => {
        if (confirmData.isPrompt) {
            onConfirmResponse(inputValue);
        } else {
            onConfirmResponse(true);
        }
    };

    return (
        <React.Fragment>
            {/* Toast Notifications */}
            <div className="toast-container">
                {notifications.map(n => (
                    <div key={n.id} className={`toast-item ${n.type}`} onClick={() => removeAlert(n.id)}>
                        <div className="toast-content">
                            <span className="toast-icon">
                                {n.type === 'success' && '✓'}
                                {n.type === 'error' && '✕'}
                                {n.type === 'warning' && '⚠'}
                                {n.type === 'info' && 'ℹ'}
                                {n.type === 'loading' && <i className="fa-solid fa-spinner fa-spin"></i>}
                            </span>
                            <span className="toast-message">{n.message}</span>
                        </div>
                        <button className="toast-close">&times;</button>
                    </div>
                ))}
            </div>

            {/* Confirmation/Prompt Modal */}
            {confirmData && (
                <div className="confirm-overlay" onClick={() => onConfirmResponse(null)}>
                    <div className="confirm-modal" onClick={(e) => e.stopPropagation()}>
                        <div className="confirm-header">
                            <h3>{confirmData.isPrompt ? 'Entry Required' : 'Confirmation'}</h3>
                            <div className="modal-glow"></div>
                        </div>
                        <div className="confirm-body">
                            <p>{confirmData.message}</p>
                            {confirmData.isPrompt && (
                                <input 
                                    type="text" 
                                    className="prompt-input"
                                    value={inputValue}
                                    onChange={(e) => setInputValue(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleConfirm()}
                                    autoFocus
                                />
                            )}
                        </div>
                        <div className="confirm-footer">
                            <button className="confirm-cancel-btn" onClick={() => onConfirmResponse(null)}>
                                Cancel
                            </button>
                            <button className="confirm-confirm-btn" onClick={handleConfirm}>
                                Confirm
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </React.Fragment>
    );
};

export default NotificationHub;
