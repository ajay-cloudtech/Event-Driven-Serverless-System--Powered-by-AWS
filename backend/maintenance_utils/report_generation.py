# maintenance_utils/report_utils.py

from datetime import datetime

def generate_report(vehicle_data, maintenance_data):
    """
    Generates a formatted report for a vehicle's maintenance entry.

    :param vehicle_data: A dictionary containing the vehicle details from the Vehicles table.
    :param maintenance_data: A dictionary containing the maintenance details.
    :return: A formatted report string with details of the vehicle and maintenance entry.
    """
    # Extract vehicle details
    make = vehicle_data.get("make", "Unknown")
    model = vehicle_data.get("model", "Unknown")
    registration_year = vehicle_data.get("year", "Unknown")
    
    # Extract maintenance details
    maintenance_type = maintenance_data.get("maintenance_type", "N/A")
    mileage = maintenance_data.get("mileage", "N/A")
    last_service_date = maintenance_data.get("last_service_date", "N/A")
    next_service_date = maintenance_data.get("next_service_date", "N/A")
    
    # Generate a formatted report string
    report = (
        f"Thank you for trusting us with your vehicle.\n"
        f"Your Vehicle Maintenance Report is shared below\n"
        f"--------------------------\n"
        f"Vehicle Make and Model  : {make} {model}\n"
        f"Registration Year       : {registration_year}\n"
        f"Maintenance Type        : {maintenance_type}\n"
        f"Mileage at Service      : {mileage}\n"
        f"Service Date            : {last_service_date}\n"
        f"Next Scheduled Service  : {next_service_date}\n"
    )
    return report
