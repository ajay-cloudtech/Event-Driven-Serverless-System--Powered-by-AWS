// src/components/Logout.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = ({ onLogout }) => {
    const navigate = useNavigate();

    useEffect(() => {
        // Clear tokens from localStorage
        localStorage.removeItem('accessToken');
        localStorage.removeItem('idToken');

        // Call the onLogout function passed from App.js
        onLogout();

        // Redirect to login page
        navigate('/login');
    }, [navigate, onLogout]);

    return null; // No UI needed for logout
};

export default Logout;
