<template>
  <div
    class="container-fluid"
    style="
      width: 100vw;
      position: sticky;
      margin: 0;
      padding: 0;
      align-items: center;
      text-align: center;
    "
  >
    <NavBar
      :cart="cart"
      :total="total"
      :user="user"
      :profile="profile"
      :favorites="favorites"
    />
    <div class="container" style="margin-top: 2%">
      <h5 v-if="!profile" style="text-align: center">
        No Profile yet, create one?
      </h5>
      <v-card class="mx-auto" max-width="500" v-if="profile">
        <v-card-item class="bg-cyan-darken-1">
          <v-card-title>
            <span class="text-h5">{{ user }}</span>
            <v-icon @click="editingProfile = !editingProfile"
              >mdi-pencil</v-icon
            >
          </v-card-title>
          <template v-slot:append>
            <v-defaults-provider
              :defaults="{
                VBtn: {
                  variant: 'text',
                  density: 'comfortable'
                }
              }"
            >
            </v-defaults-provider>
          </template>
          <!-- Update Profile -->
        </v-card-item>
        <v-sheet class="mx-auto" width="480px">
          <v-form ref="form" v-if="editingProfile">
            <v-text-field
              v-model="editedProfile.number"
              label="Telephone number"
              :rules="phoneRules"
              type="tel"
              prepend-inner-icon="mdi-phone"
              :placeholder="profile.number"
            ></v-text-field>
            <v-text-field
              v-model="editedProfile.email"
              :rules="emailRules"
              label="Secondary Email"
              type="email"
              prepend-inner-icon="mdi-email"
              :placeholder="profile.email"
            ></v-text-field>
            <v-text-field
              v-model="editedProfile.address"
              label="Address"
              type="address"
              prepend-inner-icon="mdi-map-marker"
              :placeholder="profile.address"
            ></v-text-field>
            <v-file-input
              accept="image/*"
              label="Avatar Photo"
              prepend-icon="mdi-folder-open"
              type="file"
              @change="handleFileChange"
            ></v-file-input>
            <v-img
              :src="`${backendEndpoint}/static/img/${profile.primary_email}/profile/${profile.avatar}`"
              class="imng-fluid"
              style="width: 90%; max-height: 200px"
            ></v-img>
            <v-row justify="center" align="center" style="margin-top: 5px">
              <v-col cols="6">
                <v-btn width="100%" @click="updateProfile">Save</v-btn>
              </v-col>
              <v-col cols="6">
                <v-btn width="100%" @click="cancelProfile">Cancel</v-btn>
              </v-col>
            </v-row>
          </v-form>
          <v-list v-else style="width: 450px">
            <v-list-item prepend-icon="mdi-phone" style="text-align: center">
              {{ profile.number }}
            </v-list-item>
            <v-divider inset></v-divider>
            <v-list-item prepend-icon="mdi-email" style="text-align: center">
              {{ profile.email }}
            </v-list-item>
            <v-divider inset></v-divider>
            <v-list-item
              prepend-icon="mdi-map-marker"
              style="text-align: center"
            >
              {{ profile.address }}
            </v-list-item>
            <v-list-item
              prepend-icon="mdi-account-circle"
              style="text-align: center"
            >
              <v-img
                :src="`${backendEndpoint}/static/img/${profile.primary_email}/profile/${profile.avatar}`"
                class="imng-fluid"
                style="width: 90%; max-height: 200px"
              ></v-img>
            </v-list-item>
          </v-list>
        </v-sheet>
      </v-card>
      <!-- Create Profile -->
      <div class="container" style="margin-top: 2%; width: 480px">
        <v-card v-if="!profile">
          <v-card-title class="bg-cyan-darken-1">
            <span class="text-h5">{{ user }}</span>
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="newProfile.email"
              prepend-inner-icon="mdi-email"
              :rules="emailRules"
              label="Secondary Email"
              type="email"
              required
            ></v-text-field>
            <v-text-field
              v-model="newProfile.number"
              :rules="phoneRules"
              label="Number"
              type="number"
              prepend-inner-icon="mdi-phone"
              required
            ></v-text-field>
            <v-text-field
              v-model="newProfile.address"
              label="Address"
              type="address"
              prepend-inner-icon="mdi-map-marker"
            ></v-text-field>
            <v-file-input
              @change="handleFileCreateProfile"
              accept="image/*"
              label="Avatar Photo"
              type="file"
              required
            ></v-file-input>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="createProfile" color="primary">Save</v-btn>
            <v-btn @click="cancelCreateProfile" color="secondary">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import NavBar from '@/components/MyNavbar.vue'
import config from '@/config'
import VueCookies from 'vue-cookies'
import { jwtDecode } from 'jwt-decode'
import router from '@/router'
import axios from 'axios'

export default {
  components: {
    NavBar
  },
  props: ['cart', 'total', 'avatar', 'favorites', 'profile'],
  emits: ['addToCart'],
  data() {
    return {
      editingProfile: false,
      editedProfile: {
        email: '',
        number: '',
        address: ''
      },
      newProfile: {
        email: '',
        number: '',
        address: '',
        avatar: null
      },
      file: null,
      profileImageUrl: '',
      item: this.item,
      itemId: this.itemId,
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  computed: {
    // isEmailValid() {
    //   return this.emailRules.every(rule => rule(this.email.value) === true)
    // },
    // isPhoneValid() {
    //   return this.phoneRules.every(rule => rule(this.number.value) === true)
    // },
    emailRules() {
      return [
        v => {
          if (!v) return true
          return (
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
              v
            ) || 'Must be a valid e-mail.'
          )
        }
      ]
    },
    phoneRules() {
      return [
        v => {
          if (!v) return true
          return (
            /^[\d-]{1,15}$/.test(v) ||
            'Must be a valid phone number (up to 15 digits, e.g 123-456-789, 12345678).'
          )
        }
      ]
    },
    user() {
      return this.$store.state.user
    },
    user_id() {
      return this.$store.state.user_id
    },
    accessToken() {
      return this.$store.state.accessToken
    }
  },
  created() {
    const accessToken = VueCookies.get('access_token')
    if (accessToken) {
      const user = jwtDecode(accessToken).sub
      const user_id = jwtDecode(accessToken).user_id
      this.$store.commit('UPDATE_USER', user)
      this.$store.commit('UPDATE_USER_ID', user_id)
    } else {
      router.push('/login')
    }
    this.$store.dispatch('getProfile')
  },
  methods: {
    clearErrorMessage() {
      this.$store.dispatch('setErrorMessage', '')
    },
    cancelProfile() {
      this.editingProfile = false
    },
    handleFileChange(event) {
      this.editedProfile.file = event.target.files[0]
      const file = event.target.files[0]
      this.profileImageUrl = URL.createObjectURL(file)
    },
    handleFileCreateProfile(event) {
      const file = event.target.files[0]
      this.newProfile.avatar = file
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    itemAlreadyInCart(product) {
      return this.cart.some(item => item.id === product.id)
    },
    showModal() {
      $(document).ready(function () {
        $('#global-modal').modal('show')
      })
    },
    async updateProfile() {
      if (
        !this.editedProfile.email &&
        !this.editedProfile.number &&
        !this.editedProfile.address &&
        !this.editedProfile.file
      ) {
        console.log('this.file', this.file)
        return
      }
      const formData = new FormData()
      formData.append('email', this.editedProfile.email)
      formData.append('number', this.editedProfile.number)
      formData.append('address', this.editedProfile.address)
      formData.append('file', this.editedProfile.file)
      try {
        const response = await axios.post(
          `${config.backendEndpoint}/api/profile/update_profile`,
          formData
        )
        const data = response.data
        const user = this.$store.getters.user
        const img_path = `${config.backendEndpoint}/static/img/${user}/profile/${data.avatar}`
        $('#card-email').text(`Email: ${data.email}`)
        $('#card-address').text(`Address: ${data.address}`)
        $('#card-phone').text(`Address: ${data.number}`)
        $('#avatar-image').attr('src', img_path)
        this.$store.dispatch('getProfile')
        this.editingProfile = false
      } catch (error) {
        if (error.response && error.response.status === 404) {
          $('#UpdateProfileLabel').text(
            'Unable to process Profile update, please try again later!'
          )
        }
      }
    },
    createProfile() {
      if (
        !this.newProfile.email ||
        !this.newProfile.number ||
        !this.newProfile.address ||
        !this.newProfile.avatar
      ) {
        return
      }
      const formData = new FormData()
      formData.append('email', this.newProfile.email)
      formData.append('number', this.newProfile.number)
      formData.append('address', this.newProfile.address)
      formData.append('file', this.newProfile.avatar)
      axios
        .post(`${config.backendEndpoint}/api/profile/create_profile`, formData)
        .then(() => {
          this.newProfile = {
            email: '',
            number: '',
            address: '',
            avatar: null
          }
          this.$store.dispatch('getProfile')
        })
        .catch(error => {
          if (error.response && error.response.status === 403) {
            // Handle specific error status
          } else {
            // Handle other types of errors
          }
        })
    }
  }
}
</script>

<style scoped>
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2) !important;
  margin-bottom: 10%;
  margin-top: 5% !important;
  margin: auto !important;
  text-align: center !important;
  font-family: arial !important;
  width: 20rem !important;
  height: auto !important;
}

button {
  border: none !important;
  outline: 0 !important;
  display: inline-block !important;
  padding: 8px !important;
  color: white !important;
  background-color: #0093c4 !important;
  text-align: center !important;
  cursor: pointer !important;
  width: 100% !important;
  font-size: 18px !important;
  margin-bottom: 2%;
}

.navbar {
  padding-left: 0 !important;
}
</style>
