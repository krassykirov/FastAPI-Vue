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
    <div
      class="toast"
      id="cartToast"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      data-bs-autohide="false"
      style="
        position: fixed;
        top: 11%;
        right: 0;
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
    <div
      class="container"
      style="margin-top: 2%; padding: 0; margin-left: 5%; margin-bottom: 0"
    >
      <carousel :items="filteredLaptops" :backendEndpoint="backendEndpoint" />
      <carousel
        :items="filteredSmartphones"
        :backendEndpoint="backendEndpoint"
      />
      <carousel :items="filteredTablets" :backendEndpoint="backendEndpoint" />
      <carousel
        :items="filteredSmartwatches"
        :backendEndpoint="backendEndpoint"
      />
      <carousel :items="filteredTV" :backendEndpoint="backendEndpoint" />
    </div>
  </div>
</template>

<script>
import Carousel from '@/views/CarouselVueNew.vue'
import config from '@/config'

export default {
  components: {
    Carousel
  },
  props: ['profile'],
  data() {
    return {
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  created() {
    this.$store.dispatch('checkFavoritesOnLoad')
  },
  computed: {
    filteredProducts() {
      return this.$store.getters.filteredProducts
    },
    discountedProducts() {
      return this.$store.getters.filteredProducts.filter(
        product => product.discount > 0
      )
    },
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
    errorMessage() {
      return this.$store.state.errorMessage
    },
    total() {
      return this.$store.getters.total
    },
    user() {
      return this.$store.getters.user
    },
    user_id() {
      return this.$store.getters.user_id
    },
    ratings() {
      return this.$store.getters.ratings
    },
    cart() {
      return this.$store.state.cart
    },
    favorites() {
      return this.$store.state.favorites
    },
    isFavorite(product) {
      return this.$store.state.favorites.some(
        favorite => favorite.id === product.id
      )
    },
    getHeartClasses(product) {
      const isFavorite = this.isFavorite(product)
      return isFavorite ? 'fa fa-heart red-color' : 'fa fa-heart-o'
    }
  },
  methods: {
    redirectToCategory(category) {
      this.$router.push({ name: 'category', params: { category: category } })
      document.body.scrollIntoView({ behavior: 'auto' })
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    truncateName(description, maxLength) {
      if (!description) return '' // Add this guard clause
      if (description.length > maxLength) {
        return description.substring(0, maxLength) + '..'
      }
      return description
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId)
    },
    redirectToItemFromCart(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    redirectToItemFromNavbar(itemId) {
      this.$router.push({ name: 'Item', params: { itemId } })
    },
    redirectToItemFromProduct(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    }
  }
}
</script>
