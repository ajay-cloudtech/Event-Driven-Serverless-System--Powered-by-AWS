from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.vehicle_routes import vehicle_bp
from routes.maintenance_routes import maintenance_bp
from components.vehicle_table import create_vehicle_table
from components.maintenance_table import create_maintenance_table
from components.sqs_service import create_sqs_queue  # Import the SQS queue creation function
from components.s3_service import create_bucket, get_bucket_name  # Import S3 functions
from components.lambda_service import create_lambda_function, add_sqs_trigger_to_lambda
from routes.s3_routes import s3_bp  # Import the S3 routes blueprint
from components.cognito_service import setup_cognito_resources  # Import Cognito setup function
from routes.auth_routes import auth_bp  # Import auth routes
import os
import logging

# Configure logging at the start of your application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='build')

# CORS setup: Allow requests from your frontend
CORS(app, resources={r"/*": {"origins": "*"}})

# Call the table creation functions to ensure the tables exist
create_vehicle_table()          # Create Vehicle Table if it doesn't exist
create_maintenance_table()      # Create Maintenance Table if it doesn't exist

# Set up AWS resources
queue_name = "VehicleMaintenanceQueue"
function_name = 'GenerateReportFunction'
role_arn = 'arn:aws:iam::118706183796:role/LabRole'  # Replace with your actual role ARN
handler = 'lambda_service.lambda_handler'  # Corrected handler path in Lambda function

try:
    # Step 1: Create or retrieve the SQS queue
    create_sqs_queue(queue_name)
    logging.info(f"SQS queue '{queue_name}' created or already exists.")

    # Step 2: Create or retrieve the S3 bucket
    bucket_name = get_bucket_name()  # Get the S3 bucket name
    create_bucket(bucket_name)
    logging.info(f"S3 bucket '{bucket_name}' created or already exists.")

    # Step 3: Create or retrieve the Lambda function
    create_lambda_function(function_name, role_arn)
    logging.info(f"Lambda function '{function_name}' created or already exists.")

    # Step 4: Add SQS trigger to Lambda function
    add_sqs_trigger_to_lambda(function_name)
    logging.info(f"SQS trigger added to Lambda function '{function_name}'.")

    # Set up Cognito resources
    user_pool_id, user_pool_client_id = setup_cognito_resources()
    logging.info(f"User Pool ID: {user_pool_id}, User Pool Client ID: {user_pool_client_id}")

except Exception as e:
    logging.error(f"An error occurred while setting up AWS resources: {e}")

# Register the routes
app.register_blueprint(vehicle_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(s3_bp)
app.register_blueprint(auth_bp)

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(f"build/{path}"):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
