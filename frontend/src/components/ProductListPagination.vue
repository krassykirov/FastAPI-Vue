<template>
  <div v-if="products && products.length > 0">
    <div class="product-list" id="mycard">
      <transition-group name="product-fade">
        <v-card
          v-for="product in products"
          :key="product.id"
          :data-category="product.category_id"
          class="mx-auto"
          width="282"
          height="470"
          style="padding: 3px !important; margin: 1px !important"
          elevation="5"
        >
          <v-img
            :src="`${backendEndpoint}/static/img/${product.name}/${product.image}`"
            class="card-img-top"
            @click="redirectToItemFromProduct(product.id)"
            style="cursor: pointer"
          ></v-img>
          <!-- prettier-ignore -->
          <v-card-text
          @click="redirectToItemFromProduct(product.id)"
          class="text-center"
          style="cursor: pointer; font-size: 14px; text-align: center; margin-bottom: 0; max-height: 3em"
        >
          <b>{{ truncateName(product.name, 60) }}</b>
        </v-card-text>
          <!-- prettier-ignore -->
          <v-card-text class="text-center" style="padding-left: 10px; font-size: 12px; margin-top: 10px; max-height: 1.5em">
          {{ truncateName(product.description, 70) }}
        </v-card-text>
          <v-card-actions class="pa-3" style="margin-top: 15px !important">
            <!-- prettier-ignore -->
            <v-row align="center" class="ma-0" style="font-size: 14px">
            <v-col cols="auto" class="pa-0">
              <v-rating
                :model-value="product.rating_float"
                background-color="white"
                color="orange-darken-2"
                density="compact"
                half-increments
                size="x-small"
                style="margin-left: 75px; padding: 0; margin-top: 3px"
              ></v-rating>
            </v-col>
            <span
              :id="'overall-rating' + product.id + '-float'"
              style="font-size: 12px"
              >&nbsp;{{ parseFloat(product.rating_float).toFixed(2) }}</span
            >
            &nbsp;
              <span class="grey--text text--lighten-2 caption mr-2" style="font-size: 12px">
                ({{ product.review_number }})
              </span>
          </v-row>
          </v-card-actions>
          <!-- prettier-ignore -->
          <v-card-actions style="justify-content: center; margin: 0; padding: 0">
          <span
            v-if="product.discount >= 0.01"
            class="badge bg-danger position-absolute top-0 start-0"
            style="font-size: 0.75rem; padding: 4px; margin-top: 5px; margin-left: 3px"
          >
            -{{ Math.floor(product.discount * 100) }}%
          </span>
          <span
            :class="getHeartClasses(product)"
            @click="addTofavorites(product)"
            style="
              position: absolute;
              top: 1%;
              right: 1%;
              font-weight: 900;
              font-size: 1.2em;
              cursor: pointer;
            "
          ></span>
          <!-- prettier-ignore -->
          <v-card-actions style="margin-top: -50px !important; padding: 0">
            <span
              v-if="product.discount_price"
              class="price"
              >${{ formattedPrice(product.discount_price).integerPart }}</span
            >
            <span
              v-if="product.discount_price"
              style="font-size: 0.7rem; color: #dc3545; position: relative; top: -0.4em"
              >{{ formattedPrice(product.discount_price).decimalPart }}</span
            >
          </v-card-actions>
        </v-card-actions>
          <!-- prettier-ignore -->
          <v-card-text v-if="product.discount >= 0.01" class="old-price">
           ${{ Math.floor(product.price) }}
         </v-card-text>
          <!-- prettier-ignore -->
          <v-card-text v-else class="old-price">
        </v-card-text>
          <!-- prettier-ignore -->
          <v-btn @click="addToCart(product)" color="outlined" elevation="10" width="100%"
        style="padding: 0; margin-top: 10px">
          Add to Cart &nbsp;
          <v-icon right>mdi-cart-outline</v-icon>
        </v-btn>
        </v-card>
      </transition-group>
    </div>
  </div>
  <template v-else>
    <div style="align-items: center; margin-left: 10%">
      <p style="margin-left: 22%; margin-top: 5px; font-size: 15px">
        No products were found matching your selection. Use fewer filters or
        remove all
      </p>
      <img :src="require('@/assets/no_result.gif')" />
    </div>
  </template>
</template>

<script>
import config from '@/config'

export default {
  props: {
    product: Object,
    min: Number,
    max: Number,
    cart: Array,
    favorites: Array,
    products: { type: Array, required: true },
    currentPage: { type: Number, required: true },
    itemsPerPage: { type: Number, required: true }
  },
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
.old-price {
  font-size: 0.8rem !important;
  height: 0.5em !important;
  text-decoration: line-through;
  color: #404447;
  margin-left: 115px;
  margin-top: -30px !important;
  margin-bottom: 10px !important;
  padding: 0 !important;
}
.v-btn:hover {
  background-color: #67c0ff;
}
</style>
