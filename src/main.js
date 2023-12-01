import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import Vue from 'vue';

Vue.config.productionTip = false;

new Vue({
  router, // Inject the router into the Vue instance
  render: h => h(App),
}).$mount('#app');
// createApp(App).mount('#app');