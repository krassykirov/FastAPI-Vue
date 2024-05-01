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
    <div class="container-fluid mt-5" style="margin-left: 10%">
      <div
        class="row"
        style="
          display: -ms-flexbox;
          display: flex;
          -ms-flex-wrap: wrap;
          flex-wrap: wrap;
          margin: 0 -16px;
        "
      >
        <div>
      </div>
      </div>
    </div>
    <v-container fluid>
      <v-row justify="center">
        <v-col cols="12" md="6">
          <!-- prettier-ignore -->
          <v-card class="px-6 py-8" elevation="2" outlined>
            <h3 class="text-center mb-4" style="margin-left: 14%">
              <h6 v-if="message" style="margin-right: 19%; margin-bottom: 1%">
                <i class="fa fa-search" style="font-size: 1.2rem"> </i>&nbsp;{{
                  message
                }}
              </h6>
              <div v-else style="align-items: center; margin-right: 25%">
                <img :src="require('@/assets/no_result.gif')" />
              </div>
            </h3>
            <v-row
              v-for="product in searchResults"
              :key="product.id"
              align="center"
            >
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
                <div @click="redirectToItemFromCart(product.id)" style="font-size: 14px; font-weight: 800; color: #dc3545; cursor: pointer">
                  <span style="font-size: 0.9rem;">$</span>
                  <span v-if="product.discount_price" style="font-size: 0.95rem;">{{ formattedPrice(product.discount_price).integerPart }}</span>
                  <span v-if="product.discount_price" style="font-size: 0.65rem; position: relative; top: -0.4em;">{{ formattedPrice(product.discount_price).decimalPart }}</span>
                </div>
                <v-col cols="14">
                  <!-- prettier-ignore -->
                  <div style="font-size: 14px; cursor: pointer" @click="redirectToItemFromCart(product.id)">
                  {{ product.description }}
                 </div>
                </v-col>
                <v-rating
                  :model-value="product.rating_float"
                  color="orange-darken-2"
                  density="compact"
                  size="small"
                  half-increments
                  readonly
                ></v-rating>
              </v-col>
              <v-col cols="1">
                <v-btn @click="addToCart(product)" size="small" icon="mdi-cart-outline" color="primary"></v-btn>
              </v-col>
              <!-- <v-col cols="1">
                <v-btn @click="addTofavorites(product)" size="small" icon="mdi-heart" color="red"></v-btn>
              </v-col> -->
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <div
      class="toast"
      id="cartToast"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      data-bs-autohide="false"
      style="position: fixed; top: 8%; right: 1%; width: 250px; z-index: 1000"
    >
      <div
        class="toast-body"
        id="cartToastBody"
        style="font-weight: 500; font: 1.1em"
      ></div>
    </div>
    <Footer />
  </div>
</template>

<script>
import NavBar from '@/components/MyNavbar.vue'
import Footer from '@/views/FooterVue.vue'
import config from '@/config'

export default {
  components: {
    NavBar,
    Footer
    // MessageArea
  },
  props: ['profile', 'cart', 'favorites'],
  data() {
    return {
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  created() {
    this.$store.dispatch('fetchCategories')
  },
  computed: {
    message() {
      return this.$store.state.message
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
      return this.$store.getters.accessToken
    },
    searchResults() {
      return this.$store.state.searchResults
    },
    categories() {
      return this.$store.getters.categories
    },
    formattedPrice() {
      return this.$store.getters.formattedPrice
    }
  },
  methods: {
    formatPrice(price) {
      if (price !== null || price !== undefined) {
        const [integerPart, decimalPart] = price.toFixed(2).split('.')
        const formattedIntegerPart = integerPart.replace(
          /\B(?=(\d{3})+(?!\d))/g,
          '.'
        ) // Add dots for every 3 digits
        const formattedDecimalPart = decimalPart || '00' // Ensure two decimal places

        return {
          integerPart: formattedIntegerPart,
          decimalPart: formattedDecimalPart
        }
      }
    },
    getStarClasses(index, rating) {
      const filledStars = Math.floor(rating)
      if (index <= filledStars) {
        return 'fa fa-star checked'
      } else if (index === filledStars + 1 && rating % 1 !== 0) {
        return 'fa fa-star-half-full checked'
      } else {
        return 'fa fa-star-o checked'
      }
    },
    itemAlreadyInCart(product) {
      return this.cart.some(item => item.id === product.id)
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId)
    },
    redirectToItemFromCart(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    truncateName(description, maxLength) {
      if (description.length > maxLength) {
        return description.substring(0, maxLength) + '..'
      }
      return description
    }
  }
}
</script>
