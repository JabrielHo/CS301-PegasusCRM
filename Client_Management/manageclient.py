from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
import requests

import uuid
import json

app = Flask(__name__)

CORS(app)

manage_client_blueprint = Blueprint("manage_client",__name__)

# Features to implement:
# 1. Check if can delete client

@manage_client_blueprint.route("/delete", methods=["DELETE"])
def delete_client():

    data = request.get_json()
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"error": "Client ID is required"}), 400
    
    try:
        # Check if any accounts are associated with the client ID
        # TODO: Replace with actual URL to check accounts
        response = requests.get()
        if response.data:
            return jsonify({"error": "Cannot delete client with existing accounts",
                            # TODO: Replace with actual response data
                            "accounts": response.data.account}), 400
        
        # TODO: Replace with actual URL to delete client
        response = requests.delete(f"http://localhost:5001/clients/{client_id}")
        if response.status_code == 200:
            return jsonify({"message": "Client deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete client"}), 500
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error checking accounts"}), 500

app.register_blueprint(manage_client_blueprint, url_prefix="/manage_client")

#region Setting up Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5002)
#endregion