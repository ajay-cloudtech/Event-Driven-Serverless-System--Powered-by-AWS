// src/components/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
    
            const data = await response.json();
            if (response.ok) {
                // Save the tokens and username in local storage
                localStorage.setItem('accessToken', data.AccessToken);
                localStorage.setItem('idToken', data.IdToken);
                localStorage.setItem('userId', data.Username);  // Save user ID
    
                // Log tokens and user ID to confirm they're set
                console.log('Access Token:', localStorage.getItem('accessToken'));
                console.log('ID Token:', localStorage.getItem('idToken'));
                console.log('User ID:', localStorage.getItem('userId'));  // Log user ID
    
                // Update the authentication state in App.js with tokens and user ID
                onLogin(data.AccessToken, data.IdToken, data.Username); 
                navigate('/dashboard'); // Redirect after successful login
            } else {
                setMessage(data.error || 'Login failed');
            }
        } catch (error) {
            setMessage('Login failed: ' + error.message);
        }
    };

    return (
        <div className="login">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <div>
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit">Login</button>
            </form>
            {message && <p className="error-message">{message}</p>}
            <p>
                <a href="/forgot-password">Forgot Password?</a>
            </p>
            <p>
                Don't have an account? <a href="/register">Register</a>
            </p>
        </div>
    );
};

export default Login;
