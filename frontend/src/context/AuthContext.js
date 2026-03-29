import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(sessionStorage.getItem('token') || null);
    const [loading, setLoading] = useState(true);

    const logout = useCallback(() => {
        setToken(null);
        setUser(null);
        sessionStorage.removeItem('token');
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
                logout();
            }
        } catch (error) {
            console.error("Token verification failed:", error);
            logout();
        } finally {
            setLoading(false);
        }
    }, [logout]);

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
    };

    const value = {
        user,
        token,
        loading,
        login,
        logout,
        isAdmin: user?.is_admin || false
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
