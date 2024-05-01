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
    <!-- <MessageArea /> -->
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
                <v-btn @click="paymentCheckout" color="primary" dark
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
    <!-- Modal -->
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
      data-backdrop="false"
    >
      <div class="modal-dialog" role="document" style="width: 628px">
        <div class="modal-content" style="width: 628px">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Payment Details</h5>
            <button
              type="button"
              class="close"
              id="close-modal"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" style="width: 628px">
            <div class="row">
              <div class="col-75">
                <div class="col-25" style="padding: 0">
                  <div class="container">
                    <h5>
                      Cart
                      <span style="color: black"
                        ><i class="fa fa-shopping-cart"></i>
                        <b>&nbsp;{{ cart.length }}</b></span
                      >
                    </h5>
                    <tbody style="width: 100%">
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
                        <td class="align-left text-left">
                          <div
                            class="input-group"
                            style="
                              max-width: 120px;
                              margin: auto;
                              max-height: 40px;
                            "
                          >
                            <button
                              class="btn btn-outline-secondary"
                              type="button"
                              @click="
                                updateQuantity(product.id, product.quantity - 1)
                              "
                            >
                              -
                            </button>
                            <input
                              type="number"
                              class="form-control text-center"
                              min="1"
                              max="3"
                              :value="product.quantity"
                              disabled
                            />
                            <button
                              class="btn btn-outline-secondary"
                              type="button"
                              @click="
                                updateQuantity(product.id, product.quantity + 1)
                              "
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <!-- prettier-ignore -->
                        <td
                          @click="redirectToItemFromCart(product.id)"
                          style="cursor: pointer"
                        >
                          <p style="cursor: pointer; margin: 15px; font-size: 14px">
                            {{ truncateName(product.name, 20) }}
                          </p>
                        </td>
                        <!-- prettier-ignore -->
                        <td style="width: 100px">
                          <!-- prettier-ignore -->
                          <div>
                          <span style="font-size: 0.9rem;">$</span>
                          <span v-if="product.discount_price" style="font-size: 0.9rem;">{{ formattedPrice(product.discount_price).integerPart }}</span>
                          <span v-if="product.discount_price" style="font-size: 0.6rem; position: relative; top: -0.4em;">{{ formattedPrice(product.discount_price).decimalPart }}</span>
                        </div>
                        </td>
                        <td>
                          <button
                            type="button"
                            class="btn btn-outline-danger btn-sm"
                            style="margin-bottom: 1px"
                            @click="removeFromCart(product.id)"
                          >
                            <i class="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    </tbody>
                    <hr />
                    <div
                      style="
                        width: 100%;
                        white-space: nowrap;
                        align-items: right;
                        white-space: nowrap;
                        overflow: hidden;
                      "
                    >
                      <!-- prettier-ignore -->
                      <div class="text-end mt-4">
                        <h4
                          style="
                            width: 150px;
                            margin-left: 60%;
                            margin-right: 5%;
                          "
                        > <!-- prettier-ignore -->
                          <!-- Total: ${{ total }} -->
                          <span style="font-size: 1.3rem;">$</span>
                          <span style="font-size: 1.3rem;">{{ formatTotal(total).integerPart }}</span>
                          <span style="font-size: 0.8rem; position: relative; top: -0.6em;">{{ formatTotal(total).decimalPart }}</span>
                        </h4>
                      </div>
                    </div>
                    <hr />
                  </div>
                </div>
                <div class="container">
                  <form
                    id="paymentForm"
                    enctype="multipart/form-data"
                    data-toggle="validator"
                  >
                    <div class="row">
                      <div class="col-50">
                        <h3>Shipping Address</h3>
                        <label for="fname"
                          ><i class="fa fa-user"></i> Full Name</label
                        >
                        <input
                          type="text"
                          id="fname"
                          name="firstname"
                          placeholder="John M. Doe"
                        />
                        <label for="email"
                          ><i class="fa fa-envelope"></i> Email</label
                        >
                        <input
                          type="text"
                          id="email"
                          name="email"
                          placeholder="john@example.com"
                        />
                        <label for="adr"
                          ><i class="fa fa-address-card-o"></i> Address</label
                        >
                        <input
                          type="text"
                          id="adr"
                          name="address"
                          placeholder="542 W. 15th Street"
                        />
                        <label for="city"
                          ><i class="fa fa-institution"></i> City</label
                        >
                        <input
                          type="text"
                          id="city"
                          name="city"
                          placeholder="New York"
                        />

                        <div class="row">
                          <div class="col-50">
                            <label for="state">Telephone</label>
                            <input
                              type="text"
                              id="state"
                              name="state"
                              placeholder="NY"
                            />
                          </div>
                          <div class="col-50">
                            <label for="zip">Zip</label>
                            <input
                              type="text"
                              id="zip"
                              name="zip"
                              placeholder="10001"
                            />
                          </div>
                        </div>
                      </div>
                      <div class="col-50">
                        <h3>Payment</h3>
                        <label for="fname">Accepted Cards</label>
                        <div class="icon-container">
                          <i class="fa fa-cc-visa" style="color: navy"></i>
                          <i class="fa fa-cc-amex" style="color: blue"></i>
                          <i class="fa fa-cc-mastercard" style="color: red"></i>
                          <i
                            class="fa fa-cc-discover"
                            style="color: orange"
                          ></i>
                        </div>
                        <label for="cname">Name on Card</label>
                        <input
                          type="text"
                          id="cname"
                          name="cardname"
                          placeholder="John More Doe"
                        />
                        <label for="ccnum">Credit card number</label>
                        <input
                          type="text"
                          id="ccnum"
                          name="cardnumber"
                          placeholder="1111-2222-3333-4444"
                        />
                        <label for="expmonth">Exp Month</label>
                        <input
                          type="text"
                          id="expmonth"
                          name="expmonth"
                          placeholder="September"
                        />
                        <div class="row">
                          <div class="col-50">
                            <label for="expyear">Exp Year</label>
                            <input
                              type="text"
                              id="expyear"
                              name="expyear"
                              placeholder="2018"
                            />
                          </div>
                          <div class="col-50">
                            <label for="cvv">CVV</label>
                            <input
                              type="text"
                              id="cvv"
                              name="cvv"
                              placeholder="352"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="modal-footer" style="padding-right: 40%">
                      <v-btn
                        color="primary"
                        dark
                        type="button"
                        class="btn btn-primary"
                        @click="hideModal"
                        >Cancel</v-btn
                      >
                      <v-btn
                        color="primary"
                        dark
                        type="submit"
                        class="btn btn-primary"
                        @click="paymentCheckout"
                        >Pay</v-btn
                      >
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/MyNavbar.vue'
import Footer from '@/views/FooterVue.vue'
import $ from 'jquery'
import config from '@/config'

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
      backendEndpoint: `${config.backendEndpoint}`
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
      $(document).ready(function () {
        $('#close-modal').click()
        $('#exampleModal').hide()
      })
    },
    paymentCheckout() {
      $('#paymentForm').submit(e => {
        e.preventDefault()
        const formData = new FormData(e.target)
        $.ajax({
          url: `${config.backendEndpoint}/api/items/checkout`,
          type: 'POST',
          processData: false,
          contentType: false,
          headers: {
            Authorization: `Bearer ${this.$store.state.accessToken}`
          },
          data: formData,
          success: () => {
            $(document).ready(function () {
              $('#exampleModal').hide()
            })
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
