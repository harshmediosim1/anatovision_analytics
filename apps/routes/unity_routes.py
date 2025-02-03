#Python Import

#Flask Import
from flask import Blueprint, request, jsonify
#App Import
from apps.models import AnalyticsData
from apps import db
#Third-Party Import
from datetime import datetime

unity_bp = Blueprint('unity', __name__)


"""
    The 'unity_analytics' function in the Flask blueprint 'unity_bp' handles POST requests to store
    analytics data in a database after validating and processing the incoming JSON payload.
    :return: The code is returning a JSON response based on the outcome of processing the POST request
    to the '/api/data' endpoint.
    """
@unity_bp.route('/api/data', methods=['POST'])
def create_unity_analytics():
    try:
        json_payload = request.json

        # Extract fields from the request payload
        version = json_payload.get("version")
        user_id = json_payload.get("user_id")
        college = json_payload.get("college")
        location = json_payload.get("location")
        module = json_payload.get("module")
        submodule = json_payload.get("submodule")
        time = json_payload.get("time")
        duration = json_payload.get("duration")
        date = json_payload.get("date")

        # List of required fields
        required_fields = [version, user_id, college, location, module, submodule, time, duration, date]

        # Ensure that all required fields are present
        missing_fields = [field for field, value in zip(["version", "user_id", "college", "location", "module", "time", "duration", "date"], required_fields) if not value]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Create a new AnalyticsData entry
        new_entry = AnalyticsData(
            user_id=user_id,
            version=version,
            college=college,
            location=location,
            module=module,
            submodule=submodule,
            time=time,
            duration=duration,
            date=datetime.strptime(date, "%Y-%m-%d").date()  # Ensure date is in proper format
        )

        # Save the entry to the database
        db.session.add(new_entry)
        db.session.commit()

        # Return success response along with the stored data
        return jsonify({"message": "Data successfully stored!", "id": new_entry.id}), 201

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": str(e)}), 500
    
@unity_bp.route('/test-analytics-data')
def test_analytics_data():
    data = AnalyticsData.query.all()
    return str(data)  # This will print all records in the AnalyticsData table
