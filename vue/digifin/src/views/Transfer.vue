<template>
    <div class="container">
        <h1>Transfer</h1>
        <!-- Your transfer form goes here -->
        <form @submit.prevent>
            <div class="mb-3">
                <label for="accountNumber" class="form-label">Account Number</label>
                <input type="text" class="form-control" id="accountNumber" v-model="accountNumber">
            </div>
            <div class="mb-3">
                <label for="amount" class="form-label">Amount</label>
                <input type="number" class="form-control" id="amount" v-model="amount">
            </div>
            <button class="btn btn-primary" @click="internalTransfer" >Transfer</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import {currentSession} from '../utils/amplify';
// import router from "@/router";

export default {
    name: 'Transfer',
    // Your component logic goes here
    data() {
        return {
            accountNumber: '',
            amount: 0
        }
    },
    methods: {
        async transfer(token, data){
            try {
                let headers = {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                };
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
        },

        internalTransfer() {
            let userId = localStorage.getItem('userId');
            currentSession()
            .then(async session => {
                let accessTokenString = session.accessToken.toString();
                let data = {
                    to: this.accountNumber,
                    amount: this.amount
                }

                this.transfer(accessTokenString, data)
                .then(response => {
                    console.log(response);
                    let message = response.message;
                    // alert message
                    alert(message);
                }).catch(err => {
                    console.log(err);
                });
                // router.push('/dashboard');
            })
            .catch(err => {
                console.log(err);
                // router.push('/');
            });
            }
    }
}
</script>

<style scoped>
/* Your component styles go here */
</style>