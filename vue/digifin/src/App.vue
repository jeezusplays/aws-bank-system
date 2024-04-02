<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { Amplify } from 'aws-amplify';
Amplify.configure({
    Auth: {
      Cognito: {
        userPoolClientId: "os8nip21cc8jigtltlpdnhs06",
        userPoolId: "ap-southeast-1_BlgygOvKY",
        loginWith: { // Optional
          oauth: {
            domain: "https://digifin.auth.ap-southeast-1.amazoncognito.com",
            scopes: ['openid email phone profile'],
            redirectSignIn: [],
            responseType: 'code'
          }
        }
      }
    }
  });
</script>

<template>
  <header>

      <nav class="navbar navbar-expand-lg navbar-light bg-light mb-2">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Digifin</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item" v-if="!isLoggedIn">
                <RouterLink to="/" class="nav-link">Login</RouterLink>
              </li>
              <template v-if="isLoggedIn">
                <li class="nav-item">
                  <RouterLink to="/dashboard" class="nav-link">Home</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink to="/transfer" class="nav-link">Transfer</RouterLink>
                </li>
              </template>
              
            </ul>
            <span class="navbar-text ms-auto">
              {{ user.email }}
            </span>
          </div>
        </div>
      </nav>

  </header>

  <RouterView />
</template>

<script>
  import { Hub } from 'aws-amplify/utils';
  import { getCurrentUser } from 'aws-amplify/auth';
  import router from "@/router";

  export default {
    data() {
      return {
        user: {
          email: '',
        },
        isLoggedIn: false
      }
    },
    async created() {
      try {
        const { username, userId, signInDetails } = await getCurrentUser();
        this.user.email = signInDetails.loginId;
        this.user.userId = userId;
        this.isLoggedIn = true;
        // Set local storage
        localStorage.setItem('isLoggedIn', true);
        localStorage.setItem('userId', userId);
        localStorage.setItem('email', this.user.email);

        router.push('/dashboard');
      } catch (err) {
          console.log(err);
          Hub.listen('auth', ({ payload }) => {
            console.log(payload.event);
            switch (payload.event) {
              case 'signedIn':
                router.push('/dashboard');
                
                break;
              
              case 'signedOut':
                localStorage.clear();
                router.push('/');
                break;
            }
          });
      }



    }
  }


</script>

<style scoped>

</style>
