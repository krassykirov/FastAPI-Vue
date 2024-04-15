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
          <!-- prettier-ignore -->
          <div class="d-flex justify-center">
            <v-icon class="display-3">mdi-account-circle</v-icon>
          </div>
          <!-- <div class="text-subtitle-1 text-medium-emphasis" style="text-align: center; margin-bottom: 3%">Login</div> -->
          <div class="text-subtitle-1 text-medium-emphasis">Email</div>
          <v-form ref="formRef" @submit.prevent="submit">
            <v-text-field
              v-model="email.value.value"
              @input="clearErrorMessage"
              :error-messages="email.errorMessage.value || errorMessage"
              prepend-inner-icon="mdi-email-outline"
              color="green"
              placeholder="Email address"
              class="mb-2"
              variant="outlined"
              type="email"
            >
              <template v-slot:append-inner>
                <v-icon v-if="isEmailValid" color="green">mdi-check</v-icon>
              </template>
            </v-text-field>
            <div class="text-subtitle-1 text-medium-emphasis">Password</div>
            <!-- <a
              class="text-caption text-decoration-none text-blue"
              href="#"
              rel="noopener noreferrer"
              target="_blank"
            >
              Forgot login password?
            </a> -->
            <v-text-field
              v-model="password.value.value"
              @input="clearErrorMessage"
              :error-messages="password.errorMessage.value || errorMessage"
              prepend-inner-icon="mdi-lock-outline"
              :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible ? 'email' : 'password'"
              placeholder="Enter your password"
              class="mb-2"
              variant="outlined"
              @click:append-inner="visible = !visible"
            ></v-text-field>
            <v-checkbox
              style="margin: 0; padding: 0"
              v-model="checkbox.value.value"
              label="Keep me signed in"
              type="checkbox"
            ></v-checkbox>
            <v-btn color="primary" dark block type="submit">Login</v-btn>
            <v-card-text class="text-center mt-2">
              Don't have an account?
              <a
                class="text-blue text-decoration-none login-link"
                @click="redirectToSignup"
                rel="noopener noreferrer"
                target="_blank"
              >
                Sign up here <v-icon icon="mdi-login-variant"></v-icon>
              </a>
            </v-card-text>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, watch } from 'vue'
import store from '@/store/index.js'
import router from '@/router'
import { useField, useForm } from 'vee-validate'
import VueCookies from 'vue-cookies'
// import { jwtDecode } from 'jwt-decode'

export default {
  beforeMount() {
    if (this.$store.state.accessToken) {
      const accessToken = VueCookies.get('access_token')
      if (accessToken) {
        router.push({ name: 'NewHome' })
      }
    }
  },
  setup() {
    const { handleSubmit } = useForm({
      validationSchema: {
        email(value) {
          const pattern =
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Must be a valid e-mail'
        },
        password(value) {
          if (value?.length >= 1) return true
          return 'Password required'
        }
      }
    })

    const visible = ref(false)
    const formRef = ref(null)
    const email = useField('email')
    const password = useField('password')
    const checkbox = useField('checkbox')
    const errorMessage = ref('')
    watch(
      () => store.getters.errorMessage,
      newVal => {
        errorMessage.value = newVal
      }
    )
    const submit = handleSubmit(values => {
      if (formRef.value) {
        const isFormValid = formRef.value.validate()
        if (isFormValid.valid === false) {
          return
        }
      }
      try {
        store.dispatch('login', {
          username: values.email,
          password: values.password,
          rememberMe: values.checkbox
        })
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail === 'Username or password are incorrect!'
        ) {
          store.dispatch(
            'setErrorMessage',
            'The Username or Password is Incorrect. Try again.'
          )
        } else {
          // console.error('Login Error:', error)
        }
      }
    })
    const computedErrorMessage = computed(() => {
      return store.getters.errorMessage
    })
    const isEmailValid = computed(() => {
      return email.meta.valid
    })
    const redirectToSignup = () => {
      store.state.errorMessage = ''
      router.push('/signup')
    }
    const clearErrorMessage = () => {
      store.dispatch('setErrorMessage', '')
    }

    return {
      email,
      password,
      checkbox,
      errorMessage: computedErrorMessage,
      visible,
      submit,
      redirectToSignup,
      clearErrorMessage,
      isEmailValid
    }
  }
}
</script>
<style scoped>
::v-deep .v-label {
  margin: 0 !important;
}
.login-link:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
