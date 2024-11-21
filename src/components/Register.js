import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  
import './Register.css';  

// main register function to POST user input data to /register route in the backend
const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();  

    // on click handler - passing user input details to backend route 
    const handleRegister = async (e) => {
        e.preventDefault();

        // set the url to local or prod based on the environment dynamically
        const baseUrl = process.env.NODE_ENV === 'production'
            ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
            : 'http://localhost:5000';

        try {
            const response = await fetch(`${baseUrl}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, email }),
            });

            const data = await response.json();
            setMessage(data.message || data.error);

            // if registration is successful - navigate to login page
            if (data.message) {
                setTimeout(() => {
                    navigate('/login');  
                }, 2000); 
            }
        } catch (error) {
            setMessage('Registration failed: ' + error.message);
        }
    };

    return (
        //html component for register page
        <div className="register"> 
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
                <div>
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
            <p>
                Already a user? <a href="/login">Login</a>  
            </p>
        </div>
    );
};

export default Register;
