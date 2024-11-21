import boto3
import json
from botocore.exceptions import ClientError

# initialize the s3 client
s3_client = boto3.client('s3')

# define a static bucket name
BUCKET_NAME = "vehicle-maintenance-reports-folder"  

# function to create bucket
def create_bucket(bucket_name=BUCKET_NAME, region=None):
    try:
        # check if the bucket already exists
        s3_client.head_bucket(Bucket=bucket_name)
        return f"Bucket '{bucket_name}' already exists."
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # If the bucket does not exist create it
            if region is None:
                region = 'us-east-1'
            if region == 'us-east-1': # create in us-east-1
                '''
                    using client.create_bucket with parameter Bucket=bucket_name
                '''
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                # create an S3 bucket in a specific region (other than us-east-1)
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': region
                    }
                )
            return f"Bucket '{bucket_name}' created successfully."
        else:
            return f"Error checking bucket: {e.response['Error']['Message']}"

# function to upload object to bucket
def upload_to_bucket(object_name, file_content, bucket_name=BUCKET_NAME):
    # put object in bucket
    '''
        using client.put_object with parameters
        Bucket - bucket name
        Key - object name
        Body - object data - file content
    '''
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
        return f"File uploaded to '{bucket_name}/{object_name}' successfully."
    except ClientError as e:
        return f"Error uploading file: {e.response['Error']['Message']}"

# function to get bucket name
def get_bucket_name():
    return BUCKET_NAME  

# function to list all reports specific to user in given s3 bucket
def list_user_reports(bucket_name, user_id):
    # initialize reports with empty list 
    reports = []
    try:
        # list objects in the bucket
        '''
            using client.list_objects_v2 with parameter Bucket=bucket_name
        '''
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # check if there are contents in the response
        if 'Contents' in response:
            for item in response['Contents']:
                # check if the report name includes the user_id
                if f'{user_id}_maintenance_report_' in item['Key']:
                    reports.append(item['Key'])
        return reports  
    except ClientError as e:
        return f"Error retrieving reports for user {user_id}: {e.response['Error']['Message']}"

# function to get specific report from s3
def get_report(report_name, bucket_name=BUCKET_NAME):
    try:
        # get specific object from bucket
        '''
            using client.get_object with parameters
            Bucket=bucket_name
            Key - object name
        '''
        response = s3_client.get_object(Bucket=bucket_name, Key=report_name)
        report_content = response['Body'].read().decode('utf-8')  # read the file content
        report_data = json.loads(report_content)
        return report_data  # return the JSON data
    except ClientError as e:
        return f"Error retrieving report: {e.response['Error']['Message']}"

# function to provided report data (JSON format) into an HTML formatted string
def json_to_html(report_data):
    html_content = '<html><body>'
    html_content += '<h1>Report</h1>'
    html_content += '<ul>'
    
    # loop through each key-value pair in the report data and convert it to a list item
    for key, value in report_data.items():
        html_content += f'<li><strong>{key}:</strong> {value}</li>'
    html_content += '</ul>'
    html_content += '</body></html>'
    return html_content
