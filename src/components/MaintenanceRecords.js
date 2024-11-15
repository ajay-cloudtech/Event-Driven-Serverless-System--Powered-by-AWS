import React, { useEffect } from 'react';
import './VehicleAndMaintenanceRecords.css';

const MaintenanceRecords = ({ maintenanceRecords, setMaintenanceRecords, setError, vehicles }) => {
    useEffect(() => {
        fetchMaintenanceRecords();
    }, []);

    const fetchMaintenanceRecords = async () => {
        const accessToken = localStorage.getItem('accessToken');
        try {
            const response = await fetch('http://localhost:5000/maintenance', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });
            if (!response.ok) {
                throw new Error('Failed to fetch maintenance records.');
            }
            const data = await response.json();
            console.log('Fetched maintenance records:', data);
            setMaintenanceRecords(data.items || []); // Make sure to set it correctly
        } catch (error) {
            console.error('Error fetching maintenance records:', error);
            setError('Error fetching maintenance records.');
        }
    };

    return (
        <div>
            <h2>Maintenance Records</h2>
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
                        maintenanceRecords.map(record => {
                            const vehicle = vehicles.find(v => v.vehicle_id === record.vehicle_id);
                            const vehicleDisplayName = vehicle ? `${vehicle.make} ${vehicle.model} ${vehicle.year}` : 'Unknown Vehicle';

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
                            <td colSpan="5">⏳</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default MaintenanceRecords;
