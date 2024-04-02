import Vue from "vue";
import Vuex from "vuex";
import {LOGIN_URL} from "../utils/var";
import router from "../router/index";
import { getCurrentUser } from 'aws-amplify/auth';
import axios from 'axios'; // Import the axios package

// import VuexPersistence from "vuex-persist";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    current_user: null,
    user_profile: {},
    user_bank_details: {}
  },
  mutations: {
    set_current_user(state, val) {
      state.current_user = val;
    },
    set_user_profile(state, val) {
      state.user_profile = val;
    },
    set_user_bank_details(state, val) {
      state.user_bank_details = val;
    }
  },
  actions: {
    log_out({ commit }) {
      commit("set_current_user", null);
      commit("set_user_profile", {});
      commit("set_user_bank_details", {});
      localStorage.removeItem("login");
      localStorage.removeItem("logged_acct_no");
      router.push("/auth");
    },
    update_current_user(store, val) {
      store.commit("set_current_user", val);
    },
    update_user_profile(store, val) {
      store.commit("set_user_profile", val);
    },
    update_user_bank_details(store, val) {
      store.commit("set_user_bank_details", val);
    },
    fetch_user_profile({ commit }) {
      getCurrentUser ()
        .then((username, userId, signInDetails) => {
          console.log("userId: ", userId);
          console.log("signInDetails: ", signInDetails);
          console.log("username: ", username);
          commit("set_user_profile", userId);
        })
        .catch((error) => {
          console.log(error);
          // go to login page
          window.location.href = LOGIN_URL;
        });
    },
    fetch_user_bank_details({ commit }) {
      axios.get("/api/user/bank-details")
        .then((response) => {
          commit("set_user_bank_details", response.data);
        })
        .catch((error) => {
          console.log(error);
          // go to login page
          router.push("/auth");
        });
    },
    fetch_current_user({ commit }) {
      getCurrentUser ()
        .then((username, userId, signInDetails) => {
          console.log("userId: ", userId);
          console.log("signInDetails: ", signInDetails);
          console.log("username: ", username);
          commit("set_user_profile", userId);
        })
        .catch((error) => {
          console.log(error);
          // go to login page
          window.location.href = LOGIN_URL;
        });
    },
  },
  modules: {}
});
