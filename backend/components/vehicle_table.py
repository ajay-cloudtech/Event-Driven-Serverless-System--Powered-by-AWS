import boto3
from botocore.exceptions import ClientError
import uuid
from boto3.dynamodb.conditions import Key

# initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

# define table name
table_name = 'Vehicles'

# create the Vehicles table in DynamoDB, invoked from app.py
def create_vehicle_table():
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
                {
                    'AttributeName': 'vehicle_id',
                    'KeyType': 'HASH'  # partition key to uniquely identify each vehicle
                },
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'RANGE'  # sort key to organize multiple vehicles associated with a specific user
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

# initialize the table
table = dynamodb.Table(table_name)
# function to create vehicle record in the DynamoDB table
def create_vehicle(make, model, year, user_id):
    
    # generate a unique id for vehicle
    vehicle_id = str(uuid.uuid4())   
    # Add a new vehicle to the Vehicles table
    '''
        using client.put_item with parameters
        Item - dictionary of given attributes 
    '''
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

# function to get all vehicles associated with specific user
def get_all_vehicles(user_id):
    try:
        # use scan to get all items and filter them based on user_id
        response = table.scan()  

        # filter the results to only include items for the specified user_id
        vehicles = [item for item in response['Items'] if item.get('user_id') == user_id]
        return vehicles
    except ClientError as e:
        return {'error': f"Error retrieving vehicles: {e.response['Error']['Message']}"}
    except Exception as e:
        return {'error': str(e)}

# function to retrieve all vehicles for a specific user with formatted "Make-Model-Year".
def get_vehicles_list(user_id):
    try:
        # use scan to get all items and filter them based on user_id
        response = table.scan()  
        vehicles = [item for item in response['Items'] if item.get('user_id') == user_id]

        # format each vehicle item as "Make-Model-Year"
        for vehicle in vehicles:
            vehicle['display_name'] = f"{vehicle['make']} {vehicle['model']} {vehicle['year']}"
        return vehicles
    except ClientError as e:
        return {'error': f"Error retrieving vehicles: {e.response['Error']['Message']}"}
    except Exception as e:
        return {'error': str(e)}

# function to retrieve a specific vehicle based on the vehicle_id.
def get_vehicle(vehicle_id):
    try:
        response = table.query(
            KeyConditionExpression=Key('vehicle_id').eq(vehicle_id)
        )
        items = response.get('Items', [])
        if items: 
            return items[0]
        return {'error': "Vehicle not found."}  
    except ClientError as e:
        return {'error': f"Error retrieving vehicle: {e.response['Error']['Message']}"}
    except Exception as e:
        return {'error': str(e)}

# function to update specific vehicle details for a specific user
def update_vehicle(vehicle_id, user_id, make=None, model=None, year=None):
    
    # initialize placeholders and expressions for updating attributes in DynamoDB
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
    
    # update item in the DynamoDB table
    '''
        using client.update_item with parameters
        Key - primary key of the item to be updated
        UpdateExpression - An expression that defines one or more attributes to be updated, 
                         - the action to be performed on them, and new values for them
        ExpressionAttributeValues - One or more values that can be substituted in an expression
        ExpressionAttributeNames - One or more substitution tokens for attribute names in an expression
    '''
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

# function to delete specific vehicle item for a specific user from the table
def delete_vehicle(vehicle_id, user_id):
    '''
        using client.delete_item with parameters
        Key - representing the primary key of the item to delete.
    '''
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