// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import NavBar from './components/NavBar';
import Dashboard from './components/Dashboard';
import VehicleAndMaintenanceRecords from './components/VehicleAndMaintenanceRecords';
import Profile from './components/Profile';
import Reports from './components/Reports';
import Register from './components/Register';
import Login from './components/Login';
import Logout from './components/Logout';
import ProtectedRoute from './components/ProtectedRoute';
import 'font-awesome/css/font-awesome.min.css';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('accessToken'));

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        setIsAuthenticated(!!token);
    }, []);

    const handleLogin = (accessToken, idToken) => {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('idToken', idToken);
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('idToken');
        setIsAuthenticated(false);
    };

    return (
        <Router>
            <div>
                <NavBar />
                <Routes>
                    <Route path="/" element={<Navigate to="/login" />} />
                    <Route path="/login" element={<Login onLogin={handleLogin} />} />
                    <Route path="/register" element={<Register />} />

                    {/* Protected Routes */}
                    <Route path="/dashboard" element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <Dashboard />
                        </ProtectedRoute>
                    } />
                    <Route path="/maintenance-records" element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <VehicleAndMaintenanceRecords />
                        </ProtectedRoute>
                    } />
                    <Route path="/reports" element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <Reports />
                        </ProtectedRoute>
                    } />
                    <Route path="/profile" element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <Profile />
                        </ProtectedRoute>
                    } />

                    {/* Logout Route */}
                    <Route path="/logout" element={<Logout onLogout={handleLogout} />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
