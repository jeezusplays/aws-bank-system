from flask import Flask, jsonify, request, abort
import os
import requests
import logging
import json
import jwt
import requests
from dotenv import load_dotenv
from dynamo import *
from functools import wraps
from flask_cors import CORS
import random

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filename='flask.log')

PORT = os.environ['PORT'] 
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

app = Flask(__name__)
CORS(app)

COGNITO_ISSUER = f'https://cognito-idp.ap-southeast-1.amazonaws.com/ap-southeast-1_BlgygOvKY/.well-known/jwks.json'
COGNITO_AUDIENCE = 'os8nip21cc8jigtltlpdnhs06'


# Try catch decorator
def trycatch(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError as e:
            logging.exception(e)
            abort(401, e)
        except jwt.InvalidTokenError as e:
            logging.exception(e)
            abort(401, e)
        except Exception as e:
            # Log the exception here
            print(f"An error occurred: {e}")
            # log stack trace
            logging.exception(e)
            # Return a generic error response
            return jsonify({"message": str(e)}), 500
    return decorated_function

def get_jwks():
    response = requests.get(COGNITO_ISSUER)
    return response.json()

# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logging.info('Verifying token...')
        token = request.headers.get('Authorization', None)
        if token is None:
            raise jwt.InvalidTokenError("Missing authorization token.")

        token = token.replace("Bearer ", "", 1)

        # Decode the JWT header to fetch the kid
        headers = jwt.get_unverified_header(token)
        kid = headers['kid']

        # Fetch JWKS and find the public key
        jwks = get_jwks()
        key = next((item for item in jwks["keys"] if item["kid"] == kid), None)
        if key is None:
            # throw 401 if public key not found 
            raise jwt.InvalidTokenError("Public key not found.")
        
        # Prepare the public key
        # public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        # logging.info(f'Public key: {public_key}')

        # Verify the token
        try:
            decoded = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})
            # add decoded token to payload
            kwargs['decoded'] = decoded
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token expired.")

        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token.")


        # Optionally add the decoded token to Flask's global g if you need to use it in your route
        # from flask import g
        # g.user = decoded

        return f(*args, **kwargs)

    return decorated


@app.route('/account', methods=['GET'])
@trycatch
@token_required
def get_account(*args, **kwargs):
    # get decoded token from payload
    decoded = kwargs.get('decoded')
    userid = decoded['sub']

    logging.info(f'Getting account for user {userid}')

    account = get_accounts_by_user_id(userid)[0]
    account = account.to_dict_json()

    return jsonify(account)


@app.route('/transactions', methods=['GET'])
@trycatch
@token_required
def get_transactions(*args, **kwargs):
    # get decoded token from payload
    logging.info('Getting transactions...')
    decoded = kwargs.get('decoded')
    userid = decoded['sub']

    logging.info(f'Getting transactions for user {userid}')

    accounts = get_accounts_by_user_id(userid)
    transactions = get_transactions_by_account_id(accounts[0].to_dict()['AccountID']['S'])
    transactions = [t.to_dict_json() for t in transactions]

    return jsonify(transactions)


@app.route('/transactions', methods=['POST'])
@trycatch
@token_required
def create_transactions(*args, **kwargs):
    data:dict = request.get_json()
    decoded = kwargs.get('decoded')
    userid = decoded['sub']

    suspeciousTransaction = random.choice([True, False])
    # suspeciousTransaction = False
    logging.info(f'Transaction is suspecious: {suspeciousTransaction}')

    if suspeciousTransaction:
        # send SNS message
        message = f"Suspecious transaction detected for user {userid}\n{data}"
        logging.info(f'Sending SNS message: {message}')
        send_sns_message(os.environ['SNS_TOPIC_ARN'], message)

        return jsonify({"message": "Transaction is under review."})
    
    logging.info(f'Creating transaction for user {userid}')
    try:
        make_transfer(userid, data['to'], data['amount'])
    except Exception as e:
        logging.exception(e)
        raise e
        

    return jsonify({"message": "Transaction successful."})


# Test route
@trycatch
@app.route('/test', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@trycatch
@app.route('/setup', methods=['GET'])
def setup():
    reset_database()
    insert_mock_data()
    return 'DynamoDB setup complete.'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int(PORT), debug=True)