<template>
    <div>
        <!-- Your component's template code here -->
        <div>
            <h2>Transaction History</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Description</th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="transaction in transactions.sort((a, b) => a.timestamp - b.timestamp)" :key="transaction.id">
                        <td>{{ formatDate(transaction.timestamp) }}</td>
                        <td>{{ transaction.description }}</td>
                        <td>{{ transaction.amount }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

import axios from 'axios';
import {currentSession} from '../utils/amplify';

export default {
    name: 'Transactions',
    props: {
        transactions: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            transactions: []
        }
    },
    // get transactions using user id from local storage
    async created() {
        let userId = localStorage.getItem('userId');
        let session = await currentSession();
        let accessTokenString = session.accessToken.toString();
        console.log(accessTokenString);

        this.transactions = await this.getTransactions(accessTokenString);
        console.log(this.transactions);
    },
    methods: {
        formatDate(timestamp) {
            // format to this format '%H:%M:%S %d-%m-%Y'
            // Some how tolocalstring makes it 1 month ahead
            let date = new Date(timestamp);
            console.log(date);
            return date.toLocaleString();
            
        },
        async getTransactions(token) {
            try {
                let headers = {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                };
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
        }
    }
}
</script>

<style scoped>
/* Your component's styles here */
</style>