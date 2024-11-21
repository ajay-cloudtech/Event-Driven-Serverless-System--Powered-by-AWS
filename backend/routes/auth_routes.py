# auth_routes.py
from flask import Blueprint, request, jsonify
from components.cognito_service import register_user, login_user, logout_user, get_user_profile, forgot_password, reset_password
from components.cognito_service import get_user_pool_id

# create blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

# get user pool id
user_pool_id = get_user_pool_id()

# route to register a user in cognito user pool
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    result = register_user(user_pool_id, username, password, email) # call register_user function in cognito_service.py
    return jsonify(result)

# route to enable user login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    result = login_user(user_pool_id, username, password) # call login_user function in cognito_service.py

    # check if tokens and user name are present in the result, if not display error
    if 'AccessToken' in result and 'IdToken' in result:
        return jsonify({
            "AccessToken": result["AccessToken"],
            "IdToken": result["IdToken"],
            "Username": username 
        })
    else:
        return jsonify({"error": result.get("error", "Login failed")}), 401

# route to enable logout 
@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    access_token = data.get("access_token")
    result = logout_user(access_token) # call logout_user function in cognito_service.py
    return jsonify(result)

# route to get user details
@auth_bp.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization') # retrieve auth header from request
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    # if the token has a 'Bearer' prefix, remove it to extract the actual token
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    try:
        user_data = get_user_profile(token)  # call get_user_profile function in cognito_service.py
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# helper function to extract only the user id
def extract_user_id_from_token(request):
    token = request.headers.get('Authorization') # retrieve auth header from request
    if not token:
        return None
    # if the token has a 'Bearer' prefix, remove it to extract the actual token
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    try:
        user_data = get_user_profile(token)
        return user_data.get("Username")  
    except Exception as e:
        return None

# route for requesting password reset
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password_route():
    data = request.get_json()
    email = data.get("email")
    result = forgot_password(user_pool_id, email) # call forgot_password function in cognito_service.py
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

# route for verifying otp and passing new password during reset password workflow
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_route():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("newPassword")

    result = reset_password(user_pool_id, email, otp, new_password) # call reset_password function in cognito_service.py
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)