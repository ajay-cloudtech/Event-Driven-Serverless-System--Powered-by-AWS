import React, { useState } from 'react';
import VehicleRecords from './VehicleRecords';
import MaintenanceRecords from './MaintenanceRecords';

// function to merge both vehicle and maintenance displays on to the same page
const VehicleAndMaintenanceRecords = () => {
    const [vehicles, setVehicles] = useState([]);
    const [maintenanceRecords, setMaintenanceRecords] = useState([]);
    const [error, setError] = useState(null);

    return (
        <div className="maintenance-records">
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {/* render the vehicle records component */}
            <VehicleRecords vehicles={vehicles} setVehicles={setVehicles} setError={setError} />
            {/* render the maintenance records component */}
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
