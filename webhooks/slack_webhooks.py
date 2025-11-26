from flask import request, jsonify
import json

def register_slack_routes(app):
    """Register slack routes with Flask"""

    @app.route("/slack/actions", methods=["POST"])
    def handle_slack_actions():
        
        print("=" * 60)
        print("RAW REQUEST DATA:")
        print("=" * 60)

        indentedRequest = json.dumps(request, indent=4)
        print(indentedRequest)
        print("=" * 60)

        return jsonify({"status": "recived"})