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

@app.route('/process', methods=['GET'])
def process_messages():
    try:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=20  # Long polling (better practice)
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
                
            if entity_type == "Client":
                entity_display = "Profile"
            else:
                entity_display = entity_type


            # Store transaction in DynamoDB
            table.put_item(Item=body)

            # Send Email Notification via SES
            transaction_id = body.get('transactionID', 'Unknown')
            client_name = body.get('clientName', 'Valued Client')
            receiver_email = body.get('clientEmail')
            client_id = body.get('clientID', 'Unknown')

            if receiver_email:
                subject = f"{action_type} {entity_type} Notification"

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
                    
                body_html = ""

                # Additional sections depending on action_type
                if action_type == "Create":
                    body_html += f"""
                    <html>
                    <head></head>
                    <body>
                    <p>Dear {client_name},</p>

                    <p>Your <strong>{entity_display.lower()}</strong> has been successfully created in our system.</p>
                    
                    <p>Thank you for trusting Scrooge Global Bank.</p>

                    <p>Best regards,<br>
                    Scrooge Global Bank</p>
                    </body>
                    </html>
                    """

                elif action_type == "Update":
                    attribute = body.get('attributeName', 'details')
                    before = body.get('beforeValue', 'N/A')
                    after = body.get('afterValue', 'N/A')

                    body_html += f"""
                    <html>
                    <head></head>
                    <body>
                    <p>Dear {client_name},</p>

                    <p>Your <strong>{entity_display.lower()}</strong>'s <strong>{attribute}</strong> has been successfully updated.</p>

                    <p><b>Before:</b> {before}<br>
                    <b>After:</b> {after}</p>

                    <p>If you did not request this change, please contact our support immediately.</p>

                    <p>Best regards,<br>
                    Scrooge Global Bank</p>
                    </body>
                    </html>
                    """

                elif action_type == "Delete":
                    body_html += f"""
                    <html>
                    <head></head>
                    <body>
                    <p>Dear {client_name},</p>

                    <p>Your <strong>{entity_display.lower()}</strong> has been successfully deleted from our system.</p>

                    <p>If you have any concerns, please contact our support team.</p>

                    <p>Best regards,<br>
                    Scrooge Global Bank</p>
                    </body>
                    </html>
                    """

                # (HTML version would be similar, structured nicely, we can add after)

                ses.send_email(
                    Source=SENDER_EMAIL,
                    Destination={
                        'ToAddresses': [receiver_email]
                    },
                    Message={
                        'Subject': {
                            'Data': subject,
                            'Charset': 'UTF-8'
                        },
                        'Body': {
                            'Text': {
                                'Data': body_text,
                                'Charset': 'UTF-8'
                            },
                            'Html': {
                                'Data': body_html,
                                'Charset': 'UTF-8'
                            }
                        }
                    }
                )

            else:
                print(f"Warning: No clientEmail found in message {transaction_id}, skipping email sending.")

            # Delete the processed message
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

        return jsonify({"status": "success", "message": f"Processed messages sent to {receiver_email}, sending from {SENDER_EMAIL}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)  # Make sure it's accessible inside Fargate
