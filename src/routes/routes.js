import Vue from 'vue'
import VueRouter from 'vue-router'

// component imports
import Login from '../components/Login'
import Logout from '../components/Logout'
import Terminal from '../components/Terminal'

// register VueRouter
Vue.use(VueRouter)

// register new routes here
const router = new VueRouter ({
  routes: [
    {
      path: '/',
      redirect: '/terminal', // NOTE SHOULD REDIRECT TO LOGIN (WAS CHANGED TO DEBUG TERMINAL)
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/logout',
      name: 'logout',
      component: Logout,
    },
    {
      path: '/terminal',
      name: 'terminal',
      component: Terminal,
    },
  ],
})

export default router
