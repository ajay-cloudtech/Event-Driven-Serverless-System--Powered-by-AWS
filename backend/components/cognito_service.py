import boto3
import logging
from flask import request, jsonify
from functools import wraps
from botocore.exceptions import ClientError

# initialize the Cognito client
cognito_client = boto3.client('cognito-idp')

# define names for user pool and user pool client
USER_POOL_NAME = "VehicleAppUserPool"
USER_POOL_CLIENT_NAME = "VehicleAppClient"

# helper function to check if user pool exists, if exists return user pool id
def get_user_pool_id():
    response = cognito_client.list_user_pools(MaxResults=10)
    # iterate over response until find a match to get its id
    # response is a list of dictionaries each containing details about user pool
    for pool in response['UserPools']:
        if pool['Name'] == USER_POOL_NAME:
            return pool['Id']
    return None

# helper function to check if user pool client exists, if exists return user pool client id
def get_user_pool_client_id(user_pool_id):
    response = cognito_client.list_user_pool_clients(UserPoolId=user_pool_id, MaxResults=10)
    # iterate over response until find a match to get its id
    # response is a list of dictionaries each containing details about user pool client
    for client in response['UserPoolClients']:
        if client['ClientName'] == USER_POOL_CLIENT_NAME:
            return client['ClientId']
    return None

# function to create user pool
def create_user_pool():
    try:
        '''
            using client.create_user_pool with parameters
            PoolName='string'
            Define password policies in dictionary
            Auto verify email   
        '''
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
        print("Failed to create User Pool:", e)
        raise

# function to create user pool client
def create_user_pool_client(user_pool_id):
    try:
        '''
           using client.create_user_pool_client with parameters 
           UserPoolId='string',
           ClientName='string',
           AllowedOAuthFlowsUserPoolClient - set to true to use OAuth 2.0 features - to manage user sessions with tokens (access, ID, and refresh tokens)
           GenerateSecret - set to false
           AllowedOAuthFlows set to code
           AllowedOAuthScopes - define oAuth perms for app to access email and profile information
           CallbackURLs - to redirect user to dashboard after successful authentication
        '''
        response = cognito_client.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName=USER_POOL_CLIENT_NAME,
            GenerateSecret=False,
            AllowedOAuthFlowsUserPoolClient=True,
            AllowedOAuthFlows=['code'],  
            AllowedOAuthScopes=['email', 'openid', 'profile'],
            CallbackURLs=['http://localhost:3000/dashboard', # local url
                          'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com/dashboard' # prod url
                        ]  
        )
        print("User Pool Client Created:", response['UserPoolClient']['ClientId'])
        return response['UserPoolClient']['ClientId']
    except Exception as e:
        print("Failed to create User Pool Client:", e) 
        raise

# function to setup user pool and user pool client, invoked from app.py
def setup_cognito_resources():
    # create resources only if they dont exist already
    # create user pool
    user_pool_id = get_user_pool_id()
    if not user_pool_id:
        user_pool_id = create_user_pool()
    # create user pool client
    user_pool_client_id = get_user_pool_client_id(user_pool_id)
    if not user_pool_client_id:
        user_pool_client_id = create_user_pool_client(user_pool_id)
    if user_pool_client_id is None:
        raise Exception("Failed to retrieve or create User Pool Client ID.")
    return user_pool_id, user_pool_client_id

# function to register user in user pool
def register_user(user_pool_id, username, password, email):

    try:
        # get client id before registering
        client_id = get_user_pool_client_id(user_pool_id) 
        if client_id is None:
            raise Exception("Client ID is None. Cannot register user.")
        '''
            using cognito_client.sign_up with parameters
            ClientId - user pool client id
            Username - username of the user
            Password - password of the user
            UserAttributes - user-specific information that will be associated with the user when they sign up
        '''
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
        # automatically confirm the user
        cognito_client.admin_confirm_sign_up(
            UserPoolId=user_pool_id,
            Username=username
        )
        # automatically verify the email
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

# login function to authenticate user
def login_user(user_pool_id, username, password):
    try:
        # get client id before login
        client_id = get_user_pool_client_id(user_pool_id)  
        if client_id is None:
            raise Exception("Client ID is None. Cannot log in user.")
        '''
            using client.initiate_auth with parameters
            ClientId - user pool client id
            AuthFlow - authentication flow type (using username and password)
            AuthParameters - authentication parameters
        ''' 
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        # return access token, ID token and refresh token so frontend can store in local storage
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

# funciton to logout user
def logout_user(access_token):
    '''
        using client.global_sign_out with parameters
        AccessToken - valid access token that Amazon Cognito issued to the user who you want to sign out
    '''
    try:
        cognito_client.global_sign_out(
            AccessToken=access_token
        )
        return {"message": "User logged out successfully."}
    except Exception as e:
        logging.error("An error occurred during logout: %s", e)
        return {"error": str(e)}

# function to validate token 
def validate_token(token):
    # get user info with the access token 
    try:
        response = cognito_client.get_user(AccessToken=token)
        return response  
    except cognito_client.exceptions.NotAuthorizedException:
        return None  # token is invalid
    except Exception as e:
        logging.error("Error validating token: %s", e)
        return None

# decorator to protect routes that require authentication 
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Missing token"}), 401  # unauthorized

        user_info = validate_token(token)
        if user_info is None:
            return jsonify({"error": "Invalid token"}), 401  # unauthorized

        # attach user name to request context
        request.user = user_info['Username']  
        return f(*args, **kwargs)
    return decorated_function

# function to get user profile details using get_user
def get_user_profile(access_token):
    client = boto3.client('cognito-idp')
    try:
        response = client.get_user(AccessToken=access_token)
        return response  # Returns user attributes and details
    except ClientError as e:
        raise Exception(f"Unable to fetch user profile: {e}")

# function to get user name using email details using list_users - as reset password requires email
def get_username_by_email(user_pool_id, email):
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

# function to reset password 
def forgot_password(user_pool_id, email):
    # get client id
    client_id = get_user_pool_client_id(user_pool_id)
    if not client_id:
        return {"error": "Client ID not found."}
    # fetch username based on email
    username = get_username_by_email(user_pool_id, email)
    if not username:
        return {"error": "User not found."}
    try:
        '''
            using client.forgot_password with parameters
            ClientId - The ID of the client associated with the user pool
            Username - user name of the user
        '''
        response = cognito_client.forgot_password(
            ClientId=client_id,
            Username=username  
        )
        return {"message": "Password reset instructions sent."}
    except cognito_client.exceptions.UserNotFoundException:
        return {"error": "User not found."}
    except Exception as e:
        return {"error": str(e)}

# function to reset password with otp verification and to accept new password
def reset_password(user_pool_id, email, otp, new_password):
    # get client id
    client_id = get_user_pool_client_id(user_pool_id)
    if not client_id:
        return {"error": "Client ID not found."}
    # fetch username based on email
    username = get_username_by_email(user_pool_id, email)
    if not username:
        return {"error": "User not found."}
    try:
        '''
            using client.forgot_password with parameters
            ClientId - The ID of the client associated with the user pool
            Username - user name of the user
            ConfirmationCode - OTP verification
            Password - new password
        '''
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