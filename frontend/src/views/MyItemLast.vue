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
      :user="user"
      :total="total"
      :favorites="favorites"
      :profile="profile"
    />
    <div class="container my-5">
      <div class="row" style="margin-left: 6%">
        <div class="col-md-5" style="min-height: 550px; max-height: 500px">
          <div
            class="main-img"
            v-if="item && item.images.images"
            :id="'main-image-' + item.id"
          >
            <div v-if="item" class="row my-3 previews" style="margin-left: 4%">
              <div class="row my-9" style="margin-top: 0; padding-top: 0">
                <div class="col-md-9">
                  <MyCarousel :backendEndpoint="backendEndpoint" :item="item" />
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="item && !item.images.images"
            class="main-img"
            style="margin-top: 10%"
          >
            <img
              :src="`${backendEndpoint}/static/img/${item.name}/${item.image}`"
              alt="Image"
              class="img-top"
              style="cursor: pointer"
            />
          </div>
        </div>
        <div class="col-md-7" style="margin-top: 4%; margin-left: -6%">
          <div class="main-description px-2">
            <div class="product-title text-bold my-3" v-if="item">
              {{ truncateName(item.name, 60) }}
            </div>
            <!-- prettier-ignore -->
            <div class="price-area my-4" v-if="item">
              <p class="new-price text-bold mb-1">
                <span style="font-size: 1.2rem;">$</span>
                <span v-if="item.discount_price" style="font-size: 1.2rem;">{{ formatPrice(item.discount_price).integerPart }}</span>
                <span v-if="item.discount_price" style="font-size: 0.7rem; position: relative; top: -0.6em;">{{ formatPrice(item.discount_price).decimalPart }}</span>
              </p>
              <p v-if="item.discount">
                <del style="font-size: 0.9rem">${{ item.price }} </del>
                <span class="text-danger" v-if="item.discount">&nbsp;</span>
              </p>
            </div>
            <p
              style="cursor: pointer; margin-bottom: 1%"
              v-if="item"
              @click="scrollToTarget"
            >
              <span
                v-for="i in 5"
                :key="i"
                :class="getStarClasses(i, item.rating_float)"
              ></span>
              <span
                class="overall-rating"
                style="font-size: 0.9rem !important"
                :id="'overall-rating' + item.id + '-float'"
                >&nbsp;{{ item.rating_float }}</span
              >
              <span :id="'overall-rating' + item.id" style="font-size: 0.9rem">
                ({{ item.reviewNumber }}) Review's
              </span>
            </p>
            <div class="buttons d-flex justify-content-center my-4">
              <div class="block">
                <v-btn
                  @click="addTofavorites(item)"
                  color="primary"
                  variant="outlined"
                  >Add to Favorites</v-btn
                >
              </div>
              <div class="block">
                <v-btn
                  @click="addToCart(item)"
                  ref="addToCartButton"
                  color="primary"
                  variant="outlined"
                >
                  Add to cart
                </v-btn>
              </div>
            </div>
          </div>
          <!-- prettier-ignore -->
          <div class="product-details my-2" v-if="item">
            <p class="details-title text-color mb-1">Product Details</p>
            <!-- prettier-ignore -->
            <div style="max-height: 350px; width: 400px; text-align:left; margin-left: 32%">
              <ul style="width: 400px; list-style-position: outside;">
                <li v-for="(point, index) in item.description.split(',')" :key="index">
                  {{ point.trim() }}
                </li>
              </ul>
            </div>
          </div>
          <div class="delivery my-4">
            <p class="font-weight-bold mb-0">
              <span><i class="fa-solid fa-truck"></i></span>
              <b> Delivery done in 3 days from date of purchase</b>
            </p>
            <p class="text-secondary">Order now to get this product delivery</p>
          </div>
        </div>
      </div>
    </div>
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
    <v-card style="margin-top: 10%">
      <v-tabs v-model="tab" bg-color="primary" align-tabs="center" fixed-tabs>
        <v-tab value="one">Reviews ({{ reviewsData.length }})</v-tab>
        <v-tab value="two">Specification</v-tab>
      </v-tabs>
      <v-card-text>
        <v-window v-model="tab" id="reviews">
          <v-window-item value="one">
            <div v-if="item" style="margin-left: 20%">
              <div
                class="cardgroup1"
                v-for="review in displayedReviews"
                :key="review.id"
                :id="'card' + review.id"
                style="
                  width: 65%;
                  margin-bottom: 5px;
                  border: 1px solid #ccc;
                  padding: 2px;
                  display: flex;
                  justify-content: left;
                "
              >
                <div style="flex: 1; display: flex; align-items: center">
                  <img
                    v-if="review.user_avatar"
                    :src="`${backendEndpoint}/static/img/${review.created_by}/profile/${review.user_avatar}`"
                    width="50"
                    height="50"
                    class="rounded-circle"
                  />
                  <img
                    v-else
                    :src="require('@/assets/img_avatar.png')"
                    width="50"
                    height="50"
                    class="rounded-circle"
                  />
                  <div style="margin-left: 2px">
                    <span>{{ review.created_by }}</span>
                    <br />
                    <span
                      class="fa fa-star"
                      :class="{ checked: star.checked }"
                      :id="star.id"
                      v-for="star in updateStarRatings(review)"
                      :key="star.id"
                    ></span>
                  </div>
                </div>
                <div
                  style="
                    flex: 2;
                    text-align: left;
                    padding: 10px;
                    text-align: left;
                  "
                >
                  <p>{{ review.text }}</p>
                </div>
              </div>
              <div
                class="cardgroup1"
                style="width: 650px; margin-bottom: 2px; margin-left: 10%"
                v-if="!userHasWrittenReview()"
              >
                <div class="row" style="margin-left: 2%; margin-top: 1.5%">
                  <div class="col-12">
                    <div class="rating" style="padding: 10px">
                      <input
                        type="radio"
                        name="rating"
                        value="5"
                        id="5"
                      /><label for="5">☆</label>
                      <input
                        type="radio"
                        name="rating"
                        value="4"
                        id="4"
                      /><label for="4">☆</label>
                      <input
                        type="radio"
                        name="rating"
                        value="3"
                        id="3"
                      /><label for="3">☆</label>
                      <input
                        type="radio"
                        name="rating"
                        value="2"
                        id="2"
                      /><label for="2">☆</label>
                      <input
                        type="radio"
                        name="rating"
                        value="1"
                        id="1"
                      /><label for="1">☆</label>
                    </div>
                    <div class="comment-box ml-2" style="margin-left: 3%">
                      <v-textarea
                        label="Write a Review and select a rating"
                        variant="outlined"
                        ref="commentArea"
                      ></v-textarea>
                      <div class="comment-btns mt-2">
                        <div class="row">
                          <div class="col-6">
                            <div class="pull-left"></div>
                          </div>
                          <v-btn
                            @click="addReview"
                            style="
                              width: 350px;
                              margin-left: 18%;
                              background-color: #efe8e8;
                            "
                            >Submit</v-btn
                          >
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <v-pagination
                v-if="reviewsData.length > 2"
                v-model="currentPage"
                :length="totalPages"
                prev-icon="mdi-chevron-left"
                next-icon="mdi-chevron-right"
                class="pagination"
                style="margin-left: 15%"
                @input="setCurrentPage"
              ></v-pagination></div
          ></v-window-item>
          <v-window-item value="two">
            <div>
              <!-- prettier-ignore -->
              <div v-if="item" style="max-height: 350px; width: 400px; text-align:left; margin-left: 40%">
                <ul style="width: 400px; list-style-position: outside">
                  <li v-for="(point, index) in item.description.split(',')" :key="index">
                    {{ point.trim() }}
                  </li>
                </ul>
              </div>
              <p v-else>No specification available.</p>
            </div>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
    <div
      class="container"
      style="margin-top: 2%; font-size: 2em"
      v-if="item && item.category_id"
    >
      You may also like..
    </div>
    <div
      v-if="item && item.category_id"
      style="
        margin-top: 2%;
        padding: 0;
        margin-left: 10% !important;
        margin-bottom: 1%;
      "
    >
      <Carousel
        :items="getFilteredItems(item.category_id)"
        :backendEndpoint="backendEndpoint"
      />
    </div>
    <Footer />
    <div
      class="toast bg-info"
      id="cartToast2"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      data-bs-autohide="false"
      style="position: fixed; top: 50%; left: 50%; width: 250px; z-index: 1000"
    >
      <div class="d-flex">
        <div
          class="toast-body bg-light"
          id="cartToastBody2"
          style="font-weight: 500; color: grey"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
/* global bootstrap */
import $ from 'jquery'
import MyCarousel from '@/views/CarouselMyItem.vue'
import Carousel from '@/views/CarouselVueNew.vue'
import Footer from '@/views/FooterVue.vue'
import config from '@/config'
import NavBar from '../components/MyNavbar.vue'

export default {
  components: {
    NavBar,
    Footer,
    MyCarousel,
    Carousel
  },
  props: ['cart', 'profile', 'favorites'],
  emits: ['addToCart', 'redirectToItem', 'prev-slide', 'next-slide'],
  data() {
    return {
      tab: null,
      item: this.item,
      itemId: this.itemId,
      selectedImageIndex: 0,
      reviewsData: [],
      activeTab: 'reviews',
      currentPage: 1,
      reviewsPerPage: 2,
      backendEndpoint: `${config.backendEndpoint}`
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.getProduct(to.params.itemId)
    this.setReviewsRating(to.params.itemId)
    this.item
    next()
  },
  created() {
    this.getProduct()
    this.$store.dispatch('fetchCategories')
    this.setReviewsRating(this.itemId)
    this.$store.dispatch('getProfile')
    this.$store.dispatch('getProfiles')
    this.item
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
    errorMessage() {
      return this.$store.state.errorMessage
    },
    user() {
      return this.$store.state.user
    },
    user_id() {
      return this.$store.state.user_id
    },
    total() {
      return this.$store.getters.total
    },
    profiles() {
      return this.$store.state.profiles
    },
    accessToken() {
      return this.$store.state.accessToken
    },
    categories() {
      return this.$store.getters.categories
    },
    totalPages() {
      return Math.ceil(this.reviewsData.length / this.reviewsPerPage)
    },
    pages() {
      return Array.from({ length: this.totalPages }, (_, i) => i + 1)
    },
    displayedReviews() {
      const startIndex = (this.currentPage - 1) * this.reviewsPerPage
      const endIndex = startIndex + this.reviewsPerPage
      return this.reviewsData.slice(startIndex, endIndex)
    }
  },
  methods: {
    getFilteredItems(category_id) {
      switch (category_id) {
        case 1:
          return this.filteredLaptops
        case 2:
          return this.filteredSmartphones
        case 3:
          return this.filteredTablets
        case 4:
          return this.filteredSmartwatches
        case 5:
          return this.filteredTV
      }
    },
    truncateName(name, maxLength) {
      if (!name) return '' // Add this guard clause
      if (name.length > maxLength) {
        const firstLine = name.substring(0, maxLength)
        const remainingChars = name.substring(maxLength)
        const indexOfSpace = remainingChars.indexOf(' ') // Find the index of the next space after maxLength
        if (indexOfSpace !== -1) {
          // If there is a space within the remaining characters, split at that space
          const secondLine = remainingChars.substring(0, indexOfSpace)
          return `${firstLine}\n${secondLine}`
        } else {
          // If there is no space within the remaining characters, just return the truncated first line
          return `${firstLine}..`
        }
      }
      return name
    },
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
    async getProduct(itemId) {
      try {
        const resolvedItemId = itemId || this.$route.params.itemId
        const headers = {
          Authorization: `Bearer ${this.$store.state.accessToken}`,
          Accept: 'application/json'
        }
        const res = await fetch(
          `${config.backendEndpoint}/api/items/item/${resolvedItemId}`,
          { headers: headers }
        )
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`)
        }
        const item = await res.json()
        this.item = item

        this.$nextTick(() => {
          this.getItemRating(item.id)
        })

        this.scrollToTop()
      } catch (error) {
        this.$router.push({ name: 'NotFound' })
      }
    },
    async getItemRating(itemId) {
      try {
        const response = await fetch(
          `${config.backendEndpoint}/api/reviews/item/rating?id=${itemId}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }
        )
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        const data = await response.json()
        this.item.rating = data.rating
        this.item.rating_float = parseFloat(data.rating_float).toFixed(2)
        this.item.reviewNumber = data.review_number
        this.$store.dispatch('updateItemRating', {
          itemId: itemId,
          rating: data
        })
      } catch (error) {
        // console.log('error')
      }
    },
    addToCart(product) {
      this.$store.dispatch('addToCart', product)
    },
    redirectToItem(itemId) {
      this.$store.dispatch('redirectToItem', itemId)
    },
    itemAlreadyInCart(product) {
      return this.cart.some(item => item.id === product.id)
    },
    async setReviewsRating(itemId) {
      try {
        const resolvedItemId = itemId || this.$route.params.itemId
        const response = await fetch(
          `${config.backendEndpoint}/api/reviews?item_id=${resolvedItemId}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              redirect: 'follow'
            }
          }
        )
        if (!response.ok) {
          if (response.status === 404) {
            // console.error(`Item with ID ${resolvedItemId} not found`)
          } else {
            throw new Error(
              `Error: ${response.status} - ${response.statusText}`
            )
          }
        } else {
          const data = await response.json()
          this.reviewsData = data
        }
      } catch (error) {
        // console.error('Error:', error)
      }
    },
    updateStarRatings(review) {
      return Array.from({ length: 5 }, (_, i) => i + 1).map(starIndex => ({
        id: `star${review.id}${starIndex}`,
        checked: starIndex <= review.rating
      }))
    },
    getStarClasses(index, rating) {
      let ratingValue = parseFloat(rating)
      let filledStars = Math.floor(ratingValue)
      if (index <= filledStars) {
        return 'fa fa-star checked'
      } else if (index === filledStars + 1 && rating % 1 !== 0) {
        return 'fa fa-star-half-full checked'
      } else {
        return 'fa fa-star-o checked'
      }
    },
    addReview() {
      const review = this.$refs.commentArea.value
      const rating = document.querySelector('input[name="rating"]:checked')
      if (!review || !rating) {
        const toastContent = 'Review and rating required'
        const toastElement = new bootstrap.Toast(
          document.getElementById('cartToast2'),
          {
            delay: 2000
          }
        )
        const toastBodyElement = document.getElementById('cartToastBody2')
        toastBodyElement.innerText = toastContent
        toastElement.show()
        return
      }
      const id = this.item.id
      const username = this.$store.state.user
      const ratingValue = rating.value || 0
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.$store.state.accessToken}`
        },
        body: JSON.stringify({
          text: review,
          item_id: id,
          rating: ratingValue,
          created_by: username
        })
      }
      fetch(
        `${config.backendEndpoint}/api/reviews/create_review`,
        requestOptions
      )
        .then(response => {
          if (!response.ok) {
            if (response.status === 403) {
              $('#comment-area').val(
                'You can write only one review for this item'
              )
              return Promise.reject('403 Forbidden')
            }
          }
          return response.json()
        })
        .then(data => {
          this.reviewsData.push(data)
          this.getItemRating(id)
          this.setReviewsRating(id)
        })
        .catch(error => {
          throw error
        })
    },
    userHasWrittenReview() {
      return (
        this.reviewsData &&
        this.reviewsData.some(review => review.created_by === this.user)
      )
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    setCurrentPage(page) {
      this.currentPage = page
    },
    scrollToTarget() {
      var targetDiv = document.getElementById('reviews')
      if (targetDiv) {
        targetDiv.scrollIntoView({ behavior: 'auto' })
      }
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'auto' })
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
    },
    getCategoryNameById(categoryId) {
      const categoryIdToName = {
        1: 'Laptops',
        2: 'Smartphones',
        3: 'Tablets',
        4: 'Smartwatches',
        5: 'TV'
      }
      return categoryIdToName[categoryId]
    }
  }
}
</script>
<style scoped>
.text-bold {
  font-weight: 800;
}
/* Main image - left */
.main-img {
  margin-top: 1%;
  padding: 0;
  margin: 0;
  width: 100% !important;
  height: 100% !important;
  max-height: 550px !important;
}
.main-img img {
  max-width: 90% !important;
  width: auto !important;
  height: auto !important;
  max-height: 550px !important;
}
/* Preview images */
.previews img {
  margin-top: 1%;
  width: 100% !important;
  height: auto !important;
  max-height: 200px !important;
}
.main-description .category {
  color: #0093c4;
}

.main-description .product-title {
  padding-top: 1%;
  font-size: 1.3rem;
}

.old-price-discount {
  font-weight: 600;
  font-size: 1rem;
}

.new-price {
  font-size: 1.1rem;
  color: rgb(222, 24, 24);
}

.details-title {
  font-weight: 600;
  font-size: 1.2rem;
  color: #757575;
}

.block {
  margin-right: 5px;
}

.display-5 {
  font-weight: 300;
  line-height: 1;
  font-size: 1.5em;
}

.text-center {
  text-align: center !important;
}

.container.my-5 {
  padding-top: 0 !important;
  margin-top: 0 !important;
  min-width: 1200px !important;
  max-width: 100% !important;
  height: 550px !important;
  width: 100%;
  padding-left: 15px !important;
  padding-right: 15px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

.overall-rating {
  font-size: 1em !important;
  margin-bottom: 2%;
}
.overall-rating2 {
  font-size: 0.9em !important;
  margin-bottom: 2%;
}
.v-btn:hover {
  background-color: #67c0ff;
}
</style>
