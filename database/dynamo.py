import os
import boto3
import logging
from time import sleep
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
        {
            'UserID': {'S': '1'},
            'creationDate': {'S': '1/1/2024'},
            'email': {'S': 'samuelchung95@gmail.com'},
            'name': {'S': 'Samuel Chung'},
            'password': {'S': 'password'}
        },{
            'UserID': {'S': '2'},
            'creationDate': {'S': '1/1/2024'},
            'email': {'S': 'test@gmail.com'},
            'name': {'S': 'Test User'},
            'password': {'S': 'password'}
        }
    ]

    account_items = [ 
        {
            'AccountID': {'S': '1'},
            'userID': {'S': '1'},
            'balance': {'N': '2000'},
            'creationDate': {'S': '1/1/2024'},
            'name': {'S': 'Savings Account'}
        },{
            'AccountID': {'S': '2'},
            'userID': {'S': '2'},
            'balance': {'N': '125'},
            'creationDate': {'S': '1/1/2024'},
            'name': {'S': 'Savings Account'}
        }
    ]

    transaction_items = [ 
        {
            'transactionID': {'S': '1'},
            'accountID': {'S': '1'},
            'amount': {'N': '3000'},
            'description': {'S': 'Initial deposit on account creation'},
            'internalTransaction': {'BOOL': False},
            'name': {'S': 'Initial Deposit'},
            'timestamp': {'S': '1/1/2024 12:00:00'},
            'type': {'S': 'deposit'}
        },{
            'transactionID': {'S': '2'},
            'accountID': {'S': '1'},
            'amount': {'N': '-975'},
            'description': {'S': 'Withdrawal at bukit panjang atm'},
            'internalTransaction': {'BOOL': False},
            'name': {'S': 'Withdrawal'},
            'timestamp': {'S': '2024-01-01 12:10:00'},
            'type': {'S': 'withdrawal'}
        },{
            'transactionID': {'S': '3'},
            'accountID': {'S': '1'},
            'amount': {'N': '-25'},
            'description': {'S': 'Transfer to account 2 via mobile app'},
            'internalTransaction': {'BOOL': True},
            'name': {'S': 'Transfer Out'},
            'timestamp': {'S': '2024-01-03 12:00:00'},
            'type': {'S': 'transfer'}
        },{
            'transactionID': {'S': '4'},
            'accountID': {'S': '2'},
            'amount': {'N': '100'},
            'description': {'S': 'Initial deposit on account creation'},
            'internalTransaction': {'BOOL': False},
            'name': {'S': 'Initial Deposit'},
            'timestamp': {'S': '2024-01-01 12:00:00'},
            'type': {'S': 'deposit'}
        },{
            'transactionID': {'S': '5'},
            'accountID': {'S': '2'},
            'amount': {'N': '25'},
            'description': {'S': 'Transfer from account 1 via mobile app'},
            'internalTransaction': {'BOOL': True},
            'name': {'S': 'Transfer In'},
            'timestamp': {'S': '2024-01-03 12:00:00'},
            'type': {'S': 'transfer'}
        }
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