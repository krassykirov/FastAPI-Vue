<template>
  <div
    id="carouselExampleFade"
    class="carousel slide carousel-fade"
    data-bs-ride="carousel"
    style="width: 1320px; margin-left: 8%"
  >
    <div class="carousel-indicators">
      <button
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide-to="0"
        class="active"
        aria-current="true"
        aria-label="Slide 0"
      ></button>
      <button
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide-to="1"
        aria-label="Slide 1"
      ></button>
      <button
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide-to="2"
        aria-label="Slide 2"
      ></button>
      <button
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide-to="3"
        aria-label="Slide 3"
      ></button>
      <button
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide-to="4"
        aria-label="Slide 4"
      ></button>
    </div>
    <div class="carousel-inner">
      <div class="carousel-item active" data-bs-interval="3000">
        <a @click="goToCategory('Smartwatches')">
          <img
            src="../assets/garmin-last.png"
            class="d-block w-100"
            alt="..."
            style="cursor: pointer"
          />
        </a>
        <div class="carousel-caption d-none d-md-block">
          <h5>Garmin Smartwatches</h5>
          <p>See All Offers</p>
        </div>
      </div>
      <div class="carousel-item" data-bs-interval="3000">
        <a @click="goToCategory('Laptops')">
          <img
            src="../assets/ASUS_OLED.jpeg"
            class="d-block w-100"
            alt="..."
            style="cursor: pointer"
          />
        </a>
      </div>
      <div class="carousel-item" data-bs-interval="3000">
        <a @click="goToItem(50)">
          <img
            src="../assets/samsung-banner-last2.jpeg"
            class="d-block w-100"
            alt="..."
            style="cursor: pointer"
          />
        </a>
        <div class="carousel-caption d-none d-md-block">
          <h5>Samsung Neo QLED 8K</h5>
          <p>
            Powerfully precise Take in stunning 8K resolution across all your
            content. Samsung 75" Q800T QLED 8K Smart TV.
          </p>
        </div>
      </div>
      <div class="carousel-item" data-bs-interval="3000">
        <a @click="goToItem(8)">
          <img
            src="../assets/lenovo-legion.jpeg"
            class="d-block w-100"
            alt="..."
            style="cursor: pointer"
          />
        </a>
        <div class="carousel-caption d-none d-md-block">
          <!-- <h5>First slide label</h5> -->
          <p>Lenovo Legion 5 Pro 16" Gen 8, i7-13700HX NVIDIA RTX 4070</p>
        </div>
      </div>
      <div class="carousel-item" data-bs-interval="3000">
        <a @click="goToItem(49)">
          <img
            src="../assets/Xiaomi-13-Ultra.jpg"
            class="d-block w-100"
            alt="..."
            style="cursor: pointer"
          />
        </a>
        <div class="carousel-caption d-none d-md-block">
          <!-- <h5>First slide label</h5> -->
          <p>XIAOMI 14 ULTRA LEICA PROFFESIONNAL OPTICAL LENS WQHD+ 6.73"</p>
        </div>
      </div>
    </div>
    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#carouselExampleFade"
      data-bs-slide="prev"
      style="margin-left: -75px"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#carouselExampleFade"
      data-bs-slide="next"
      style="margin-right: -75px"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script>
import config from '@/config'
// /* global bootstrap */

export default {
  props: {
    products: Array,
    carouselId: String
  },
  data() {
    return {
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  created() {
    Promise.all([this.$store.dispatch('checkFavoritesOnLoad')])
  },
  computed: {
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
    categories() {
      return this.$store.state.categories
    }
  },
  methods: {
    goToCategory(category) {
      this.$router.push({ name: 'category', params: { category: category } })
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: 'auto' })
      })
    },
    goToItem(itemId) {
      this.$router.push({ name: 'Item', params: { itemId } })
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
    getHeartClasses(product) {
      const isFavorite = this.isFavorite(product)
      return isFavorite ? 'fa fa-heart red-color' : 'fa fa-heart-o'
    },
    isFavorite(product) {
      return this.$store.state.favorites.some(
        favorite => favorite.id === product.id
      )
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
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
<style scoped>
.carousel img {
  height: 620px;
  width: 1920px;
  margin-bottom: 1%;
  border-radius: 20px;
}

.carousel .carousel-indicators li {
  background-color: rgb(140, 140, 196) !important;
}
.carousel-inner {
  width: 100%;
}
</style>
