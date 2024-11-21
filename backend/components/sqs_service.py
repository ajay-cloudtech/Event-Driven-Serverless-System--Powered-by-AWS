import boto3
from botocore.exceptions import ClientError

# initialize the SQS client
sqs = boto3.client('sqs')

# function to create sqs queue, invoked from app.py
def create_sqs_queue(queue_name):
    try:
        # check if the queue already exists
        response = sqs.get_queue_url(QueueName=queue_name)
        queue_url = response['QueueUrl']
        return queue_url
    except ClientError as e:
        # if the queue does not exist, create it
        if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
            try:
                # create the queue if not found
                '''
                    using client.create_queue with parameters
                    QueueName - name of the queue
                    Attributes - A map of attributes with their corresponding value
                        DelaySeconds - time to delay the message before it becomes visible to consumers - 0 seconds
                        VisibilityTimeout - time a message is hidden from other consumers after being retrieved - 1 minute
                        MessageRetentionPeriod - time in seconds message is retained in queue -  1 day
                '''
                response = sqs.create_queue(
                    QueueName=queue_name,
                    Attributes={
                        'DelaySeconds': '0',
                        'VisibilityTimeout': '60',
                        'MessageRetentionPeriod': '86400'
                    }
                )
                queue_url = response['QueueUrl']
                return queue_url
            except ClientError as ce:
                print(f"Error creating SQS queue: {ce.response['Error']['Message']}")
                return None
        else:
            print(f"Error checking for existing queue: {e.response['Error']['Message']}")
            return None

# function to get sqs url    
def get_sqs_queue_url(queue_name):
    return create_sqs_queue(queue_name)

# function to send sqs message
def send_sqs_message(queue_url, message_body):
    try:
        # send message
        '''
            using client.send_message with parameters
            QueueUrl - sqs queue url
            MessageBody - message to be sent
        '''
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        return response
    except ClientError as e:
        print(f"Error sending message to SQS: {e.response['Error']['Message']}")
        return None