# auth_routes.py
from flask import Blueprint, request, jsonify
from components.cognito_service import register_user, login_user, logout_user, get_user_profile, forgot_password, reset_password
from components.cognito_service import get_user_pool_id

auth_bp = Blueprint('auth', __name__)

user_pool_id = get_user_pool_id()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    result = register_user(user_pool_id, username, password, email)
    return jsonify(result)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    result = login_user(user_pool_id, username, password)

    # Check if the tokens are present in the result
    if 'AccessToken' in result and 'IdToken' in result:
        return jsonify({
            "AccessToken": result["AccessToken"],
            "IdToken": result["IdToken"],
            "Username": username  # Include the username in the response
        })
    else:
        return jsonify({"error": result.get("error", "Login failed")}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    access_token = data.get("access_token")
    result = logout_user(access_token)
    return jsonify(result)

@auth_bp.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    # If the token has a 'Bearer' prefix, remove it
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        user_data = get_user_profile(token)  # This should retrieve user details based on the token
        return jsonify(user_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Helper function to extract only the user ID
def extract_user_id_from_token(request):
    token = request.headers.get('Authorization')
    if not token:
        return None

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        user_data = get_user_profile(token)
        # Change this to retrieve the Username directly
        return user_data.get("Username")  # Use Username as the user ID
    except Exception as e:
        print(f"Error extracting user ID from token: {str(e)}")  # Debugging line
        return None

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password_route():
    data = request.get_json()
    email = data.get("email")
    result = forgot_password(user_pool_id, email)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_route():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("newPassword")

    result = reset_password(user_pool_id, email, otp, new_password)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)