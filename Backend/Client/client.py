from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import json
import re
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

secret_string = os.getenv("SECRET_STRING")

secrets = json.loads(secret_string)

AWS_REGION = secrets.get("AWS_REGION")
AWS_ACCESS_KEY_ID = secrets.get("AWS_ACCESS_KEY_ID")
DB_USER = secrets.get("DB_USER")
DB_PASSWORD = secrets.get("DB_PASSWORD")
DB_HOST = secrets.get("DB_HOST")
DB_NAME = secrets.get("DB_NAME")
QUEUE_URL = secrets.get("QUEUE_URL")
DB_PORT = 3306

# Set SQS
sqs = boto3.client('sqs', region_name=AWS_REGION)

# Set the SQLAlchemy URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

# Initialize a session using Amazon S3
s3 = boto3.client("s3")
BUCKET_NAME = "ubs-agents"
EXPIRATION = 60 # URL expires in 1 minute
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "application/pdf"]

db = SQLAlchemy(app)

CORS(app)

client_blueprint = Blueprint("client",__name__)

# Helper Function
# Send Email
def send_email(recipient, clientId, user_name):

    client = boto3.client('ses', region_name='ap-southeast-1')

    # Construct email body
    subject = "Upload Your Documents Securely via the Provided Link"
    body_text = f"""
    Dear {user_name},

    To facilitate the secure upload of your documents, please use the link below, which is unique to you and can only be used by you to upload your documents:

    http://scrooge-upload-website.s3-website-ap-southeast-1.amazonaws.com/?id={clientId}

    Instructions for Uploading Your Documents:
      1.  Click the Link: Open the link provided above in your web browser.
      2.  Select Your Documents: Use the upload interface to select the documents you wish to upload.
      3.  Upload: Follow the on-screen prompts to complete the upload process.

    Important: Please do not share this link with others. It is meant for your secure and private use only.

    Thank you for your prompt attention to this matter.

    Best regards,
    Scrooge Global Bank
    """
    
    body_html = f"""
    <html>
    <head></head>
    <body>
      <p>Dear {user_name},</p>

      <p>To facilitate the secure upload of your documents, please use the link below, which is unique to you and can only be used by you to upload your documents:</p>

      <p><a href="http://scrooge-upload-website.s3-website-ap-southeast-1.amazonaws.com/?id={clientId}">Upload Document</a></p>

      <p><b>Instructions for Uploading Your Documents:</b></p>
      <ul>
        <li>Click the Link: Open the link provided above in your web browser.</li>
        <li>Select Your Documents: Use the upload interface to select the documents you wish to upload.</li>
        <li>Upload: Follow the on-screen prompts to complete the upload process.</li>
      </ul>
      
      <p><b>Important:</b> Please do not share this link with others. It is meant for your secure and private use only.</p>

      <p>Thank you for your prompt attention to this matter.</p>

      <p>Best regards,</p>
      <p>Scrooge Global Bank</p>
    </body>
    </html>
    """

    try:
        response = client.send_email(
            Source="noreplyitsag2t2@gmail.com",
            Destination={
                'ToAddresses': [recipient],
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
        print(f"Email sent! Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")

def send_message_to_sqs(message_body):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )
    print(f"Message sent! Message ID: {response['MessageId']}")

# Client Model
class Client(db.Model):
    # Table Name is client
    __tablename__ = 'client'

    ClientID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    AgentID = db.Column(db.String(36), nullable=False)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    DateOfBirth = db.Column(db.Date, nullable=False)
    EmailAddress = db.Column(db.String(50), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(50), unique=True, nullable=False)
    Address = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(50), nullable=False)
    State = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    PostalCode = db.Column(db.String(10), nullable=False)
    Gender = db.Column(db.Enum('Male', 'Female', 'Non-binary', 'Prefer not to say'), nullable=False)
    Verified = db.Column(db.Boolean, default=False, nullable=False)  # Added Verified field
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)  # Added deleted_at field
    attempted_uploads = db.Column(db.Integer, default=0, nullable=False)  # Added attempted_uploads field

    def __init__(self, AgentID, FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, Address, City, State, Country, PostalCode, Gender, Verified=False, deleted_at=None):
        self.ClientID = str(uuid.uuid4())
        self.AgentID = AgentID
        self.FirstName = FirstName
        self.LastName = LastName
        self.DateOfBirth = DateOfBirth
        self.EmailAddress = EmailAddress
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.City = City
        self.State = State
        self.Country = Country
        self.PostalCode = PostalCode
        self.Gender = Gender
        self.Verified = Verified
        self.deleted_at = deleted_at
        self.attempted_uploads = 0  # Initialize attempted_uploads to 0

    def json(self):
        return {
            "ClientID": self.ClientID,
            "AgentID": self.AgentID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "DateOfBirth": str(self.DateOfBirth),
            "EmailAddress": self.EmailAddress,
            "PhoneNumber": self.PhoneNumber,
            "Address": self.Address,
            "City": self.City,
            "State": self.State,
            "Country": self.Country,
            "PostalCode": self.PostalCode,
            "Gender": self.Gender,
            "Verified": self.Verified,
            "deleted_at": self.deleted_at,
            "attempted_uploads": self.attempted_uploads # Added attempted_uploads field      
        }

# Health Check
@client_blueprint.route('/health', methods=['GET'])
def home():
    return "OK",200

# Create Client
@client_blueprint.route('', methods=['POST'])
def create_client():

    # Input Validation
    data = request.get_json()
    is_valid = validate_input(data=data)
    if(is_valid['status'] == "error"):
        return is_valid, 400
    
    # Check Email (unique?)
    if db.session.scalar(db.select(Client).filter_by(EmailAddress=data["EmailAddress"])):
        return jsonify(
            {
                "status": "error",
                "error": "email is in system already!"
            }
        ), 409
    
    # Check Phone Number (unique?)
    if db.session.scalar(db.select(Client).filter_by(PhoneNumber=data["PhoneNumber"])):
        return jsonify(
            {
                "status": "error",
                "error": "Phone Number is in system already!"
            }
        ), 409
    
    client = Client(**data)

    try:
        db.session.add(client)
        db.session.commit()

        # Create S3 bucket directory using ClientID
        s3_directory = f"{client.AgentID}/{client.ClientID}/"
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_directory)

        transaction_id = str(uuid.uuid4())

        send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Create|Client",
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        }
    )   

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "An error occurred creating the client",
            "error": str(e)
        }),500

    return jsonify(
        {
            "status": "success",
            "message": f"{client.FirstName} {client.LastName} added!"        }
        ),201

# Verify Client
@client_blueprint.route('<string:clientId>/verify', methods=['POST'])
def verify_client(clientId):

    # Check if client exists
    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    # Set Attempts to 0
    client.attempted_uploads = 0
    db.session.commit()

    if not client:
        return jsonify(
            {
                "status": "error",
                "message": "Client not found"
            }
        ), 404
    
    # Send email to client with link to upload their credentials
    send_email(client.EmailAddress, client.ClientID, client.FirstName + " " + client.LastName)    
    
    transaction_id = str(uuid.uuid4())

    send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Verify|Client",
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        }
    )

    return jsonify(
        {
            "status": "success",
            "message": f"Verification email sent to {client.EmailAddress}"
        }
    ), 200

# Update Client
# SQS Not Done
@client_blueprint.route('<string:clientId>', methods=['PUT'])
def update_client(clientId):
    
    data = request.get_json()

    if not data:
        return jsonify(
            {
                "status": "error",
                "message": "No input data provided"
            }
        ),400
    
    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    if not client:
        return jsonify(
            {
                "status": "error",
                "message": "Client not found"
            }
        )
    
    old_values = {}

    # Input Validation
    is_valid = validate_input(data)
    if(is_valid['status'] == "error"):
        return is_valid, 400
    
    # Update client fields only if new data is provided (keeping old data if not)
    if client.FirstName != data['FirstName']:
        old_values['FirstName'] = client.FirstName
        client.FirstName = data['FirstName']
    if client.LastName != data['LastName']:
        old_values['LastName'] = client.LastName
        client.LastName = data['LastName']
    if client.EmailAddress != data['EmailAddress']:
        old_values['EmailAddress'] = client.EmailAddress
        client.EmailAddress = data['EmailAddress']
    if client.PhoneNumber != data['PhoneNumber']:
        old_values['PhoneNumber'] = client.PhoneNumber
        client.PhoneNumber = data['PhoneNumber']
    if client.Address != data['Address']:
        old_values['Address'] = client.Address
        client.Address = data['Address']
    if client.City != data['City']:
        old_values['City'] = client.City
        client.City = data['City']
    if client.State != data['State']:
        old_values['State'] = client.State
        client.State = data['State']
    if client.Country != data['Country']:
        old_values['Country'] = client.Country
        client.Country = data['Country']
    if client.PostalCode != data['PostalCode']:
        old_values['PostalCode'] = client.PostalCode
        client.PostalCode = data['PostalCode']
    if client.Gender != data['Gender']:
        old_values['Gender'] = client.Gender
        client.Gender = data['Gender']
    
    db.session.commit()

    edited_fields = {}
    for field, old_value in old_values.items():
        edited_fields[field] = {
            "old": old_value,
            "new": getattr(client, field)
        }

    return jsonify(
        {
            "status": "success",
            "message": "Client updated successfully",
            "edited_fields": edited_fields
        }
    ),200

# Get Client
@client_blueprint.route('/<string:clientId>', methods=['GET'])
def get_client(clientId):

    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId, deleted_at=None))

    if client:

        transaction_id = str(uuid.uuid4())

        send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Read|Client",
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        })

        return jsonify(
            {
                "status": "success",
                "client": client.json()
            }
        ), 200
    return jsonify(
        {
            "status": "error",
            "message": "Client not found"
        }
    ), 404

# Get All Clients for Agent
@client_blueprint.route('/all/<string:agentId>', methods=['GET'])
def get_client_by_id(agentId):
    # Get all clients for a specific agent
    clients = db.session.scalars(db.select(Client).filter_by(AgentID=agentId, deleted_at=None)).all()

    if clients:
        return jsonify(
            {
                "status": "success",
                "clients": [client.json() for client in clients]
            }
        ), 200
    return jsonify(
        {
            "status": "error",
            "message": "No clients found"
        }
    ), 404

# Delete Client
@client_blueprint.route('/<string:clientId>', methods=["DELETE"])
def delete_client(clientId):

    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))
    # NOTE: 
    # Set up Cron Job to hard delete periodically?
    # Check if client exists
    if not client:
        return jsonify(
            {
                "status": "error",
                "message": "Client not found"
            }
        ), 404
    # Check if client is already deleted
    if client.deleted_at:
        return jsonify(
            {
                "status": "error",
                "message": "Client already deleted"
            }
        ), 400
    if client:
        try:
            # Soft Delete by setting datetime to datetime.now()
            client.deleted_at = datetime.now()
            db.session.commit()
            return jsonify(
                {
                "status": "success",
                "message": f"{client.FirstName} {client.LastName} deleted!"
                }
            ), 200
        except:
            return jsonify(
                {
                    "status": "error",
                    "message": "An error occurred deleting the client"
                }
            ), 500
    else:
        return jsonify(
            {
                "status": "error",
                "message": "Client not found"
            }            
        ), 404

# Generate Presigned URL
@client_blueprint.route('/<string:clientId>/presigned_url', methods=['POST'])
def generate_presigned_url(clientId, expiration=EXPIRATION):

    data = request.get_json()
    filename = data.get('filename')
    content_type = data.get('content_type')
    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    if not client:
        return jsonify({"error": "Client not found"}), 404

    if not filename or not content_type:
        return jsonify({"error": "Filename and content type are required"}), 400
    
    # Validate content type
    if content_type not in ALLOWED_CONTENT_TYPES:
        return jsonify({"error": "Invalid content type"}), 400
    
    if client.attempted_uploads >= 5:
        return jsonify({"error": "Maximum upload attempts reached, please contact your Agent"}), 403
    
    try:
        # Construct the object key dynamically using the client ID and filename
        object_key = f"{clientId}/{filename}"

        # Generate the presigned URL for the 'put_object' action
        url = s3.generate_presigned_url(
            'put_object',
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
                "ContentType": content_type
            },
            ExpiresIn=expiration
        )
        client.attempted_uploads += 1
        db.session.commit()
        
        transaction_id = str(uuid.uuid4())

        send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Generate Link|Client",
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        })

        return jsonify({
            "link": url
        }), 200

    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return jsonify({"error": "Error generating presigned URL"}), 500

# Verify User
@client_blueprint.route('/<string:clientId>/verify_user', methods=['PUT'])
def verify_user(clientId):
    data = request.get_json()
    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    if not client:
        return jsonify({"error": "Client not found"}), 404
    
    client.Verified = data.get('Verified')
    db.session.commit()

    transaction_id = str(uuid.uuid4())

    send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Verify|Client",
            "attributeName": "Verified",
            "beforeValue": str(not client.Verified),
            "afterValue": str(client.Verified),
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        })
    
    return jsonify({
        "status": "success",
        "message": f"{client.FirstName} {client.LastName} verified!"
    }), 200

# Get Client Documents
@client_blueprint.route('/<string:clientId>/documents', methods=['GET'])
def view_client_documents(clientId):

    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    if not client:
        return jsonify({"error": "Client not found"}), 404

    # List all objects in the S3 bucket directory for the client
    s3_directory = f"{client.ClientID}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_directory)

    documents = []
    if 'Contents' in response:
        for obj in response['Contents']:
            documents.append(obj['Key'])
    
    transaction_id = str(uuid.uuid4())

    send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "Get Documents|Client",
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        })

    return jsonify({
        "documents": documents
    }), 200

# View Client Documents
@client_blueprint.route('/<string:clientId>/documents/presign/<string:documentName>', methods=['GET'])
def view_client_document(clientId, documentName):
    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    if not client:
        return jsonify({"error": "Client not found"}), 404

    # Generate a presigned URL for the specified document
    object_key = f"{client.ClientID}/{documentName}"
    
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key
            },
            ExpiresIn=EXPIRATION
        )

        transaction_id = str(uuid.uuid4())

        send_message_to_sqs(
        {
            "transactionID": transaction_id,
            "action": "View Documents|Client",
            "agentID": client.AgentID,
            "clientID": client.ClientID,
            "dateTime": datetime.now().isoformat(),
            "clientName": f"{client.FirstName} {client.LastName}",
            "clientEmail": f"{client.EmailAddress}",
        })
        return jsonify({
            "link": url
        }), 200

    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return jsonify({"error": "Error generating presigned URL"}), 500

# Validate Input
def validate_input(data):
    errors = []

    # FirstName: min 2 chars, max 50 chars, alphabetic + spaces only
    if not re.match(r'^[A-Za-z ]{2,50}$', data.get('FirstName', '')):
        errors.append("First Name must be 2-50 characters long and contain only alphabetic characters and spaces.")
    
    # LastName: min 2 chars, max 50 chars, alphabetic + spaces only
    if not re.match(r'^[A-Za-z ]{2,50}$', data.get('LastName', '')):
        errors.append("Last Name must be 2-50 characters long and contain only alphabetic characters and spaces.")
    
    # DOB: valid date format, in the past, age between 18 and 100 years
    try:
        dob = datetime.strptime(data.get('DateOfBirth', ''), '%Y-%m-%d')
        age = (datetime.now() - dob).days // 365
        if dob >= datetime.now():
            errors.append("Date Of Birth must be in the past.")
        elif age < 18 or age > 100:
            errors.append("Age must be between 18 and 100 years.")
    except ValueError:
        errors.append("Date Of Birth must be in the format YYYY-MM-DD.")
    
    # Gender: must be one of Male, Female, Non-binary, Prefer not to say
    if data.get('Gender') not in ['Male', 'Female', 'Non-binary', 'Prefer not to say']:
        errors.append("Gender must be one of Male, Female, Non-binary, Prefer not to say.")
    
    # Email: valid email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('EmailAddress', '')):
        errors.append("Email Address must be a valid email format.")
    
    # PhoneNumber: valid phone number, min 10 digits, max 15 digits
    if not re.match(r'^\+?\d{10,15}$', data.get('PhoneNumber', '')):
        errors.append("Phone Number must be between 10 and 15 digits.")
    
    # Address: min 5 chars, max 100 chars
    if not (5 <= len(data.get('Address', '')) <= 100):
        errors.append("Address must be between 5 and 100 characters.")
    
    # City: min 2 chars, max 50 chars
    if not (2 <= len(data.get('City', '')) <= 50):
        errors.append("City must be between 2 and 50 characters.")
    
    # State: min 2 chars, max 50 chars
    if not (2 <= len(data.get('State', '')) <= 50):
        errors.append("State must be between 2 and 50 characters.")
    
    # Country: min 2 chars, max 50 chars
    if not (2 <= len(data.get('Country', '')) <= 50):
        errors.append("Country must be between 2 and 50 characters.")
    
    # PostalCode: valid postal code format, min 4 chars, max 10 chars
    if not re.match(r'^[A-Za-z0-9 ]{4,10}$', data.get('PostalCode', '')):
        errors.append("PostalCode must be between 4 and 10 characters and follow the valid format.")

    # Load JSON file with countries and their postal code format
    # Credits: https://gist.github.com/lkopocinski/bd4494588458f5a8cc8ffbd12a4deefd for the file!
    with open('postal_codes_regex.json', "r") as file:
        postal_codes = json.load(file)

    country = next((c for c in postal_codes if c["name"].lower() == data["Country"].lower()), None)

    if country:
        # Get the regex pattern for postal code from the JSON
        postal_regex = country.get("postal")

    # Compare the postal code input against the regex for that country
        if not re.match(postal_regex, data.get('PostalCode', '')):
            errors.append(f"Postal Code for {country['name']} is invalid.")
    else:
        errors.append(f"Country {data['Country']} not found in the postal codes list.")

    # Return errors or indicate success
    if errors:
        return {"status": "error", "errors": errors}
    else:
        return {"status": "success", "message": "Validation passed."}

app.register_blueprint(client_blueprint, url_prefix="/clients")

#region Setting up Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5001)
#endregion


