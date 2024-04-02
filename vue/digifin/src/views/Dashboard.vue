<template>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <div class="card m-3">
                        <div class="card-body">
                            <h5 class="card-title">Account Balance</h5>
                            <p class="card-text">{{ account.balance }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <transactions></transactions>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {getAccount} from '../utils/api';
import {currentSession} from '../utils/amplify';
import Transactions from '../components/Transactions.vue';
import router from "@/router";

export default {
    name: 'Dashboard',
    components: {
        Transactions
    },
    data() {
        return {
            account: {
                balance: 0
            },
        }
    },
    async created() {
        let userId = localStorage.getItem('userId');
        currentSession()
        .then(async session => {
            let accessTokenString = session.accessToken.toString();
            this.account = await getAccount(accessTokenString);
        })
        .catch(err => {
            router.push
        });
 
    },
    methods: {
        async getAccount(token) {
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
        }
    }
}
</script>

<style scoped>
/* Your component styles go here */
</style>