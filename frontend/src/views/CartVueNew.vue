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
    <v-container fluid>
      <v-row justify="center" style="margin-top: 1%">
        <v-col cols="12" md="6">
          <v-card class="px-6 py-8" elevation="2" outlined>
            <h3 class="text-center mb-4">
              <v-icon size="24" class="mr-2">mdi-cart-outline</v-icon>
              Shopping Cart
            </h3>
            <v-row v-for="product in cart" :key="product.id" align="center">
              <v-divider class="my-4" color="blue-darken-4" thickness="3"></v-divider>
              <v-col cols="2">
                <v-img
                  :src="`${backendEndpoint}/static/img/${product.id}/${product.image}`"
                  max-width="128"
                  max-height="128"
                  contain
                ></v-img>
              </v-col>
              <v-col cols="8">
                <div
                  class="text-overline"
                  @click="redirectToItemFromCart(product.id)"
                  style="cursor: pointer; font-size: 14px; font-weight: 800"
                >
                  {{ product.name }}
                </div>
                  <!-- prettier-ignore -->
                <div style="color: #dc3545; font-weight: 800">
                  <span style="font-size: 0.9rem">$</span>
                  <span v-if="product.discount_price" style="font-size: 0.9rem;">{{ formattedPrice(product.discount_price).integerPart }}</span>
                  <span v-if="product.discount_price" style="font-size: 0.6rem; position: relative; top: -0.4em;">{{ formattedPrice(product.discount_price).decimalPart }}</span>
                </div>
                <v-col cols="14">
                  <div style="font-size: 14px">
                   {{ product.description }}
                 </div>
                </v-col>
                <v-rating
                  :model-value="product.rating_float"
                  color="orange-darken-2"
                  density="compact"
                  size="small"
                  readonly
                ></v-rating>
              </v-col>
              <v-col cols="1">
                <v-row justify="center" align="center">
                  <v-btn
                    style="width: 25px; height: 25px; margin-right: 7px"
                    @click="updateQuantity(product.id, product.quantity - 1)"
                    icon
                    ><v-icon style="font-size: 0.8rem">mdi-minus</v-icon></v-btn
                  >
                  <div>{{ product.quantity }}</div>
                  <v-btn
                    style="width: 25px; height: 25px; margin-left: 7px"
                    @click="updateQuantity(product.id, product.quantity + 1)"
                    icon
                    ><v-icon style="font-size: 0.8rem">mdi-plus</v-icon></v-btn
                  >
                </v-row>
              </v-col>
              <v-col cols="1">
                <!-- prettier-ignore -->
                <v-btn @click="removeFromCart(product.id)" size="x-small" icon="mdi-trash-can-outline"></v-btn>
              </v-col>
            </v-row>
            <v-divider class="my-4"></v-divider>
            <v-row align="center">
              <v-col cols="6">
                <!-- prettier-ignore -->
                <div class="text-h6">
                  Total:
                  <span style="font-size: 1.3rem;">$</span>
                  <span style="font-size: 1.3rem;">{{ formatTotal(total).integerPart }}</span>
                  <span style="font-size: 0.8rem; position: relative; top: -0.6em;">.{{ formatTotal(total).decimalPart }}</span>
                </div>
              </v-col>
              <v-col cols="6">
                <!-- prettier-ignore -->
                <v-btn @click="showModal" color="primary" dark
                  type="button"
                  class="btn btn-primary"
                  data-toggle="modal"
                  data-target="#exampleModal"
                  >Proceed to Payment</v-btn
                >
              </v-col>
            </v-row>
            <div class="delivery my-4">
              <p class="font-weight-bold">
                <v-icon size="18" class="mr-1">mdi-truck-delivery</v-icon>
                Delivery done in 3 days from date of purchase
              </p>
              <p class="text-caption">
                Order now to get this product delivered
              </p>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <!-- prettier-ignore -->
    <v-dialog v-model="dialog" max-width="800px" style="font-size: 12px">
      <v-card color="grey-lighten-4" style="font-size: 12px">
        <v-card-title>
          <span class="headline">Payment Details</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="hideModal" size="x-small">
            <v-icon size="x-small">mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" id="paymentForm" @submit.prevent="paymentCheckout" v-model="valid">
            <v-container>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th></th>
                      <th style="padding-left: 150px">Name</th>
                      <th style="padding-left: 30px">Quantity</th>
                      <th style="padding-left: 15px">Price</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in cart" :key="product.id">
                      <td>
                        <img
                          :src="`${backendEndpoint}/static/img/${product.id}/${product.image}`"
                          class="img"
                          alt="Product Image"
                          style="
                            max-width: 50px;
                            max-height: 35px;
                            margin: 5px;
                          "
                        />
                      </td>
                      <td>{{ product.name }}</td>
                      <td class="align-left text-left">
                        <div
                          class="input-group"
                          style="
                            max-width: 120px;
                            max-height: 40px;
                          "
                        >
                          <v-btn
                            class="btn btn-outline-secondary"
                            type="button"
                            size="x-small"
                            @click="
                              updateQuantity(product.id, product.quantity - 1)
                            "
                          >
                            -
                          </v-btn>
                          <input
                            type="number"
                            class="form-control text-center"
                            min="1"
                            max="3"
                            style="height: 22px"
                            :value="product.quantity"
                            disabled
                          />
                          <v-btn
                            class="btn btn-outline-secondary"
                            type="button"
                            size="x-small"
                            @click="
                              updateQuantity(product.id, product.quantity + 1)
                            "
                          >
                            +
                          </v-btn>
                        </div>
                      </td>
                      <td style="padding-left: 10px; padding-bottom: 15px">${{ product.price }}</td>
                      <td style="padding-left: 10px; padding-bottom: 15px">
                        <v-btn @click="removeFromCart(product.id)" size="x-small" icon="mdi-trash-can-outline"></v-btn>
                      </td>
                    </tr>
                    <div class="text-end mt-4">
                      <h4
                        style="
                          width: 120px;
                          margin-left: 90%;
                        "
                      > <!-- prettier-ignore -->
                        <span style="font-size: 1rem;">Total: $</span>
                        <span style="font-size: 1rem;">{{ formatTotal(total).integerPart }}</span>
                        <span style="font-size: 0.6rem; position: relative; top: -0.4em;">{{ formatTotal(total).decimalPart }}</span>
                      </h4>
                    </div>
                  </tbody>
                </template>
              </v-simple-table>
              <h6>Shipping Address</h6>
              <v-text-field v-model="formData.firstname" label="Full Name" required prepend-icon="mdi-account" type="address"></v-text-field>
              <v-text-field v-model="formData.email" label="Email" required prepend-icon="mdi-email" type="email"></v-text-field>
              <v-text-field v-model="formData.address" label="Address" required prepend-icon="mdi-home" type="address"></v-text-field>
              <v-text-field v-model="formData.city" label="City" required prepend-icon="mdi-city" type="address"></v-text-field>
              <v-row>
                <v-col cols="6">
                  <v-text-field v-model="formData.tel" label="Telephone" required pattern="[0-9]{10,}" prepend-icon="mdi-phone" type="tel"></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field v-model="formData.zip" label="Zip" pattern="[0-9]" prepend-icon="mdi-map-marker" type="tel"></v-text-field>
                </v-col>
              </v-row>
              <h6>Payment</h6>
              <v-text-field v-model="formData.cardname" label="Name on Card" prepend-icon="mdi-credit-card" type="address"></v-text-field>
              <v-text-field v-model="formData.cardnumber" label="Credit Card Number" prepend-icon="mdi-credit-card-outline" type="tel"></v-text-field>
              <v-row>
                <v-col cols="6">
                  <v-text-field v-model="formData.expmonth" label="Exp Month" prepend-icon="mdi-calendar" type="tel"></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field v-model="formData.expyear" label="Exp Year" prepend-icon="mdi-calendar" type="tel"></v-text-field>
                </v-col>
              </v-row>
              <v-text-field v-model="formData.cvv" label="CVV" width="150" type="tel" prepend-icon="mdi-lock"></v-text-field>
            </v-container>
            <v-card-actions>
              <v-btn color="blue darken-1" @click="hideModal">Cancel</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" type="submit" :disabled="!valid">Pay</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/MyNavbar.vue'
import Footer from '@/views/FooterVue.vue'
import $ from 'jquery'
import config from '@/config'
import axios from 'axios'

export default {
  components: {
    NavBar,
    Footer
  },
  props: ['profile'],
  data() {
    return {
      item: null,
      itemId: this.itemId,
      backendEndpoint: `${config.backendEndpoint}`,
      dialog: false,
      valid: false,
      formData: {
        firstname: '',
        email: '',
        address: '',
        city: '',
        tel: '',
        zip: '',
        cardname: '',
        cardnumber: '',
        expmonth: '',
        expyear: '',
        cvv: ''
      }
    }
  },
  created() {
    this.$store.dispatch('getProducts')
    this.$store.dispatch('fetchCategories')
  },
  computed: {
    formattedPrice() {
      return this.$store.getters.formattedPrice
    },
    categories() {
      return this.$store.getters.categories
    },
    errorMessage() {
      return this.$store.state.errorMessage
    },
    total() {
      return this.$store.getters.total
    },
    user() {
      return this.$store.getters.user
    },
    accessToken() {
      return this.$store.state.accessToken
    },
    cart() {
      return this.$store.state.cart
    },
    favorites() {
      return this.$store.state.favorites
    }
  },
  methods: {
    formatTotal(price) {
      const [integerPart, decimalPart] = price.toString().split('.')
      return {
        integerPart: parseInt(integerPart).toLocaleString(),
        decimalPart: decimalPart || '00'
      }
    },
    itemAlreadyInCart(product) {
      return this.cart.some(item => item.id === product.id)
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId)
    },
    redirectToItemFromCart(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    updateQuantity(product_id, newQuantity) {
      this.$store.dispatch('UpdateItemQuantity', {
        product_id,
        newQuantity
      })
    },
    truncateName(description, maxLength) {
      if (!description) return ''
      if (description.length > maxLength) {
        return description.substring(0, maxLength) + '..'
      }
      return description
    },
    hideModal() {
      this.dialog = false
    },
    showModal() {
      this.dialog = true
    },
    paymentCheckout() {
      this.$refs.form.validate().then(isValid => {
        if (!isValid) return

        const formData = new FormData()
        Object.keys(this.formData).forEach(key => {
          formData.append(key, this.formData[key])
        })

        axios
          .post(`${config.backendEndpoint}/api/items/checkout`, formData, {})
          .then(() => {
            // Handle success
            this.closeModal()
          })
          .catch(error => {
            if (error.response && error.response.status === 403) {
              $('#error').text('Item with that name already exists!')
            }
            // Handle other errors
          })
      })
    }
  }
}
</script>

<style scoped>
input[type='number']::-webkit-inner-spin-button {
  position: absolute;
  width: 12.5%;
  height: 100%;
  top: 0;
  right: 0;
  margin: 0;
  padding: 0;
}
</style>
