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

# initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

# define table name
table_name = 'Maintenance'

# create the Maintenance table in DynamoDB, invoked from app.py
def create_maintenance_table():
    try:
        # Check if the table already exists
        existing_tables = dynamodb.tables.all()
        if table_name in [table.name for table in existing_tables]:
            return "Table already exists."
        
        # create the table
        '''
            using client.create_table with parameters
            TableName - name of the table
            KeySchema - list of dictionaries - define partition key and sort key
            AttributeDefinitions - describe the key schema for the table
            BillingMode - controls how you are charged for read and write throughput 
                        - using pay per request for unpredictable workloads
        '''
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # partition key to organize records per user
                {'AttributeName': 'maintenance_id', 'KeyType': 'RANGE'}  # sort key to uniquely identify each maintenance record
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'}, 
                {'AttributeName': 'maintenance_id', 'AttributeType': 'S'} 
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        return f"Table created. Status: {table.table_status}"
    except ClientError as e:
        return f"Error creating table: {e.response['Error']['Message']}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# initialize the table
table = dynamodb.Table(table_name)

# function to create maintenance record in the DynamoDB table
def create_maintenance_record(user_id, vehicle_id, maintenance_type, mileage, last_service_date):
    
    # Check if the vehicle exists before proceeding
    existing_vehicle_response = get_vehicle(vehicle_id)
    if 'error' in existing_vehicle_response:
        print(f"Error: {existing_vehicle_response['error']}. Vehicle not found.")
        return {"error": "Vehicle not found."}, 404  # Return 404 if the vehicle doesn't exist
   
    maintenance_id = str(uuid.uuid4())  # generate a unique id for maintenance record

    # calculate the next service date using the published library
    # args - last_service_date, months
    next_service_date = calculate_next_service_date(last_service_date, 6)

    # Add a new maintenance record to the Maintenance table
    '''
        using client.put_item with parameters
        Item - dictionary of given attributes 
    '''
    try:
        table.put_item(
            Item={
                'user_id': user_id,
                'maintenance_id': maintenance_id,
                'vehicle_id': vehicle_id,
                'maintenance_type': maintenance_type,
                'mileage': mileage,
                'last_service_date': last_service_date,
                'next_service_date': next_service_date  # store the next service date
            }
        )
        time.sleep(1)
        
        # retrieve vehicle data, passing user_id
        vehicle_data_response = get_vehicle(vehicle_id)
        
        # Check if the vehicle exists
        if 'error' in vehicle_data_response:
            print(f"Error: {vehicle_data_response['error']}. Vehicle not found.")
            return {"error": "Vehicle not found."}, 404  # Return 404 if the vehicle doesn't exist

        vehicle_data = vehicle_data_response

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

        # fetch the queue URL
        queue_url = get_sqs_queue_url('VehicleMaintenanceQueue')

        # Send the message to SQS
        send_sqs_message(queue_url, json.dumps(message))  # Send the message as a JSON string

        return {"message": "Maintenance record added successfully."}, 201 
    except ClientError as e:
        return {"error": f"Error creating maintenance record: {e.response['Error']['Message']}"}, 500  # HTTP status code for server error

# function to get all maintenance records associated with specific user
def get_all_maintenance_records(user_id):

    try:
        # perform the query
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        # Check if there are any items returned
        if 'Items' in response:
            return {"items": response['Items']}
        else:
            return {"items": []} 
    except ClientError as e:
        return {"error": f"Error retrieving maintenance records: {e.response['Error']['Message']}"}
    except Exception as e:
        return {"error": str(e)}