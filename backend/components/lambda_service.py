import json
import boto3
import io
import zipfile
import os
from botocore.exceptions import ClientError
from components.s3_service import create_bucket, upload_to_bucket, get_bucket_name
from components.sqs_service import get_sqs_queue_url

# Initialize the Boto3 clients
lambda_client = boto3.client('lambda')
sqs_client = boto3.client('sqs')

# Lambda function code as a string
lambda_code = """
import json
import boto3
from components.s3_service import upload_to_bucket, get_bucket_name
from maintenance_utils.report_generation import generate_report
from datetime import datetime

def lambda_handler(event, context):
    print("Raw event received:", json.dumps(event))
    s3 = boto3.client('s3')
    bucket_name = get_bucket_name()
    
    for record in event['Records']:
        print("Record before parsing:", record)
        try:
            message_body = json.loads(record['body'])
            print("Parsed message body:", message_body)  # Log the parsed message body
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return {
                'statusCode': 400,
                'body': 'Failed to decode message body as JSON'
            }
        
        vehicle_id = message_body['vehicle_id']
        user_id = message_body['user_id']  # Extract user ID from the message body
        make = message_body['make']
        model = message_body['model']
        year = message_body['year']
        maintenance_type = message_body['maintenance_type']
        mileage = message_body['mileage']
        last_service_date = message_body['last_service_date']
        next_service_date = message_body['next_service_date']
        
        report = generate_report(
            {'make': make, 'model': model, 'year': year},
            {'maintenance_type': maintenance_type, 'mileage': mileage, 'last_service_date': last_service_date, 'next_service_date': next_service_date}
        )
        
        # Prepare a unique object name with user_id and timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        print("Generated report data:", report)  # Debug log for generated report
        object_name = f'reports/{user_id}_maintenance_report_{timestamp}.json'  # Include user_id in the report name
        upload_message = upload_to_bucket(object_name, json.dumps(report), bucket_name)
        print("Upload response:", upload_message)  # Debug log for S3 upload
    
    return {
        'statusCode': 200,
        'body': 'Report generated and stored successfully!'
    }
"""

def get_lambda_zip_bytes():
    """
    Creates an in-memory zip file containing the Lambda function code and all required components.
    """
    # Create an in-memory bytes buffer
    buffer = io.BytesIO()

    # Create a zip file and add the lambda code and necessary components
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add the lambda function code to the root of the zip file
        zip_file.writestr('lambda_service.py', lambda_code)

        # Add the components directory and its contents
        for folder_name, subfolders, filenames in os.walk('components'):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                # Write the file with the correct relative path
                zip_file.write(file_path, os.path.relpath(file_path, os.path.dirname('components')))

        # Add maintenance_utils directory and its contents
        for folder_name, subfolders, filenames in os.walk('maintenance_utils'):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_file.write(file_path, os.path.relpath(file_path, os.path.dirname('maintenance_utils')))
    
    # Get the byte content of the zip file
    buffer.seek(0)
    return buffer.read()


def create_lambda_function(function_name, role_arn):
    """
    Create a Lambda function if it does not exist.
    
    :param function_name: The name of the Lambda function.
    :param role_arn: The ARN of the IAM role that Lambda assumes.
    :return: A message indicating whether the function was created or already exists.
    """
    try:
        response = lambda_client.get_function(FunctionName=function_name)
        return f"Lambda function '{function_name}' already exists."
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # Retrieve the zip byte string
            zip_bytes = get_lambda_zip_bytes()

            # Create the Lambda function using the zip bytes
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_service.lambda_handler',  # Correct handler path
                Code={'ZipFile': zip_bytes},
                Description='Lambda function to generate reports',
                Timeout=30,
                MemorySize=128
            )

            bucket_name = get_bucket_name()
            create_bucket(bucket_name)
            return f"Lambda function '{function_name}' created successfully."
        else:
            return f"Error creating Lambda function: {e.response['Error']['Message']}"

def add_sqs_trigger_to_lambda(function_name, queue_name="VehicleMaintenanceQueue"):
    """
    Adds SQS as a trigger to the Lambda function if it does not already exist.
    
    :param function_name: The name of the Lambda function.
    :param queue_name: The name of the SQS queue.
    :return: A message indicating whether the trigger was added, already exists, or if an error occurred.
    """
    try:
        # Get the SQS queue URL
        queue_url = get_sqs_queue_url(queue_name)
        
        # Get the ARN of the SQS queue
        queue_attributes = sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['QueueArn']
        )
        queue_arn = queue_attributes['Attributes']['QueueArn']

        # List existing event source mappings for the Lambda function
        mappings = lambda_client.list_event_source_mappings(
            FunctionName=function_name
        )

        # Check if the SQS trigger already exists
        for mapping in mappings['EventSourceMappings']:
            if mapping['EventSourceArn'] == queue_arn:
                return f"SQS trigger already exists for Lambda function '{function_name}'."

        # Create the event source mapping if it does not exist
        lambda_client.create_event_source_mapping(
            EventSourceArn=queue_arn,
            FunctionName=function_name,
            Enabled=True,
            BatchSize=1,  # Adjust as needed
        )

        return f"SQS trigger added to Lambda function '{function_name}'."
    except ClientError as e:
        return f"Error adding SQS trigger: {e.response['Error']['Message']}"
