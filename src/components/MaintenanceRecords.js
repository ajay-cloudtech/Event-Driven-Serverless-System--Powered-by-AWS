import React, { useEffect, useState } from 'react';
import './VehicleAndMaintenanceRecords.css';

const MaintenanceRecords = ({ maintenanceRecords, setMaintenanceRecords, setError, vehicles }) => {
    // Local state to handle loading and error
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchMaintenanceRecords();
    }, []); // Fetch maintenance records when the component mounts

    const fetchMaintenanceRecords = async () => {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
            setError('No access token found.');
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch('http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com/maintenance', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to fetch maintenance records.');
            }

            const data = await response.json();
            console.log('Fetched maintenance records:', data); // Log the response data

            if (data && data.items) {
                setMaintenanceRecords(data.items); // Set the records if they exist
            } else {
                setError('No maintenance records found.');
            }
        } catch (error) {
            console.error('Error fetching maintenance records:', error);
            setError('Error fetching maintenance records.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h2>Maintenance Records</h2>

            {/* Display loading message if data is being fetched */}
            {isLoading ? (
                <p>Loading maintenance records...</p>
            ) : (
                <table className="records-table">
                    <thead>
                        <tr>
                            <th>Vehicle</th>
                            <th>Maintenance Type</th>
                            <th>Mileage</th>
                            <th>Last Service Date</th>
                            <th>Next Service Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {maintenanceRecords.length > 0 ? (
                            maintenanceRecords.map((record) => {
                                // Find the vehicle associated with the maintenance record
                                const vehicle = vehicles.find((v) => v.vehicle_id === record.vehicle_id);
                                const vehicleDisplayName = vehicle
                                    ? `${vehicle.make} ${vehicle.model} ${vehicle.year}`
                                    : 'Unknown Vehicle';

                                return (
                                    <tr key={record.maintenance_id}>
                                        <td>{vehicleDisplayName}</td>
                                        <td>{record.maintenance_type}</td>
                                        <td>{record.mileage}</td>
                                        <td>{record.last_service_date}</td>
                                        <td>{record.next_service_date}</td>
                                    </tr>
                                );
                            })
                        ) : (
                            <tr>
                                <td colSpan="5">No maintenance records available</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default MaintenanceRecords;
