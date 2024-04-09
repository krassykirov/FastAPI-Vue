import { createApp } from 'vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import VueLazyload from 'vue-lazyload'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'
import axios from 'axios'
import store from '@/store/index.js'
import App from './App.vue'
import VueCookies from 'vue-cookies'
import $ from 'jquery'
window.$ = window.jQuery = $
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'

axios.defaults.baseURL = process.env.BASE_URL || 'localhost:8081'
import router from './router'

let isRefreshing = false

axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response && error.response.status === 401) {
      if (
        error.response.data.detail === 'Username or password are incorrect!'
      ) {
        store.dispatch(
          'setErrorMessage',
          'The Username or Password is Incorrect. Try again.'
        )
        return
      }
      const hasRefreshToken = store.state.refreshToken !== null
      if (hasRefreshToken) {
        if (!isRefreshing) {
          isRefreshing = true
          try {
            const newAccessToken = await store.dispatch('refreshAccessToken')
            error.config.headers.Authorization = `Bearer ${newAccessToken}`
            return axios.request(error.config)
          } catch (refreshError) {
            if (refreshError.response.data.detail === 'Token has expired') {
              store.dispatch(
                'setErrorMessage',
                'Session has expired. Please log in.'
              )
              store.dispatch('logout')
              router.push({ name: 'login' })
            } else {
              throw refreshError
            }
          } finally {
            isRefreshing = false
          }
        }
      }
    }
    // Pass other errors through without handling
    return Promise.reject(error)
  }
)
axios.interceptors.request.use(
  config => {
    if (store.state.accessToken !== null) {
      config.headers.Authorization = `Bearer ${store.state.accessToken}`
      config.headers.Accept = 'application/json'
      return config
    } else {
      router.push('/login')
      return config
    }
  },
  error => {
    return Promise.reject(error)
  }
)
const vuetify = createVuetify({
  components,
  directives
})
const app = createApp(App)
app
  .use(router)
  .use(store)
  .use(vuetify)
  .use(VueCookies)
  .use(VueLazyload, {
    preLoad: 1.3,
    attempt: 1
  })
  .mount('#app')
