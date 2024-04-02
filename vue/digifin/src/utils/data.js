class User {
    constructor(user_id, email, name) {
        this.user_id = user_id;
        this.email = email;
        this.name = name;
    }

    to_dict() {
        return {
            'UserID': {'S': this.user_id},
            'email': {'S': this.email},
            'name': {'S': this.name}
        };
    }
}

class Account {
    constructor(account_id, user_id, balance, creation_date, name) {
        this.account_id = account_id;
        this.user_id = user_id;
        this.balance = balance;
        this.creation_date = new Date(creation_date);
        this.name = name;
    }

    to_dict() {
        return {
            'AccountID': {'S': this.account_id},
            'UserID': {'S': this.user_id},
            'balance': {'N': this.balance.toString()},
            'creationDate': {'S': this.creation_date.toISOString()},
            'name': {'S': this.name}
        };
    }
}

class Transaction {
    constructor(transaction_id, account_id, amount, description, internal_transaction, name, timestamp, transaction_type, detected_fraud) {
        this.transaction_id = transaction_id;
        this.account_id = account_id;
        this.amount = amount;
        this.description = description;
        this.internal_transaction = internal_transaction;
        this.name = name;
        this.timestamp = new Date(timestamp);
        this.transaction_type = transaction_type;
        this.detected_fraud = detected_fraud;
    }

    to_dict() {
        return {
            'TransactionID': {'S': this.transaction_id},
            'AccountID': {'S': this.account_id},
            'amount': {'N': this.amount.toString()},
            'description': {'S': this.description},
            'internalTransaction': {'BOOL': this.internal_transaction},
            'name': {'S': this.name},
            'timestamp': {'S': this.timestamp.toISOString()},
            'type': {'S': this.transaction_type},
            'detectedFraud': {'BOOL': this.detected_fraud},
        };
    }
}