import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getDeviceFingerprint } from '../utils/deviceFingerprint';
import API_BASE_URL from '../config';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [hasUnlimitedAccess, setHasUnlimitedAccess] = useState(false);
    const [autoSaveGeneratedRuns, setAutoSaveGeneratedRuns] = useState(false);
    const [token, setToken] = useState(() => {
        const sessionToken = sessionStorage.getItem('token');
        if (sessionToken) return sessionToken;
        
        const localToken = localStorage.getItem('token');
        if (localToken) {
            // Copy it to this tab's isolated session so it can diverge later if needed
            sessionStorage.setItem('token', localToken);
            return localToken;
        }
        return null;
    });
    const [loading, setLoading] = useState(true);

    const logout = useCallback(() => {
        setToken(null);
        setUser(null);
        setHasUnlimitedAccess(false);
        // Explicit logout: clear the token and the reauth flag, but intentionally
        // KEEP device_fingerprint so that re-logging in on the same device
        // after a voluntary logout does NOT trigger the security question challenge.
        sessionStorage.removeItem('token');
        localStorage.removeItem('token'); // Clears the "remember me" globally
        localStorage.removeItem('needs_reauth');
    }, []);

    const loadAutoSavePreference = useCallback(async (currentToken) => {
        try {
            const response = await fetch(
                `${API_BASE_URL}/api/user/auto-save-generated-runs`,
                {
                    headers: {
                        'Authorization': `Bearer ${currentToken}`
                    }
                }
            );
            if (response.ok) {
                const data = await response.json();
                setAutoSaveGeneratedRuns(data.auto_save_generated_runs);
            }
        } catch (error) {
            console.error('Failed to load auto-save preference:', error);
        }
    }, []);

    const toggleAutoSaveGeneratedRuns = async () => {
        if (!token) return;
        const newValue = !autoSaveGeneratedRuns;
        try {
            const response = await fetch(
                `${API_BASE_URL}/api/user/auto-save-generated-runs`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        auto_save_generated_runs: newValue
                    })
                }
            );
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Failed to update auto-save preference');
            }
            setAutoSaveGeneratedRuns(data.auto_save_generated_runs);
        } catch (error) {
            console.error('Failed to update auto-save preference:', error);
            throw error;
        }
    };

    const verifyToken = useCallback(async (currentToken) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setUser(data.user);
                const accessResponse = await fetch(`${API_BASE_URL}/api/auth/access-status`, {
                    headers: {
                        'Authorization': `Bearer ${currentToken}`
                    }
                });

                if (accessResponse.ok) {
                    const accessData = await accessResponse.json();
                    setHasUnlimitedAccess(accessData.has_unlimited_access);
                }
                await loadAutoSavePreference(currentToken);
            } else {
                // JWT expired or invalid — flag this device for a security challenge
                // on the next login attempt. We keep device_fingerprint so the system
                // knows this is the same device (but the token is gone / stale).
                localStorage.setItem('needs_reauth', 'true');
                setToken(null);
                setUser(null);
                sessionStorage.removeItem('token');
            }
        } catch (error) {
            // Network error — clear session silently without flagging reauth,
            // since the failure may be transient rather than a real expiry.
            console.error('Token verification failed:', error);
            setToken(null);
            setUser(null);
            sessionStorage.removeItem('token');
        } finally {
            setLoading(false);
        }
    }, [loadAutoSavePreference]);

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
        sessionStorage.setItem('token', newToken);
        localStorage.setItem('token', newToken); // Sets the "remember me" for future tabs
        // Trust this device — store its fingerprint and clear the reauth flag.
        // From this point on, re-logins on this same browser won't require the
        // security question until the token expires or a different device is detected.
        localStorage.setItem('device_fingerprint', getDeviceFingerprint());
        localStorage.removeItem('needs_reauth');
    };

    const requestRecovery = async (username, requestType) => {
        const response = await fetch(`${API_BASE_URL}/api/auth/recovery-request`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, request_type: requestType })
        });
        return await response.json();
    };

    const getRecoveryRequests = async (masterKey) => {
        const response = await fetch(`${API_BASE_URL}/api/admin/recovery-requests`, {
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
        const response = await fetch(`${API_BASE_URL}/api/admin/recovery-resolve`, {
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
        hasUnlimitedAccess,
        autoSaveGeneratedRuns,
        toggleAutoSaveGeneratedRuns,
        patreonConnected: user?.patreon_connected || false,
        patreonTier: user?.patreon_tier || null,
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
