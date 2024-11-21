from flask import Blueprint, request, jsonify
from maintenance_utils import sort_records_by_date
from maintenance_utils.count_records import count_records
from routes.auth_routes import extract_user_id_from_token
from components.maintenance_table import create_maintenance_record, get_all_maintenance_records
from maintenance_utils.count_upcoming_maintenance import count_upcoming_maintenance

# create blueprint for maintenance routes
maintenance_bp = Blueprint('maintenance', __name__)

# route for adding maintenance record in maintenance table
@maintenance_bp.route('/maintenance', methods=['POST'])
def add_maintenance():
    user_id = extract_user_id_from_token(request)  # extract the user id from auth token
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401  
    # get details from json payload
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    maintenance_type = data.get('maintenance_type')
    mileage = data.get('mileage')
    last_service_date = data.get('last_service_date')
    # call create_maintenance_reocrd function in maintenance_table.py
    result = create_maintenance_record(user_id, vehicle_id, maintenance_type, mileage, last_service_date)
    return jsonify(result)

# route to get maintenance records from maintenance table
@maintenance_bp.route('/maintenance', methods=['GET'])
def get_maintenance_records():
    user_id = extract_user_id_from_token(request) # extract the user id from auth token
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    response = get_all_maintenance_records(user_id) # call get_all_maintenance_records function in maintenance table
    records = response.get("items", [])
    sorted_records = sort_records_by_date(records, 'next_service_date') # sort records by next_service_date
    return jsonify({'items': sorted_records})

# route to count total maintenance records in the table
@maintenance_bp.route('/maintenance/count', methods=['GET'])
def count_maintenance_route():
    user_id = extract_user_id_from_token(request) # extract the user id from auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        maintenance_count = count_records("Maintenance", user_id)
        return jsonify({'maintenance_count': maintenance_count})
    except Exception as e:
        return jsonify({'error': f"Failed to count maintenance records: {str(e)}"}), 500
    
# route to count upcoming maintenance records due in the next 30 days
@maintenance_bp.route('/maintenance/upcoming/count', methods=['GET'])
def count_upcoming_maintenance_route():
    user_id = extract_user_id_from_token(request)  # extract the user id from the auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # get 'days' as 30 for upcoming maintenance and table_name as 'Maintenance'
    try:
        upcoming_maintenance_count = count_upcoming_maintenance(user_id, 30, 'Maintenance')
        return jsonify({'upcoming_maintenance_count': upcoming_maintenance_count})
    except Exception as e:
        return jsonify({'error': f"Failed to count upcoming maintenance records: {str(e)}"}), 500