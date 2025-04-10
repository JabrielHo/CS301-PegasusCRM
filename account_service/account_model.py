from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'Account'
    
    accountId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clientId = db.Column(db.String(36), nullable=False)
    accountType = db.Column(db.String(50), nullable=False)
    accountStatus = db.Column(db.String(50), nullable=False)
    openingDate = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc))
    initialDeposit = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    branchId = db.Column(db.String(36), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    
    def to_dict(self):
        return {
            'accountId': self.accountId,
            'clientId': self.clientId,
            'accountType': self.accountType,
            'accountStatus': self.accountStatus,
            'openingDate': self.openingDate.isoformat(),
            'initialDeposit': float(self.initialDeposit),
            'currency': self.currency,
            'branchId': self.branchId,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
        
    @property
    def is_deleted(self):
        return self.deleted_at is not None

class Branch(db.Model):
    __tablename__ = 'Branch'
    
    branchId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    branchName = db.Column(db.String(100), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    
    def to_dict(self):
        return {
            'branchId': self.branchId,
            'branchName': self.branchName,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None