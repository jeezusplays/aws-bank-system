<script setup>
    import { Authenticator } from "@aws-amplify/ui-vue";
    import "@aws-amplify/ui-vue/styles.css";

</script>

<template>
  <authenticator class="mt-5">
    <template v-slot="{ user, signOut }">
      <h1>Hello {{ user.signInDetails.loginId }}!</h1>
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator>
</template>

<script>
  export default {
    name: 'Cognito',
    data(){
      return {
        user: {
          email: '',
          userId: '',
        }
      }
    },
    
  }

  

</script>