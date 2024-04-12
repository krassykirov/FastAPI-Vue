<template>
  <v-lazy
    :min-height="200"
    :options="{ threshold: 0.5 }"
    transition="fade-transition"
  >
    <div
      class="card"
      :id="product.id"
      :data-category="product.category_id"
      style="margin: 0.15%; padding: 0.15%"
    >
      <div class="card-body" style="padding: 1%">
        <!-- Discount badge -->
        <span
          class="badge bg-danger position-absolute top-0 start-0"
          v-if="product.discount >= 0.01"
          style="font-size: 0.8rem; margin: 1%; top: 0"
        >
          -{{ Math.floor(product.discount * 100) }}%
        </span>

        <!-- Favorite icon -->
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

        <!-- Product image -->
        <img
          :src="
            `${backendEndpoint}/static/img/` +
            product.name +
            '/' +
            product.image
          "
          class="card-img-top"
          @click="redirectToItemFromProduct(product.id)"
          style="cursor: pointer"
        />
        <p
          @click="redirectToItemFromProduct(product.id)"
          class="card-title"
          style="
            margin-bottom: 1%;
            padding: 1%;
            height: 3em;
            font-size: 14px;
            font-weight: 600;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            line-height: 1;
            cursor: pointer;
          "
        >
          {{ truncateName(product.name, 60) }}
        </p>
        <p
          style="cursor: pointer; margin-bottom: 1%; font-size: 1em"
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
          >
            &nbsp;{{ parseFloat(product.rating_float).toFixed(2) }}
          </span>
          <span :id="'overall-rating' + product.id" class="text-muted">
            ({{ product.review_number }})
          </span>
        </p>
        <div
          style="
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            margin-top: 1.7%;
          "
        >
          <span
            style="
              font-size: 0.95rem;
              color: #dc3545;
              font-weight: 800;
              margin-bottom: 1%;
              margin-left: -12px;
            "
          >
            <span v-if="product.discount_price" style="font-size: 0.95rem">
              ${{ formattedPrice(product.discount_price).integerPart }}
            </span>
            <span
              v-if="product.discount_price"
              style="font-size: 0.7rem; position: relative; top: -0.4em"
            >
              {{ formattedPrice(product.discount_price).decimalPart }}
            </span>
          </span>
          <span v-if="product.discount >= 0.01" class="old-price">
            ${{ Math.floor(product.price) }}
          </span>
          <span v-else class="old-price2">&nbsp;</span>
        </div>
        <v-btn
          @click="addToCart(product)"
          color="outlined"
          elevation="10"
          width="100%"
          style="padding: 0; margin-top: 16px !important"
        >
          Add to Cart &nbsp;
          <v-icon right>mdi-cart-outline</v-icon>
        </v-btn>
      </div>
    </div>
  </v-lazy>
</template>

<script>
import config from '@/config'

export default {
  props: ['product', 'min', 'max', 'cart', 'favorites', 'products'],
  emits: ['addToCart', 'redirectToItem', 'addTofavorites'],
  data() {
    return {
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  computed: {
    formattedPrice() {
      return this.$store.getters.formattedPrice
    },
    filteredProducts() {
      return this.$store.getters.filteredProducts
    },
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    isFavorite(product) {
      return this.$store.state.favorites.some(
        favorite => favorite.id === product.id
      )
    },
    getHeartClasses() {
      return product => {
        const isFavorite = this.$store.state.favorites.some(
          favProduct => favProduct.id === product.id
        )
        return isFavorite ? 'fa fa-heart red-color' : 'fa fa-heart-o'
      }
    }
  },
  methods: {
    redirectToItemFromProduct(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    itemAlreadyInCart(product) {
      return this.$store.getters.isItemInCart(product.id)
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
    },
    removeFromFavorites(itemId) {
      this.$store.dispatch('removeFromFavorites', itemId)
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
    truncateName(description, maxLength) {
      if (!description) return '' // Add this guard clause
      if (description.length > maxLength) {
        return description.substring(0, maxLength) + '..'
      }
      return description
    }
  }
}
</script>
<style scoped>
.v-btn:hover {
  background-color: #5e95e2;
}
</style>
