<template>
  <!-- prettier-ignore -->
  <v-toolbar>
  <v-btn @click="goHome" style="font-size: 1.2rem; margin-top: 5px">
    <v-icon left>mdi-home-outline</v-icon>
  </v-btn>
  <div class="text-center" style="padding-left: 5%">
    <v-menu open-on-hover>
      <template v-slot:activator="{ props }">
        <v-btn elevation="0" v-bind="props" width="200px" height="30px">
          <v-icon start>mdi-menu</v-icon>
          CATEGORIES
        </v-btn>
      </template>
      <v-list width="200px" style="margin-top: 3px">
        <v-list-item
          v-for="(category, index) in categories"
          :key="index"
          @click="selectCategory(category[0])"
          :prepend-icon="getCategoryIcon(category[0])"
        >
          <v-list-item-title class="category-item">{{
            category[0]
          }}</v-list-item-title>
        </v-list-item>
        <!-- prettier-ignore -->
        <v-list-item prepend-icon="mdi mdi-devices" style="cursor: pointer" @click="goToAllProducts">
              <v-list-item-title class="category-item">
                All Products
              </v-list-item-title>
            </v-list-item>
      </v-list>
    </v-menu>
  </div>
  <form
    class="form-inline"
    @submit.prevent="search"
    style="padding-left: 10%"
  >
    <div class="input-group" style="width: 700px; margin-top: 20px">
      <input
        class="form-control"
        type="search"
        id="filter"
        placeholder="Search by Keyword"
        aria-label="Search"
        v-model="searchQuery"
        required
      />
      <div class="input-group-append">
        <button type="submit" class="btn btn-outline-success">
          <i class="fas fa-search"></i>
        </button>
        <!-- <button class="btn btn-outline-danger" @submit.prevent="clearSearch">
          <i class="fas fa-times"></i>
        </button> -->
      </div>
    </div>
  </form>
  <div class="text-center" style="margin-left: 2%">
    <v-menu open-on-hover v-model="favoritesVisible" :close-on-content-click="false">
      <template v-slot:activator="{ props }">
        <v-btn
          v-if="cart && accessToken"
          v-bind="props"
          @dblclick="redirectToFavorites"
        >
          <i class="fa fa-heart-o" style="font-size: 1rem"></i>
          FAVORITES
          <span class="badge text-bg-danger rounded-pill">{{ favorites.length }}</span>
        </v-btn>
      </template>
      <div v-if="favorites && favorites.length > 0" class="d-flex justify-center" style="margin-left: -50px; margin-top: 10px" @mouseleave="handleFavoritestMenuLeave">
        <v-list width="290px" style="padding: 0; margin: 0; max-height: 350px; overflow-y: auto">
          <v-card v-for="(item, index) in favorites" :key="index" width="x-small" class="mx-2 my-2">
            <v-row no-gutters align="center" style="height: 75px">
              <v-col cols="3">
                <v-img :src="`${backendEndpoint}/static/img/${item.name}/${item.image}`" width="40" height="40" style="margin-left: 5px"/>
              </v-col>
              <v-col cols="7" @click="redirectToItemFromNavbar(item.id)" style="cursor: pointer">
                <div style="font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ truncateDescription(item.name, 40) }}</div>
                <div style="font-size: 0.7rem; margin-top: 4px;">${{ item.discount_price ? formattedPrice(item.discount_price).integerPart : '' }}
                <span v-if="item.discount_price" style="font-size: 0.7rem;">.{{ formattedPrice(item.discount_price).decimalPart }}</span></div>
              </v-col>
              <v-col cols="2" class="text-right">
                <v-btn @click="removeFromFavorites(item.id)" icon size="x-small" color="red">
                  <v-icon size="x-small">mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
          <v-btn @click="redirectToFavorites" size="small" width="290" color="#029cf5"
          style="margin-top: -9px">
            Go to Favorites
          </v-btn>
        </v-list>
      </div>
    </v-menu>
  </div>
  <div class="text-center" style="margin-left: 3%">
    <v-menu open-on-hover v-model="cartVisible" :close-on-content-click="false">
      <template v-slot:activator="{ props }">
        <v-btn
          v-if="cart && accessToken"
          v-bind="props"
          @dblclick="redirectToCart"
        >
          <v-icon right>mdi-cart-outline</v-icon>
          CART
          <span class="badge text-bg-primary rounded-pill">{{ cart.length }}</span>
        </v-btn>
      </template>
      <div v-if="cart && cart.length > 0" class="d-flex justify-center" style="margin-left: -70px; margin-top: 10px" @mouseleave="handleCartMenuLeave">
        <v-list width="280px" style="padding: 0; margin: 0; max-height: 350px; overflow-y: auto">
          <v-card v-for="(item, index) in cart" :key="index" width="x-small" class="mx-2 my-2">
            <v-row no-gutters align="center" style="height: 75px">
              <v-col cols="3">
                <v-img :src="`${backendEndpoint}/static/img/${item.name}/${item.image}`" width="40" height="40" style="margin-left: 5px"/>
              </v-col>
              <v-col cols="7" @click="redirectToItemFromNavbar(item.id)" style="cursor: pointer">
                <div style="font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ truncateDescription(item.name, 40) }}</div>
                <div style="font-size: 0.7rem; margin-top: 4px;">${{ item.discount_price ? formattedPrice(item.discount_price).integerPart : '' }}
                <span v-if="item.discount_price" style="font-size: 0.7rem;">.{{ formattedPrice(item.discount_price).decimalPart }}</span></div>
              </v-col>
              <v-col cols="2" class="text-right">
                <v-btn @click="removeFromCart(item.id)" icon size="x-small" color="red">
                  <v-icon size="x-small">mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
          <v-btn @click="redirectToCart" size="small" width="290" color="#029cf5"
          style="margin-top: -9px">
            Go to Cart
          </v-btn>
        </v-list>
      </div>
    </v-menu>
  </div>
  <div class="text-center" style="margin-left: 3%">
    <v-menu open-on-hover>
      <template v-slot:activator="{ props }">
        <v-list-item>
        <v-avatar v-bind="props">
          <v-img
            v-if="profile"
            :src="`${backendEndpoint}/static/img/${profile.primary_email}/profile/${profile.avatar}`"
            style="cursor: pointer"
          ></v-img>
          <v-img
            v-else
            :src="require('@/assets/img_avatar.png')"
            style="cursor: pointer"
          ></v-img>
        </v-avatar>
        <v-icon class="dropdown-icon" v-bind="props">mdi-menu-down</v-icon>
      </v-list-item>
      </template>
      <div class="d-flex justify-center" style="margin-left: -50px; margin-top: 10px">
      <v-list density="compact" nav class="profile-list" width="160px">
        <v-list-item
          prepend-icon="mdi-account"
          style="margin: 0; padding: 0"
          :subtitle="user"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-account"
          style="margin: 0; padding: 0"
          title="My Account"
          value="account"
          :to="{ name: 'Profile' }"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-logout"
          style="margin: 0; padding: 0"
          title="Logout"
          value="logout"
          @click="logout"
        ></v-list-item>
        <a
          class="dropdown-item"
          v-if="user === 'krassy@mail.bg'"
          data-toggle="modal"
          data-target="#addItem"
          href="#"
          style="font-family: inherit; margin-top: 14%"
        >
          Add Product
        </a>
        <a
          class="dropdown-item"
          v-if="user === 'krassy@mail.bg'"
          data-toggle="modal"
          data-target="#patchItem"
          href="#"
          style="font-family: inherit; margin-top: 14%"
        >
          Update Product
        </a>
      </v-list>
    </div>
    </v-menu>
  </div>
</v-toolbar>
  <div
    class="modal fade"
    id="patchItem"
    role="dialog"
    aria-labelledby="updateItemLabel"
    aria-hidden="true"
    data-backdrop="false"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="updateItemLabel">Update Product</h5>
        </div>
        <div class="modal-body">
          <form
            enctype="multipart/form-data"
            data-toggle="validator"
            id="updateItem"
            @submit.prevent="updateItem"
          >
            <div class="form-group">
              <label for="itemID" class="col-form-label">Item ID: </label>
              <input
                type="number"
                name="itemID"
                id="itemID"
                placeholder="itemID"
                required
              />
            </div>
            <div class="form-group" form-group-file>
              <label for="file" class="col-form-label">Upload Photo:</label>
              <input
                type="file"
                id="file"
                name="file"
                class="form-control"
                data-filesize="1000000"
                data-filesize-error="File must be smaller then 1MB"
                accept="image/*"
              />
            </div>
            <div class="form-group" form-group-file>
              <label for="files" class="col-form-label">Upload Photos:</label>
              <input
                type="file"
                id="files"
                name="files"
                class="form-control"
                data-filesize="1000000"
                data-filesize-error="File must be smaller than 1MB"
                accept="image/*"
                multiple
              />
            </div>
            <div class="form-group">
              <label for="price" class="col-form-label">Price: </label>
              <input
                type="number"
                step="any"
                name="price"
                id="item-price"
                placeholder="99.99"
                max="10000"
                min="1"
              />
            </div>
            <div class="form-group">
              <label for="description" class="col-form-label"
                >Description:</label
              >
              <textarea
                name="description"
                id="add-description"
                rows="4"
                cols="50"
                maxlength="250"
              ></textarea>
            </div>
            <div class="form-group">
              <label for="Category" class="col-form-label">Category:</label>
              <select name="Category">
                <option value="Laptops">Laptops</option>
                <option value="Smartphones">Smartphones</option>
                <option value="Tablets">Tablets</option>
                <option value="Smartwatches">Smart Watches</option>
                <option value="TV">TV</option>
              </select>
            </div>
            <div class="form-group">
              <label for="discount" class="col-form-label">Discount: </label>
              <input
                type="number"
                step="0.01"
                name="discount"
                id="discount-price"
                placeholder="0.8"
                max="0.95"
                min="0.01"
              />
            </div>
            <div class="form-group">
              <label for="brand" class="col-form-label">Brand: </label>
              <input type="text" name="brand" id="brand" placeholder="ASUS" />
            </div>
            <button id="update-button" class="btn btn-primary">Save</button>
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
              id="close-modal"
            >
              Close
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="addItem"
    role="dialog"
    aria-labelledby="addItemlLabel"
    aria-hidden="true"
    data-backdrop="false"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addItemLabel">Add Product</h5>
        </div>
        <div class="modal-body">
          <form
            enctype="multipart/form-data"
            data-toggle="validator"
            id="createItem"
            @submit.prevent="createItem"
          >
            <p id="error" style="text-align: left"></p>
            <div class="form-group">
              <label for="name" class="col-form-label">Name:</label>
              <input
                type="text"
                name="name"
                id="item-name"
                placeholder="Item Name"
                maxlength="55"
                required
              />
            </div>
            <div class="form-group">
              <label for="price" class="col-form-label">Price: </label>
              <input
                type="number"
                step="any"
                name="price"
                id="item-price"
                placeholder="99.99"
                max="10000"
                min="1"
                required
              />
            </div>
            <div class="form-group">
              <label for="discount" class="col-form-label">Discount: </label>
              <input
                type="number"
                step="0.01"
                name="discount"
                id="discount-price"
                placeholder="0.8"
                max="0.95"
                min="0.01"
              />
            </div>
            <div class="form-group">
              <label for="brand" class="col-form-label">Brand: </label>
              <input type="text" name="brand" id="brand" placeholder="ASUS" />
            </div>
            <div class="form-group" form-group-file>
              <label for="file" class="col-form-label">Upload Photo:</label>
              <input
                type="file"
                id="file"
                name="file"
                class="form-control"
                data-filesize="1000000"
                data-filesize-error="File must be smaller then 1MB"
                accept="image/*"
                required
              />
            </div>
            <div class="form-group" form-group-file>
              <label for="files" class="col-form-label">Upload Photos:</label>
              <input
                type="file"
                id="files"
                name="files"
                class="form-control"
                data-filesize="1000000"
                data-filesize-error="File must be smaller than 1MB"
                accept="image/*"
                required
                multiple
              />
            </div>
            <div class="form-group">
              <label for="Category" class="col-form-label">Category:</label>
              <select name="Category">
                <option value="Laptops">Laptops</option>
                <option value="Smartphones">Smartphones</option>
                <option value="Tablets">Tablets</option>
                <option value="Smartwatches">Smart Watches</option>
                <option value="TV">TV</option>
              </select>
            </div>
            <div class="form-group">
              <label for="description" class="col-form-label"
                >Description:</label
              >
              <textarea
                name="description"
                id="add-description"
                rows="4"
                cols="50"
                maxlength="250"
              ></textarea>
            </div>
            <button
              id="submit-button"
              class="btn btn-primary"
              @click="hideModal"
            >
              Save
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
              id="close-modal"
            >
              Close
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import axios from 'axios'
import VueCookies from 'vue-cookies'
import config from '@/config'
import router from '@/router'

export default {
  props: ['cart', 'avatar', 'profile', 'favorites', 'total', 'user', 'user_id'],
  emits: [
    'addToCart',
    'redirectToItem',
    'addTofavorites',
    'removeFromCart',
    'redirectToItemFromNavbar'
  ],
  data() {
    return {
      drawerVisible: false,
      displayCart: true,
      displayLiked: true,
      displayCategories: true,
      isDropdownVisible: false,
      backendEndpoint: `${config.backendEndpoint}`,
      searchQuery: '',
      categoryName: null,
      favoritesVisible: false,
      cartVisible: false
    }
  },
  computed: {
    formattedPrice() {
      return this.$store.getters.formattedPrice
    },
    errorMessage() {
      return this.$store.getters.errorMessage
    },
    accessToken() {
      return this.$store.getters.accessToken || null
    },
    categories() {
      return this.$store.getters.categories
    }
  },
  methods: {
    getCategoryIcon(categoryName) {
      // Map category names to icons here
      switch (categoryName.toLowerCase()) {
        case 'laptops':
          return 'mdi-laptop'
        case 'smartphones':
          return 'mdi-cellphone'
        case 'tablets':
          return 'mdi-tablet'
        case 'smartwatches':
          return 'mdi-watch'
        case 'tv':
          return 'mdi-television'
        default:
          return ''
      }
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
    formatTotal(price) {
      const [integerPart, decimalPart] = price.toString().split('.')
      return {
        integerPart: parseInt(integerPart).toLocaleString(),
        decimalPart: decimalPart || '00'
      }
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
    async search() {
      if (this.searchQuery.trim() === '' || !this.searchQuery) {
        return
      }
      try {
        const response = await axios.get(
          `${config.backendEndpoint}/api/items/search/`,
          {
            params: {
              q: this.searchQuery
            }
          }
        )
        const products = response.data
        if (products.length > 0) {
          this.$store.commit('SET_SEARCH_RESULTS', products)
          this.$store.state.searchResults.map(product => {
            return this.$store.dispatch('getItemRating', product.id)
          })
          this.$store.dispatch(
            'updateMessage',
            `Found ${products.length} results for ${this.searchQuery}'`
          )
          this.$router.push('/search')
        } else {
          document.getElementById('filter').value =
            `No results found for "${this.searchQuery}"`
          this.$store.dispatch(
            'updateMessage',
            `Found ${products.length} results for '${this.searchQuery}'`
          )
        }
      } catch (error) {
        // console.error('Error fetching items:', error)
      }
    },
    redirectToItemFromNavbar(itemId) {
      this.$router.push({ name: 'Item', params: { itemId } })
    },
    redirectToCart() {
      this.$router.push({ name: 'ItemsInCart' })
    },
    redirectToFavorites() {
      this.$router.push({ name: 'ItemsInFavorites' })
    },
    handleCartMenuLeave() {
      this.cartVisible = false
    },
    handleFavoritestMenuLeave() {
      this.favoritesVisible = false
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId)
      this.cartVisible = true
    },
    addTofavorites(product) {
      this.$store.dispatch('addTofavorites', product)
    },
    removeFromFavorites(itemId) {
      this.$store.dispatch('removeFromFavorites', itemId)
      this.favoritesVisible = true
    },
    logout() {
      this.$store.state.accessToken = null
      this.$store.state.refreshToken = null
      VueCookies.remove('access_token')
      VueCookies.remove('refresh_token')
      this.$store.dispatch('setErrorMessage', 'You have been logged out')
      router.push('/login')
    },
    handleMouseLeave() {
      this.hideCart()
    },
    handleMouseLFavLeave() {
      this.hideFavorites()
    },
    hideCart() {
      setTimeout(() => {
        this.displayCart = true
      }, 300)
    },
    showCart() {
      setTimeout(() => {
        this.displayCart = false
        this.displayLiked = true
      }, 300)
    },
    hideFavorites() {
      setTimeout(() => {
        this.displayLiked = true
      }, 300)
    },
    showFavorites() {
      setTimeout(() => {
        this.displayLiked = false
        this.displayCart = true
      }, 300)
    },
    createItem() {
      const formData = new FormData(document.getElementById('createItem'))
      axios
        .post(`${config.backendEndpoint}/api/items/create_item`, formData, {})
        .then(response => {
          if (response.status === 201) {
            // router.push('/')
            window.location.href = '/'
          }
        })
        .catch(error => {
          if (error.response.status === 403) {
            $('#error').text('Item with that name already exists!')
          }
        })
    },
    updateItem() {
      const formData = new FormData(document.getElementById('updateItem'))
      axios
        .post(`${config.backendEndpoint}/api/items/update_item`, formData, {})
        .then(response => {
          if (response.status === 201) {
            // router.push('/')
            window.location.href = '/'
          }
        })
        .catch(error => {
          if (error.response.status === 403) {
            $('#error').text('Item with that name already exists!')
          }
        })
    },
    hideModal() {
      $(document).ready(function () {
        $('#close-modal').click()
      })
    },
    truncateDescription(description, maxLength) {
      if (description.length > maxLength) {
        return description.substring(0, maxLength) + '..'
      }
      return description
    }
  }
}
</script>
<style scoped>
.category-item {
  font-size: 14px;
  height: 20px;
  padding: 0;
  margin: 0;
}
.profile-list {
  font-size: 14px;
  margin-left: -40px;
  margin-top: 10px;
}
</style>
