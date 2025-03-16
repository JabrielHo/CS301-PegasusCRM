CREATE SCHEMA UBS;
USE UBS;

CREATE TABLE CLIENT (
	ClientID CHAR(36) NOT NULL PRIMARY KEY UNIQUE,
	AgentID CHAR(36) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DateOfBirth date NOT NULL,
    EmailAddress VARCHAR(50) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(50) NOT NULL UNIQUE,
    Address VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    PostalCode VARCHAR(10) NOT NULL,
    Gender ENUM('Male', 'Female', 'Non-binary', 'Prefer not to say') NOT NULL
);