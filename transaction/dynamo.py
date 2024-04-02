import os
import boto3
import logging
import uuid
from sns import *
from functools import wraps
from datetime import datetime
from time import sleep
from data import *
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# Create a session using the credentials
if AWS_ACCESS_KEY and AWS_SECRET_KEY:
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="ap-southeast-1"
    )
else:
    session = boto3.Session(
        region_name="ap-southeast-1"
    )

# Create a DynamoDB client
dynamodb = session.client('dynamodb')

# Decorator to catch exceptions
def trycatch(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.info(f"Error: {e}")
    return decorated_function

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
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'AccountID',
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
                'AttributeName': 'TransactionID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'AccountID',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'TransactionID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'AccountID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # if 'Users' in table_names:
    #     logging.info("Deleting Users table...")
    #     dynamodb.delete_table(TableName='Users')
    #     while 'Users' in get_table_names():
    #         logging.info("Waiting for table to be deleted...")
    #         sleep(1)


    sleep(20)
    
# Insert mock data into the database
@trycatch
def insert_mock_data():
    # TODO: Implement your logic to insert mock data here
    
    logging.info("Inserting mock data into the database...")

    # user_items = [
    #     User(user_id='1', email='samuelchung95@gmail.com', name='Samuel Chung').to_dict(),
    #     User(user_id='2', email='test@gmail.com', name='Test User').to_dict()
    # ]

    # datetime 1/1/2024
    creation_date = datetime.strptime("2024-01-01 12:00:00", "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S %d-%m-%Y")

    account_items = [
        Account(account_id='1', user_id='1', balance=2000, creation_date=creation_date, name='Savings Account').to_dict(),
        Account(account_id='2', user_id='2', balance=125, creation_date=creation_date, name='Savings Account').to_dict()
    ]

    transaction_items = [
        Transaction(transaction_id='1', account_id='1', amount=3000, description='Initial deposit on account creation', internal_transaction=False, name='Initial Deposit', timestamp=datetime.strptime('2024-01-01 12:10:00', '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d-%m-%Y'), transaction_type='deposit', detected_fraud=False).to_dict(),
        Transaction(transaction_id='2', account_id='1', amount=-975, description='Withdrawal at bukit panjang atm', internal_transaction=False, name='Withdrawal', timestamp=datetime.strptime('2024-01-01 12:10:00', '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d-%m-%Y'), transaction_type='withdrawal', detected_fraud=False).to_dict(),
        Transaction(transaction_id='3', account_id='1', amount=-25, description='Transfer to account 2 via mobile app', internal_transaction=True, name='Transfer Out', timestamp=datetime.strptime('2024-01-03 12:00:00', '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d-%m-%Y'), transaction_type='transfer', detected_fraud=False).to_dict(),
        Transaction(transaction_id='4', account_id='2', amount=100, description='Initial deposit on account creation', internal_transaction=False, name='Initial Deposit', timestamp=datetime.strptime('2024-01-01 12:00:00', '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d-%m-%Y'), transaction_type='deposit', detected_fraud=False).to_dict(),
        Transaction(transaction_id='5', account_id='2', amount=25, description='Transfer from account 1 via mobile app', internal_transaction=True, name='Transfer In', timestamp=datetime.strptime('2024-01-03 12:00:00', '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d-%m-%Y'), transaction_type='transfer', detected_fraud=False).to_dict()
    ]

    # for item in user_items:
    #     response = dynamodb.put_item(TableName='Users', Item=item)
    #     logging.info(f"Inserted item: {response}")

    for item in account_items:
        response = dynamodb.put_item(TableName='Accounts', Item=item)
        logging.info(f"Inserted item: {response}")

    for item in transaction_items:
        response = dynamodb.put_item(TableName='Transactions', Item=item)
        logging.info(f"Inserted item: {response}")

# Get users by user ID and parse the response into a User object
@trycatch
def get_user_by_id(user_id: str) -> User:
    response = dynamodb.get_item(TableName='Users', Key={'UserID': {'S': user_id}})
    item = response['Item']
    user = User(user_id=item['UserID']['S'], email=item['email']['S'], name=item['name']['S'])
    return user

# Get accounts by user ID and parse the response into a list of Account objects

def get_accounts_by_user_id(user_id: str) -> List[Account]:
    response = dynamodb.scan(
        TableName='Accounts',
        FilterExpression='UserID = :user_id',
        ExpressionAttributeValues={
            ':user_id': {'S': user_id}
        }
    )

    logging.info(f"Response: {response}")
    items = response['Items']
    accounts = []
    for item in items:
        account = Account(account_id=item['AccountID']['S'], user_id=item['UserID']['S'], balance=float(item['balance']['N']), creation_date=item['creationDate']['S'], name=item['name']['S'])
        accounts.append(account)
    return accounts

def update_account_balance(account_id: str, amount: float):
    response = dynamodb.update_item(
        TableName='Accounts',
        Key={'AccountID': {'S': account_id}},
        UpdateExpression='SET balance = balance + :amount',
        ExpressionAttributeValues={
            ':amount': {'N': str(amount)}
        }
    )
    logging.info(f"Updated item: {response}")
    return True

# Get transactions by account ID and parse the response into a list of Transaction objects
@trycatch
def get_transactions_by_account_id(account_id: str) -> List[Transaction]:
    response = dynamodb.scan(
        TableName='Transactions',
        FilterExpression='AccountID = :account_id',
        ExpressionAttributeValues={
            ':account_id': {'S': account_id}
        }
    )
    items = response['Items']
    transactions = []
    for item in items:
        transaction = Transaction(transaction_id=item['TransactionID']['S'], account_id=item['AccountID']['S'], amount=float(item['amount']['N']), description=item['description']['S'], internal_transaction=item['internalTransaction']['BOOL'], name=item['name']['S'], timestamp=item['timestamp']['S'], transaction_type=item['type']['S'], detected_fraud=item['detectedFraud']['BOOL'])
        transactions.append(transaction)
    return transactions

# Create transaction and insert into the database
@trycatch
def create_transaction(transaction: Transaction):
    item = transaction.to_dict()
    response = dynamodb.put_item(TableName='Transactions', Item=item)
    logging.info(f"Inserted item: {response}")

# Make a transfer between two accounts
def make_transfer(from_user_id: str, to_account_id: str, amount: float):
    logging.info(f"Making transfer from user {from_user_id} to account {to_account_id} amount {amount}")

    # Get the account details
    from_account = get_accounts_by_user_id(from_user_id)[0]

    logging.info(f"From account: {from_account.to_dict_json()}")

    # Check if the from account has sufficient balance
    if from_account.balance < amount:
        raise Exception("Insufficient balance")
    
    # Update the account balances
    success1 = update_account_balance(from_account.account_id, -amount)
    success2 = update_account_balance(to_account_id, amount)

    # Check if the update was successful
    logging.info(f"Success1: {success1}, Success2: {success2}")
    print(f"Success1: {success1}, Success2: {success2}")

    if not success1 or not success2:
        raise Exception("Transfer failed")
    
    
    time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    uuid1 = str(uuid.uuid4())
    uuid2 = str(uuid.uuid4())

    # Create transactions for the transfer
    from_transaction = Transaction(transaction_id=uuid1, account_id=from_account.account_id, amount=-amount, description='Transfer to account ' + to_account_id, internal_transaction=True, name='Transfer Out', timestamp=time, transaction_type='transfer', detected_fraud=False)
    to_transaction = Transaction(transaction_id=uuid2, account_id=to_account_id, amount=amount, description='Transfer from account ' + from_account.account_id, internal_transaction=True, name='Transfer In', timestamp=time, transaction_type='transfer', detected_fraud=False)

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