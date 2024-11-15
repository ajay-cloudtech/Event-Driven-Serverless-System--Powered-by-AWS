import logging
import boto3
import json
from botocore.exceptions import ClientError
import uuid  # Importing the UUID module
from maintenance_utils.calculate_next_service import calculate_next_service_date
from components.vehicle_table import get_vehicle  # Import the function to get vehicle data
from components.sqs_service import send_sqs_message, get_sqs_queue_url  # Import your SQS message sending function
from boto3.dynamodb.conditions import Key
import time

logging.basicConfig(level=logging.INFO)

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = 'Maintenance'

# Create the Maintenance table in DynamoDB
def create_maintenance_table():
    try:
        # Check if the table already exists
        existing_tables = dynamodb.tables.all()
        if table_name in [table.name for table in existing_tables]:
            return "Table already exists."
        
        # Create the table with user_id as the hash key and maintenance_id as the sort key
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'maintenance_id', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},  # String
                {'AttributeName': 'maintenance_id', 'AttributeType': 'S'}  # String
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        return f"Table created. Status: {table.table_status}"
    except ClientError as e:
        return f"Error creating table: {e.response['Error']['Message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Initialize the table
table = dynamodb.Table(table_name)

def create_maintenance_record(user_id, vehicle_id, maintenance_type, mileage, last_service_date):
    # Check if the vehicle exists before proceeding
    existing_vehicle_response = get_vehicle(vehicle_id)
    if 'error' in existing_vehicle_response:
        print(f"Error: {existing_vehicle_response['error']}. Vehicle not found.")
        return {"error": "Vehicle not found."}, 404  # Return 404 if the vehicle doesn't exist
    
    maintenance_id = str(uuid.uuid4())  # Generate a new UUID for maintenance_id

    # Calculate the next service date using the library function
    next_service_date = calculate_next_service_date(last_service_date, 6)
    print(f"Next service date is: {next_service_date}")

    # Add a new maintenance record to the Maintenance table
    try:
        table.put_item(
            Item={
                'user_id': user_id,
                'maintenance_id': maintenance_id,
                'vehicle_id': vehicle_id,
                'maintenance_type': maintenance_type,
                'mileage': mileage,
                'last_service_date': last_service_date,
                'next_service_date': next_service_date  # Store the next service date
            }
        )
        time.sleep(1)
        print(f"Retrieving vehicle data for user {user_id}, vehicle {vehicle_id}...")

        # Retrieve vehicle data, passing user_id
        vehicle_data_response = get_vehicle(vehicle_id)
        print(f"Vehicle data response is: {vehicle_data_response}")

        # Check if the vehicle exists
        if 'error' in vehicle_data_response:
            print(f"Error: {vehicle_data_response['error']}. Vehicle not found.")
            return {"error": "Vehicle not found."}, 404  # Return 404 if the vehicle doesn't exist

        vehicle_data = vehicle_data_response
        print(f"Vehicle data: {vehicle_data}")

        # Prepare the message for SQS
        message = {
            'user_id': user_id,
            'vehicle_id': vehicle_id,
            'make': vehicle_data.get("make", "Unknown"),
            'model': vehicle_data.get("model", "Unknown"),
            'year': vehicle_data.get("year", "Unknown"),
            'maintenance_type': maintenance_type,
            'mileage': mileage,
            'last_service_date': last_service_date,
            'next_service_date': next_service_date
        }

        # Get the queue URL
        queue_url = get_sqs_queue_url('VehicleMaintenanceQueue')
        print(f"Queue URL retrieved: {queue_url}")

        # Send the message to SQS
        send_sqs_message(queue_url, json.dumps(message))  # Send the message as a JSON string
        print(f"Message prepared: {json.dumps(message)}")

        return {"message": "Maintenance record added successfully."}, 201  # HTTP status code for created
    except ClientError as e:
        return {"error": f"Error creating maintenance record: {e.response['Error']['Message']}"}, 500  # HTTP status code for server error

def get_all_maintenance_records(user_id):
    """
    Retrieve all maintenance records associated with a specific user.
    """
    try:
        # Perform the query
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        
        # Debugging: Log the entire response
        print("Query Response:", response)

        # Check if there are any items returned
        if 'Items' in response:
            return {"items": response['Items']}
        else:
            return {"items": []}  # Return an empty list if no items found

    except ClientError as e:
        return {"error": f"Error retrieving maintenance records: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"error": str(e)}


def update_maintenance_record(user_id, maintenance_id, maintenance_type=None, mileage=None, last_service_date=None):
    update_expression = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    if maintenance_type:
        update_expression.append("#mt = :mt")
        expression_attribute_values[":mt"] = maintenance_type
        expression_attribute_names["#mt"] = "maintenance_type"
    if mileage:
        update_expression.append("#m = :m")
        expression_attribute_values[":m"] = mileage
        expression_attribute_names["#m"] = "mileage"
    if last_service_date:
        update_expression.append("#d = :d")
        expression_attribute_values[":d"] = last_service_date
        expression_attribute_names["#d"] = "last_service_date"
        # Update the next service date when last service date is updated
        next_service_date = calculate_next_service_date(last_service_date, 6)
        update_expression.append("#nsd = :nsd")
        expression_attribute_values[":nsd"] = next_service_date
        expression_attribute_names["#nsd"] = "next_service_date"

    if not update_expression:
        return {"error": "No fields to update."}

    try:
        table.update_item(
            Key={
                'user_id': user_id,
                'maintenance_id': maintenance_id
            },
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
        return {"message": "Maintenance record updated successfully."}
    except ClientError as e:
        return {"error": f"Error updating maintenance record: {e.response['Error']['Message']}"}

def delete_maintenance_record(user_id, maintenance_id):
    try:
        table.delete_item(
            Key={
                'user_id': user_id,
                'maintenance_id': maintenance_id
            }
        )
        return {"message": "Maintenance record deleted successfully."}
    except ClientError as e:
        return {"error": f"Error deleting maintenance record: {e.response['Error']['Message']}"}
