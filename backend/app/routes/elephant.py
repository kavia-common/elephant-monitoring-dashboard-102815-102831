from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
import time

# Simple hardcoded elephant data for demonstration
ELEPHANTS = [
    {"id": 1, "name": "Dumbo", "action": "Eating"},
    {"id": 2, "name": "Ella", "action": "Playing"},
    {"id": 3, "name": "Rajah", "action": "Bathing"},
    {"id": 4, "name": "Sunda", "action": "Sleeping"},
]

# In-memory stats store
API_STATS = {
    "hit_count": 0,
    "response_times": []
}

blp = Blueprint(
    "Elephants",
    "elephants",
    url_prefix="/elephants",
    description="Endpoints for elephant data"
)

metrics_blp = Blueprint(
    "Metrics",
    "metrics",
    url_prefix="/metrics",
    description="API server metrics"
)

def record_api_usage(start_time):
    """Track API usage and response time."""
    API_STATS["hit_count"] += 1
    duration = time.time() - start_time
    API_STATS["response_times"].append(duration)

# PUBLIC_INTERFACE
@blp.route("/")
class ElephantList(MethodView):
    """
    Get the list of elephants and their details.
    Returns an array of elephants and a count.
    """
    def get(self):
        start_time = time.time()
        elephants = ELEPHANTS
        record_api_usage(start_time)
        return jsonify({
            "count": len(elephants),
            "elephants": elephants
        })

# PUBLIC_INTERFACE
@blp.route("/count")
class ElephantCount(MethodView):
    """
    Get the number of elephants in the enclosure.
    """
    def get(self):
        start_time = time.time()
        count = len(ELEPHANTS)
        record_api_usage(start_time)
        return jsonify({"count": count})

# PUBLIC_INTERFACE
@blp.route("/actions")
class ElephantActions(MethodView):
    """
    Get a list of actions each elephant is currently performing.
    """
    def get(self):
        start_time = time.time()
        actions = [{ "id": e["id"], "name": e["name"], "action": e["action"] } for e in ELEPHANTS]
        record_api_usage(start_time)
        return jsonify({"actions": actions})

# PUBLIC_INTERFACE
@metrics_blp.route("/hit_count")
class HitCount(MethodView):
    """
    Get the number of API calls made.
    """
    def get(self):
        # No record_api_usage here to avoid self-increment
        return jsonify({"hit_count": API_STATS["hit_count"]})

# PUBLIC_INTERFACE
@metrics_blp.route("/response_times")
class ResponseTimes(MethodView):
    """
    Get a list of all API response times (in seconds).
    """
    def get(self):
        # No record_api_usage here to avoid self-increment
        return jsonify({"response_times": API_STATS["response_times"]})
