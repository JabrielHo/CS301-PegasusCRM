from flask import Flask, jsonify
import boto3
from boto3.dynamodb.conditions import Attr
import json
import os
from dotenv import load_dotenv
from flask import request
from flask_cors import CORS

app = Flask(__name__)

load_dotenv()

CORS(app)  # Enable CORS for all routes 

# Again, no manual credentials needed
sqs = boto3.client('sqs', region_name='ap-southeast-1')
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
ses = boto3.client('ses', region_name='ap-southeast-1')

# START: UNCOMMENT OUT THIS WHEN PUSHING UR CODE BACK
secret_string = os.getenv('SECRET_STRING')

secrets = json.loads(secret_string)

SQS_QUEUE_URL = secrets.get('QUEUE_URL')
DYNAMODB_TABLE = secrets.get('DYNAMO_TABLE')
SENDER_EMAIL = secrets.get('SENDER_EMAIL')
# END

# START: COMMENT OUT WHEN PUSHING
# SQS_QUEUE_URL = os.getenv('QUEUE_URL')
# DYNAMODB_TABLE = os.getenv('DYNAMO_TABLE')
# SENDER_EMAIL = os.getenv('SENDER_EMAIL')
# END

table = dynamodb.Table(DYNAMODB_TABLE)

def create_record_logic(data):
    if 'transactionID' not in data:
        raise ValueError("Missing transactionID field")
    table.put_item(Item=data)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Create (Insert) a new record
@app.route('/records', methods=['POST'])
def create_record():
    try:
        data = request.json
        if 'transactionID' not in data:
            return jsonify({"error": "Missing transactionID field"}), 400
        
        table.put_item(Item=data)
        return jsonify({"status": "success", "message": "Record created successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Get all transaction records
@app.route('/records', methods=['GET'])
def get_all_records():
    try:
        response = table.scan()
        records = response.get('Items', [])

        return jsonify(records), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Get by agentID
@app.route('/records/<string:agentID>', methods=['GET'])
def read_record(agentID):
    try:
        # scan the table where agentID matches
        response = table.scan(
            FilterExpression=Attr('agentID').eq(agentID)
        )
        items = response.get('Items')

        if not items:
            return jsonify({"error": "Record not found"}), 404

        return jsonify(items), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Update an existing record by transactionID
@app.route('/records/<string:transactionID>', methods=['PUT'])
def update_record(transactionID):
    try:
        data = request.json
        update_expression = "SET "
        expression_attributes = {}

        for idx, (key, value) in enumerate(data.items()):
            update_expression += f"{key} = :val{idx}, "
            expression_attributes[f":val{idx}"] = value

        update_expression = update_expression.rstrip(", ")

        table.update_item(
            Key={'transactionID': transactionID},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attributes
        )
        return jsonify({"status": "success", "message": "Record updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Delete a record by transactionID
@app.route('/records/<string:transactionID>', methods=['DELETE'])
def delete_record(transactionID):
    try:
        table.delete_item(Key={'transactionID': transactionID})
        return jsonify({"status": "success", "message": "Record deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/process', methods=['GET'])
def process_messages():
    try:
        total_processed = 0

        while True:
            response = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,  # Max allowed
                WaitTimeSeconds=10      # Long polling to reduce empty responses
            )

            messages = response.get('Messages', [])
            if not messages:
                break  # Exit loop when no messages left

            for message in messages:
                body = json.loads(message['Body'])

                action_full = body.get('action', 'Unknown|Unknown')
                action_parts = action_full.split('|')

                if len(action_parts) == 2:
                    action_type, entity_type = action_parts
                else:
                    action_type, entity_type = 'Unknown', 'Unknown'

                entity_display = "Profile" if entity_type == "Client" else entity_type

                # Store transaction using shared logic
                create_record_logic(body)

                transaction_id = body.get('transactionID', 'Unknown')
                client_name = body.get('clientName', 'Valued Client')
                receiver_email = body.get('clientEmail')
                client_id = body.get('clientID', 'Unknown')

                if receiver_email:
                    subject = f"{action_type} {entity_type} Notification"

                    # Email Body (Text)
                    if action_type == "Create":
                        body_text = f"""
                        Dear {client_name},

                        Your {entity_display.lower()} has been successfully created in our system.

                        Thank you for trusting Scrooge Global Bank.

                        Best regards,
                        Scrooge Global Bank
                        """
                    elif action_type == "Update":
                        attribute = body.get('attributeName', 'details')
                        before = body.get('beforeValue', '')
                        after = body.get('afterValue', '')

                        body_text = f"""
                        Dear {client_name},

                        Your {entity_display.lower()}'s {attribute} has been successfully updated.

                        Before: {before}
                        After: {after}

                        If you did not request this change, please contact our support immediately.

                        Best regards,
                        Scrooge Global Bank
                        """
                    elif action_type == "Delete":
                        body_text = f"""
                        Dear {client_name},

                        Your {entity_display.lower()} has been successfully deleted from our system.

                        If you have any concerns, please contact our support team.

                        Best regards,
                        Scrooge Global Bank
                        """
                    else:
                        body_text = f"""
                        Dear {client_name},

                        This is a notification regarding your {entity_type.lower()}.

                        For more details, please contact our support team.

                        Best regards,
                        Scrooge Global Bank
                        """

                    # Email Body (HTML)
                    body_html = f"""
                    <html>
                    <head></head>
                    <body>
                    <p>Dear {client_name},</p>
                    <p>Your <strong>{entity_display.lower()}</strong> has been successfully {action_type.lower()}d in our system.</p>
                    <p>Best regards,<br>Scrooge Global Bank</p>
                    </body>
                    </html>
                    """

                    try:
                        ses.send_email(
                            Source=SENDER_EMAIL,
                            Destination={'ToAddresses': [receiver_email]},
                            Message={
                                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                                'Body': {
                                    'Text': {'Data': body_text, 'Charset': 'UTF-8'},
                                    'Html': {'Data': body_html, 'Charset': 'UTF-8'}
                                }
                            }
                        )

                        table.update_item(
                            Key={'transactionID': transaction_id},
                            UpdateExpression="SET emailSent = :val1",
                            ExpressionAttributeValues={':val1': True}
                        )

                    except Exception as email_error:
                        print(f"Failed to send email to {receiver_email}: {str(email_error)}")

                else:
                    print(f"Warning: No clientEmail found in message {transaction_id}, skipping email sending.")

                # Delete processed message
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )

                total_processed += 1

        return jsonify({"status": "success", "message": f"Processed {total_processed} messages"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
