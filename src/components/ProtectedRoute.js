import React from 'react';
import { Navigate } from 'react-router-dom';

// protects different routes and defaults to login page if user is not logged in
const ProtectedRoute = ({ isAuthenticated, children }) => {
    return isAuthenticated ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
