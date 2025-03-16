from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import uuid
import json

import re
from datetime import datetime

app = Flask(__name__)
# Query from Local MySQL UBS DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/UBS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

client_blueprint = Blueprint("client",__name__)

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

    def __init__(self, AgentID, FirstName, LastName, DateOfBirth, EmailAddress, PhoneNumber, Address, City, State, Country, PostalCode, Gender):
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
            "Gender": self.Gender
        }

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
    
    client = Client("A123", **data)

    try:
        db.session.add(client)
        db.session.commit()
    except:
        return jsonify({
            "status": "error",
            "message": "An error occurred creating the client"
        }),500

    return jsonify(
        {
            "status": "success",
            "message": f"{client.FirstName} {client.LastName} added!"        }
        ),201

# Verify Client
# BRUH WTF DO I DO FOR THIS
@client_blueprint.route('<clientId>/verify', methods=['POST'])
def verify_client():
    return

# Update Client
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

    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))

    if client:
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

# Delete Client
# NOTE: They say do a soft deletion? Should I change to become active/inactive instead?
@client_blueprint.route('/<string:clientId>', methods=["DELETE"])
def delete_client(clientId):

    client = db.session.scalar(db.select(Client).filter_by(ClientID=clientId))
    if client:
        try:
            db.session.delete(client)
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

app.register_blueprint(client_blueprint, url_prefix="/clients")

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

#region Setting up Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8080, debug=True)
#endregion