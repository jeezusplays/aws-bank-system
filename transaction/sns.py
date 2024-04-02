import os
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

if AWS_ACCESS_KEY and AWS_SECRET_KEY:
    sns_client = boto3.client('sns',
                            region_name='ap-southeast-1',
                            aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY)

else:
    sns_client = boto3.client('sns',
                            region_name='ap-southeast-1')

def send_sns_message(topic_arn, message):
    
    # Publish the message to the specified topic
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )

    # Print the response
    print(response)
