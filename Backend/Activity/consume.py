from flask import Flask, jsonify
import boto3
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Again, no manual credentials needed
sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))
ses = boto3.client('ses', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))

SQS_QUEUE_URL = os.getenv('QUEUE_URL')
DYNAMODB_TABLE = os.getenv('DYNAMO_TABLE')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')  # This should be verified in SES

table = dynamodb.Table(DYNAMODB_TABLE)

def create_record_logic(data):
    if 'transactionID' not in data:
        raise ValueError("Missing transactionID field")
    table.put_item(Item=data)

from flask import request

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

# Read (Get) a record by transactionID
@app.route('/records/<transactionID>', methods=['GET'])
def read_record(transactionID):
    try:
        response = table.get_item(Key={'transactionID': transactionID})
        
        if 'Item' not in response:
            return jsonify({"error": "Record not found"}), 404

        return jsonify(response['Item']), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Update an existing record by transactionID
@app.route('/records/<transactionID>', methods=['PUT'])
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
@app.route('/records/<transactionID>', methods=['DELETE'])
def delete_record(transactionID):
    try:
        table.delete_item(Key={'transactionID': transactionID})
        return jsonify({"status": "success", "message": "Record deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/process', methods=['GET'])
def process_messages():
    try:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=20  # Long polling
        )

        if 'Messages' not in response:
            return jsonify({"status": "success", "message": "No messages to process"}), 200

        for message in response['Messages']:
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

            # Email notification details
            transaction_id = body.get('transactionID', 'Unknown')
            client_name = body.get('clientName', 'Valued Client')
            receiver_email = body.get('clientEmail')
            client_id = body.get('clientID', 'Unknown')

            if receiver_email:
                # Build Email Subject
                subject = f"{action_type} {entity_type} Notification"

                # Build Email Body (Text)
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

                # Build Email Body (HTML)
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
                    # Send email via SES
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

                    # Only mark emailSent=True if sending succeeded
                    table.update_item(
                        Key={'transactionID': transaction_id},
                        UpdateExpression="SET emailSent = :val1",
                        ExpressionAttributeValues={':val1': True}
                    )

                except Exception as email_error:
                    print(f"Failed to send email to {receiver_email}: {str(email_error)}")
                    # Optionally you can also record email failure reason if you want

            else:
                print(f"Warning: No clientEmail found in message {transaction_id}, skipping email sending.")

            # Delete the processed SQS message
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

        return jsonify({"status": "success", "message": "Processed and sent notifications"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/process/status/<clientID>', methods=['GET'])
def get_process_status(clientID):
    try:
        # Query all records matching the clientID
        response = table.scan(
            FilterExpression='clientID = :clientIDVal',
            ExpressionAttributeValues={':clientIDVal': clientID}
        )
        
        records = response.get('Items', [])

        # Create a status list
        status_list = []
        for record in records:
            status_list.append({
                "transactionID": record.get('transactionID', 'Unknown'),
                "emailSent": record.get('emailSent', False)
            })

        return jsonify({
            "status": "success",
            "clientID": clientID,
            "recordsFound": len(status_list),
            "emailStatuses": status_list
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)  # Make sure it's accessible inside Fargate
