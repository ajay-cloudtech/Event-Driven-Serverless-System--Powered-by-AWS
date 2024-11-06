import boto3
import json
import time
from components.sqs_service import get_sqs_queue_url  # Import your function to get the SQS URL
from maintenance_utils.report_generation import generate_report

def process_messages():
    sqs = boto3.client('sqs')
    queue_name = 'VehicleMaintenanceQueue'  # Specify your SQS queue name
    queue_url = get_sqs_queue_url(queue_name)  # Use the function to get the queue URL

    if not queue_url:
        print("Failed to retrieve queue URL. Exiting.")
        return

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        if 'Messages' in response:
            for message in response['Messages']:
                message_body = json.loads(message['Body'])

                # Extract vehicle and maintenance data
                vehicle_id = message_body['vehicle_id']
                make = message_body['make']
                model = message_body['model']
                year = message_body['year']
                maintenance_type = message_body['maintenance_type']
                mileage = message_body['mileage']
                last_service_date = message_body['last_service_date']
                next_service_date = message_body['next_service_date']

                # Generate the report using the received data
                report = generate_report(
                    {
                        'make': make,
                        'model': model,
                        'year': year
                    },
                    {
                        'maintenance_type': maintenance_type,
                        'mileage': mileage,
                        'last_service_date': last_service_date,
                        'next_service_date': next_service_date
                    }
                )

                # Here you might want to save the report to a file, database, or send it via email
                print(report)  # For now, just print it

                # Delete the message from the queue after processing
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            print("No messages to process.")
            time.sleep(5)  # Sleep for a while before polling again

if __name__ == "__main__":
    process_messages()
