from typing import List, Dict, Union
from datetime import datetime

class User:
    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name

    def to_dict(self) -> Dict[str, Dict[str, Union[str, int, bool]]]:
        return {
            'UserID': {'S': self.user_id},
            'email': {'S': self.email},
            'name': {'S': self.name}
        }

    def to_dict_json(self) -> Dict[str, Union[str, int, bool]]:
        return {
            'UserID': self.user_id,
            'email': self.email,
            'name': self.name
        }

class Account:
    def __init__(self, account_id: str, user_id: str, balance: float, creation_date: str, name: str):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance
        self.creation_date:datetime = datetime.strptime(creation_date, '%H:%M:%S %d-%m-%Y')
        self.name = name

    def to_dict(self) -> Dict[str, Dict[str, Union[str, int, bool]]]:
        return {
            'AccountID': {'S': self.account_id},
            'UserID': {'S': self.user_id},
            'balance': {'N': str(self.balance)},
            'creationDate': {'S': self.creation_date.strftime('%H:%M:%S %d-%m-%Y')},
            'name': {'S': self.name}
        }

    def to_dict_json(self) -> Dict[str, Union[str, int, bool]]:
        return {
            'AccountID': self.account_id,
            'UserID': self.user_id,
            'balance': self.balance,
            'creationDate': self.creation_date.strftime('%H:%M:%S %d-%m-%Y'),
            'name': self.name
        }

class Transaction:
    def __init__(self, transaction_id: str, account_id: str, amount: float, description: str, internal_transaction: bool, name: str, timestamp: str, transaction_type: str, detected_fraud: bool):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.description = description
        self.internal_transaction = internal_transaction
        self.name = name
        self.timestamp:datetime = datetime.strptime(timestamp, '%H:%M:%S %d-%m-%Y')
        self.transaction_type = transaction_type
        self.detected_fraud = detected_fraud

    def to_dict(self) -> Dict[str, Dict[str, Union[str, int, bool]]]:
        if self.transaction_id is None:
            return {
                'AccountID': {'S': self.account_id},
                'amount': {'N': str(self.amount)},
                'description': {'S': self.description},
                'internalTransaction': {'BOOL': self.internal_transaction},
                'name': {'S': self.name},
                'timestamp': {'S': self.timestamp.strftime('%H:%M:%S %d-%m-%Y')},
                'type': {'S': self.transaction_type},
                'detectedFraud': {'BOOL': self.detected_fraud},
            }
        return {
            'TransactionID': {'S': self.transaction_id},
            'AccountID': {'S': self.account_id},
            'amount': {'N': str(self.amount)},
            'description': {'S': self.description},
            'internalTransaction': {'BOOL': self.internal_transaction},
            'name': {'S': self.name},
            'timestamp': {'S': self.timestamp.strftime('%H:%M:%S %d-%m-%Y')},
            'type': {'S': self.transaction_type},
            'detectedFraud': {'BOOL': self.detected_fraud},
        }

    def to_dict_json(self) -> Dict[str, Union[str, int, bool]]:
        return {
            'TransactionID': self.transaction_id,
            'AccountID': self.account_id,
            'amount': self.amount,
            'description': self.description,
            'internalTransaction': self.internal_transaction,
            'name': self.name,
            'timestamp': self.timestamp.strftime('%H:%M:%S %d-%m-%Y'),
            'type': self.transaction_type,
            'detectedFraud': self.detected_fraud,
        }

