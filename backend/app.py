from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.vehicle_routes import vehicle_bp
from routes.maintenance_routes import maintenance_bp
from components.vehicle_table import create_vehicle_table
from components.maintenance_table import create_maintenance_table
from components.sqs_service import create_sqs_queue  
from components.s3_service import create_bucket, get_bucket_name  
from components.lambda_service import create_lambda_function, add_sqs_trigger_to_lambda
from routes.s3_routes import s3_bp  
from components.cognito_service import setup_cognito_resources  
from routes.auth_routes import auth_bp  
import os
import logging

# configure logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='build')

# setup CORS to allow requests from frontend
CORS(app, resources={r"/*": {"origins": "*"}})

# create Vehicles table and Maintenance table in DynamoDB
create_vehicle_table()       
create_maintenance_table()      

# setup other AWS resources
queue_name = "VehicleMaintenanceQueue" # SQS queue name
function_name = 'GenerateReportFunction' # Lambda function name
role_arn = 'arn:aws:iam::118706183796:role/LabRole'  # AWS role that can be assumed for comms between services
handler = 'lambda_service.lambda_handler'  # Lambda hanlder

try:
    # create the SQS queue
    create_sqs_queue(queue_name)

    # create the S3 bucket
    bucket_name = get_bucket_name()
    create_bucket(bucket_name)

    # create the Lambda function
    create_lambda_function(function_name, role_arn)

    # add SQS trigger to Lambda function
    add_sqs_trigger_to_lambda(function_name)

    # set up Cognito resources - user pool and app client
    user_pool_id, user_pool_client_id = setup_cognito_resources()

except Exception as e:
    logging.error(f"An error occurred while setting up AWS resources: {e}")

# register the routes
app.register_blueprint(vehicle_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(s3_bp)
app.register_blueprint(auth_bp)

# serve react static files in the build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(f"build/{path}"):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')

# run the app on all network interfaces (host=0.0.0.0) and port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
