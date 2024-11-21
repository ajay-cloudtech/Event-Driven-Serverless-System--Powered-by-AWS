import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

//main logout function 
const Logout = ({ onLogout }) => {
    const navigate = useNavigate();

    useEffect(() => {
        // clear tokens from localStorage
        localStorage.removeItem('accessToken');
        localStorage.removeItem('idToken');
        localStorage.removeItem('userId');

        // call the onLogout function passed from App.js
        onLogout();

        // redirect to login page
        navigate('/login');
    }, [navigate, onLogout]);

    //no UI needed for logout
    return null; 
};

export default Logout;
