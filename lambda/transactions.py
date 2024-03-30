import json
import boto3
import random
import logging
import pymysql

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filename='fraud.log')


def lambda_handler(event, context):
    
    logging.info(event, context)
    
    # Parse the event data (payload)
    data = json.loads(event['body'])
    transactionID = data['transactionID']
    accountID = data['accountID']
    amount = data['amount']
    description = data['description']
    internalTransaction = data['internalTransaction']
    name = data['name']
    timestamp = data['timestamp']
    type = data['type']
    
    try:
        
        # Connect to your RDS instance
        # Replace values with your RDS endpoint, username, password, etc.
        HOST = 'your_rds_endpoint'
        USER = 'your_db_username'
        PASSWORD = 'your_db_password'
        DATABASE = 'transactionDB'
        
        connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD)
        
        # Insert data into the database
        with connection.cursor() as cur:
            cur.execute("USE {}".format(DATABASE))
            cur.execute("INSERT INTO transaction (transactionID, accountID, amount, description, internalTransaction, name, timestamp, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (transactionID, accountID, amount, description, internalTransaction, name, timestamp, type))
            connection.commit()

        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Items added to RDS successfully."
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
    
    # Your fraud detection logic here
    fraud_detected = False  # Placeholder for fraud detection logic
    if random.randint(0,1)==1:
        fraud_detected = True
    
    if not fraud_detected:
        # If no fraud detected, add items to RDS
        
    else:
        # If fraud detected, send to SNS topic
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Fraud detected. Items not added to RDS."
            })
        }