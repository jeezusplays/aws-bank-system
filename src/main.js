import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router/index";
import store from "./store/index";
import vuetify from "./plugins/vuetify";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "@mdi/font/css/materialdesignicons.css";

Vue.config.productionTip = false;

setTimeout(
  () =>
    new Vue({
      router,
      store,
      vuetify,
      render: h => h(App)
    }).$mount("#app"),
  7000
);