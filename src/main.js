import Vue from 'vue'

import App from './App.vue'
import Router from './routes/routes.js'

Vue.config.productionTip = false

require('bootstrap')

new Vue({
  router: Router,
  render: h => h(App),
}).$mount('#app')
