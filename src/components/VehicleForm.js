// VehicleForm.js
import React, { useState } from 'react';
import './VehicleForm.css';

const VehicleForm = ({ onCancel }) => {
    const [make, setMake] = useState('');
    const [model, setModel] = useState('');
    const [year, setYear] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const vehicleData = { make, model, year };
        const accessToken = localStorage.getItem('accessToken'); // Retrieve the token
        console.log('Access Token:', accessToken); // Check the token value
    
        try {
            const response = await fetch('http://127.0.0.1:5000/vehicles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}` // Attach the token
                },
                body: JSON.stringify(vehicleData),
            });
    
            const data = await response.json();
            console.log('API Response:', data); // Debugging log
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to add vehicle');
            }

            alert(data.message || 'Vehicle added successfully');
            
            setMake('');
            setModel('');
            setYear('');
        } catch (error) {
            console.error('Error adding vehicle:', error);
            alert(`Failed to add vehicle: ${error.message || 'Unknown error'}`);
        }
    };    

    return (
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
