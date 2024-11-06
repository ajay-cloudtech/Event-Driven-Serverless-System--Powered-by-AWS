// src/components/Dashboard.js
import React, { useState } from 'react';
import VehicleForm from './VehicleForm';
import AddMaintenanceForm from './AddMaintenanceForm'; // Import the AddMaintenanceForm component
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation
import './Dashboard.css';
import carImage from '../assets/carimage.jpg';

const Dashboard = () => {
    const navigate = useNavigate(); // Initialize useNavigate hook
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [showVehicleForm, setShowVehicleForm] = useState(false);
    const [showMaintenanceForm, setShowMaintenanceForm] = useState(false); // State to control the Maintenance form visibility

    const vehicles = ['Toyota Camry', 'Honda Accord', 'Ford Mustang']; // Sample vehicle data

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    const handleAddVehicle = () => {
        setShowVehicleForm(true);
        setIsDropdownOpen(false);
    };

    const handleAddMaintenance = () => {
        setShowMaintenanceForm(true);
        setIsDropdownOpen(false);
    };

    const handleCancelVehicle = () => {
        setShowVehicleForm(false);
    };

    const handleCancelMaintenance = () => {
        setShowMaintenanceForm(false);
    };

    // Navigation functions
    const handleTotalVehiclesClick = () => {
        navigate('/maintenance-records'); // Navigate to maintenance records
    };

    const handleUpcomingMaintenancesClick = () => {
        navigate('/maintenance-records'); // Navigate to Maintenances
    };

    const handleMaintenanceCompletedClick = () => {
        navigate('/maintenance-records'); // Navigate to maintenance records
    };

    return (
        <div className="dashboard"
            style={{ 
                backgroundImage: `url(${carImage})`,
                backgroundSize: 'cover', 
                backgroundPosition: 'center', 
                backgroundRepeat: 'no-repeat', 
                minHeight: '75vh', 
            }}
        >
            <div className="dashboard-header">
                <h2>Quick Actions</h2>
                <div className="quick-actions">
                    <button onClick={toggleDropdown} className="dropdown-button">
                        Add ▼
                    </button>
                    {isDropdownOpen && (
                        <div className="dropdown-menu">
                            <a href="#" onClick={handleAddVehicle}><b>Vehicle</b></a>
                            <a href="#" onClick={handleAddMaintenance}><b>Maintenance</b></a>
                        </div>
                    )}
                </div>
            </div>
            {showVehicleForm && <VehicleForm onCancel={handleCancelVehicle} />}
            {showMaintenanceForm && <AddMaintenanceForm vehicles={vehicles} onCancel={handleCancelMaintenance} />} {/* Pass vehicles to AddMaintenanceForm */}
            <div className="dashboard-description">
                <h3>Welcome to Vehicle Service Scheduler</h3>
                <p>
                    This application helps you manage your vehicle maintenance and services effectively. 
                    Use the options above to quickly add a vehicle or schedule maintenance.
                </p>
                <p>
                    You can view all your vehicles, track upcoming maintenance services, and review completed maintenance records.
                </p>
                <p>
                    <strong>Useful Links:</strong>
                </p>
                <ul>
                    <li><a href="/vehicles" style={{ color: '#4CAF50' }}>View Vehicles</a></li>
                    <li><a href="/maintenance-records" style={{ color: '#4CAF50' }}>View Maintenance Records</a></li>
                    <li><a href="/upcoming-maintenance" style={{ color: '#4CAF50' }}>Upcoming Maintenance</a></li>
                </ul>
            </div>
        </div>
    );
};

export default Dashboard;
