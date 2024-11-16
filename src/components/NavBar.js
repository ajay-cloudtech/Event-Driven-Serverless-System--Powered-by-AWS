import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './NavBar.css'; // Optional: Add this if you want to style it

const NavBar = () => {
    const accessToken = localStorage.getItem('accessToken'); // Check if the user is logged in by the presence of an access token

    return (
        <nav className="navbar">
            <h1 className='h1'>CarCare🚗</h1>
            <ul>
                {accessToken && (
                    <>
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
                    </>
                )}
            </ul>
        </nav>
    );
};

export default NavBar;
