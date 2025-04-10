CREATE DATABASE account_service;
use account_service; 
CREATE TABLE Account (
    accountId CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    clientId CHAR(36) NOT NULL,
    accountType VARCHAR(50) NOT NULL,                  
    accountStatus VARCHAR(50) NOT NULL,                
    openingDate DATE NOT NULL,                       
    initialDeposit DECIMAL(10, 2) NOT NULL,            
    currency CHAR(3) NOT NULL,                        
    branchId CHAR(36) NOT NULL,                         
    deleted_at DATETIME DEFAULT NULL                
)

CREATE TABLE Branch (
    branchId CHAR(36) PRIMARY KEY DEFAULT (UUID()),   
    branchName VARCHAR(100) NOT NULL,
    deleted_at DATETIME DEFAULT NULL                    
)