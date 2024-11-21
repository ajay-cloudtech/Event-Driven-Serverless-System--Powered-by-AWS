import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

// main login function to POST user input details to /login route in the backend
const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    // set the url to local or prod based on the environment dynamically
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';
    
    // on click handler - passing user input details to backend route 
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${baseUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
    
            const data = await response.json();
            if (response.ok) {
                // save the tokens and username in the local storage
                localStorage.setItem('accessToken', data.AccessToken);
                localStorage.setItem('idToken', data.IdToken);
                localStorage.setItem('userId', data.Username); 
    
                // updating the authentication state in App.js with tokens and user id
                onLogin(data.AccessToken, data.IdToken, data.Username); 
                // navigate to dashboard after successful login
                navigate('/dashboard'); 
            } else {
                setMessage(data.error || 'Login failed');
            }
        } catch (error) {
            setMessage('Login failed: ' + error.message);
        }
    };

    return (
        //html component for login page
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
