import boto3
from botocore.exceptions import ClientError
import uuid
from boto3.dynamodb.conditions import Key

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = 'Vehicles'

# Create the Vehicles table in DynamoDB
def create_vehicle_table():
    try:
        # Check if the table already exists
        existing_tables = dynamodb.tables.all()
        if table_name in [table.name for table in existing_tables]:
            return "Table already exists."
        
        # Create the table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'vehicle_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'vehicle_id',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'  # String
                }
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

def create_vehicle(make, model, year, user_id):
    vehicle_id = str(uuid.uuid4())  # Generate a new UUID for vehicle_id
    
    # Add a new vehicle to the Vehicles table
    try:
        table.put_item(
            Item={
                'vehicle_id': vehicle_id,
                'user_id': user_id,
                'make': make,
                'model': model,
                'year': year
            }
        )
        return "Vehicle entry added successfully."
    except ClientError as e:
        return f"Error creating vehicle: {e.response['Error']['Message']}"

def get_all_vehicles(user_id):
    """
    Retrieve all vehicles associated with a specific user.
    """
    try:
        # Use scan to get all items and filter them based on user_id
        response = table.scan()  # Scan the entire table

        # Filter the results to only include items for the specified user_id
        vehicles = [item for item in response['Items'] if item.get('user_id') == user_id]

        return vehicles
    except ClientError as e:
        return {'error': f"Error retrieving vehicles: {e.response['Error']['Message']}"}
    except Exception as e:
        return {'error': str(e)}

def get_vehicles_list(user_id):
    """
    Retrieve all vehicles for a specific user with formatted "Make-Model-Year".
    """
    try:
        # Use scan to get all items and filter them based on user_id
        response = table.scan()  # Scan the entire table
        vehicles = [item for item in response['Items'] if item.get('user_id') == user_id]

        # Format each vehicle item as "Make-Model-Year"
        for vehicle in vehicles:
            vehicle['display_name'] = f"{vehicle['make']} {vehicle['model']} {vehicle['year']}"

        return vehicles
    except ClientError as e:
        return {'error': f"Error retrieving vehicles: {e.response['Error']['Message']}"}
    except Exception as e:
        return {'error': str(e)}

def get_vehicle(vehicle_id):
    """
    Retrieve a specific vehicle based on the vehicle_id.
    """
    try:
        response = table.query(
            KeyConditionExpression=Key('vehicle_id').eq(vehicle_id)
        )
        
        print(f"Raw response from DynamoDB: {response}")  # Log the response

        items = response.get('Items', [])
        if items:  # Check if we have any items returned
            return items[0]  # Return the first item found
        
        return {'error': "Vehicle not found."}  # Return structured error if no item found
    except ClientError as e:
        return {'error': f"Error retrieving vehicle: {e.response['Error']['Message']}"}
    except Exception as e:
        return {'error': str(e)}

def update_vehicle(vehicle_id, user_id, make=None, model=None, year=None):
    """
    Update a specific vehicle's attributes for the provided user.
    """
    update_expression = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    # Check if each attribute is provided and add it to the expression
    if make:
        update_expression.append("#m = :m")
        expression_attribute_values[":m"] = make
        expression_attribute_names["#m"] = "make"
    if model:
        update_expression.append("#mo = :mo")
        expression_attribute_values[":mo"] = model
        expression_attribute_names["#mo"] = "model"
    if year:
        update_expression.append("#yr = :y")
        expression_attribute_values[":y"] = year
        expression_attribute_names["#yr"] = "year"

    if not update_expression:
        return "No fields to update."

    try:
        table.update_item(
            Key={
                'vehicle_id': vehicle_id,
                'user_id': user_id
            },
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
        return "Vehicle updated successfully."
    except ClientError as e:
        return f"Error updating vehicle: {e.response['Error']['Message']}"

def delete_vehicle(vehicle_id, user_id):
    """
    Delete a specific vehicle for the provided user.
    """
    try:
        table.delete_item(
            Key={
                'vehicle_id': vehicle_id,
                'user_id': user_id
            }
        )
        return "Vehicle deleted successfully."
    except ClientError as e:
        return f"Error deleting vehicle: {e.response['Error']['Message']}"