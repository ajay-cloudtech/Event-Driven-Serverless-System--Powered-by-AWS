from flask import Blueprint, jsonify, request
from components.s3_service import list_user_reports, get_report, get_bucket_name

# Create a Blueprint for S3-related routes
s3_bp = Blueprint('s3', __name__)

@s3_bp.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        user_id = request.args.get('user_id')  # Get user_id from query parameters
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        print(f"Received user ID: {user_id}")  # Debugging line

        reports = list_user_reports(get_bucket_name(), user_id)  # Fetch user-specific reports
        
        print(f"Reports found for user {user_id}: {reports}")  # Debugging line
        
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@s3_bp.route('/api/reports/<path:report_name>', methods=['GET'])
def get_report_by_name(report_name):
    try:
        report_key = 'reports/' + report_name
        report_data = get_report(report_key)  # Fetch specific report from S3
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500