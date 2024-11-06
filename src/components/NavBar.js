import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css'; // Optional: Add this if you want to style it

const NavBar = () => {
    return (
        <nav className="navbar">
            <h1 class = 'h1'>CarCare🚗</h1>
            <ul>
                <li>
                    <Link to="/dashboard">Quick Actions</Link> {/* Link to Dashboard */}
                </li>
                <li>
                    <Link to="/maintenance-records">Vehicle | Maintenance</Link> {/* Link to Vehicle & Maintenance Records */}
                </li>
                <li>
                    <Link to="/reports">Reports</Link> {/* Link to Reports */}
                </li>
                <li>
                    <Link to="/profile">Profile</Link> {/* Link to Profile */}
                </li>
                <li>
                    <Link to="/logout">Logout</Link> {/* Logout link */}
                </li>
            </ul>
        </nav>
    );
};

export default NavBar;
