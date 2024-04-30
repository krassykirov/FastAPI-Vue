<template>
  <div
    class="container-fluid"
    style="width: 100vw; position: sticky; margin: 0; padding: 0"
  >
    <MyNavbar
      :cart="cart"
      :favorites="favorites"
      :total="total"
      :user="user"
      :user_id="user_id"
      :is_admin="is_admin"
      :profile="profile"
      @addToCart="addToCart"
      @removeFromCart="removeFromCart"
      @redirectToItemFromNavbar="redirectToItemFromNavbar"
    />
    <div class="submenu2">
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
      <div class="filter-products-container row col-4">
        <div class="filter-card">
          <div class="filter-content collapse show" id="collapse_2">
            <label style="display: block; margin-bottom: 10px"
              >Filter by Category
            </label>
            <div class="card-body">
              <div
                class="container"
                v-for="category in categories"
                :key="category[2]"
                :class="{ active: category[1] !== 0 }"
                style="padding-left: 7px"
              >
                <label>
                  <input
                    style="font-size: 0.8rem; margin-bottom: 2px"
                    type="checkbox"
                    class="cat-checkbox"
                    :data-category="category[2]"
                    :data-category-name="category[0]"
                    :disabled="category[1] === 0"
                    @change="handleCategoryChange"
                  />
                  <span style="padding-left: 5px">
                    {{ category[0] }}
                  </span>
                </label>
                <span
                  class="text-muted"
                  style="
                    font-size: 0.8rem;
                    font-family: sans-serif;
                    font-weight: 500;
                  "
                >
                  ({{ category[1] }})
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="filter-card">
          <div class="card-body">
            <label style="margin-bottom: 20px">Filter by Price</label>
          </div>
          <div>
            <v-range-slider
              v-model="range"
              strict
              color="#5e95e2"
              :max="productMax"
              :min="productMin"
              :step="50"
              class="align-center"
              @update:modelValue="updateSliderRange"
              hide-details
              thumb-size="14"
              track-size="2"
              thumb-label="always"
              :disabled="isPriceRangesSelected"
            ></v-range-slider>
          </div>
          <div class="range-display">
            <span style="font-weight: 400">${{ min }}</span> -
            <span style="font-weight: 400">${{ max }}</span>
          </div>
        </div>
        <div class="filter-card">
          <div class="card-body">
            <label> Price Range </label>
            <div
              class="form-check"
              style="padding-left: 5px; font-weight: 400"
              v-for="(range, index) in priceRanges"
              :key="index"
            >
              <input
                type="checkbox"
                class="price-checkbox"
                :value="range.value"
                :price-range="range.value"
                :data-price-label="range.label"
                style="
                  font-size: 14px;
                  margin-bottom: 2px;
                  margin-left: 0;
                  font-weight: 400;
                "
                @change="handlePriceRangeChange"
              />
              <label :for="range.value" style="margin-left: 5px">{{
                range.label
              }}</label>
              <span
                class="text-muted"
                style="
                  font-size: 0.8rem;
                  font-family: sans-serif;
                  font-weight: 400;
                "
              >
                ({{ getProductCount(range.value) }})
              </span>
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
              style="display: flex; align-items: left"
            >
              <input
                class="brand-checkbox"
                type="checkbox"
                id="discountCheckbox"
                v-model="isChecked"
                @change="handleDiscountChange"
                style="margin-bottom: 12px; margin-left: -17px"
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
                class="rating-checkbox"
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
                  style="font-size: 15px; margin-top: 8px"
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
        v-if="isLoading && filteredProducts && filteredProducts.length === 0"
      >
        <div style="align-items: center; margin-left: 25%; margin-top: 5%">
          <img :src="require('@/assets/loading2.gif')" />
        </div>
      </template>
      <div class="main-filter-container">
        <template
          v-if="!isLoading && filteredProducts && filteredProducts.length > 0"
        >
          <div class="apply-filter-container card">
            <div>
              <div
                style="
                  font-weight: 500;
                  font-size: 0.9rem;
                  margin-bottom: 0;
                  margin-top: 5px;
                "
              >
                Active Filters ({{ appliedFilters.length }}) Products ({{
                  paginatedProducts.length
                }}/{{ filteredProducts.length }}) Page({{ this.currentPage }}/{{
                  totalPages
                }})
              </div>
              <button
                v-for="(filter, index) in appliedFilters"
                :key="index"
                class="shadow btn custom-btn remove-filter-btn"
                :class="{
                  'remove-filter-btn': filter !== '$' + min + ' - $' + max
                }"
                style="
                  margin-bottom: 0;
                  margin-top: 10px;
                  width: 135px;
                  max-width: 150px;
                "
                @click="removeFilter(filter)"
              >
                {{ filter }}
                <i
                  v-if="
                    filter !== '$' + min + ' - $' + max ||
                    min !== productMin ||
                    max !== productMax
                  "
                  class="bi bi-x-circle-fill remove-icon"
                ></i>
              </button>
            </div>
            <hr />
            <!-- Area 2: Sort button, Reset Button, Select -->
            <div
              style="display: flex; flex-direction: row; justify-content: left"
            >
              <button
                v-if="appliedFilters.length > 1"
                class="shadow btn custom-btn remove-filter-btn"
                @click="removeAllFilters"
                style="margin-bottom: 15px; width: 135px"
              >
                Reset Filters
                <i
                  v-if="appliedFilters.length > 1"
                  class="bi bi-x-circle-fill remove-icon"
                ></i>
              </button>
              <button
                class="shadow btn custom-btn remove-filter-btn"
                @click="toggleSortOrder"
                style="align-items: center; margin-bottom: 15px; width: 135px"
              >
                Sort Price
                <span
                  v-if="sortOrder === 'asc'"
                  class="bi bi-sort-up-alt align-middle"
                  style="font-size: 0.9rem"
                ></span>
                <span
                  v-else
                  class="bi bi-sort-down align-middle"
                  style="font-size: 0.9rem"
                ></span>
              </button>
              <select
                @change="changeItemsPerPage"
                class="shadow btn custom-btn remove-filter-btn"
                style="margin-bottom: 15px; width: 135px"
              >
                <option v-for="option in options" :value="option" :key="option">
                  {{ option }}
                </option>
              </select>
            </div>
          </div>
        </template>
        <template v-if="filteredProducts && filteredProducts.length > 0">
          <div class="product-list" id="mycard">
            <transition-group name="product-fade">
              <ProductList
                :products="paginatedProducts"
                :key="products"
                :currentPage="currentPage"
                :itemsPerPage="itemsPerPage"
                :cart="cart"
                :favorites="favorites"
                @addToCart="addToCart"
                @addTofavorites="addTofavorites"
                @removeFromCart="removeFromCart"
                @removeFromFavorites="removeFromFavorites"
                @redirectToItem="redirectToItem"
                style="justify-content: left; margin-top: 0"
              />
            </transition-group>
          </div>
        </template>
        <template
          v-else-if="
            !isLoading && filteredProducts && filteredProducts.length === 0
          "
        >
          <div style="align-items: center; margin-left: 10%">
            <p style="margin-left: 12%; margin-top: 5px; font-size: 15px">
              No products were found matching your selection. Use fewer filters
              or remove all
            </p>
            <img :src="require('@/assets/no_result.gif')" />
          </div>
        </template>
        <!-- prettier-ignore -->
        <div v-if="totalPages > 1" style="margin-top: 30px; margin-left: -25%">
          <nav>
            <v-pagination
              v-model="currentPage"
              :length="totalPages"
              @input="paginatedProducts"
            ></v-pagination>
          </nav>
          <p style="margin-left: 48%">
            Products ({{
              paginatedProducts.length}}/{{ filteredProducts.length }})
         </p>
        </div>
      </div>
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
        style="font-weight: 500; font: 1.1rem"
      ></div>
    </div>
  </div>
</template>

<script>
// import $ from 'jquery'
// import 'bootstrap'
import router from '@/router'
import VueCookies from 'vue-cookies'
import { jwtDecode } from 'jwt-decode'
import ProductList from '@/components/ProductListPagination.vue'
import MyNavbar from '@/components/MyNavbar.vue'
import Footer from '@/views/FooterVue.vue'
import config from '@/config'
import debounce from 'lodash/debounce'
// import store from '@/store/index.js'

export default {
  name: 'HomeView',
  emits: [
    'addToCart',
    'redirectToItem',
    'addTofavorites',
    'redirectToItemFromNavbar'
  ],
  components: {
    ProductList,
    MyNavbar,
    Footer
  },
  data() {
    return {
      range: [1, 10000],
      isChecked: this.$store.state.isDiscountedChecked,
      backendEndpoint: `${config.backendEndpoint}`,
      currentPage: 1,
      itemsPerPage: 32,
      options: ['32 per page', '64 per page', '100 per page'],
      visiblePageRange: 5,
      isLoading: true,
      appliedFilters: [],
      priceRanges: [
        { value: 'range1', label: 'Under $500' },
        { value: 'range2', label: '$500 - $1000' },
        { value: 'range3', label: '$1000 - $2000' },
        { value: 'range4', label: '$2000 & Above' }
      ]
    }
  },
  watch: {
    filteredProducts() {
      this.updateAppliedFilters()
      if (this.filteredProducts && this.filteredProducts.length > 0) {
        this.isLoading = false
      }
    }
  },
  updated() {
    this.updateAppliedFilters()
  },
  beforeUnmount() {
    this.appliedFilters = []
  },
  mounted() {
    if (this.filteredProducts && this.filteredProducts.length > 0) {
      this.isLoading = false
    }
  },
  created() {
    if (!this.$store.state.accessToken) {
      const accessToken = VueCookies.get('access_token')
      if (accessToken) {
        const user = jwtDecode(accessToken).sub
        const user_id = jwtDecode(accessToken).user_id
        const is_admin = jwtDecode(accessToken).is_admin
        const hasProfile = jwtDecode(accessToken).hasProfile
        this.$store.commit('UPDATE_USER', user)
        this.$store.commit('UPDATE_USER_ID', user_id)
        this.$store.commit('UPDATE_IS_ADMIN', is_admin)
        this.$store.commit('UPDATE_HAS_PROFILE', hasProfile)
      } else {
        this.errorMessage = 'Please Login'
        router.push('/login')
      }
    }
    this.removeAllFilters()
    this.updateAppliedFilters()
    this.$store
      .dispatch('getProducts')
      .then(() => this.$store.dispatch('getProfile'))
      .then(() => this.$store.dispatch('fetchCategories'))
      .then(() => this.$store.dispatch('checkFavoritesOnLoad'))
      .then(() => this.$store.dispatch('updateHomeProductRange'))
      .catch(error => {
        if (error.message !== 'Token Expired') {
          // console.error('error', error)
        }
      })
    if (this.filteredProducts && this.filteredProducts.length > 0) {
      this.isLoading = false
    }
    this.$watch(
      () => [this.$store.state.productMin, this.$store.state.productMax],
      () => {
        this.updateRangeFromStore()
      }
    )
    this.updateRangeFromStore()
  },
  computed: {
    isPriceRangesSelected() {
      return this.$store.state.selectedPriceRanges.length > 0
    },
    selectedPriceRanges() {
      return this.$store.state.selectedPriceRanges
    },
    paginatedProducts() {
      const products = this.$store.getters.filteredProducts
      const itemsPerPage = this.itemsPerPage
      const startIdx = (this.currentPage - 1) * itemsPerPage
      const endIdx = startIdx + itemsPerPage

      const paginatedAndFilteredProducts = products
        .slice(startIdx, endIdx)
        .filter(item => {
          const categoryCondition =
            this.$store.state.selectedCategories.length === 0 ||
            this.$store.state.selectedCategories.includes(
              String(item.category_id)
            )
          const priceCondition =
            item.price >= this.$store.getters.min &&
            item.price <= this.$store.state.max
          const ratingCondition =
            this.$store.state.selectedRating.length === 0 ||
            this.$store.state.selectedRating.includes(
              Math.round(item.rating_float)
            )
          const discountCondition =
            !this.$store.state.isDiscountedChecked || item.discount != null

          return (
            categoryCondition &&
            priceCondition &&
            ratingCondition &&
            discountCondition
          )
        })
      this.scrollToTop()
      return paginatedAndFilteredProducts
    },
    totalPages() {
      const filteredProducts = this.$store.getters.filteredProducts
      const itemsPerPage = this.itemsPerPage
      const filteredAndPaginatedProducts = filteredProducts.filter(item => {
        const categoryCondition =
          this.$store.state.selectedCategories.length === 0 ||
          this.$store.state.selectedCategories.includes(
            String(item.category_id)
          )

        const priceCondition =
          item.price >= this.$store.getters.min &&
          item.price <= this.$store.state.max

        const ratingCondition =
          this.$store.state.selectedRating.length === 0 ||
          this.$store.state.selectedRating.includes(
            Math.round(item.rating_float)
          )

        const discountCondition =
          !this.$store.state.isDiscountedChecked || item.discount != null

        return (
          categoryCondition &&
          priceCondition &&
          ratingCondition &&
          discountCondition
        )
      })
      const totalPages = Math.ceil(
        filteredAndPaginatedProducts.length / itemsPerPage
      )
      return totalPages
    },
    visiblePages() {
      const start = Math.max(1, this.currentPage - this.visiblePageRange)
      const end = Math.min(this.totalPages, start + this.visiblePageRange * 2)
      const pages = []
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
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
    is_admin() {
      return this.$store.state.is_admin
    },
    profile() {
      return this.$store.state.profile
    },
    categories() {
      return this.$store.getters.categories
    },
    sortOrder() {
      return this.$store.getters.sortOrder
    }
  },
  methods: {
    debouncedUpdateSliderRange: debounce(function () {
      let [minVal, maxVal] = this.range
      if (maxVal - minVal < 100) {
        minVal = Math.max(
          minVal - Math.ceil((100 - (maxVal - minVal)) / 2),
          this.productMin
        )
        maxVal = Math.min(
          maxVal + Math.ceil((100 - (maxVal - minVal)) / 2),
          this.productMax
        )
        return
      }
      this.$store.commit('SET_MIN_PRICE', minVal)
      this.$store.commit('SET_MAX_PRICE', maxVal)
    }, 500),
    updateRangeFromStore() {
      this.range = [this.$store.state.productMin, this.$store.state.productMax]
    },
    updateSliderRange() {
      this.debouncedUpdateSliderRange()
    },
    isActiveLink(link) {
      return this.$route.name === link || !this.$route.name
    },
    isActiveCategory(category) {
      return (
        this.$route.name === 'category' &&
        this.$route.params.category === category
      )
    },
    setCurrentPage(page) {
      this.currentPage = page
      window.scrollTo({ top: 0, left: 0 })
    },
    goHome() {
      this.$router.push({ name: 'NewHome' })
    },
    goToAllProducts() {
      this.$router.push({ name: 'home' })
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
    changeItemsPerPage(event) {
      this.itemsPerPage = parseInt(event.target.value)
      this.setCurrentPage(1)
    },
    removeAllFilters() {
      this.appliedFilters = []
      const checkboxes = document.querySelectorAll('input[type="checkbox"]')
      checkboxes.forEach(checkbox => {
        checkbox.checked = false
      })
      const prices = this.$store.state.products.map(product => product.price)
      const minPrice = Math.floor(Math.min(...prices))
      const maxPrice = Math.ceil(Math.max(...prices))
      this.$store.commit('SET_MIN_PRICE', minPrice)
      this.$store.commit('SET_MAX_PRICE', maxPrice)
      this.selectedRating = []
      this.isChecked = false
      this.handleCategoryChange()
      this.handlePriceRangeChange()
      this.handleDiscountChange()
      this.updateRangeFromStore()
    },
    removeFilter(filter) {
      if (filter === 'Discounts %') {
        this.isChecked = false
        this.handleDiscountChange()
        return
      } else if (filter.startsWith('Rating')) {
        const rating = Number(filter.split(': ')[1])
        const index = this.selectedRating.findIndex(item => item === rating)
        if (index !== -1) {
          this.selectedRating.splice(index, 1)
        }
        return
      } else if (
        filter.includes('-') ||
        filter.startsWith('Under') ||
        filter.includes('&')
      ) {
        const checkbox = document.querySelector(
          `input[data-price-label="${filter}"]`
        )
        if (checkbox) {
          checkbox.checked = false
          this.handlePriceRangeChange()
          this.range = [this.$store.state.min, this.$store.state.max]
        } else {
          const prices = this.$store.state.products.map(
            product => product.price
          )
          const minPrice = Math.floor(Math.min(...prices))
          const maxPrice = Math.ceil(Math.max(...prices))
          this.$store.commit('SET_MIN_PRICE', minPrice)
          this.$store.commit('SET_MAX_PRICE', maxPrice)
          this.range = [this.$store.state.min, this.$store.state.max]
        }
        return
      } else if (
        ['Laptops', 'Smartwatches', 'TV', 'Smartphones', 'Tablets'].includes(
          filter
        )
      ) {
        const checkbox = document.querySelector(
          `input[data-category-name="${filter}"]`
        )
        if (checkbox) {
          checkbox.checked = false
          this.handleCategoryChange()
        }
      }
    },
    updateAppliedFilters() {
      const filters = []
      const priceRanges = this.$store.state.selectedPriceRanges
        .map(range => {
          switch (range) {
            case 'range1':
              return 'Under $500'
            case 'range2':
              return '$500 - $1000'
            case 'range3':
              return '$1000 - $2000'
            case 'range4':
              return '$2000 & Above'
            default:
              return null
          }
        })
        .filter(range => range !== null)

      if (priceRanges.length > 0) {
        const prices = this.$store.state.products.map(product => product.price)
        this.$store.state.productMin = Math.floor(Math.min(...prices))
        this.$store.state.productMax = Math.ceil(Math.max(...prices))
        this.$store.state.min = Math.floor(Math.min(...prices))
        this.$store.state.max = Math.ceil(Math.max(...prices))
        filters.push(...priceRanges)
      } else {
        filters.push(`$${this.$store.state.min} - $${this.$store.state.max}`)
      }
      const selectedCategories = this.$store.state.selectedCategories.map(
        categoryId => {
          return this.getCategoryLabel(categoryId)
        }
      )
      selectedCategories.forEach(category => {
        filters.push(category)
      })
      if (this.isChecked) {
        filters.push('Discounts %')
      }
      if (this.$store.state.selectedRating.length > 0) {
        const selectedRatings = this.$store.state.selectedRating.map(rating => {
          return `Rating: ${rating}`
        })
        filters.push(...selectedRatings)
      }
      const newFilters = JSON.stringify(filters)
      if (newFilters !== JSON.stringify(this.appliedFilters)) {
        this.appliedFilters = filters
      }
      if (this.currentPage > this.totalPages) {
        this.currentPage = 1
      }
    },
    getCategoryLabel(categoryId) {
      categoryId = parseInt(categoryId)
      const category = this.categories.find(cat => cat[2] === categoryId)
      return category ? category[0] : ''
    },
    getProductCount(rangeValue) {
      return this.products.filter(product => {
        switch (rangeValue) {
          case 'range1':
            return product.price <= 500
          case 'range2':
            return product.price > 500 && product.price <= 1000
          case 'range3':
            return product.price > 1000 && product.price <= 2000
          case 'range4':
            return product.price > 2000
        }
      }).length
    },
    async handlePriceRangeChange() {
      const selectedPriceRanges = await this.$store.dispatch(
        'getSelectedPriceRanges'
      )
      this.$store.commit('UPDATE_SELECTED_PRICE_RANGES', selectedPriceRanges)
      this.currentPage = 1
    },
    updateProductRange() {
      const prices = this.$store.state.products.map(product => product.price)
      this.$store.state.productMin = Math.ceil(Math.min(...prices))
      this.$store.state.productMax = Math.ceil(Math.max(...prices))
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
      this.currentPage = 1
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
      const items = this.$store.state.products // Assuming products are stored in the store
      const count = items.reduce((accumulator, item) => {
        const floatRating = parseFloat(item.rating_float)
        const roundedRating = Math.floor(floatRating + 0.5) // Round to the nearest integer
        if (roundedRating === rating) {
          return accumulator + 1
        }
        return accumulator
      }, 0)
      return count
    },
    handlePaginationInput() {
      this.scrollToTop()
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
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
#newsletter {
  display: flex;
  width: 200px;
  height: 50px;
  margin-top: 4%;
  margin-left: 30%;
  margin-bottom: 0;
  padding: 0;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  background-repeat: no-repeat;
  background-color: #ffffff;
  color: blue;
}

.custom-btn {
  background-color: #fdfeff;
  font-size: 12.5px;
  color: rgb(10, 0, 0);
  max-width: 220px;
  height: 35px;
  border-radius: 5px;
  border: 1px solid #cfcdcd;
  border-bottom: 2px solid darkred;
}
.remove-filter-btn {
  margin-bottom: 0;
  margin-top: 10px;
  border-bottom: 2px solid darkred;
}

.remove-filter-btn:hover {
  background-color: #ebeff2;
  border: 1px solid #cfcdcd;
  border-bottom: 2px solid darkred;
}
.remove-icon {
  margin-left: 5px;
  vertical-align: middle;
  color: darkred;
}

.remove-filter-btn .remove-icon {
  opacity: 0.8;
  transition: opacity 0.3s ease-in-out;
}

.remove-filter-btn:hover .remove-icon {
  opacity: 1;
  border-bottom: 2px solid darkred;
}
.arrow {
  font-size: 1.2em;
}
.nav-text {
  font-size: 0.7em;
  letter-spacing: 0.3em;
}
</style>
