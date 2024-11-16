# cognito_service.py
import boto3
import logging
from flask import request, jsonify
from functools import wraps
from botocore.exceptions import ClientError

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp')
USER_POOL_NAME = "VehicleAppUserPool"
USER_POOL_CLIENT_NAME = "VehicleAppClient"

def get_user_pool_id():
    """
    Check if a user pool with the desired name exists.
    If it exists, return its ID. If not, return None.
    """
    response = cognito_client.list_user_pools(MaxResults=10)  # Adjust MaxResults as needed
    print("User Pools Found:", response['UserPools'])  # Debugging statement
    for pool in response['UserPools']:
        if pool['Name'] == USER_POOL_NAME:
            print(f"User Pool '{USER_POOL_NAME}' found with ID:", pool['Id'])
            return pool['Id']
    print("User Pool not found.")
    return None

def get_user_pool_client_id(user_pool_id):
    """
    Check if a user pool client with the desired name exists in the specified user pool.
    If it exists, return its ID. If not, return None.
    """
    response = cognito_client.list_user_pool_clients(UserPoolId=user_pool_id, MaxResults=10)
    print("User Pool Clients Found:", response['UserPoolClients'])  # Debugging statement
    for client in response['UserPoolClients']:
        if client['ClientName'] == USER_POOL_CLIENT_NAME:
            print(f"User Pool Client '{USER_POOL_CLIENT_NAME}' found with ID:", client['ClientId'])
            return client['ClientId']
    print("No User Pool Client found with the specified name.")  # Debugging statement
    return None

def create_user_pool():
    """
    Creates a new Cognito User Pool and returns the User Pool ID.
    """
    try:
        response = cognito_client.create_user_pool(
            PoolName=USER_POOL_NAME,
            AutoVerifiedAttributes=['email'],
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': False
                }
            }
        )
        print("User Pool Created:", response['UserPool']['Id'])
        return response['UserPool']['Id']
    except Exception as e:
        print("Failed to create User Pool:", e)  # Debugging statement
        raise

def create_user_pool_client(user_pool_id):
    """Creates a new Cognito User Pool Client and returns the Client ID."""
    try:
        response = cognito_client.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=USER_POOL_CLIENT_NAME,
            GenerateSecret=False,
            AllowedOAuthFlowsUserPoolClient=True,
            AllowedOAuthFlows=['code'],  # Adjusted here to a single valid flow
            AllowedOAuthScopes=['email', 'openid', 'profile'],
            CallbackURLs=['http://localhost:3000/dashboard']  # Add your callback URL here
        )
        print("User Pool Client Created:", response['UserPoolClient']['ClientId'])
        return response['UserPoolClient']['ClientId']
    except Exception as e:
        print("Failed to create User Pool Client:", e)  # Debugging statement
        raise


def setup_cognito_resources():
    """
    Set up the Cognito User Pool and User Pool Client, creating them only if they don't already exist.
    """
    user_pool_id = get_user_pool_id()
    if not user_pool_id:
        user_pool_id = create_user_pool()

    user_pool_client_id = get_user_pool_client_id(user_pool_id)
    if not user_pool_client_id:
        user_pool_client_id = create_user_pool_client(user_pool_id)

    # Check if we successfully retrieved the client ID
    if user_pool_client_id is None:
        raise Exception("Failed to retrieve or create User Pool Client ID.")

    print("User Pool ID:", user_pool_id)  # Debug statement
    print("User Pool Client ID:", user_pool_client_id)  # Debug statement

    return user_pool_id, user_pool_client_id

def register_user(user_pool_id, username, password, email):
    """
    Register a new user in the Cognito User Pool.
    """
    try:
        client_id = get_user_pool_client_id(user_pool_id)  # Get the client ID before registering
        if client_id is None:
            raise Exception("Client ID is None. Cannot register user.")
            
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )
        logging.info("User registration successful for username: %s", username)
        # Automatically confirm the user
        cognito_client.admin_confirm_sign_up(
            UserPoolId=user_pool_id,
            Username=username
        )
        cognito_client.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ]
        )
        return {"message": "User registration successful."}
    except cognito_client.exceptions.UsernameExistsException:
        return {"error": "User already exists."}
    except Exception as e:
        logging.error("An error occurred during user registration: %s", e)
        return {"error": str(e)}

def login_user(user_pool_id, username, password):
    """
    Authenticate a user and retrieve tokens.
    """
    try:
        client_id = get_user_pool_client_id(user_pool_id)  # Get the client ID before login
        if client_id is None:
            raise Exception("Client ID is None. Cannot log in user.")
            
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return {
            "AccessToken": response['AuthenticationResult']['AccessToken'],
            "IdToken": response['AuthenticationResult']['IdToken'],
            "RefreshToken": response['AuthenticationResult']['RefreshToken']
        }
    except cognito_client.exceptions.NotAuthorizedException:
        return {"error": "Invalid credentials."}
    except Exception as e:
        logging.error("An error occurred during user login: %s", e)
        return {"error": str(e)}

def logout_user(access_token):
    """
    Log out the user by revoking their session.
    """
    try:
        cognito_client.global_sign_out(
            AccessToken=access_token
        )
        return {"message": "User logged out successfully."}
    except Exception as e:
        logging.error("An error occurred during logout: %s", e)
        return {"error": str(e)}
    
def validate_token(token):
    """
    Validate the token with Cognito and return the user claims if valid.
    """
    try:
        response = cognito_client.get_user(AccessToken=token)
        return response  # Returns user attributes if token is valid
    except cognito_client.exceptions.NotAuthorizedException:
        return None  # Token is invalid
    except Exception as e:
        logging.error("Error validating token: %s", e)
        return None

def login_required(f):
    """
    Decorator to protect routes that require authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Missing token"}), 401  # Unauthorized

        user_info = validate_token(token)
        if user_info is None:
            return jsonify({"error": "Invalid token"}), 401  # Unauthorized

        # Optionally, attach user ID to request context
        request.user = user_info['Username']  # or any other user attribute
        return f(*args, **kwargs)

    return decorated_function

def get_user_profile(access_token):
    client = boto3.client('cognito-idp')
    try:
        response = client.get_user(AccessToken=access_token)
        return response  # Returns user attributes and details
    except ClientError as e:
        raise Exception(f"Unable to fetch user profile: {e}")

def get_username_by_email(user_pool_id, email):
    """Fetch the username using email to ensure compatibility with forgot password."""
    try:
        response = cognito_client.list_users(
            UserPoolId=user_pool_id,
            Filter=f'email = "{email}"'
        )
        # Confirm that a user was found
        if response['Users']:
            return response['Users'][0]['Username']
        else:
            return None  # User not found
    except ClientError as e:
        print(f"Error fetching username by email: {e}")
        return None

def forgot_password(user_pool_id, email):
    client_id = get_user_pool_client_id(user_pool_id)
    if not client_id:
        return {"error": "Client ID not found."}

    # Fetch username based on email if needed
    username = get_username_by_email(user_pool_id, email)
    if not username:
        return {"error": "User not found."}

    try:
        response = cognito_client.forgot_password(
            ClientId=client_id,
            Username=username  # Using resolved username instead of email
        )
        return {"message": "Password reset instructions sent."}
    except cognito_client.exceptions.UserNotFoundException:
        return {"error": "User not found."}
    except Exception as e:
        return {"error": str(e)}

def reset_password(user_pool_id, email, otp, new_password):
    client_id = get_user_pool_client_id(user_pool_id)
    if not client_id:
        return {"error": "Client ID not found."}

    # Fetch username based on email
    username = get_username_by_email(user_pool_id, email)
    if not username:
        return {"error": "User not found."}

    try:
        # Confirm the password reset with OTP and new password
        response = cognito_client.confirm_forgot_password(
            ClientId=client_id,
            Username=username,
            ConfirmationCode=otp,
            Password=new_password
        )
        return {"message": "Password reset successfully."}
    except cognito_client.exceptions.CodeMismatchException:
        return {"error": "Invalid OTP code."}
    except cognito_client.exceptions.ExpiredCodeException:
        return {"error": "OTP code has expired."}
    except Exception as e:
        return {"error": str(e)}
