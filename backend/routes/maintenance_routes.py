from flask import Blueprint, request, jsonify
from maintenance_utils import sort_records_by_date
from maintenance_utils.count_records import count_records
from routes.auth_routes import extract_user_id_from_token
from components.maintenance_table import (
    create_maintenance_record,
    get_all_maintenance_records,
    update_maintenance_record,
    delete_maintenance_record
)

# Create a blueprint for maintenance routes
maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/maintenance', methods=['POST'])
def add_maintenance():
    user_id = extract_user_id_from_token(request)  # Extract the user ID from the token
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401  # Return an unauthorized error if user ID cannot be extracted

    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    maintenance_type = data.get('maintenance_type')
    mileage = data.get('mileage')
    last_service_date = data.get('last_service_date')

    # Create the maintenance record
    result = create_maintenance_record(user_id, vehicle_id, maintenance_type, mileage, last_service_date)
    return jsonify(result)

@maintenance_bp.route('/maintenance', methods=['GET'])
def get_maintenance_records():
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Retrieve maintenance records for the specific user
    response = get_all_maintenance_records(user_id)
    records = response.get("items", [])
    sorted_records = sort_records_by_date(records, 'next_service_date')
    return jsonify({'items': sorted_records})


@maintenance_bp.route('/maintenance/<string:maintenance_id>', methods=['PUT'])
def update_maintenance(maintenance_id):
    user_id = extract_user_id_from_token(request)  # Extract the user ID from the token
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    maintenance_type = data.get('maintenance_type')
    mileage = data.get('mileage')
    last_service_date = data.get('last_service_date')
    
    # Update the maintenance record for the specific user and maintenance ID
    result = update_maintenance_record(user_id, maintenance_id, maintenance_type, mileage, last_service_date)
    return jsonify(result)

@maintenance_bp.route('/maintenance/<string:maintenance_id>', methods=['DELETE'])
def delete_maintenance(maintenance_id):
    user_id = extract_user_id_from_token(request)  # Extract the user ID from the token
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Delete the maintenance record for the specific user and maintenance ID
    result = delete_maintenance_record(user_id, maintenance_id)
    return jsonify(result)

@maintenance_bp.route('/maintenance/count', methods=['GET'])
def count_maintenance_route():
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # Pass the user_id to the count_records function
        maintenance_count = count_records("Maintenance", user_id)
        return jsonify({'maintenance_count': maintenance_count})
    except Exception as e:
        return jsonify({'error': f"Failed to count maintenance records: {str(e)}"}), 500