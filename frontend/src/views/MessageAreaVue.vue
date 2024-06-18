<template>
  <carousel :items="filteredLaptops" :backendEndpoint="backendEndpoint" />
  <carousel :items="filteredSmartphones" :backendEndpoint="backendEndpoint" />
  <carousel :items="filteredTablets" :backendEndpoint="backendEndpoint" />
  <carousel :items="filteredSmartwatches" :backendEndpoint="backendEndpoint" />
  <carousel :items="filteredTV" :backendEndpoint="backendEndpoint" />
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
    scopes() {
      return this.$store.state.scopes
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
    }
  }
}
</script>
