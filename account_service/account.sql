CREATE DATABASE account_service;
use account_service; 
CREATE TABLE Account (
    accountId CHAR(36) PRIMARY KEY DEFAULT (UUID()),    -- Auto-generated unique identifier as a UUID
    clientId CHAR(36) NOT NULL,                         -- Unique identifier for the associated client
    accountType VARCHAR(50) NOT NULL,                   -- Type of account (e.g., Savings, Checking, Business)
    accountStatus VARCHAR(50) DEFAULT "Active",         -- Status of the account (e.g., Active, Inactive, Pending)
    openingDate DATE NOT NULL,                          -- Date when the account was opened
    initialDeposit DECIMAL(10, 2) NOT NULL,             -- Amount of the initial deposit
    currency CHAR(3) NOT NULL,                          -- Currency (SGD for Singapore Dollar)
    branchId CHAR(36) NOT NULL,                         -- Identifier for the branch as a string
    deleted_at DATETIME DEFAULT NULL                    -- Soft delete flag
)