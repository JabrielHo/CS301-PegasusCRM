from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import boto3
import datetime
import asyncio
import aiohttp
from functools import wraps

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


# Decorator to run async functions in Flask routes
def async_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return decorated_function

# Health Check
@manage_client_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Delete by clientId
@manage_client_blueprint.route("/delete", methods=["DELETE"])
@async_route
async def delete_client():
    data = request.get_json()
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"error": "Client ID is required"}), 400

    try:
        async with aiohttp.ClientSession() as session:
            # Get client data
            async with session.get(
                f"{CLIENT_SERVICE_URL}/clients/{client_id}"
            ) as client_response:
                if client_response.status != 200:
                    return jsonify(await client_response.json()), client_response.status

                client_data = await client_response.json()

            async with session.get(
                f"{ACCOUNT_SERVICE_URL}/api/accounts/client/{client_id}"
            ) as response:
                if response.status == 200:
                    accounts_data = await response.json()
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
            async with session.delete(
                f"{CLIENT_SERVICE_URL}/clients/{client_id}"
            ) as delete_response:
                message = {
                    "action": "Delete|Client",
                    "agentID": client_data["client"].get("AgentID"),
                    "clientID": client_id,
                    "dateTime": datetime.datetime.now().isoformat(),
                    "clientName": f"{client_data['client'].get('FirstName')} {client_data['client'].get('LastName')}",
                    "clientEmail": client_data["client"].get("EmailAddress"),
                }

                print(message)
                # send_message_to_sqs(message)

                return jsonify(await delete_response.json()), delete_response.status

    except aiohttp.ClientError as e:
        return jsonify({"error": f"Error checking accounts: {str(e)}"}), 500


# Create Account
@manage_account_blueprint.route("/create", methods=["POST"])
@async_route
async def create_account():
    data = request.get_json()

    if not data.get("clientId"):
        return jsonify({"error": "clientId is required"}), 400

    try:
        async with aiohttp.ClientSession() as session:
            # Get client data
            async with session.get(
                f"{CLIENT_SERVICE_URL}/clients/{data['clientId']}"
            ) as client_response:
                if client_response.status != 200:
                    return jsonify(await client_response.json()), client_response.status

                client_data = await client_response.json()

            # Set account status based on client verification status
            is_verified = client_data["client"].get("Verified")
            data["accountStatus"] = "Active" if is_verified else "Pending"

            # Create account
            async with session.post(
                f"{ACCOUNT_SERVICE_URL}/api/accounts", json=data
            ) as response:
                if response.status != 201:
                    return jsonify(await response.json()), response.status

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

                return jsonify(await response.json()), response.status

    except aiohttp.ClientError as e:
        return jsonify({"error": f"Error communicating with services: {str(e)}"}), 500


# Delete Account
@manage_account_blueprint.route("/delete/<string:account_id>", methods=["DELETE"])
@async_route
async def delete_account(account_id):
    try:
        async with aiohttp.ClientSession() as session:
            # First retrieve the account details to get the client ID
            async with session.get(
                f"{ACCOUNT_SERVICE_URL}/api/accounts/{account_id}"
            ) as account_response:
                if account_response.status != 200:
                    return (
                        jsonify(await account_response.json()),
                        account_response.status,
                    )

                # Extract client ID from account data
                account_data = await account_response.json()
                client_id = account_data.get("clientId")

            # Get client data
            async with session.get(
                f"{CLIENT_SERVICE_URL}/clients/{client_id}"
            ) as client_response:
                if client_response.status != 200:
                    return jsonify(await client_response.json()), client_response.status

                client_data = await client_response.json()

            # Call the account service to delete the account
            async with session.delete(
                f"{ACCOUNT_SERVICE_URL}/api/accounts/{account_id}"
            ) as delete_response:
                if delete_response.status != 200:
                    return jsonify(await delete_response.json()), delete_response.status

                message = {
                    "action": "Delete|Account",
                    "status": "Inactive",
                    "agentID": client_data["client"].get("AgentID"),
                    "clientID": client_data["client"].get("ClientID"),
                    "dateTime": datetime.datetime.now().isoformat(),
                    "clientName": f"{client_data['client'].get('FirstName')} {client_data['client'].get('LastName')}",
                    "clientEmail": client_data["client"].get("EmailAddress"),
                }

                print(message)
                # send_message_to_sqs(message)

                return jsonify(await delete_response.json()), delete_response.status

    except aiohttp.ClientError as e:
        return jsonify({"error": f"Error communicating with services: {str(e)}"}), 500


# Update Account
@manage_account_blueprint.route("/update/<string:account_id>", methods=["PUT"])
@async_route
async def update_account(account_id):
    data = request.get_json()
    if not data or "accountStatus" not in data:
        return jsonify({"error": "accountStatus is required"}), 400
    try:
        async with aiohttp.ClientSession() as session:
            # Get account data
            async with session.get(
                f"{ACCOUNT_SERVICE_URL}/api/accounts/{account_id}"
            ) as account_response:
                if account_response.status != 200:
                    return (
                        jsonify(await account_response.json()),
                        account_response.status,
                    )

                # Extract client ID from account data
                account_data = await account_response.json()
                client_id = account_data.get("clientId")

            # Get client data
            async with session.get(
                f"{CLIENT_SERVICE_URL}/clients/{client_id}"
            ) as client_response:
                if client_response.status != 200:
                    return jsonify(await client_response.json()), client_response.status

                client_data = await client_response.json()

            # Update account
            async with session.put(
                f"{ACCOUNT_SERVICE_URL}/api/accounts/{account_id}",
                json={"accountStatus": data["accountStatus"]},
            ) as update_response:
                if update_response.status != 200:
                    return jsonify(await update_response.json()), update_response.status

                message = {
                    "action": "Update|Account",
                    "attributeName": "accountStatus",
                    "beforeValue": account_data.get("accountStatus"),
                    "afterValue": data["accountStatus"],
                    "agentID": client_data["client"].get("AgentID"),
                    "clientID": client_id,
                    "dateTime": datetime.datetime.now().isoformat(),
                    "clientName": f"{client_data['client'].get('FirstName')} {client_data['client'].get('LastName')}",
                    "clientEmail": client_data["client"].get("EmailAddress"),
                }

                print(message)
                # send_message_to_sqs(message)

                return jsonify(await update_response.json()), update_response.status

    except aiohttp.ClientError as e:
        return jsonify({"error": f"Error communicating with services: {str(e)}"}), 500


# Read Account by clientId
@manage_account_blueprint.route("/retrieve/<string:client_id>", methods=["GET"])
@async_route
async def retrieve_account(client_id):
    try:
        async with aiohttp.ClientSession() as session:
            # First check if the client exists
            async with session.get(
                f"{CLIENT_SERVICE_URL}/clients/{client_id}"
            ) as client_response:
                if client_response.status != 200:
                    return jsonify(await client_response.json()), client_response.status

                client_data = await client_response.json()

            # Get accounts for this client
            async with session.get(
                f"{ACCOUNT_SERVICE_URL}/api/accounts/client/{client_id}"
            ) as accounts_response:
                if accounts_response.status != 200:
                    return (
                        jsonify(await accounts_response.json()),
                        accounts_response.status,
                    )

                message = {
                    "action": "Read|Account",
                    "agentID": client_data["client"].get("AgentID"),
                    "clientID": client_data["client"].get("ClientID"),
                    "dateTime": datetime.datetime.now().isoformat(),
                    "clientName": f"{client_data['client'].get('FirstName')} {client_data['client'].get('LastName')}",
                    "clientEmail": client_data["client"].get("EmailAddress"),
                }

                print(message)
                # send_message_to_sqs(message)

                return jsonify(await accounts_response.json()), accounts_response.status

    except aiohttp.ClientError as e:
        return jsonify({"error": f"Error retrieving accounts: {str(e)}"}), 500


app.register_blueprint(manage_client_blueprint, url_prefix="/manage_client")
app.register_blueprint(manage_account_blueprint, url_prefix="/manage_account")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
