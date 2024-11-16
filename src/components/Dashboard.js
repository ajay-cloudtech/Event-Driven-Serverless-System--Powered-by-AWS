import React, { useState, useEffect } from 'react';
import VehicleForm from './VehicleForm';
import AddMaintenanceForm from './AddMaintenanceForm';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';
import carImage from '../assets/carimage.jpg';

const Dashboard = () => {
    const navigate = useNavigate();
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [showVehicleForm, setShowVehicleForm] = useState(false);
    const [showMaintenanceForm, setShowMaintenanceForm] = useState(false);
    const [vehicleCount, setVehicleCount] = useState(null); // Default to null to show loading state
    const [maintenanceCount, setMaintenanceCount] = useState(null); // Default to null to show loading state
    const [loading, setLoading] = useState(true); // Loading state for counts

    // Fetch token from localStorage or other secure storage
    const token = localStorage.getItem('accessToken'); // Replace with your token retrieval method

    useEffect(() => {
        const fetchCounts = async () => {
            if (!token) {
                console.error("No token found in localStorage");
                return;
            }

            try {
                setLoading(true); // Set loading state to true while fetching

                // Fetch vehicle count
                const vehicleResponse = await fetch('http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com/vehicles/count', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    }
                });
                const vehicleData = await vehicleResponse.json();
                if (vehicleResponse.ok) {
                    setVehicleCount(vehicleData.vehicle_count || 0);
                } else {
                    console.error('Error fetching vehicle count:', vehicleData.error || 'Unknown error');
                    setVehicleCount(0);
                }

                // Fetch maintenance count
                const maintenanceResponse = await fetch('http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com/maintenance/count', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    }
                });
                const maintenanceData = await maintenanceResponse.json();
                if (maintenanceResponse.ok) {
                    setMaintenanceCount(maintenanceData.maintenance_count || 0);
                } else {
                    console.error('Error fetching maintenance count:', maintenanceData.error || 'Unknown error');
                    setMaintenanceCount(0);
                }
            } catch (error) {
                console.error("Failed to fetch counts:", error);
            } finally {
                setLoading(false); // Set loading state to false after the fetch completes
            }
        };

        fetchCounts();
    }, [token]);

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    const handleAddVehicle = () => {
        setShowVehicleForm(true);
        setShowMaintenanceForm(false); // Hide Maintenance form if it's already showing
        setIsDropdownOpen(false);
    };

    const handleAddMaintenance = () => {
        setShowMaintenanceForm(true);
        setShowVehicleForm(false); // Hide Vehicle form if it's already showing
        setIsDropdownOpen(false);
    };

    const handleCancelVehicle = () => {
        setShowVehicleForm(false);
    };

    const handleCancelMaintenance = () => {
        setShowMaintenanceForm(false);
    };

    const handleTotalVehiclesClick = () => {
        navigate('/vehicles');
    };

    const handleMaintenanceRecordsClick = () => {
        navigate('/maintenance-records');
    };

    // Handle form submission and redirect to homepage
    const handleFormSubmission = () => {
        navigate('/'); // Redirect to homepage after form submission
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

            {/* Show only one form based on the user's selection */}
            {showVehicleForm && <VehicleForm onCancel={handleCancelVehicle} onSubmit={handleFormSubmission} />}
            {showMaintenanceForm && <AddMaintenanceForm vehicles={['Toyota Camry', 'Honda Accord', 'Ford Mustang']} onCancel={handleCancelMaintenance} onSubmit={handleFormSubmission} />}

            <div className="dashboard-description">
                <h3>Welcome to Vehicle Service Scheduler</h3>
                <p>
                    This application helps you manage your vehicle maintenance and services effectively. 
                    Use the options above to quickly add a vehicle or schedule maintenance.
                </p>
                <p>
                    You can view all your vehicles, track upcoming maintenance services, and review completed maintenance records.
                </p>
                <p><strong>Useful Links:</strong></p>
                <ul>
                    <li>
                        <a href="/vehicles" style={{ color: '#4CAF50' }} onClick={handleTotalVehiclesClick}>
                            View Vehicles - {loading ? "⏳" : vehicleCount}
                        </a>
                    </li>
                    <li>
                        <a href="/maintenance-records" style={{ color: '#4CAF50' }} onClick={handleMaintenanceRecordsClick}>
                            View Maintenance Records - {loading ? "⏳" : maintenanceCount}
                        </a>
                    </li>
                    <li>
                        <a href="/maintenance-records" style={{ color: '#4CAF50' }}>Upcoming Maintenance</a>
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default Dashboard;
