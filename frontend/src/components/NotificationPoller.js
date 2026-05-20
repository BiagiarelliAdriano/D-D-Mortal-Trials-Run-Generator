import { useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';

const NotificationPoller = () => {
    const { token, user } = useAuth();
    const { confirm } = useNotification();

    const checkNotifications = useCallback(async () => {
        if (!token || !user) return;

        try {
            const res = await fetch('/api/users/notifications', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!res.ok) return;

            const notifications = await res.json();
            
            // For each unread notification, display it then mark as read
            for (const notif of notifications) {
                // Show standard confirm to ensure they acknowledge it
                await confirm(`New Message from Admin:\n\n${notif.message}`);
                
                // Mark as read
                await fetch(`/api/users/notifications/${notif.id}/read`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            }
        } catch (err) {
            console.error("Error checking notifications:", err);
        }
    }, [token, user, confirm]);

    useEffect(() => {
        // Check once on mount/auth
        checkNotifications();
        
        // And optionally poll every few minutes
        const interval = setInterval(checkNotifications, 5 * 60 * 1000);
        return () => clearInterval(interval);
    }, [checkNotifications]);

    return null; // This is a logic-only component
};

export default NotificationPoller;
