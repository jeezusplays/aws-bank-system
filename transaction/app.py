from flask import Flask
import os
import requests
import logging
import json
from flask import request

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', filename='flask.log')
LAMBDA_ENDPOINT = os.environ['LAMBDA_ENDPOINT']
PORT = os.environ['PORT'] 

app = Flask(__name__)


# Try catch decorator
def trycatch(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            return str(e), 500
    return wrapped

@trycatch
@app.route('/transactions/<userid>', methods=['GET'])
def get_transactions(userid):

    # Make a call to the lambda function
    response = requests.post(LAMBDA_ENDPOINT, json=json.dumps({'userid': userid}))

    if response.status_code != 200:
        return f'Error: {response.status_code}', response.status_code

    return response.json()

@trycatch
@app.route('/transactions', methods=['POST'])
def create_transactions():
    data:dict = request.get_json()

    # Make a call to the lambda function
    response = requests.post(LAMBDA_ENDPOINT, json=json.dumps(data))

    if response.status_code != 200:
        return f'Error: {response.status_code}', response.status_code

    return response.json()


# Test route
@trycatch
@app.route('/test/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int(PORT), debug=True)