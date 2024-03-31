-- transactionID (primarykey)
-- accountID 
-- amount
-- description
-- internalTransaction
-- name
-- timestamp 
-- type (deposit, withdrawal, transferIn, transferOut)

DROP DATABASE IF EXISTS transactionDB;
CREATE DATABASE transactionDB;
USE transactionDB;

DROP TABLE IF EXISTS transaction;

CREATE TABLE transaction (
    transactionID INT PRIMARY KEY AUTO_INCREMENT,
    accountID INT NOT NULL,
    amount DECIMAL(10,2),
    description VARCHAR(255),
    internalTransaction BOOLEAN,
    name VARCHAR(255),
    timestamp TIMESTAMP,
    type ENUM('deposit', 'withdrawal', 'transfer')
);

-- Insert data into transaction table

INSERT INTO transaction (accountID, amount, description, internalTransaction, name, timestamp, type) VALUES
(1, 3000.00, 'Initial deposit on account creation', 0, 'Initial Deposit', '2024-01-01 12:00:00', 'deposit'),
(1, 50.00, 'Withdrawal at bukit panjang atm', 0, 'Withdrawal', '2024-01-01 12:10:00', 'withdrawal'),
(1, -25.00, 'Transfer to account 2 via mobile app', 0, 'Transfer Out', '2024-01-03 12:00:00', 'transfer'),
(2, 100.00, 'Initial deposit on account creation', 0, 'Initial Deposit', '2024-01-01 12:00:00', 'deposit'),
(2, 25.00, 'Transfer from account 1 via mobile app', 0, 'Transfer In', '2024-01-03 12:00:00', 'transfer');

