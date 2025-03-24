from flask import Flask, request, jsonify
from flask_cors import CORS
from account_model import db, Account
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

db.init_app(app)


# Health Check for ALB
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Get Account
@app.route("/api/accounts/<string:accountId>", methods=["GET"])
def get_account(accountId):
    account = db.session.get(Account, accountId)

    if not account or account.isDeleted:
        return jsonify({"message": "Account not found"}), 404

    return jsonify(account.to_dict()), 200


# Create Account
@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.json

    required_fields = [
        "clientId",
        "accountType",
        "accountStatus",
        "initialDeposit",
        "currency",
        "branchId",
    ]

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return (
            jsonify(
                {"message": "Missing required fields", "missing_fields": missing_fields}
            ),
            400,
        )

    try:
        initial_deposit = float(data["initialDeposit"])
        if initial_deposit <= 0:
            return jsonify({"message": "initialDeposit must be a positive number"}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "initialDeposit must be a valid number"}), 400

    if len(data["currency"]) != 3:
        return jsonify({"message": "currency must be a 3-letter ISO code"}), 400

    ## Need to check proper authorization method with cognito
    #
    # client_header = request.headers.get("ClientID")
    # if client_header and client_header != data["clientId"]:
    #     return (
    #         jsonify(
    #             {"message": "Unauthorized: ClientID mismatch between header and body"}
    #         ),
    #         403,
    #     )

    try:
        if "openingDate" in data:
            opening_date = data["openingDate"]
            datetime.date.fromisoformat(opening_date)
        else:
            opening_date = datetime.date.today().isoformat()
    except ValueError:
        return (
            jsonify(
                {
                    "message": "Invalid date format for openingDate. Use YYYY-MM-DD format."
                }
            ),
            400,
        )

    new_account = Account(
        clientId=data["clientId"],
        accountType=data["accountType"],
        accountStatus=data["accountStatus"],
        openingDate=opening_date,
        initialDeposit=initial_deposit,
        currency=data["currency"],
        branchId=data["branchId"],
        isDeleted=False,
    )

    db.session.add(new_account)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Account created successfully",
                "account": new_account.to_dict(),
            }
        ),
        201,
    )


# Delete Account
@app.route("/api/accounts/<string:accountId>", methods=["DELETE"])
def delete_account(accountId):
    account = db.session.get(Account, accountId)

    if not account or account.isDeleted:
        return jsonify({"message": "Account not found"}), 404
    
    ## Need to check proper authorization method with cognito
    #
    # client_header = request.headers.get("ClientID")
    # if not client_header:
    #     return jsonify({"message": "Unauthorized: missing ClientID header"}), 401

    # if account.clientId != client_header:
    #     return (
    #         jsonify(
    #             {"message": "Unauthorized: you are not allowed to delete this account"}
    #         ),
    #         403,
    #     )

    account.isDeleted = True
    db.session.commit()

    return jsonify({"message": "Account deleted successfully"}), 200

# Unccoment for local
# if __name__ == "__main__":
#     app.run(port=5000, debug=True)

# Uncomment for docker
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
