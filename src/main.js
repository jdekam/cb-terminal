import Vue from 'vue'

// import base layout and router
import App from './App.vue'
import Router from './routes/routes.js'

// get rid of annoying console statement
Vue.config.productionTip = false

// registering dependencies so we don't need to import libraries in each component
import axios from 'axios'
Object.defineProperty(Vue.prototype, '$axios', { value: axios })

// create Vue object
new Vue({
  router: Router,
  render: h => h(App),
}).$mount('#app')
