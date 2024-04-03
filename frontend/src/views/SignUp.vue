<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Sign Up</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn text @click="redirectToLogin">Login</v-btn>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="submitForm">
              <v-text-field
                v-model="email.value"
                label="E-mail"
                class="mb-4"
                type="email"
                :rules="emailRules"
              ></v-text-field>
              <v-text-field
                v-model="password.value"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :error-messages="errorMessage"
                :type="show1 ? 'text' : 'password'"
                class="mb-4"
                label="Password"
                :rules="passwordRules"
                @click:append="show1 = !show1"
              ></v-text-field>
              <v-text-field
                v-model="password2.value"
                :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                :error-messages="errorMessage"
                :type="show2 ? 'text' : 'password'"
                class="mb-4"
                label="Repeat Password"
                :rules="confirmPasswordRules"
                @click:append="show2 = !show2"
              ></v-text-field>
              <v-btn color="primary" dark type="submit">Sign Up</v-btn>
              <v-btn color="primary" @click="redirectToLogin">Login</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import store from '@/store/index.js'
import config from '@/config'

export default {
  data() {
    return {
      show1: false,
      show2: false,
      email: { value: '' },
      password: { value: '' },
      password2: { value: '' },
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  computed: {
    errorMessage() {
      return this.$store.state.errorMessage
    },
    emailRules() {
      return [
        v => !!v || 'Email is required',
        v =>
          /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
            v
          ) || 'Must be a valid e-mail.'
      ]
    },
    passwordRules() {
      return [
        v => v?.length >= 1 || 'Password must be at least 6 characters',
        v => !!v || 'Password is required'
      ]
    },
    confirmPasswordRules() {
      return [
        v => v === this.password.value || 'Passwords do not match',
        v => !!v || 'Confirm Password is required'
      ]
    }
  },
  methods: {
    async submitForm() {
      const formData = new URLSearchParams()
      formData.append('username', this.email.value)
      formData.append('password', this.password.value)
      formData.append('password2', this.password2.value)
      if (this.password.value !== this.password2.value) {
        store.dispatch('setErrorMessage', 'Passwords do not match')
        return
      }
      try {
        const response = await axios.post(
          `${config.backendEndpoint}/signup`,
          formData
        )
        if (response.status === 200) {
          router.push('/login')
        } else {
          throw new Error(response.data.detail || 'An error occurred.')
        }
      } catch (error) {
        this.errorMessage = error.message || 'An error occurred.'
      }
    },
    redirectToLogin() {
      router.push('/login')
    }
  },
  watch: {
    'store.getters.errorMessage'(newVal) {
      this.errorMessage = newVal
    }
  }
}
</script>
