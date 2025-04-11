# Refer to this file for how to publish to SQS
import boto3
import json
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

# No manual session needed — boto3 automatically uses the IAM Role in Fargate!
sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))

SQS_QUEUE_URL = os.getenv('QUEUE_URL')  # Load from environment variable

def send_message_to_sqs(message_body):
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )
    print(f"Message sent! Message ID: {response['MessageId']}")

if __name__ == "__main__":
    transaction_id = str(uuid.uuid4())
    
    print(f"QUEUE_URL loaded is: {SQS_QUEUE_URL}")
    
    # Create Client profile
    # send_message_to_sqs(
    #     {
    #         "transactionID": transaction_id,
    #         "action": "Create|Client",
    #         "agentID": 1,
    #         "clientID": 1,
    #         "dateTime": "2025-04-01T10:30:00",
    #         "clientName": "Rainer",
    #         "clientEmail": "rainer.tan.2023@scis.smu.edu.sg"
    #     }
    # )
    
    # Delete Client profile
    # send_message_to_sqs(
    #     {
    #         "transactionID": transaction_id,
    #         "action": "Delete|Client",
    #         "agentID": 1,
    #         "clientID": 1,
    #         "dateTime": "2025-04-01T10:30:00",
    #         "clientName": "Rainer",
    #         "clientEmail": "rainer.tan.2023@scis.smu.edu.sg"
    #     }
    # )
    
    # Update Client
    send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Update|Client",
            "attributeName": "FirstName|Address",
            "beforeValue": "Lee|Pasir Ris",
            "afterValue": "Tan|Tampines",
            "agentID": 1,
            "clientID": 1,
            "dateTime": "",
            "clientName": "Rainer",
            "clientEmail": "rainer.tan.2023@scis.smu.edu.sg"
        }
    )
