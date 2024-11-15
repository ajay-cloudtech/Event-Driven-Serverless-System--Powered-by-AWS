# s3_service.py

import boto3
import json
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

# Define a static bucket name
BUCKET_NAME = "vehicle-maintenance-reports-folder"  # Adjust the bucket name as needed

def create_bucket(bucket_name=BUCKET_NAME, region=None):
    """
    Create an S3 bucket if it does not exist.
    
    :param bucket_name: The name of the bucket to create.
    :param region: The region to create the bucket in (default is us-east-1).
    :return: A message indicating whether the bucket was created or already exists.
    """
    try:
        # Check if the bucket already exists
        s3_client.head_bucket(Bucket=bucket_name)
        return f"Bucket '{bucket_name}' already exists."
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # If the bucket does not exist, create it
            if region is None:
                region = 'us-east-1'
            if region == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': region
                    }
                )
            return f"Bucket '{bucket_name}' created successfully."
        else:
            return f"Error checking bucket: {e.response['Error']['Message']}"

def upload_to_bucket(object_name, file_content, bucket_name=BUCKET_NAME):
    """
    Upload a file to an S3 bucket.
    
    :param object_name: The name of the object in the bucket.
    :param file_content: The content of the file to upload.
    :param bucket_name: The name of the bucket to upload to (default is the static bucket name).
    :return: A message indicating the result of the upload operation.
    """
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
        return f"File uploaded to '{bucket_name}/{object_name}' successfully."
    except ClientError as e:
        return f"Error uploading file: {e.response['Error']['Message']}"

def get_bucket_name():
    """
    Return the static S3 bucket name.
    
    :return: The S3 bucket name.
    """
    return BUCKET_NAME  

import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client
s3_client = boto3.client('s3')

def list_user_reports(bucket_name, user_id):
    """
    List all report files for a specific user in the specified S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param user_id: The user ID to filter reports.
    :return: A list of user-specific report file keys or an error message.
    """
    reports = []
    try:
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check if there are contents in the response
        if 'Contents' in response:
            for item in response['Contents']:
                # Check if the report name includes the user_id
                if f'{user_id}_maintenance_report_' in item['Key']:
                    reports.append(item['Key'])
                    print(f"Found report for user {user_id}: {item['Key']}")  # Print each found report

        return reports  # Ensure this returns a list
    except ClientError as e:
        return f"Error retrieving reports for user {user_id}: {e.response['Error']['Message']}"



def get_report(report_name, bucket_name=BUCKET_NAME):
    """
    Retrieve a specific report from S3.

    :param report_name: The name of the report to retrieve.
    :param bucket_name: The name of the bucket to retrieve the report from.
    :return: The report content as JSON.
    """
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=report_name)
        report_content = response['Body'].read().decode('utf-8')  # Read the file content
        report_data = json.loads(report_content)  # Assuming the content is in JSON format
        return report_data  # Return the JSON data
    except ClientError as e:
        return f"Error retrieving report: {e.response['Error']['Message']}"


    

def json_to_html(report_data):
    html_content = '<html><body>'
    html_content += '<h1>Report</h1>'
    html_content += '<ul>'
    for key, value in report_data.items():
        html_content += f'<li><strong>{key}:</strong> {value}</li>'
    html_content += '</ul>'
    html_content += '</body></html>'
    return html_content
