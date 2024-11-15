import React, { useState, useEffect } from 'react';
import './AddMaintenanceForm.css';
import { useNavigate } from 'react-router-dom';  // Import the useNavigate hook

const AddMaintenanceRecord = ({ onCancel }) => {
    const [vehicles, setVehicles] = useState([]);
    const [selectedVehicle, setSelectedVehicle] = useState('');
    const [maintenanceType, setMaintenanceType] = useState('');
    const [mileage, setMileage] = useState('');
    const [lastServiceDate, setLastServiceDate] = useState('');

    const maintenanceTypes = ['Comprehensive Service'];

    const navigate = useNavigate();  // Hook to navigate after successful form submission

    // Fetch vehicles from the backend on component mount
    useEffect(() => {
        const fetchVehicles = async () => {
            const accessToken = localStorage.getItem('accessToken');
            try {
                const response = await fetch('http://localhost:5000/vehiclesList', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });
                
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Unauthorized: Please log in again.');
                    }
                    throw new Error('Failed to fetch vehicles: ' + response.statusText);
                }

                const data = await response.json();
                setVehicles(data);
            } catch (error) {
                console.error('Error fetching vehicles:', error);
                alert(`Error fetching vehicles: ${error.message}`);
            }
        };
    
        fetchVehicles();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedVehicle || !maintenanceType || !mileage || !lastServiceDate) {
            alert('Please fill out all required fields.');
            return;
        }

        const maintenanceRecord = {
            vehicle_id: selectedVehicle,
            maintenance_type: maintenanceType,
            mileage: mileage,
            last_service_date: lastServiceDate,
        };

        try {
            const accessToken = localStorage.getItem('accessToken');
            const response = await fetch('http://localhost:5000/maintenance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
                body: JSON.stringify(maintenanceRecord),
            });

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Unauthorized: Please log in again.');
                }
                throw new Error('Failed to add maintenance record: ' + response.statusText);
            }

            // Clear the form after successful submission
            setSelectedVehicle('');
            setMaintenanceType('');
            setMileage('');
            setLastServiceDate('');
            window.alert('Maintenance record added successfully!');

            // Redirect to the /maintenance-records page after successful submission
            navigate('/maintenance-records');  // Redirect to maintenance records page
        } catch (error) {
            console.error('Error adding maintenance record:', error);
            alert(`Failed to add maintenance record: ${error.message}`);
        }
    };

    return (
        <div className="add-maintenance-form">
            <h2>Add Maintenance Record</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="vehicle">Vehicle:</label>
                    <select
                        id="vehicle"
                        value={selectedVehicle}
                        onChange={(e) => setSelectedVehicle(e.target.value)}
                        required
                    >
                        <option value="">Select a vehicle</option>
                        {Array.isArray(vehicles) && vehicles.length > 0 ? (
                            vehicles.map((vehicle) => (
                                <option key={vehicle.vehicle_id} value={vehicle.vehicle_id}>
                                    {vehicle.display_name}
                                </option>
                            ))
                        ) : (
                            <option value="" disabled>No vehicles available</option>
                        )}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="maintenanceType">Maintenance Type:</label>
                    <select
                        id="maintenanceType"
                        value={maintenanceType}
                        onChange={(e) => setMaintenanceType(e.target.value)}
                        required
                    >
                        <option value="">Select maintenance type</option>
                        {maintenanceTypes.map((type, index) => (
                            <option key={index} value={type}>
                                {type}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="mileage">Mileage:</label>
                    <input
                        type="number"
                        id="mileage"
                        value={mileage}
                        onChange={(e) => setMileage(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="lastServiceDate">Last Service Date:</label>
                    <input
                        type="date"
                        id="lastServiceDate"
                        value={lastServiceDate}
                        onChange={(e) => setLastServiceDate(e.target.value)}
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

export default AddMaintenanceRecord;
