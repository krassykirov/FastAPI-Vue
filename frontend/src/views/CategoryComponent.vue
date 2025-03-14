<template>
  <div
    class="container-fluid"
    style="width: 100vw; position: sticky; margin: 0; padding: 0"
  >
    <nav class="navbar navbar-expand-lg fixed-top bg-light" style="height: 4em">
      <MyNavbar
        :cart="cart"
        :favorites="favorites"
        :total="total"
        :user="user"
        :user_id="user_id"
        :scopes="scopes"
        :profile="profile"
        @addToCart="addToCart"
        @removeFromCart="removeFromCart"
        @redirectToItemFromNavbar="redirectToItemFromNavbar"
      />
    </nav>
    <div class="submenu">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item" :class="{ active: isActiveLink('home') }">
            <a @click="goToAllProducts">All Products</a>
          </li>
          <li
            v-for="(category, index) in categories"
            :key="index"
            class="breadcrumb-item"
            :class="{ active: isActiveCategory(category[0]) }"
          >
            <a @click="selectCategory(category[0])">{{ category[0] }}</a>
          </li>
        </ol>
      </nav>
    </div>
    <div class="product-container">
      <div class="filter-products-container row col-2">
        <div class="filter-card">
          <div class="filter-content collapse show" id="collapse_2">
            <label style="display: block; margin-bottom: 10px"
              >Filter by Brand</label
            >
            <div class="card-body" style="height: 200px; overflow-y: auto">
              <div
                class="container"
                v-for="brand in uniqueBrands"
                :key="brand"
                :class="{ active: getBrandCount(brand) !== 0 }"
                style="padding-left: 8px"
              >
                <label>
                  <input
                    style="
                      font-size: 0.9rem;
                      margin-bottom: 2px;
                      padding-left: 0;
                    "
                    type="checkbox"
                    class="brand-checkbox"
                    :data-brand="brand"
                    :disabled="getBrandCount(brand) === 0"
                    @change="handleBrandChange($event, brand)"
                  />
                  <span
                    style="
                      padding-left: 8px;
                      font-size: 0.8rem;
                      font-weight: 500;
                    "
                  >
                    {{ brand }}
                  </span>
                </label>
                <span
                  class="text-muted"
                  style="font-size: 0.8rem; padding-left: 0; font-weight: 400"
                >
                  ({{ getBrandCount(brand) }})
                </span>
              </div>
            </div>
          </div>
        </div>
        <!-- prettier-ignore -->
        <div class="filter-card">
          <div class="card-body">
            <label style="margin-bottom: 20px">Filter by Price</label>
          </div>
          <!-- Slider -->
          <div>
            <v-range-slider
              v-model="range"
              strict
              color="#5e95e2"
              :max="productMax"
              :min="productMin"
              :step="30"
              class="align-center"
              @update:modelValue="updateSliderRange"
              hide-details
              thumb-size="14"
              track-size="2"
              thumb-label="always"
            ></v-range-slider>
            <div class="range-display">
              <span style="font-weight: 400">${{ min }}</span> -
              <span style="font-weight: 400">${{ max }}</span>
            </div>
          </div>
        </div>
        <div
          class="filter-card"
          style="height: 45px; align-items: center; text-align: left"
        >
          <div class="filter-content collapse show" id="collapse_3">
            <div
              class="form-check form-check-inline"
              style="display: flex; align-items: center"
            >
              <input
                class="brand-checkbox"
                type="checkbox"
                id="discountCheckbox"
                v-model="isChecked"
                @change="handleDiscountChange"
                style="
                  font-size: 0.9rem;
                  margin-bottom: 11px;
                  margin-left: -17px;
                "
              />
              <label style="margin-top: 0; margin-bottom: 0; padding-left: 5px"
                >Discounted Products</label
              >
            </div>
          </div>
        </div>
        <div class="filter-card">
          <div
            class="filter-content collapse show"
            id="collapse_4"
            v-if="ratings && ratings.length"
          >
            <label> Filter by Rating </label>
            <div
              class="form-check form-check-inline"
              v-for="rating in ratings.slice().reverse()"
              :key="rating"
              style="
                display: flex;
                align-items: center;
                font-size: 0.8rem;
                margin-left: 0;
                padding-left: 0;
              "
            >
              <input
                style="font-size: 0.9rem; margin-bottom: 8px; margin-left: 8px"
                class="brand-checkbox"
                type="checkbox"
                :id="'rating' + rating"
                :value="rating"
                :disabled="getRatingItemCount(rating) === 0"
                v-model="selectedRating"
              />
              <label
                class="form-check-label"
                :for="'rating' + rating"
                style="margin-left: 5px"
              >
                <span
                  v-for="i in 5"
                  :key="i"
                  class="fa"
                  :class="{
                    'fa-star checked': i <= rating,
                    'fa-star unchecked': i > rating
                  }"
                  style="font-size: 14px; margin-top: 9px"
                >
                </span>
                <!-- prettier-ignore -->
                <span class="text-muted"
                  style="
                    font-size: 0.8rem;
                    padding-left: 0;
                    font-weight: 500;
                  "
                >&nbsp;({{ getRatingItemCount(rating) }})
              </span>
              </label>
            </div>
          </div>
        </div>
      </div>
      <template
        v-if="isLoading && selectedProducts && selectedProducts.length === 0"
      >
        <div style="align-items: center; margin-left: 25%; margin-top: 5%">
          <img :src="require('@/assets/loading2.gif')" />
        </div>
      </template>
      <template v-if="selectedProducts && selectedProducts.length > 0">
        <!-- prettier-ignore -->
        <v-container fluid class="product-list-category" id="mycard">
          <transition-group name="product-fade">
            <ProductList
              v-for="product in selectedProducts"
              :key="product.id"
              :cart="cart"
              :favorites="favorites"
              class="row g-0 col-auto"
              :product="product"
              :min="min"
              :max="max"
              :total="total"
              @addToCart="addToCart"
              @addTofavorites="addTofavorites"
              @removeFromCart="removeFromCart"
              @removeFromFavorites="removeFromFavorites"
              v-on:redirectToItem="redirectToItem"
              style="justify-content: left"
            ></ProductList>
          </transition-group>
        </v-container>
      </template>
      <template
        v-if="!isLoading && selectedProducts && selectedProducts.length === 0"
      >
        <div style="align-items: center; margin-left: 10%; margin-top: 3%">
          <img :src="require('@/assets/no_result.gif')" />
        </div>
      </template>
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
import config from '@/config'
import ProductList from '@/components/ProductList.vue'
import MyNavbar from '@/components/MyNavbar.vue'
import Footer from '@/views/FooterVue.vue'
import VueCookies from 'vue-cookies'
import { jwtDecode } from 'jwt-decode'
import router from '@/router'
import debounce from 'lodash/debounce'

// /* global bootstrap */

export default {
  components: {
    ProductList,
    MyNavbar,
    Footer
  },
  props: ['category'],
  emits: [
    'addToCart',
    'redirectToItem',
    'addTofavorites',
    'redirectToItemFromNavbar'
  ],
  data() {
    return {
      range: [1, 10000],
      isChecked: this.$store.state.isDiscountedChecked,
      backendEndpoint: `${config.backendEndpoint}`,
      categoryName: null,
      isLoading: true
    }
  },
  mounted() {
    this.isLoading = true
    if (this.selectedProducts.length > 0) {
      this.isLoading = false
    }
  },
  watch: {
    selectedProducts() {
      if (this.selectedProducts && this.selectedProducts.length > 0) {
        this.isLoading = false
      }
    }
  },
  created() {
    if (!this.$store.state.accessToken) {
      const accessToken = VueCookies.get('access_token')
      if (accessToken) {
        const user = jwtDecode(accessToken).sub
        const user_id = jwtDecode(accessToken).user_id
        this.$store.commit('UPDATE_USER', user)
        this.$store.commit('UPDATE_USER_ID', user_id)
      } else {
        this.errorMessage = 'Session expired'
        router.push('/login')
      }
    }
    const category = this.$route.params.category
    if (category) {
      this.$store
        .dispatch('getProducts')
        .then(() => this.$store.dispatch('fetchCategories'))
        .then(() => this.$store.dispatch('updateProductRange', category))
        .then(() => this.$store.dispatch('checkFavoritesOnLoad'))
        .catch(error => {
          if (error.message !== 'Token Expired') {
            // console.error('error', error)
          }
        })
      this.$watch(
        () => [this.$store.state.productMin, this.$store.state.productMax],
        () => {
          this.updateRangeFromStore()
        }
      )
      this.updateRangeFromStore()
    }
  },
  computed: {
    isPriceRangesSelected() {
      return this.$store.state.selectedPriceRanges.length > 0
    },
    selectedProducts() {
      if (!this.category) return []
      const category = this.$store.getters.categories.find(
        cat => cat[0] === this.category
      )
      if (category) {
        const categoryName = category[0]
        return this.filterProductsByCategory(categoryName)
      } else {
        return []
      }
    },
    uniqueBrands() {
      const brandCounts = {}
      let categoryId

      const selectedCategory = this.$route.params.category
      if (selectedCategory) {
        const category = this.$store.state.categories.find(
          category => category[0] === selectedCategory
        )
        if (category) {
          categoryId = category[2]
        }
      }
      if (categoryId !== undefined) {
        const filteredProducts = this.$store.state.products.filter(
          product => product.category_id === categoryId
        )
        filteredProducts.forEach(product => {
          const brand = product.brand
          brandCounts[brand] = (brandCounts[brand] || 0) + 1
        })
      }
      const uniqueBrands = Object.keys(brandCounts).filter(
        brand => brandCounts[brand] > 0
      )
      return uniqueBrands.sort()
    },
    formattedLastActive() {
      if (!this.lastActiveDate) return ''
      return new Date(this.lastActiveDate).toLocaleString()
    },
    formattedInactiveTime() {
      return this.inactiveTime >= 0 ? `${this.inactiveTime} min` : ''
    },
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    total() {
      return this.$store.getters.total
    },
    filteredProducts() {
      return this.$store.getters.filteredProducts
    },
    products() {
      return this.$store.getters.products
    },
    cart() {
      return this.$store.getters.cart
    },
    favorites() {
      return this.$store.getters.favorites
    },
    min() {
      return this.$store.getters.min
    },
    max() {
      return this.$store.getters.max
    },
    productMin() {
      return this.$store.getters.productMin
    },
    productMax() {
      return this.$store.getters.productMax
    },
    selectedCategories() {
      return this.$store.getters.selectedCategories
    },
    selectedBrands() {
      return this.$store.getters.selectedBrands
    },
    selectedRating: {
      get() {
        return this.$store.getters.selectedRating
      },
      set(value) {
        this.$store.commit('SET_SELECTED_RATING', value)
      }
    },
    ratings() {
      return this.$store.getters.ratings
    },
    accessToken() {
      return this.$store.getters.accessToken
    },
    accessTokenExpiration() {
      return this.$store.getters.accessTokenExpiration
    },
    refreshTokenExpiration() {
      return this.$store.getters.refreshTokenExpiration
    },
    user_id() {
      return this.$store.state.user_id
    },
    user() {
      return this.$store.state.user
    },
    categories() {
      return this.$store.getters.categories
    },
    profile() {
      return this.$store.getters.profile
    },
    sortOrder() {
      return this.$store.getters.sortOrder
    }
  },
  methods: {
    updateRangeFromStore() {
      this.range = [this.$store.state.productMin, this.$store.state.productMax]
    },
    debouncedUpdateSliderRange: debounce(function () {
      let [minVal, maxVal] = this.range
      if (maxVal - minVal < 200) {
        minVal = Math.max(
          minVal - Math.ceil((200 - (maxVal - minVal)) / 2),
          this.productMin
        )
        maxVal = Math.min(
          maxVal + Math.ceil((200 - (maxVal - minVal)) / 2),
          this.productMax
        )
        return
      }
      this.$store.commit('SET_MIN_PRICE', minVal)
      this.$store.commit('SET_MAX_PRICE', maxVal)
    }, 500),
    updateSliderRange() {
      this.debouncedUpdateSliderRange()
    },
    isActiveLink(link) {
      return this.$route.name === link
    },
    isActiveCategory(category) {
      return (
        this.$route.name === 'category' &&
        this.$route.params.category === category
      )
    },
    goHome() {
      this.$router.push({ name: 'NewHome' })
    },
    goToAllProducts() {
      this.$router.push({ name: 'home' })
      // window.location.assign('/products')
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: 'auto' })
      })
    },
    selectCategory(category) {
      this.$store.commit('SET_SELECTED_BRANDS', [])
      const checkboxes = document.querySelectorAll('input[type="checkbox"]')
      checkboxes.forEach(checkbox => {
        checkbox.checked = false
      })
      this.$store
        .dispatch('updateProductRange', category)
        .then(() => {
          this.$router.push({ name: 'category', params: { category } })
          window.scrollTo({
            top: 0,
            behavior: 'auto'
          })
        })
        .catch(error => {
          throw error
        })
    },
    filterProductsByCategory(categoryID) {
      return this.$store.getters.filteredProductsByCategory(categoryID)
    },
    getBrandCount(brand) {
      const selectedCategory = this.$route.params.category
      const categoryId = this.$store.state.categories.find(
        category => category[0] === selectedCategory
      )[2]
      const filteredProducts = this.$store.state.products.filter(
        product => product.category_id === categoryId
      )
      return filteredProducts.filter(product => product.brand === brand).length
    },
    handleBrandChange(event, brand) {
      const checkbox = event.target
      const selectedBrands = [...this.selectedBrands]

      if (checkbox.checked) {
        selectedBrands.push(brand)
      } else {
        const index = selectedBrands.indexOf(brand)
        if (index !== -1) {
          selectedBrands.splice(index, 1)
        }
      }
      this.$store.commit('SET_SELECTED_BRANDS', selectedBrands)
    },
    async getProduct(itemId) {
      this.$store.dispatch('getProduct', itemId)
    },
    async getProducts() {
      this.$store.dispatch('getProducts')
    },
    async fetchCategories() {
      this.$store.dispatch('fetchCategories')
    },
    async handleCategoryChange() {
      const selectedCategories = await this.$store.dispatch(
        'getSelectedCategories'
      )
      this.$store.commit('UPDATE_SELECTED_CATEGORIES', selectedCategories)
    },
    getSelectedCategories() {
      this.$store.dispatch('getSelectedCategories')
    },
    toggleSortOrder() {
      this.$store.dispatch('toggleSortOrder')
    },
    redirectToItem(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    handleRatingChange(rating) {
      this.$store.dispatch('handleRatingChange', rating)
    },
    getRatingItemCount(rating) {
      let categoryId

      const selectedCategory = this.$route.params.category
      if (selectedCategory) {
        const category = this.$store.state.categories.find(
          category => category[0] === selectedCategory
        )
        if (category) {
          categoryId = category[2]
        }
      }
      if (categoryId !== undefined) {
        const filteredProducts = this.$store.state.products.filter(
          product => product.category_id === categoryId
        )
        const items = filteredProducts
        const count = items.reduce((accumulator, item) => {
          const floatRating = parseFloat(item.rating_float)
          const roundedRating = Math.floor(floatRating + 0.5)
          if (roundedRating === rating) {
            return accumulator + 1
          }
          return accumulator
        }, 0)
        return count
      }
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'auto' })
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId)
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
    },
    removeFromFavorites(itemId) {
      this.$store.dispatch('removeFromFavorites', itemId)
    },
    handleDiscountChange() {
      this.$store.dispatch('handleDiscountChange', this.isChecked)
    },
    redirectToItemFromNavbar(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    }
  }
}
</script>
<style scoped>
.product-list-category {
  padding: 0 !important;
  margin: 0 !important;
  margin-right: 8.5% !important;
  display: grid !important;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  text-align: left;
}
.col-auto {
  padding: 1px !important;
}
</style>
