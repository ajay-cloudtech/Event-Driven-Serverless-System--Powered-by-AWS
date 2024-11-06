import boto3
from botocore.exceptions import ClientError

# Initialize the SQS client
sqs = boto3.client('sqs')

def create_sqs_queue(queue_name):
    try:
        # Check if the queue already exists
        response = sqs.get_queue_url(QueueName=queue_name)
        queue_url = response['QueueUrl']
        print(f"Queue already exists. URL: {queue_url}")
        return queue_url
    except ClientError as e:
        # If the queue does not exist, create it
        if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
            try:
                # Create the queue if not found
                response = sqs.create_queue(
                    QueueName=queue_name,
                    Attributes={
                        'DelaySeconds': '0',
                        'VisibilityTimeout': '60',
                        'MessageRetentionPeriod': '86400'
                    }
                )
                queue_url = response['QueueUrl']
                print(f"Queue created successfully. URL: {queue_url}")
                return queue_url
            except ClientError as ce:
                print(f"Error creating SQS queue: {ce.response['Error']['Message']}")
                return None
        else:
            print(f"Error checking for existing queue: {e.response['Error']['Message']}")
            return None
        
def get_sqs_queue_url(queue_name):
    """
    Retrieves the SQS queue URL, creating it if it does not exist.
    
    :param queue_name: Name of the SQS queue.
    :return: The URL of the SQS queue.
    """
    return create_sqs_queue(queue_name)

def send_sqs_message(queue_url, message_body):
    """
    Sends a message to the specified SQS queue.

    :param queue_url: The URL of the SQS queue.
    :param message_body: The body of the message to send.
    :return: The response from the send_message API call.
    """
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to SQS: {response['MessageId']}")
        return response
    except ClientError as e:
        print(f"Error sending message to SQS: {e.response['Error']['Message']}")
        return None