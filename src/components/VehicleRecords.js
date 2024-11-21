import React, { useEffect } from 'react';
import './VehicleAndMaintenanceRecords.css';

// function to fetch and display vehicles data on frontend
const VehicleRecords = ({ vehicles, setVehicles, setError }) => {
    // set the url to local or prod based on the environment dynamically
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';

    // checks for access token in local storage to get user specific data from vehicles table
    useEffect(() => {
        const fetchVehicles = async () => {
            try {
                const accessToken = localStorage.getItem('accessToken'); 
                const response = await fetch(`${baseUrl}/vehicles`, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}` 
                    }
                });

                if (!response.ok) throw new Error('Network response was not ok');

                const data = await response.json();

                if (Array.isArray(data)) {
                    setVehicles(data); 
                } else {
                    console.error('Expected an array but got:', data);
                    setVehicles([]); 
                }
            } catch (error) {
                console.error('Error fetching vehicles:', error);
                setError('Error fetching vehicles');
            }
        };

        fetchVehicles();
    }, [setVehicles, setError]); 

    //edit function for vehicles data on the frontend
    const handleEditVehicle = (vehicleId) => {
        const updatedVehicles = vehicles.map(vehicle => {
            if (vehicle.vehicle_id === vehicleId) {
                return { ...vehicle, isEditing: true, originalData: { ...vehicle } };
            }
            return vehicle;
        });
        setVehicles(updatedVehicles);
    };

    // input change function while edit is active
    const handleInputChange = (vehicleId, field, value) => {
        const updatedVehicles = vehicles.map(vehicle => {
            if (vehicle.vehicle_id === vehicleId) {
                return { ...vehicle, [field]: value };
            }
            return vehicle;
        });
        setVehicles(updatedVehicles);
    };

    // function to save edit details and put the updated data in vehicles table in the backend
    const handleSaveVehicle = async (vehicleId) => {
        const vehicleToSave = vehicles.find(vehicle => vehicle.vehicle_id === vehicleId);
        try {
            const accessToken = localStorage.getItem('accessToken'); 
            const response = await fetch(`${baseUrl}/vehicles/${vehicleId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}` 
                },
                body: JSON.stringify({
                    make: vehicleToSave.make,
                    model: vehicleToSave.model,
                    year: vehicleToSave.year,
                }),
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const updatedVehicles = vehicles.map(vehicle =>
                vehicle.vehicle_id === vehicleId ? { ...vehicle, isEditing: false } : vehicle
            );
            setVehicles(updatedVehicles);
        } catch (error) {
            console.error('Error saving vehicle:', error);
            setError('Error saving vehicle');
        }
    };

    //function to cancel the edit request
    const handleCancelVehicle = (vehicleId) => {
        const updatedVehicles = vehicles.map(vehicle =>
            vehicle.vehicle_id === vehicleId
                ? { ...vehicle, ...vehicle.originalData, isEditing: false }
                : vehicle
        );
        setVehicles(updatedVehicles);
    };

    // function to delete vehicle data, send delete request to vehicle table in the backend 
    const handleDeleteVehicle = async (vehicleId) => {
        if (window.confirm('Are you sure you want to delete this vehicle?')) {
            try {
                const accessToken = localStorage.getItem('accessToken'); 
                const response = await fetch(`${baseUrl}/vehicles/${vehicleId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${accessToken}` 
                    }
                });
                if (!response.ok) throw new Error('Network response was not ok');
                setVehicles(prevVehicles =>
                    prevVehicles.filter(vehicle => vehicle.vehicle_id !== vehicleId)
                );
            } catch (error) {
                console.error('Error deleting vehicle:', error);
                setError('Error deleting vehicle');
            }
        }
    };

    return (
        //html component to display vehicle data on frontend
        <div>
            <h2>Vehicles</h2>
            <table className="records-table">
                <thead>
                    <tr>
                        <th>Make</th>
                        <th>Model</th>
                        <th>Year</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {Array.isArray(vehicles) && vehicles.length > 0 ? (
                        vehicles.map(vehicle => (
                            <tr key={vehicle.vehicle_id}>
                                <td>
                                    {vehicle.isEditing ? (
                                        <input
                                            type="text"
                                            value={vehicle.make}
                                            onChange={(e) => handleInputChange(vehicle.vehicle_id, 'make', e.target.value)}
                                            required
                                        />
                                    ) : (
                                        vehicle.make
                                    )}
                                </td>
                                <td>
                                    {vehicle.isEditing ? (
                                        <input
                                            type="text"
                                            value={vehicle.model}
                                            onChange={(e) => handleInputChange(vehicle.vehicle_id, 'model', e.target.value)}
                                            required
                                        />
                                    ) : (
                                        vehicle.model
                                    )}
                                </td>
                                <td>
                                    {vehicle.isEditing ? (
                                        <input
                                            type="number"
                                            value={vehicle.year}
                                            onChange={(e) => handleInputChange(vehicle.vehicle_id, 'year', e.target.value)}
                                            required
                                        />
                                    ) : (
                                        vehicle.year
                                    )}
                                </td>
                                <td>
                                    {vehicle.isEditing ? (
                                        <>
                                            <i
                                                className="fa fa-check"
                                                aria-hidden="true"
                                                style={{ marginRight: '10px', cursor: 'pointer', color: 'green' }}
                                                onClick={() => handleSaveVehicle(vehicle.vehicle_id)}
                                            ></i>
                                            <i
                                                className="fa fa-times"
                                                aria-hidden="true"
                                                style={{ cursor: 'pointer', color: 'red' }}
                                                onClick={() => handleCancelVehicle(vehicle.vehicle_id)}
                                            ></i>
                                        </>
                                    ) : (
                                        <>
                                            <i
                                                className="fa fa-pencil"
                                                aria-hidden="true"
                                                style={{ marginRight: '10px', cursor: 'pointer' }}
                                                onClick={() => handleEditVehicle(vehicle.vehicle_id)}
                                            ></i>
                                            <i
                                                className="fa fa-trash"
                                                aria-hidden="true"
                                                style={{ cursor: 'pointer', color: 'red' }}
                                                onClick={() => handleDeleteVehicle(vehicle.vehicle_id)}
                                            ></i>
                                        </>
                                    )}
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="4"></td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default VehicleRecords;
