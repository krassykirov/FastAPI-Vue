<template>
  <v-container fluid style="margin-top: 5%">
    <v-row justify="center">
      <v-col cols="10" md="6" lg="4">
        <v-card
          class="mx-auto pa-6 pb-8"
          elevation="8"
          rounded="lg"
          max-width="448"
        >
          <div class="d-flex justify-center">
            <v-icon class="display-3">mdi-account-circle</v-icon>
          </div>
          <div
            class="text-subtitle-1 text-medium-emphasis"
            style="text-align: center; margin-bottom: 3%"
          >
            Create your Account
          </div>
          <v-form ref="formSignup" @submit.prevent="submitForm">
            <v-text-field
              v-model="email.value"
              @input="clearErrorMessage"
              :error-messages="errorMessage"
              prepend-inner-icon="mdi-email-outline"
              placeholder="Email address"
              class="mb-2"
              variant="outlined"
              type="email"
              :rules="emailRules"
              color="green"
            >
              <template v-slot:append-inner>
                <v-icon v-if="isEmailValid" color="green">mdi-check</v-icon>
              </template>
            </v-text-field>
            <v-text-field
              v-model="password.value"
              @input="clearErrorMessage"
              prepend-inner-icon="mdi-lock-outline"
              :append-inner-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
              variant="outlined"
              :type="show1 ? 'email' : 'password'"
              class="mb-2"
              label="Password"
              :rules="passwordRules"
              @click:append-inner="show1 = !show1"
            >
            </v-text-field>
            <v-text-field
              v-model="password2.value"
              @input="clearErrorMessage"
              prepend-inner-icon="mdi-lock-outline"
              :append-inner-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
              variant="outlined"
              :type="show2 ? 'email' : 'password'"
              class="mb-2"
              label="Repeat Password"
              :rules="confirmPasswordRules"
              @click:append-inner="show2 = !show2"
            ></v-text-field>
            <!-- prettier-ignore -->
            <v-btn color="primary" dark block type="submit">Create Account</v-btn>
            <!-- prettier-ignore -->
            <v-card-text v-if="successMessage" color="green" class="text-center mt-2 success-text" style="font-size:14px">
              {{ successMessage }}
            </v-card-text>
            <!-- prettier-ignore -->
            <v-card-text class="text-center mt-2">
              Already have an account?
              <a
                class="text-blue text-decoration-none login-link"
                @click="redirectToLogin"
                rel="noopener noreferrer"
                target="_blank"
              >
                Login here <v-icon icon="mdi-login-variant"></v-icon>
              </a>
            </v-card-text>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import router from '@/router'
import store from '@/store/index.js'
import config from '@/config'

export default {
  data() {
    return {
      show1: false,
      show2: false,
      successMessage: '',
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
    isEmailValid() {
      return this.emailRules.every(rule => rule(this.email.value) === true)
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
        v => v?.length >= 1 || 'Password is required',
        v => !!v || 'Password is required',
        v => {
          if (this.password2.value) {
            return v === this.password2.value || 'Passwords do not match'
          }
          return true
        }
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
      const isFormValid = await this.$refs.formSignup.validate()
      if (isFormValid.valid === false) {
        return
      }
      const formData = new URLSearchParams()
      formData.append('username', this.email.value)
      formData.append('password', this.password.value)
      formData.append('password2', this.password2.value)
      if (this.password.value !== this.password2.value) {
        store.dispatch('setErrorMessage', 'Passwords do not match')
        return
      }
      fetch(`${config.backendEndpoint}/signup`, {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (response.ok) {
            this.successMessage = 'Sign-up successful! You can now login'
          } else if (response.status === 403) {
            store.dispatch(
              'setErrorMessage',
              'This Email is taken. Try another.'
            )
            this.email.value = ''
            this.password.value = ''
            this.password2.value = ''
            return
          } else {
            throw new Error(`HTTP error! Status: ${response.status}`)
          }
        })
        .catch(error => {
          throw error
        })
    },
    redirectToLogin() {
      router.push('/login')
    },
    clearErrorMessage() {
      store.dispatch('setErrorMessage', '')
    }
  },
  watch: {
    'store.getters.errorMessage'(newVal) {
      this.errorMessage = newVal
    }
  }
}
</script>
<style scoped>
.success-text {
  color: green;
  font-size: 20px;
}
.login-link:hover {
  cursor: pointer;
}
</style>
