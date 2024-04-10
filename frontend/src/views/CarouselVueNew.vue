<template>
  <Carousel :items-to-show="6" :wrap-around="false">
    <Slide v-for="(product, index) in items" :key="index">
      <div class="carousel__item">
        <div
          class="card small"
          :id="product.id"
          :data-category="product.category_id"
          style="margin: 0.15%; padding: 0.15%"
        >
          <div class="card-body" style="padding: 1%; max-width: 400px">
            <span
              class="badge bg-danger position-absolute top-0 start-0"
              v-if="product.discount >= 0.01"
              style="font-size: 0.8rem; margin: 1%; top: 0"
              >-{{ Math.floor(product.discount * 100) }}%
            </span>
            <span
              :class="getHeartClasses(product)"
              @click="addTofavorites(product)"
              :id="'heart' + product.id"
              style="
                position: absolute;
                top: 1%;
                right: 1%;
                font-weight: 900;
                font-size: 1.2em;
                cursor: pointer;
              "
            ></span>
            <img
              :src="
                `${backendEndpoint}/static/img/` +
                product.name +
                '/' +
                product.image
              "
              class="card-img-top"
              @click="redirectToItemFromProduct(product.id)"
              style="cursor: pointer; width: 95% !important"
            />
            <h6
              @click="redirectToItemFromProduct(product.id)"
              class="card-title"
              style="
                margin-bottom: 1%;
                padding: 1%;
                height: 3em;
                font-size: 1rem;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                line-height: 1;
                cursor: pointer;
              "
            >
              {{ truncateName(product.name, 60) }}
            </h6>
            <p
              style="cursor: pointer; margin-bottom: 1%; font-size: 0.9rem"
              @click="redirectToItemFromProduct(product.id)"
            >
              <span
                v-for="i in 5"
                :key="i"
                :class="getStarClasses(i, product.rating_float)"
              ></span>
              <span
                :id="'overall-rating' + product.id + '-float'"
                class="overall-rating"
                >&nbsp;{{ parseFloat(product.rating_float).toFixed(2) }}</span
              >
              <span :id="'overall-rating' + product.id" class="overall-rating2">
                ({{ product.review_number }})
              </span>
            </p>
            <input type="number" :data-price="product.price" hidden />
            <div
              style="
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
              "
            >
              <span
                style="
                  font-size: 0.95rem;
                  color: #dc3545;
                  font-weight: 800;
                  margin-bottom: 1%;
                  margin-top: 1%;
                  margin-left: -12px;
                "
              >
                <!-- prettier-ignore -->
                <div>
                <!-- prettier-ignore -->
                <span style="font-size: 1rem">$</span>
                <span v-if="product.discount_price" style="font-size: 1rem">{{ formattedPrice(product.discount_price).integerPart }}</span>
                <span v-if="product.discount_price" style="font-size: 0.7rem; position: relative; top: -0.4em">{{ formattedPrice(product.discount_price).decimalPart }}</span>
              </div>
              </span>
            </div>
          </div>
          <span v-if="product.discount >= 0.01" class="old-price">
            ${{ Math.floor(product.price) }}
          </span>
          <span v-else style="font-size: 1em; margin-top: 1%">&nbsp;</span>
          <v-btn
            @click="addToCart(product)"
            flat
            width="100%"
            style="padding: 0; margin-top: 10px !important"
          >
            Add to Cart &nbsp;
            <v-icon right>mdi-cart-outline</v-icon>
          </v-btn>
        </div>
      </div>
    </Slide>
    <template #addons>
      <Navigation />
      <!-- <Pagination /> -->
    </template>
  </Carousel>
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
      style="font-weight: 500; font: 1.1rem"
    ></div>
  </div>
</template>
<script>
import { Carousel, Navigation, Slide } from 'vue3-carousel'
import { defineComponent } from 'vue'
import 'vue3-carousel/dist/carousel.css'

export default defineComponent({
  name: 'WrapAround',
  components: {
    Carousel,
    Slide,
    Navigation
    // Pagination
  },
  props: {
    backendEndpoint: {
      type: String,
      required: true
    },
    items: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    currentSlide: 0
  }),
  computed: {
    formattedPrice() {
      return this.$store.getters.formattedPrice
    }
  },
  methods: {
    slideTo(val) {
      this.currentSlide = val
    },
    isFavorite(product) {
      return this.$store.state.favorites.some(
        favorite => favorite.id === product.id
      )
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
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
    redirectToItemFromProduct(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    }
  }
})
</script>
<style scoped>
:root {
  --vc-clr-primary: #2e76db;
}
.carousel {
  max-width: 1440px;
  padding: 0;
  margin: 0;
}
.carousel__item {
  max-width: 330px !important;
  font-size: 18px;
  display: flex;
  padding: 1px !important;
  height: 21vw;
  margin: 5px !important;
}
.carousel__viewport {
  perspective: 2000px;
}
.carousel__slide {
  padding: 5px;
  margin: 0 !important;
}
.carousel__slide--sliding {
  transition: 0.3s;
}
.carousel__slide {
  transform: rotateY(-20deg) scale(0.9);
}
.carousel__prev,
.carousel__next {
  border: 1px;
  color: rgb(94, 152, 202);
  border-radius: 50%;
  margin-left: -40px;
  margin-right: -40px;
  width: 40px;
  height: 40px;
  display: flex;
}
.v-btn:hover {
  background-color: #5e95e2;
}
</style>
