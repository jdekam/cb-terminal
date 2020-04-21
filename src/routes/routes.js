import Vue from 'vue'
import VueRouter from 'vue-router'

// component imports
import Login from '../components/Login'
import Terminal from '../components/Terminal'

// register VueRouter
Vue.use(VueRouter)

// register new routes here
const router = new VueRouter({
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/terminal',
      name: 'terminal',
      component: Terminal,
    },
  ],
})

export default router
