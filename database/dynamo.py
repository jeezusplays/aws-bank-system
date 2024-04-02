import os
import boto3
import logging
from datetime import datetime
from time import sleep
from data import *
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve AWS access key and secret from environment variables
access_key = os.getenv("AWS_ACCESS_KEY")
secret_key = os.getenv("AWS_SECRET_KEY")


# Create a session using the credentials
session = boto3.Session(
    region_name="ap-southeast-1",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# Create a DynamoDB client
dynamodb = session.client('dynamodb')

# Decorator to catch exceptions
def trycatch(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.info(f"Error: {e}")
    return wrapper

def get_table_names():
    response = dynamodb.list_tables()
    return response['TableNames']

# Reset the data in the database
@trycatch
def reset_database():
    # TODO: Implement your logic to reset the database here
    # Delete all the tables in the database
    # Check if the tables exist before deleting them
    table_names = get_table_names()
    logging.info(f"Tables: {table_names}")
    if 'Accounts' in table_names:
        logging.info("Deleting Accounts table...")
        dynamodb.delete_table(TableName='Accounts')
        while 'Accounts' in get_table_names():
            logging.info("Waiting for table to be deleted...")
            sleep(1)
    
    logging.info("Creating Accounts table...")
    dynamodb.create_table(
        TableName='Accounts',
        KeySchema=[
            {
                'AttributeName': 'AccountID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'userID',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'AccountID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'userID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    if 'Transactions' in table_names:
        logging.info("Deleting Transactions table...")
        dynamodb.delete_table(TableName='Transactions')
        while 'Transactions' in get_table_names():
            logging.info("Waiting for table to be deleted...")
            sleep(1)

    logging.info("Creating Transactions table...")
    dynamodb.create_table(
        TableName='Transactions',
        KeySchema=[
            {
                'AttributeName': 'transactionID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'accountID',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'transactionID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'accountID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    if 'Users' in table_names:
        logging.info("Deleting Users table...")
        dynamodb.delete_table(TableName='Users')
        while 'Users' in get_table_names():
            logging.info("Waiting for table to be deleted...")
            sleep(1)
    logging.info("Creating Users table...")
    dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {
                'AttributeName': 'UserID',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    sleep(20)
    
# Insert mock data into the database
@trycatch
def insert_mock_data():
    # TODO: Implement your logic to insert mock data here
    
    logging.info("Inserting mock data into the database...")

    user_items = [
        User(user_id='1', email='samuelchung95@gmail.com', name='Samuel Chung').to_dict(),
        User(user_id='2', email='test@gmail.com', name='Test User').to_dict()
    ]

    account_items = [
        Account(account_id='1', user_id='1', balance=2000, creation_date='1/1/2024', name='Savings Account').to_dict(),
        Account(account_id='2', user_id='2', balance=125, creation_date='1/1/2024', name='Savings Account').to_dict()
    ]

    transaction_items = [
        Transaction(transaction_id='1', account_id='1', amount=3000, description='Initial deposit on account creation', internal_transaction=False, name='Initial Deposit', timestamp='1/1/2024 12:00:00', transaction_type='deposit', detected_fraud=False).to_dict(),
        Transaction(transaction_id='2', account_id='1', amount=-975, description='Withdrawal at bukit panjang atm', internal_transaction=False, name='Withdrawal', timestamp='2024-01-01 12:10:00', transaction_type='withdrawal', detected_fraud=False).to_dict(),
        Transaction(transaction_id='3', account_id='1', amount=-25, description='Transfer to account 2 via mobile app', internal_transaction=True, name='Transfer Out', timestamp='2024-01-03 12:00:00', transaction_type='transfer', detected_fraud=False).to_dict(),
        Transaction(transaction_id='4', account_id='2', amount=100, description='Initial deposit on account creation', internal_transaction=False, name='Initial Deposit', timestamp='2024-01-01 12:00:00', transaction_type='deposit', detected_fraud=False).to_dict(),
        Transaction(transaction_id='5', account_id='2', amount=25, description='Transfer from account 1 via mobile app', internal_transaction=True, name='Transfer In', timestamp='2024-01-03 12:00:00', transaction_type='transfer', detected_fraud=False).to_dict()
    ]

    for item in user_items:
        response = dynamodb.put_item(TableName='Users', Item=item)
        logging.info(f"Inserted item: {response}")

    for item in account_items:
        response = dynamodb.put_item(TableName='Accounts', Item=item)
        logging.info(f"Inserted item: {response}")

    for item in transaction_items:
        response = dynamodb.put_item(TableName='Transactions', Item=item)
        logging.info(f"Inserted item: {response}")

# Get users by user ID and parse the response into a User object
@trycatch
def get_user_by_id(user_id: str):
    response = dynamodb.get_item(TableName='Users', Key={'UserID': {'S': user_id}})
    item = response['Item']
    user = User(user_id=item['UserID']['S'], email=item['email']['S'], name=item['name']['S'])
    return user

# Get accounts by user ID and parse the response into a list of Account objects
@trycatch
def get_accounts_by_user_id(user_id: str) -> List[Account]:
    response = dynamodb.query(
        TableName='Accounts',
        KeyConditionExpression='UserID = :user_id',
        ExpressionAttributeValues={
            ':user_id': {'S': user_id}
        }
    )
    items = response['Items']
    accounts = []
    for item in items:
        account = Account(account_id=item['AccountID']['S'], user_id=item['userID']['S'], balance=float(item['balance']['N']), creation_date=item['creationDate']['S'], name=item['name']['S'])
        accounts.append(account)
    return accounts

# Get transactions by account ID and parse the response into a list of Transaction objects
@trycatch
def get_transactions_by_account_id(account_id: str) -> List[Transaction]:
    response = dynamodb.query(
        TableName='Transactions',
        KeyConditionExpression='AccountID = :account_id',
        ExpressionAttributeValues={
            ':account_id': {'S': account_id}
        }
    )
    items = response['Items']
    transactions = []
    for item in items:
        transaction = Transaction(transaction_id=item['transactionID']['S'], account_id=item['accountID']['S'], amount=float(item['amount']['N']), description=item['description']['S'], internal_transaction=item['internalTransaction']['BOOL'], name=item['name']['S'], timestamp=item['timestamp']['S'], transaction_type=item['type']['S'], detected_fraud=item['detectedFraud']['BOOL'])
        transactions.append(transaction)
    return transactions

# Create transaction and insert into the database
@trycatch
def create_transaction(transaction: Transaction):
    item = transaction.to_dict()
    response = dynamodb.put_item(TableName='Transactions', Item=item)
    logging.info(f"Inserted item: {response}")

# Make a transfer between two accounts
@trycatch
def make_transfer(from_account_id: str, to_account_id: str, amount: float):
    # Get the account details
    from_account = get_accounts_by_user_id(from_account_id)[0]
    to_account = get_accounts_by_user_id(to_account_id)

    # Check if the from account has sufficient balance
    if from_account.balance < amount:
        return "Insufficient balance"
    
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create transactions for the transfer
    from_transaction = Transaction(transaction_id='1', account_id=from_account_id, amount=-amount, description='Transfer to account ' + to_account_id, internal_transaction=True, name='Transfer Out', timestamp=time, transaction_type='transfer', detected_fraud=False)
    to_transaction = Transaction(transaction_id='2', account_id=to_account_id, amount=amount, description='Transfer from account ' + from_account_id, internal_transaction=True, name='Transfer In', timestamp=time, transaction_type='transfer', detected_fraud=False)

    # Insert transactions into the database
    create_transaction(from_transaction)
    create_transaction(to_transaction)

    return "Transfer successful"



if __name__ == "__main__":
    reset_database()
    insert_mock_data()
    print("Database has been reset and mock data has been inserted successfully.")


# Accounts Table
# AccountID (String)
# userID (String) Sort Key
# balance
# creationDate
# name

# Transactions Table
# transactionID (String)
# accountID (String) Sort Key
# amount
# description
# internalTransaction
# name
# timestamp
# type

# Users Table
# UserID (String)
# creationDate
# email
# name
# password