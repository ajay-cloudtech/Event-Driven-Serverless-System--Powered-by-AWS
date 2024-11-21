import React, { useEffect, useState } from 'react';
import './Profile.css';

//main profile function to fetch user details from backend 
const Profile = () => {
    const [userData, setUserData] = useState(null);
    const [message, setMessage] = useState('');

    //check user is logged in or not with access token in local storage 
    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                setMessage('Please log in to see your profile.');
                return;
            }
            
            // set the url to local or prod based on the environment dynamically
            const baseUrl = process.env.NODE_ENV === 'production'
                ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
                : 'http://localhost:5000';

            try {
                const response = await fetch(`${baseUrl}/profile`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,  
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
        //html component for profile page
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
