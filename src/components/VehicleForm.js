import React, { useState } from 'react';
import './VehicleForm.css';
import { useNavigate } from 'react-router-dom';  

//main vehicle form function to accept user input and send it to backend
const VehicleForm = ({ onCancel }) => {
    const [make, setMake] = useState('');
    const [model, setModel] = useState('');
    const [year, setYear] = useState('');

    // hook to navigate after successful form submission
    const navigate = useNavigate();  

    // set the url to local or prod based on the environment dynamically
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';

    //on submit form function to post user data to backend 
    const handleSubmit = async (e) => {
        e.preventDefault();

        const vehicleData = { make, model, year };
        //check if user is logged in through local storage access token
        const accessToken = localStorage.getItem('accessToken'); 
        if (!accessToken) {
            alert('Please log in again.');
            window.location.href = '/login';
            return;
        }

        try {
            const response = await fetch(`${baseUrl}/vehicles`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`, 
                },
                body: JSON.stringify(vehicleData),
            });

            const data = await response.json();
            console.log('API Response:', data);

            if (!response.ok) {
                if (response.status === 401) {
                    alert('Session expired. Please log in again.');
                    window.location.href = '/login';  
                    return;
                }
                throw new Error(data.error || 'Failed to add vehicle');
            }

            alert(data.message || 'Vehicle added successfully');

            setMake('');
            setModel('');
            setYear('');

            // Redirect to the /maintenance-records page after successful submission
            navigate('/maintenance-records');  
        } catch (error) {
            console.error('Error adding vehicle:', error);
            alert(`Failed to add vehicle: ${error.message || 'Unknown error'}`);
        }
    };

    return (
        //html component for vehicle form
        <div className="vehicle-form">
            <h2>Add Vehicle</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="make">Make:</label>
                    <input
                        type="text"
                        id="make"
                        value={make}
                        onChange={(e) => setMake(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="model">Model:</label>
                    <input
                        type="text"
                        id="model"
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="year">Year:</label>
                    <input
                        type="number"
                        id="year"
                        value={year}
                        onChange={(e) => setYear(e.target.value)}
                        required
                    />
                </div>
                <button type="button" className="cancel-button" onClick={onCancel}>
                    Cancel
                </button>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default VehicleForm;
