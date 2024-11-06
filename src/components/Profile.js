// src/components/Profile.js
import React, { useEffect, useState } from 'react';
import './Profile.css';

const Profile = () => {
    const [userData, setUserData] = useState(null);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                setMessage('Please log in to see your profile.');
                return;
            }
            try {
                const response = await fetch('http://localhost:5000/profile', {
                    headers: {
                        'Authorization': `Bearer ${token}`,  // Include 'Bearer' prefix
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setUserData(data);
                } else {
                    setMessage('Failed to fetch user data');
                }
            } catch (error) {
                setMessage('Error fetching user data: ' + error.message);
            }
        };

        fetchUserData();
    }, []);

    return (
        <div className="profile">
            <h1>Profile</h1>
            {message && <p className="error-message">{message}</p>}
            {userData ? (
                <div className="user-info">
                    <p><strong>Username:</strong> {userData.Username}</p>
                    <p><strong>Email:</strong> {userData.UserAttributes.find(attr => attr.Name === 'email')?.Value}</p>
                </div>
            ) : (
                !message && <p>Loading profile data...</p>
            )}
        </div>
    );
};

export default Profile;
