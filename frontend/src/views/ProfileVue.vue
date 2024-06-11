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
    <!-- prettier-ignore -->
    <div class="container" style="margin-top: 2%">
      <h5 v-if="!profile" style="text-align: center">
        No Profile yet, create one?
      </h5>
      <v-card class="mx-auto" width="480" color="grey-lighten-4" max-width="500" v-if="profile">
        <v-toolbar flat color="grey-lighten-3">
          <v-btn icon="mdi-account"></v-btn>
          <v-toolbar-title class="font-weight-light">
            User Profile
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="isEditing = !isEditing">
            <v-fade-transition leave-absolute>
              <v-icon v-if="isEditing">mdi-close</v-icon>
              <v-icon v-else>mdi-pencil</v-icon>
            </v-fade-transition>
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <v-form enctype="multipart/form-data" v-if="isEditing" @submit.prevent="updateProfile">
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
            <!-- <v-img
              :src="`${backendEndpoint}/static/img/${profile.primary_email}/profile/${profile.avatar}`"
              class="imng-fluid"
              style="width: 90%; max-height: 200px"
            ></v-img> -->
            <v-card-actions style="margin-top: 15px">
              <v-spacer></v-spacer>
              <v-btn type="submit" width="200px" elevation="5">Save</v-btn>
            </v-card-actions>
          </v-form>
          <v-form v-else>
            <v-text-field
              :model-value="profile.number"
              label="Telephone number"
              type="tel"
              prepend-inner-icon="mdi-phone"
              readonly
            ></v-text-field>
            <v-text-field
              :model-value="profile.email"
              label="Secondary Email"
              type="email"
              prepend-inner-icon="mdi-email"
              readonly
            ></v-text-field>
            <v-text-field
              :model-value="profile.address"
              label="Address"
              type="address"
              prepend-inner-icon="mdi-map-marker"
              readonly
            ></v-text-field>
            <v-img
              :src="`${backendEndpoint}/static/img/${profile.primary_email}/profile/${profile.avatar}`"
              class="img-fluid"
              style="width: 90%; max-height: 200px"
            ></v-img>
          </v-form>
          <v-snackbar
          v-model="hasSaved"
          :timeout="2000"
          location="bottom left"
          position="absolute"
          attach
        >
          Your profile has been updated
        </v-snackbar>
        </v-card-text>
        <v-divider></v-divider>
      </v-card>
      <!-- Create Profile -->
      <div class="container" style="margin-top: 2%; width: 480px">
        <v-card v-if="!profile">
          <v-card-title class="blue-darken-1" style="text-align: center">
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
import axios from 'axios'

export default {
  components: {
    NavBar
  },
  props: ['cart', 'total', 'avatar', 'favorites', 'profile'],
  emits: ['addToCart'],
  data() {
    return {
      hasSaved: false,
      isEditing: false,
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
  methods: {
    clearErrorMessage() {
      this.$store.dispatch('setErrorMessage', '')
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
        return
      }
      const formData = new FormData()
      formData.append('email', this.editedProfile.email)
      formData.append('number', this.editedProfile.number)
      formData.append('address', this.editedProfile.address)
      if (
        this.editedProfile.file !== 'undefined' &&
        this.editedProfile.file !== 'null'
      ) {
        formData.append('file', this.editedProfile.file)
      }
      try {
        const response = await axios.post(
          `${config.backendEndpoint}/api/profile/update_profile`,
          formData
        )
        this.$store.commit('UPDATE_PROFILE', response.data)
        this.editedProfile = {
          email: '',
          number: '',
          address: '',
          file: null
        }
        this.isEditing = false
        this.hasSaved = true
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
          this.$store.commit('UPDATE_HAS_PROFILE', true)
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
