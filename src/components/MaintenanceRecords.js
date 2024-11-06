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

    const handleEditMaintenance = (maintenanceId) => {
        const updatedRecords = maintenanceRecords.map(record =>
            record.maintenance_id === maintenanceId
                ? { ...record, isEditing: true, originalData: { ...record } }
                : record
        );
        setMaintenanceRecords(updatedRecords);
    };

    const handleMaintenanceInputChange = (maintenanceId, field, value) => {
        const updatedRecords = maintenanceRecords.map(record =>
            record.maintenance_id === maintenanceId ? { ...record, [field]: value } : record
        );
        setMaintenanceRecords(updatedRecords);
    };

    const handleSaveMaintenance = async (maintenanceId) => {
        const recordToSave = maintenanceRecords.find(record => record.maintenance_id === maintenanceId);
        const accessToken = localStorage.getItem('accessToken');

        try {
            const response = await fetch(`http://localhost:5000/maintenance/${recordToSave.vehicle_id}/${maintenanceId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`,
                },
                body: JSON.stringify({
                    maintenance_type: recordToSave.maintenance_type,
                    mileage: recordToSave.mileage,
                    last_service_date: recordToSave.last_service_date,
                }),
            });
            if (!response.ok) throw new Error('Failed to save maintenance record.');

            const updatedRecords = maintenanceRecords.map(record =>
                record.maintenance_id === maintenanceId ? { ...record, isEditing: false } : record
            );
            setMaintenanceRecords(updatedRecords);
        } catch (error) {
            console.error('Error saving maintenance record:', error);
            setError('Error saving maintenance record.');
        }
    };

    const handleCancelMaintenance = (maintenanceId) => {
        const updatedRecords = maintenanceRecords.map(record =>
            record.maintenance_id === maintenanceId
                ? { ...record, ...record.originalData, isEditing: false }
                : record
        );
        setMaintenanceRecords(updatedRecords);
    };

    const handleDeleteMaintenance = async (maintenanceId) => {
        if (window.confirm('Are you sure you want to delete this maintenance record?')) {
            const accessToken = localStorage.getItem('accessToken');
            try {
                const recordToDelete = maintenanceRecords.find(record => record.maintenance_id === maintenanceId);
                const response = await fetch(`http://localhost:5000/maintenance/${recordToDelete.vehicle_id}/${maintenanceId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });
                if (!response.ok) throw new Error('Failed to delete maintenance record.');

                setMaintenanceRecords(prevRecords =>
                    prevRecords.filter(record => record.maintenance_id !== maintenanceId)
                );
            } catch (error) {
                console.error('Error deleting maintenance record:', error);
                setError('Error deleting maintenance record.');
            }
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
                        <th>Actions</th>
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
                                    <td>
                                        {record.isEditing ? (
                                            <input
                                                value={record.maintenance_type}
                                                onChange={(e) => handleMaintenanceInputChange(record.maintenance_id, 'maintenance_type', e.target.value)}
                                            />
                                        ) : (
                                            record.maintenance_type
                                        )}
                                    </td>
                                    <td>
                                        {record.isEditing ? (
                                            <input
                                                type="number"
                                                value={record.mileage}
                                                onChange={(e) => handleMaintenanceInputChange(record.maintenance_id, 'mileage', e.target.value)}
                                            />
                                        ) : (
                                            record.mileage
                                        )}
                                    </td>
                                    <td>
                                        {record.isEditing ? (
                                            <input
                                                type="date"
                                                value={record.last_service_date}
                                                onChange={(e) => handleMaintenanceInputChange(record.maintenance_id, 'last_service_date', e.target.value)}
                                            />
                                        ) : (
                                            record.last_service_date
                                        )}
                                    </td>
                                    <td>{record.next_service_date}</td>
                                    <td>
                                        {record.isEditing ? (
                                            <>
                                                <i
                                                    className="fa fa-check"
                                                    style={{ marginRight: '10px', cursor: 'pointer', color: 'green' }}
                                                    onClick={() => handleSaveMaintenance(record.maintenance_id)}
                                                ></i>
                                                <i
                                                    className="fa fa-times"
                                                    style={{ cursor: 'pointer', color: 'red' }}
                                                    onClick={() => handleCancelMaintenance(record.maintenance_id)}
                                                ></i>
                                            </>
                                        ) : (
                                            <>
                                                <i
                                                    className="fa fa-pencil"
                                                    style={{ marginRight: '10px', cursor: 'pointer' }}
                                                    onClick={() => handleEditMaintenance(record.maintenance_id)}
                                                ></i>
                                                <i
                                                    className="fa fa-trash"
                                                    style={{ cursor: 'pointer', color: 'red' }}
                                                    onClick={() => handleDeleteMaintenance(record.maintenance_id)}
                                                ></i>
                                            </>
                                        )}
                                    </td>
                                </tr>
                            );
                        })
                    ) : (
                        <tr>
                            <td colSpan="6">No maintenance records found.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default MaintenanceRecords;
