from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import date
import os

DB_USER = os.environ.get("DB_USER", "")
DB_PASS = os.environ.get("DB_PASS", "")  
DB_HOST = os.environ.get("DB_HOST", "")
DB_PORT = os.environ.get("DB_PORT", "")
DB_NAME = os.environ.get("DB_NAME", "")

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Transaction model matching your schema
class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    client_account_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    # client_account_id = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(1), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_account_id': self.client_account_id,
            'transaction_type': self.transaction_type,
            'amount': float(self.amount),
            'transaction_date': self.transaction_date.isoformat(),
            'status': self.status
        }


# Get transactions by client ID
@app.route('/api/transactions/client/<client_id>', methods=['GET'])
def get_transactions_by_client(client_id):
    transactions = Transaction.query.filter_by(client_id=client_id).all()
    return jsonify([transaction.to_dict() for transaction in transactions])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)