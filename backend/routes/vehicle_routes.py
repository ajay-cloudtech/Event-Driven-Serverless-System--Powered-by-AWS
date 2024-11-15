from flask import Blueprint, request, jsonify
from components.vehicle_table import create_vehicle, get_all_vehicles, get_vehicles_list, get_vehicle, update_vehicle, delete_vehicle
from routes.auth_routes import extract_user_id_from_token  # Import helper function
from maintenance_utils.count_records import count_records  # Import count_records function


vehicle_bp = Blueprint('vehicle', __name__)

@vehicle_bp.route('/vehicles', methods=['POST'])
def create_vehicle_route():
    data = request.get_json()
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    response = create_vehicle(make, model, year, user_id)
    return jsonify({'message': response})

@vehicle_bp.route('/vehicles', methods=['GET'])
def get_all_vehicles_route():
    user_id = extract_user_id_from_token(request)
    print(f"Extracted user_id: {user_id}")  # Debugging line
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    response = get_all_vehicles(user_id)

    if 'error' in response:
        print(f"Error response: {response}")  # Debugging line
        return jsonify(response), 500

    return jsonify(response)

@vehicle_bp.route('/vehiclesList', methods=['GET'])
def get_vehicles_list_route():
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    vehicles = get_vehicles_list(user_id)
    if 'error' in vehicles:
        return jsonify(vehicles), 500

    return jsonify([
        {'vehicle_id': vehicle['vehicle_id'], 'display_name': vehicle['display_name']}
        for vehicle in vehicles
    ])

@vehicle_bp.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle_route(vehicle_id):
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    response = get_vehicle(vehicle_id, user_id)
    return jsonify({'message': response})

@vehicle_bp.route('/vehicles/<vehicle_id>', methods=['PUT'])
def update_vehicle_route(vehicle_id):
    data = request.get_json()
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    response = update_vehicle(vehicle_id, user_id, make, model, year)
    return jsonify({'message': response})

@vehicle_bp.route('/vehicles/<vehicle_id>', methods=['DELETE'])
def delete_vehicle_route(vehicle_id):
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    response = delete_vehicle(vehicle_id, user_id)
    return jsonify({'message': response})

@vehicle_bp.route('/vehicles/count', methods=['GET'])
def count_vehicles_route():
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # Pass the user_id to the count_records function
        vehicle_count = count_records("Vehicles", user_id)
        return jsonify({'vehicle_count': vehicle_count})
    except Exception as e:
        return jsonify({'error': f"Failed to count vehicles: {str(e)}"}), 500
