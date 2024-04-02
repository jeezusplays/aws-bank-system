import axios from 'axios';

const endpoint = "http://localhost:8000";


// Define your helper functions for API calls
const getTransactions = async (token) => {
    try {
        let headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
        console.log(`getting transactions ${'http://localhost:8000/transactions'}`);
        let response = await axios.get('http://localhost:8000/transactions', { headers });
        if (response.status === 200) {
            console.log(response.data);
            // for each transaction, convert timestamp string to epoch
            response.data.forEach(transaction => {
                // timestamp is formated as '%H:%M:%S %d-%m-%Y'
                let parts = transaction.timestamp.split(' ');
                let time = parts[0].split(':');
                let date = parts[1].split('-');
                let timestamp = new Date(date[2], date[1]-1, date[0], time[0], time[1], time[2]).getTime();
                transaction.timestamp = timestamp;
            });

            return response.data;
        }
        return [];
    } catch (error) {
        console.error(error);
        return [];
    }
};

const getAccount = async (token) => {
    // Implement your API call logic here using Axios
    try {
        let headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
        console.log(`getting account ${'http://localhost:8000/account'}`);
        let response = await axios.get('http://localhost:8000/account', { headers });
        if (response.status === 200) {
            console.log(response.data);
            return response.data;
        }
        return null;
    } catch (error) {
        console.error(error);
        return null;
    }
};

const transfer = async (token, data) => {
    try {
        let headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
        console.log(`transfer ${'http://localhost:8000/transactions'}`);
        let response = await axios.post('http://localhost:8000/transactions', data, { headers });
        if (response.status === 200) {
            console.log(response.data);
        }
        return response.data;
    }
    catch (error) {
        // from api
        // return jsonify({"message": "An unexpected error occurred"}), 500

        let error_message = error.response.data;

        console.error(error_message);
        return error_message;
    }
}

// Export the helper functions
export { getTransactions, getAccount, transfer };