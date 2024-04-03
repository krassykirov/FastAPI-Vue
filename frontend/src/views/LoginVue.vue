<template>
  <v-sheet class="bg-deep-purple pa-12" rounded>
    <v-card class="mx-auto px-6 py-8" max-width="344">
      <form @submit.prevent="submit">
        <v-text-field
          v-model="email.value.value"
          :error-messages="email.errorMessage.value || errorMessage"
          label="E-mail"
          class="mb-4"
          type="email"
        ></v-text-field>
        <v-text-field
          v-model="password.value.value"
          type="password"
          class="mb-4"
          label="Password"
          :error-messages="password.errorMessage.value || errorMessage"
        ></v-text-field>
        <v-checkbox
          v-model="checkbox.value.value"
          label="RememberMe"
        ></v-checkbox>

        <v-btn class="me-4" type="submit"> Login </v-btn>

        <v-btn @click="redirectToSignup"> SignUp </v-btn>
      </form>
    </v-card>
  </v-sheet>
</template>

<script>
import { ref, computed, watch } from 'vue'
import store from '@/store/index.js'
import router from '@/router'
import { useField, useForm } from 'vee-validate'

export default {
  setup() {
    const { handleSubmit } = useForm({
      validationSchema: {
        email(value) {
          const pattern =
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Must be a valid e-mail.'
        },
        password(value) {
          if (value?.length >= 1) return true
          return 'Password length needs to be at least 6.'
        }
      }
    })

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
            'Username or password are incorrect!'
          )
        } else {
          // console.error('Login Error:', error)
        }
      }
    })

    // Define computed errorMessage
    const computedErrorMessage = computed(() => {
      return errorMessage.value
    })
    const redirectToSignup = () => {
      router.push('/signup')
    }

    return {
      email,
      password,
      checkbox,
      errorMessage: computedErrorMessage,
      submit,
      redirectToSignup
    }
  }
}
</script>
<style scoped>
::v-deep .v-label {
  margin: 0 !important;
}
</style>
