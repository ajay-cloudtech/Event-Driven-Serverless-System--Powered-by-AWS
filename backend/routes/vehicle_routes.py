from flask import Blueprint, request, jsonify
from components.vehicle_table import create_vehicle, get_all_vehicles, get_vehicles_list, get_vehicle, update_vehicle, delete_vehicle
from routes.auth_routes import extract_user_id_from_token  
from maintenance_utils.count_records import count_records  # importing function from PyPi library

#create a blueprint for vehicle routes
vehicle_bp = Blueprint('vehicle', __name__)

# route for creating vehicles in Vehicles table 
@vehicle_bp.route('/vehicles', methods=['POST'])
def create_vehicle_route():
    data = request.get_json() # extract json data from incoming request
    user_id = extract_user_id_from_token(request) # extract user id from auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    # extract make, model and year
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    response = create_vehicle(make, model, year, user_id) # call create_vehicle function in vehicle_table.py
    return jsonify({'message': response})

# route to get all vehicles and their details
@vehicle_bp.route('/vehicles', methods=['GET'])
def get_all_vehicles_route():
    user_id = extract_user_id_from_token(request) # extract user id from auth token
    print(f"Extracted user_id: {user_id}")  
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_all_vehicles(user_id) # call get_all_vehicles function in vehicle_table.py

    if 'error' in response:
        print(f"Error response: {response}")  
        return jsonify(response), 500

    return jsonify(response)

# route to get  list of vehicles with only vehicle_id and display_name
@vehicle_bp.route('/vehiclesList', methods=['GET'])
def get_vehicles_list_route():
    user_id = extract_user_id_from_token(request) # extract user id from auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    # calling get_vehicles_list function  in vehicle_table.py
    vehicles = get_vehicles_list(user_id)
    if 'error' in vehicles:
        return jsonify(vehicles), 500

    return jsonify([
        {'vehicle_id': vehicle['vehicle_id'], 'display_name': vehicle['display_name']}
        for vehicle in vehicles
    ])

#route to get a specific vehicle detail using its id
@vehicle_bp.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle_route(vehicle_id):
    user_id = extract_user_id_from_token(request) # extract user id from auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    response = get_vehicle(vehicle_id, user_id) # call get_vehicle function in vehicle_table.py
    return jsonify({'message': response})

#route to update vehicle detail using its id
@vehicle_bp.route('/vehicles/<vehicle_id>', methods=['PUT'])
def update_vehicle_route(vehicle_id):
    data = request.get_json()
    user_id = extract_user_id_from_token(request)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    # extract make, model and year
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    response = update_vehicle(vehicle_id, user_id, make, model, year) # call update_vehicle function in vehicle_table.py
    return jsonify({'message': response})

# route to delete vehicle from the table
@vehicle_bp.route('/vehicles/<vehicle_id>', methods=['DELETE'])
def delete_vehicle_route(vehicle_id):
    user_id = extract_user_id_from_token(request) # extract user id from auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    response = delete_vehicle(vehicle_id, user_id)  # call delete_vehicle function in vehicle_table.py
    return jsonify({'message': response})

# route to count total vehicles in the vehicle table
@vehicle_bp.route('/vehicles/count', methods=['GET'])
def count_vehicles_route():
    user_id = extract_user_id_from_token(request) # extract user id from auth token
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        vehicle_count = count_records("Vehicles", user_id) # call count_records function
        return jsonify({'vehicle_count': vehicle_count})
    except Exception as e:
        return jsonify({'error': f"Failed to count vehicles: {str(e)}"}), 500
