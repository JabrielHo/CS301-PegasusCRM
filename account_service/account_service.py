from flask import Flask, request, jsonify
from flask_cors import CORS
from account_model import db, Account
from sqlalchemy import select
import os
from dotenv import load_dotenv
import datetime
from datetime import timezone
import json

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with open("currencies.json", "r") as f:
    VALID_CURRENCIES = json.load(f)


# Health Check for ALB
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Get Account Details by accountId
@app.route("/api/accounts/<string:accountId>", methods=["GET"])
def get_account(accountId):
    account = db.session.get(Account, accountId)

    if not account or account.is_deleted:
        return jsonify({"message": "Account not found"}), 404

    return jsonify(account.to_dict()), 200


# Get Account Details by clientId
@app.route("/api/accounts/client/<string:clientId>", methods=["GET"])
def get_accounts_by_client(clientId):
    stmt = select(Account).where(
        Account.clientId == clientId, Account.deleted_at == None
    )
    accounts = db.session.execute(stmt).scalars().all()

    if not accounts:
        return jsonify({"message": "No accounts found for this client"}), 404

    return (
        jsonify(
            {
                "clientId": clientId,
                "accounts": [account.to_dict() for account in accounts],
            }
        ),
        200,
    )


# Create Account
@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.json

    required_fields = [
        "clientId",
        "accountType",
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

        # Update the date handling in create_account:
    try:
        if "openingDate" in data:
            opening_date = datetime.datetime.fromisoformat(data["openingDate"]).date()
        else:
            opening_date = datetime.datetime.now(timezone.utc).date()
    except ValueError:
        return (
            jsonify(
                {
                    "message": "Invalid date format for openingDate. Use YYYY-MM-DD format."
                }
            ),
            400,
        )

    try:
        initial_deposit = float(data["initialDeposit"])
        if initial_deposit <= 0:
            return jsonify({"message": "initialDeposit must be a positive number"}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "initialDeposit must be a valid number"}), 400

    if data["currency"] not in VALID_CURRENCIES:
        return (
            jsonify(
                {
                    "message": f"Invalid currency code. Please provide a valid ISO 4217 currency code."
                }
            ),
            400,
        )

    new_account = Account(
        clientId=data["clientId"],
        accountType=data["accountType"],
        accountStatus="Active",  # Auto set to Active
        openingDate=opening_date,
        initialDeposit=initial_deposit,
        currency=data["currency"],
        branchId=data["branchId"],
    )

    db.session.add(new_account)
    db.session.commit()

    try:
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
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"message": "Failed to create account due to database error"}),
            500,
        )
    
# Update Account Status by accountId
@app.route("/api/accounts/<string:accountId>", methods=["PUT"])
def update_account_status(accountId):
    data = request.json
    
    if not data or "accountStatus" not in data:
        return jsonify({"message": "accountStatus field is required"}), 400
    
    account_status = data["accountStatus"]
    
    allowed_statuses = ["Active", "Inactive", "Pending", "Closed"]
    if account_status not in allowed_statuses:
        return (
            jsonify({
                "message": f"Invalid account status. Allowed values: {', '.join(allowed_statuses)}"
            }),
            400
        )
    
    try:
        stmt = select(Account).where(Account.accountId == accountId, Account.deleted_at == None)
        account = db.session.execute(stmt).scalar_one_or_none()
        
        if not account:
            return jsonify({"message": "Account not found"}), 404
        
        if account.accountStatus == account_status:
            return jsonify({
                "message": f"Account status is already '{account_status}', no changes made",
            }), 200
            
        account.accountStatus = account_status
        db.session.commit()
        
        return jsonify({
            "message": "Account status updated successfully",
            "account": account.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update account status due to database error"}), 500


# Delete Account by accountId
@app.route("/api/accounts/<string:accountId>", methods=["DELETE"])
def delete_account_by_accountId(accountId):
    try:
        # First check if account exists regardless of deletion status
        account_check = db.session.execute(
            select(Account).where(Account.accountId == accountId)
        ).scalar_one_or_none()
        
        if not account_check:
            return jsonify({"message": "Account not found"}), 404
            
        if account_check.deleted_at is not None:
            return jsonify({
                "message": "Account was already deleted",
                "deleted_at": account_check.deleted_at.isoformat()
            }), 409
        
        account_check.deleted_at = datetime.datetime.now(timezone.utc)
        db.session.commit()

        return jsonify({
            "message": "Account deleted successfully",
            "deleted_at": account_check.deleted_at.isoformat(),
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete account due to database error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)