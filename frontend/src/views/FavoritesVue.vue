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
      :scopes="scopes"
      :profile="profile"
      :favorites="favorites"
    />
    <v-container fluid>
      <v-row justify="center" style="margin-top: 1%">
        <v-col cols="12" md="6">
          <v-card class="px-6 py-8" elevation="2" outlined>
            <h3 class="text-center mb-4" style="margin-right: 3%">
              <v-icon size="32" class="mr-2" color="red"
                >mdi-heart-outline</v-icon
              >
              Favorite Products
            </h3>
            <!-- prettier-ignore -->
            <v-row
              v-for="product in favorites"
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
                <div style="font-size: 14px; font-weight: 800; color: #dc3545">
                  <span style="font-size: 0.9rem;">$</span>
                  <span v-if="product.discount_price" style="font-size: 0.9rem;">{{ formattedPrice(product.discount_price).integerPart }}</span>
                  <span v-if="product.discount_price" style="font-size: 0.6rem; position: relative; top: -0.4em;">{{ formattedPrice(product.discount_price).decimalPart }}</span>
                </div>
                <v-col cols="14">
                  <!-- prettier-ignore -->
                  <div style="font-size: 14px">
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
                <!-- prettier-ignore -->
                <v-btn @click="addToCart(product)" size="x-small" icon="mdi-cart-outline"></v-btn>
              </v-col>
            </v-row>
            <v-divider class="my-4"></v-divider>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <h3 class="text-center mb-4" style="margin-right: 7%">
      You may also like..
    </h3>
    <div style="margin-left: 9%">
      <MessageArea />
    </div>
    <Footer />
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
  </div>
</template>

<script>
import NavBar from '@/components/MyNavbar.vue'
import MessageArea from '@/views/MessageAreaVue.vue'
import Footer from '@/views/FooterVue.vue'
import config from '@/config'

export default {
  components: {
    NavBar,
    MessageArea,
    Footer
  },
  props: ['profile'],
  data() {
    return {
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  created() {
    this.$store.dispatch('fetchCategories')
  },
  computed: {
    filteredLaptops() {
      return this.products.filter(item => {
        return item.category_id === 1
      })
    },
    products() {
      return this.$store.getters.products
    },
    filteredTablets() {
      return this.products.filter(item => {
        return item.category_id === 3
      })
    },
    filteredSmartphones() {
      return this.products.filter(item => {
        return item.category_id === 2
      })
    },
    filteredSmartwatches() {
      return this.products.filter(item => {
        return item.category_id === 4
      })
    },
    filteredTV() {
      return this.products.filter(item => {
        return item.category_id === 5
      })
    },
    filteredProducts() {
      return this.$store.getters.filteredProducts
    },
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
    scopes() {
      return this.$store.state.scopes
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
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
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
    redirectToItemFromCart(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    truncateName(description, maxLength) {
      if (!description) return ''
      if (description.length > maxLength) {
        return description.substring(0, maxLength) + '..'
      }
      return description
    }
  }
}
</script>
