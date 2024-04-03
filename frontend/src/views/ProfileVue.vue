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
    <nav
      class="navbar navbar-expand-lg bg-white sticky-top navbar-light shadow-lg"
      style="
        height: 4em;
        margin-left: 0;
        margin-right: 0;
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
    </nav>
    <div class="container" style="margin-top: 2%">
      <h5 v-if="!profile" style="text-align: center">
        No Profile yet, create one?
      </h5>
      <v-btn
        v-if="!profile"
        class="dropbtn"
        data-toggle="modal"
        data-target="#addProfile"
        style="float: left"
      >
        Create Profile
      </v-btn>
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
        </v-card-item>
        <v-sheet class="mx-auto" width="480px">
          <v-form ref="form" v-if="editingProfile">
            <v-text-field
              v-model="editedProfile.number"
              label="Number"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedProfile.email"
              label="Secondary Email"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedProfile.address"
              label="Address"
              required
            ></v-text-field>
            <v-file-input
              accept="image/*"
              label="Avatar Photo"
              @change="handleFileChange"
              required
            ></v-file-input>
            <v-row justify="center" align="center">
              <v-col cols="5">
                <v-btn width="100%" @click="saveProfile">Save</v-btn>
              </v-col>
              <v-col cols="5">
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
              ></v-img>
            </v-list-item>
          </v-list>
        </v-sheet>
      </v-card>
      <div
        class="modal fade"
        id="addProfile"
        tabindex="-1"
        role="dialog"
        aria-labelledby="addProfileLabel"
        aria-hidden="true"
        data-backdrop="false"
      >
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="addProfileLabel">Create Profile</h5>
            </div>
            <div class="modal-body">
              <form
                id="create-profile"
                enctype="multipart/form-data"
                data-toggle="validator"
              >
                <div class="form-group">
                  <label for="email" class="col-form-label"
                    >Secondary Email:</label
                  >
                  <input
                    type="email"
                    name="email"
                    id="email"
                    placeholder="Email"
                    required
                  />
                  <!-- <input type="text" name="name" id="item-name" pattern="^[a-zA-Z]*" oninvalid="setCustomValidity('Please use only letters')" placeholder="Item Name"  required> -->
                </div>
                <div class="form-group">
                  <label for="number" class="col-form-label">Number:</label>
                  <input
                    type="tel"
                    name="number"
                    id="tel-number"
                    placeholder="Telephone number"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="address" class="col-form-label">Number:</label>
                  <input
                    type="text"
                    name="address"
                    id="address"
                    placeholder="Address"
                  />
                </div>
                <div class="form-group" form-group-file>
                  <label for="file" class="col-form-label"
                    >Upload Avatar Photo:</label
                  >
                  <input
                    type="file"
                    id="file"
                    name="file"
                    class="form-control"
                    data-filesize="1000000"
                    data-filesize-error="File must be smaller then 1MB"
                    accept="image/*"
                    required
                  />
                </div>
                <button
                  id="submit-button"
                  @click="createProfile"
                  class="dropbtn"
                >
                  Submit
                </button>
                <button
                  id="Close-Profile"
                  type="button"
                  class="dropbtn"
                  data-dismiss="modal"
                  style="margin-bottom: 5px; margin-top: 5px"
                >
                  Close
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div
        class="toast"
        id="cartToast"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        data-bs-autohide="false"
        style="
          position: fixed;
          top: 10%;
          right: 5%;
          transform: translate(0, -50%);
          width: 250px;
          z-index: 1000;
        "
      >
        <div
          class="toast-body"
          id="cartToastBody"
          style="font-weight: 900; font: 1.1em"
        ></div>
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
      file: null,
      profileImageUrl: '',
      item: this.item,
      itemId: this.itemId,
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  computed: {
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
    cancelProfile() {
      this.editingProfile = false
    },
    handleFileChange(event) {
      this.editedProfile.file = event.target.files[0]
      const file = event.target.files[0]
      this.profileImageUrl = URL.createObjectURL(file)
    },
    saveProfile() {
      const formData = new FormData()
      formData.append('email', this.editedProfile.email)
      formData.append('number', this.editedProfile.number)
      formData.append('address', this.editedProfile.address)
      formData.append('file', this.editedProfile.file)
      $.ajax({
        url: `${config.backendEndpoint}/api/profile/update_profile`,
        type: 'POST',
        processData: false,
        contentType: false,
        headers: {
          Authorization: `Bearer ${this.$store.state.accessToken}`
        },
        data: formData,
        success: data => {
          var user = this.$store.getters.user
          var img_path = `${config.backendEndpoint}/static/img/${user}/profile/${data.avatar}`
          $('#card-email').text(`Email: ${data.email}`)
          $('#card-address').text(`Address: ${data.address}`)
          $('#card-phone').text(`Address: ${data.number}`)
          $('#avatar-image').attr('src', img_path)
          this.editingProfile = false
        },
        error: function (xhr) {
          if (xhr.status === 404) {
            $('#UpdateProfileLabel').text(
              'Unable to process Profile update, please try again later!'
            )
          }
        }
      })
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
    updateProfile() {
      $('#update-profile').submit(e => {
        e.preventDefault()
        const formData = new FormData(e.target)
        $.ajax({
          url: `${config.backendEndpoint}/api/profile/update_profile`,
          type: 'POST',
          processData: false,
          contentType: false,
          headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`
          },
          data: formData,
          success: data => {
            // Use an arrow function here
            $('#UpdateProfile').modal('hide')
            $('#close-button').click()
            var user = this.$store.getters.user
            var img_path = `${config.backendEndpoint}/static/img/${user}/profile/${data.avatar}`
            $('#card-email').text(`Email: ${data.email}`)
            $('#card-address').text(`Address: ${data.address}`)
            $('#card-phone').text(`Address: ${data.number}`)
            $('#avatar-image').attr('src', img_path)
          },
          error: function (xhr) {
            if (xhr.status === 404) {
              $('#UpdateProfileLabel').text(
                'Unable to process Profile update, please try again later!'
              )
            }
          }
        })
      })
    },
    createProfile() {
      $('#create-profile').submit(e => {
        e.preventDefault()
        const formData = new FormData(e.target)
        $.ajax({
          url: `${config.backendEndpoint}/api/profile/create_profile`,
          type: 'POST',
          processData: false,
          contentType: false,
          headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`
          },
          data: formData,
          success: () => {
            $('#create-profile').modal('hide')
            $('#Close-Profile').click()
            this.$store.dispatch('getProfile')
          },
          error: function (xhr) {
            if (xhr.status === 403) {
              $('#error').text('Item with that name already exists!')
            }
          }
        })
      })
    }
  }
}
</script>
<style scoped>
.body {
  overflow-x: visible !important;
}
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
.title {
  color: grey !important;
  font-size: 18px !important;
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

.user-row {
  margin-bottom: 14px;
}

.table-user-information > tbody > tr {
  border-top: 1px solid #ccc;
}

.table-user-information > tbody > tr:first-child {
  border-top: 0;
}

.table-user-information > tbody > tr > td {
  border-top: 0;
}

.panel {
  margin-top: 20px;
}
</style>
