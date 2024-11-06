// src/components/Register.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate
import './Register.css';  // Import the CSS file

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();  // Initialize useNavigate

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, email }),
            });

            const data = await response.json();
            setMessage(data.message || data.error);

            // If registration is successful, navigate to login page
            if (data.message) {
                setTimeout(() => {
                    navigate('/login');  // Redirect to the login page
                }, 2000); // Optional: Delay the redirect for 2 seconds
            }
        } catch (error) {
            setMessage('Registration failed: ' + error.message);
        }
    };

    return (
        <div className="register"> {/* Apply the register class for styling */}
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
                <div>
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
            <p>
                Already a user? <a href="/login">Login</a>  {/* Hyperlink to the login page */}
            </p>
        </div>
    );
};

export default Register;
