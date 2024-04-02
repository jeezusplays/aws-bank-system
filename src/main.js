import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router/index";
import store from "./store/index";
import vuetify from "./plugins/vuetify";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "@mdi/font/css/materialdesignicons.css";
import '@aws-amplify/ui-components';
import {
  applyPolyfills,
  defineCustomElements
} from '@aws-amplify/ui-components/loader';


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

Vue.config.ignoredElements = [/amplify-\w*/];

applyPolyfills().then(() => {
  defineCustomElements(window);
});
