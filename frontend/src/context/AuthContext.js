import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getDeviceFingerprint } from '../utils/deviceFingerprint';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token') || null);
    const [loading, setLoading] = useState(true);

    const logout = useCallback(() => {
        setToken(null);
        setUser(null);
        // Explicit logout: clear the token and the reauth flag, but intentionally
        // KEEP device_fingerprint so that re-logging in on the same device
        // after a voluntary logout does NOT trigger the security question challenge.
        localStorage.removeItem('token');
        localStorage.removeItem('needs_reauth');
    }, []);

    const verifyToken = useCallback(async (currentToken) => {
        try {
            const response = await fetch('/api/auth/verify', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setUser(data.user);
            } else {
                // JWT expired or invalid — flag this device for a security challenge
                // on the next login attempt. We keep device_fingerprint so the system
                // knows this is the same device (but the token is gone / stale).
                localStorage.setItem('needs_reauth', 'true');
                setToken(null);
                setUser(null);
                localStorage.removeItem('token');
            }
        } catch (error) {
            // Network error — clear session silently without flagging reauth,
            // since the failure may be transient rather than a real expiry.
            console.error('Token verification failed:', error);
            setToken(null);
            setUser(null);
            localStorage.removeItem('token');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (token) {
            verifyToken(token);
        } else {
            setLoading(false);
        }
    }, [token, verifyToken]);

    const login = (newToken, userData) => {
        setToken(newToken);
        setUser(userData);
        localStorage.setItem('token', newToken);
        // Trust this device — store its fingerprint and clear the reauth flag.
        // From this point on, re-logins on this same browser won't require the
        // security question until the token expires or a different device is detected.
        localStorage.setItem('device_fingerprint', getDeviceFingerprint());
        localStorage.removeItem('needs_reauth');
    };

    const requestRecovery = async (username, requestType) => {
        const response = await fetch('/api/auth/recovery-request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, request_type: requestType })
        });
        return await response.json();
    };

    const getRecoveryRequests = async (masterKey) => {
        const response = await fetch('/api/admin/recovery-requests', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ master_key: masterKey })
        });
        return await response.json();
    };

    const resolveRecovery = async (requestId, action, masterKey, extraData = {}) => {
        const response = await fetch('/api/admin/recovery-resolve', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                request_id: requestId, 
                action, 
                master_key: masterKey,
                ...extraData 
            })
        });
        return await response.json();
    };

    const value = {
        user,
        token,
        loading,
        login,
        logout,
        isAdmin: user?.is_admin || false,
        requestRecovery,
        getRecoveryRequests,
        resolveRecovery
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
