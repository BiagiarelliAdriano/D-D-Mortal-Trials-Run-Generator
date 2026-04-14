import React, { createContext, useContext, useState, useCallback } from 'react';
import NotificationHub from '../components/common/NotificationHub';

const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
    const [notifications, setNotifications] = useState([]);
    const [confirmState, setConfirmState] = useState(null); // { message, resolve, isPrompt, defaultValue }

    const removeAlert = useCallback((id) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    }, []);

    /**
     * Add a toast notification
     * @param {string} message 
     * @param {string} type - 'success' | 'error' | 'info' | 'warning'
     * @param {number} duration - ms before auto-dismiss
     */
    const addAlert = useCallback((message, type = 'info', duration = 5000) => {
        const id = Date.now() + Math.random();
        setNotifications(prev => [...prev, { id, message, type }]);

        if (duration) {
            setTimeout(() => {
                removeAlert(id);
            }, duration);
        }
    }, [removeAlert]);

    /**
     * Show a confirmation modal or prompt
     * @param {string} message 
     * @param {boolean} isPrompt
     * @param {string} defaultValue
     * @returns {Promise<any>}
     */
    const confirm = useCallback((message, isPrompt = false, defaultValue = '') => {
        return new Promise((resolve) => {
            setConfirmState({ message, resolve, isPrompt, defaultValue });
        });
    }, []);

    const prompt = useCallback((message, defaultValue = '') => {
        return confirm(message, true, defaultValue);
    }, [confirm]);

    const handleConfirmResponse = (value) => {
        if (confirmState) {
            confirmState.resolve(value);
            setConfirmState(null);
        }
    };

    return (
        <NotificationContext.Provider value={{ addAlert, confirm, prompt }}>
            {children}
            <NotificationHub 
                notifications={notifications} 
                removeAlert={removeAlert}
                confirmData={confirmState}
                onConfirmResponse={handleConfirmResponse}
            />
        </NotificationContext.Provider>
    );
};

export const useNotification = () => {
    const context = useContext(NotificationContext);
    if (!context) {
        throw new Error('useNotification must be used within a NotificationProvider');
    }
    return context;
};
