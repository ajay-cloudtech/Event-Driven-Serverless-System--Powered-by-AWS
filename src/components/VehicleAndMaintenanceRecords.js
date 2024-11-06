// VehicleAndMaintenanceRecords.js
import React, { useState } from 'react';
import VehicleRecords from './VehicleRecords';
import MaintenanceRecords from './MaintenanceRecords';

const VehicleAndMaintenanceRecords = () => {
    const [vehicles, setVehicles] = useState([]);
    const [maintenanceRecords, setMaintenanceRecords] = useState([]);
    const [error, setError] = useState(null);

    return (
        <div className="maintenance-records">
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <VehicleRecords vehicles={vehicles} setVehicles={setVehicles} setError={setError} />
            <MaintenanceRecords
                vehicles={vehicles}
                maintenanceRecords={maintenanceRecords}
                setMaintenanceRecords={setMaintenanceRecords}
                setError={setError}
            />
        </div>
    );
};

export default VehicleAndMaintenanceRecords;
