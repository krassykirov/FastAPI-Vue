import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from '@/store/index.js'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    props: () => ({ profile: store.state.profile })
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginVue.vue')
  },
  {
    path: '/cart',
    name: 'ItemsInCart',
    component: () => import('../views/CartVueNew.vue'),
    props: () => ({ cart: store.state.cart, profile: store.state.profile })
  },
  // {
  //   path: '/item/:itemId',
  //   name: 'item',
  //   component: () => import('../views/MyItemNew.vue'),
  //   props: route => ({ itemId: route.params.itemId, cart: store.state.cart })
  // },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/SignUp.vue')
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: () => import('../views/ProfileVue.vue'),
    props: () => ({ cart: store.state.cart })
  },
  {
    path: '/item/:itemId',
    name: 'Item',
    component: () => import('../views/MyItemLast.vue'),
    props: route => ({
      itemId: route.params.itemId,
      cart: store.state.cart,
      profile: store.state.profile
    })
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
