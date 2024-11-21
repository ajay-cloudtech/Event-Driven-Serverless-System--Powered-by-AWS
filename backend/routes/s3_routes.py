from flask import Blueprint, jsonify, request
from components.s3_service import list_user_reports, get_report, get_bucket_name

# create a blueprint for S3 routes
s3_bp = Blueprint('s3', __name__)

# route to get all reports from S3 for the user
@s3_bp.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        user_id = request.args.get('user_id')  # get user_id from query parameters
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        reports = list_user_reports(get_bucket_name(), user_id)  # call list_user_reports function in s3_service.py
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# route to get the content of a specific report
@s3_bp.route('/api/reports/<path:report_name>', methods=['GET'])
def get_report_by_name(report_name):
    try:
        report_key = 'reports/' + report_name # full key to uniquely identify object in s3 bucket
        report_data = get_report(report_key)  # call get_report function in s3_service.py
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500