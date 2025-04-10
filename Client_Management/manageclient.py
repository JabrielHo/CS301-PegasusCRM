from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json
import uuid
import boto3
import datetime

app = Flask(__name__)
CORS(app)
load_dotenv()

# Service URLs
CLIENT_SERVICE_URL = os.getenv("CLIENT_SERVICE_URL", "http://localhost:5001")
ACCOUNT_SERVICE_URL = os.getenv("ACCOUNT_SERVICE_URL", "http://localhost:5003")

# Blueprints
manage_client_blueprint = Blueprint("manage_client", __name__)
manage_account_blueprint = Blueprint("manage_account", __name__)

# SQS Setup
sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "ap-southeast-1"))
SQS_QUEUE_URL = os.getenv("QUEUE_URL")


# SQS Publish function
def send_message_to_sqs(message_body):
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(message_body)
    )
    print(f"Message sent! Message ID: {response['MessageId']}")


# Delete by clientId
@manage_client_blueprint.route("/delete", methods=["DELETE"])
def delete_client():
    data = request.get_json()
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"error": "Client ID is required"}), 400

    try:
        # Check if any accounts are associated with the client ID
        response = requests.get(
            f"{ACCOUNT_SERVICE_URL}/api/accounts/client/{client_id}"
        )
        if response.status_code == 200:
            accounts_data = response.json()
            if "accounts" in accounts_data and accounts_data["accounts"]:
                return (
                    jsonify(
                        {
                            "error": "Cannot delete client with existing accounts",
                            "accounts": accounts_data["accounts"],
                        }
                    ),
                    400,
                )

        # Delete client if no accounts found
        delete_response = requests.delete(f"{CLIENT_SERVICE_URL}/clients/{client_id}")
        if delete_response.status_code == 200:
            return jsonify({"message": "Client deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete client"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error checking accounts: {str(e)}"}), 500


# Create Account
@manage_account_blueprint.route("/create", methods=["POST"])
def create_account():
    data = request.get_json()

    if not data.get("clientId"):
        return jsonify({"error": "clientId is required"}), 400

    try:
        client_response = requests.get(
            f"{CLIENT_SERVICE_URL}/clients/{data['clientId']}"
        )
        if client_response.status_code != 200:
            return jsonify(client_response.json()), client_response.status_code

        client_data = client_response.json()

        # Set account status based on client verification status
        is_verified = client_data["client"].get("Verified")
        data["accountStatus"] = "Active" if is_verified else "Pending"
        response = requests.post(f"{ACCOUNT_SERVICE_URL}/api/accounts", json=data)

        if response.status_code != 201:
            return jsonify(response.json()), response.status_code

        account_data = response.json()

        # Create SQS message
        message = {
            "action": "Create|Account",
            "status": data["accountStatus"],
            "agentID": client_data["client"].get("AgentID"),
            "clientID": data["clientId"],
            "dateTime": datetime.datetime.now().isoformat(),
            "clientName": f"{client_data['client'].get('FirstName')} {client_data['client'].get('LastName')}",
            "clientEmail": client_data["client"].get("EmailAddress"),
        }

        print(message)
        # send_message_to_sqs(message)

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with services: {str(e)}"}), 500


# Delete Account
@manage_account_blueprint.route("/delete", methods=["DELETE"])
def delete_account():
    pass


# Update Account
@manage_account_blueprint.route("/update", methods=["PUT"])
def update_account():
    pass


# Read Account by clientId
@manage_account_blueprint.route("/retrieve", methods=["GET"])
def retrieve_account():
    pass


app.register_blueprint(manage_client_blueprint, url_prefix="/manage_client")
app.register_blueprint(manage_account_blueprint, url_prefix="/manage_account")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
