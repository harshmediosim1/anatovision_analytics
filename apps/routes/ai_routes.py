#Python Import

#Flask Import
from flask import Blueprint, jsonify
#App Import 
from apps.models import AnalyticsData
#Third-Party Import

ai_bp = Blueprint('ai', __name__)


"""
    This Flask route retrieves analytics data from a database, orders it by date, and returns a JSON
    response with selected fields.
    :return: The code defines a Flask Blueprint named 'ai' with a route '/analytics/data' that handles
    GET requests. Inside the route function 'get_data()', it retrieves all records from the
    AnalyticsData model ordered by date, prepares a response with selected fields, and returns the data
    as a JSON response with a status code of 200 if successful. If an exception occurs during this
    process, it returns a JSON
    """

@ai_bp.route('/analytics/data', methods=['GET'])
def get_data():
    try:
        # Retrieve all records from AnalyticsData ordered by date (timestamp can be used, or 'date' field as needed)
        records = AnalyticsData.query.order_by(AnalyticsData.date.desc()).all()

        # Prepare response data with selected fields
        result = [
            {
                "id": r.id,
                "version": r.version,
                "user_id": r.user_id,
                "college": r.college,
                "location": r.location,
                "date": r.date.isoformat(),  # Converting date to string format
                "module": r.module,
                "submodule": r.submodule,
                "time": r.time,
                "duration": r.duration
            }
            for r in records
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500