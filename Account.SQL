CREATE TABLE Account (
    AccountID CHAR(36) PRIMARY KEY DEFAULT (UUID()),  -- Auto-generated unique identifier as a UUID
    ClientID CHAR(36) NOT NULL,                       -- Unique identifier for the associated client as a string
    AccountType VARCHAR(50) NOT NULL,                 -- Type of account (e.g., Savings, Checking, Business)
    AccountStatus VARCHAR(50) NOT NULL,               -- Status of the account (e.g., Active, Inactive, Pending)
    OpeningDate DATE NOT NULL,                        -- Date when the account was opened
    InitialDeposit DECIMAL(10, 2) NOT NULL,           -- Amount of the initial deposit
    Currency CHAR(3) NOT NULL,                        -- Currency (SGD for Singapore Dollar)
    BranchID CHAR(36) NOT NULL                        -- Identifier for the branch as a string
)