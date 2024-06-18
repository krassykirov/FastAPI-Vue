<template>
  <!-- prettier-ignore -->
  <div
    class="container-fluid"
    style="width: 100vw; position: sticky; margin: 0; padding: 0;"
  >
    <MyNavbar
      :cart="cart"
      :favorites="favorites"
      :total="total"
      :user="user"
      :user_id="user_id"
      :scopes="scopes"
      :profile="profile"
    />
    <div class="container" style="margin-top: 0.7%; margin-left: 7.3%; background-color: #f2f6f6" >
      <CarouselMain carouselId="discount-products-carousel" />
    </div>
    <!-- prettier-ignore -->
    <v-container fluid style="width: 90%; position: sticky; background-color: #f2f6f6; margin-left: 5%; margin-right: 15%">
      <v-row dense>
        <v-col
          v-for="(card, index) in cards"
          :key="card.title"
          :cols="index < 2 ? card.flex * 2 : card.flex"
          @click="goToCategory(card.title)"
        >
          <v-card :width="card.width" :height="card.height" elevation="15" rounded="lg">
            <v-img
              :src="card.src"
              :aspect-ratio="card.aspectratio"
              class="align-end"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              cover
              style="cursor: pointer; object-fit: cover !important"
            >
              <v-card-title class="text-white" v-text="card.title"></v-card-title>
            </v-img>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="surface-variant" icon="mdi-heart" size="small" variant="text"></v-btn>
              <v-btn color="surface-variant" icon="mdi-bookmark" size="small" variant="text"></v-btn>
              <v-btn color="surface-variant" icon="mdi-share-variant" size="small" variant="text"></v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <div
      class="container-fluid"
      style="margin: 0 !important; margin-left: 10% !important; background-color: #f2f6f6"
    >
      <MessageArea />
    </div>
    <Footer />
  </div>
</template>

<script>
import router from '@/router'
import VueCookies from 'vue-cookies'
import { jwtDecode } from 'jwt-decode'
import MyNavbar from '@/components/MyNavbar.vue'
import CarouselMain from '@/views/CarouselMainNew.vue'
import MessageArea from '@/views/MessageAreaVue.vue'
import Footer from '@/views/FooterVue.vue'
// /* global bootstrap */
export default {
  name: 'NewHome',
  components: {
    MyNavbar,
    CarouselMain,
    MessageArea,
    Footer
  },
  data() {
    return {
      hover: false,
      cards: [
        {
          title: 'Laptops',
          src: require('@/assets/laptop-banner.jpeg'),
          width: '819px',
          height: '448px',
          aspectratio: '16/9'
        },
        {
          title: 'Smartphones',
          src: require('@/assets/smartphone-banner.png'),
          width: '819px',
          height: '448px',
          aspectratio: '16/9'
        },
        {
          title: 'Tablets',
          src: require('@/assets/ipad.jpeg'),
          width: '540px',
          height: '295px',
          aspectratio: '16/9'
        },
        {
          title: 'Smartwatches',
          src: require('@/assets/smart-watch-banner.jpg'),
          width: '540px',
          height: '295px',
          aspectratio: '19/10'
        },
        {
          title: 'TV',
          src: require('@/assets/tv-banner.webp'),
          width: '540px',
          height: '295px',
          aspectratio: '16/9'
        }
      ]
    }
  },
  created() {
    const urlParams = new URLSearchParams(window.location.search)
    const token = urlParams.get('token')
    const refresh_token = urlParams.get('refresh_token')
    if (!this.$store.state.accessToken) {
      const accessToken = VueCookies.get('access_token')
      if (accessToken) {
        const user = jwtDecode(accessToken).sub
        const user_id = jwtDecode(accessToken).user_id
        const hasProfile = jwtDecode(accessToken).hasProfile
        const scopes = jwtDecode(accessToken).scopes
        this.$store.commit('UPDATE_USER', user)
        this.$store.commit('UPDATE_USER_ID', user_id)
        this.$store.commit('UPDATE_HAS_PROFILE', hasProfile)
        this.$store.commit('UPDATE_SCOPES', scopes)
      } else if (token !== null && refresh_token !== null) {
        const decodedToken = jwtDecode(token)
        const expires_in = decodedToken.exp
        const user = decodedToken.sub
        const user_id = decodedToken.user_id
        const hasProfile = decodedToken.hasProfile
        const scopes = decodedToken.scopes
        this.lastActiveDate = new Date()
        this.inactiveTime = 0
        const expiresInMinutes = Math.max(
          0,
          Math.floor((expires_in - Math.floor(Date.now() / 1000)) / 60)
        )
        VueCookies.set('access_token', token, {
          expires: new Date(Date.now() + expiresInMinutes * 60 * 1000)
        })
        const refresh_token_expires_in = jwtDecode(refresh_token).exp
        const expiresInMinutesrefreshToken = Math.max(
          0,
          Math.floor(
            (refresh_token_expires_in - Math.floor(Date.now() / 1000)) / 60
          )
        )
        VueCookies.set('refresh_token', refresh_token, {
          expires: new Date(
            Date.now() + expiresInMinutesrefreshToken * 60 * 1000
          )
        })
        this.$store.commit('UPDATE_USER', user)
        this.$store.commit('UPDATE_USER_ID', user_id)
        this.$store.commit('UPDATE_HAS_PROFILE', hasProfile)
        this.$store.commit('UPDATE_SCOPES', scopes)
        console.log('scopes', scopes)
        this.$store.commit('setAccessToken', token)
        this.$store.commit('setRefreshToken', refresh_token)
        router.push({ name: 'NewHome' })
      } else {
        this.$store.dispatch('setErrorMessage', 'Session expired')
        router.push('/login')
      }
    }
    this.$store
      .dispatch('getProducts')
      .then(() => this.$store.dispatch('getProfile'))
      .then(() => this.$store.dispatch('fetchCategories'))
      .catch(error => {
        if (error.message !== 'Token Expired') {
          console.error('error', error)
        }
      })
  },
  methods: {
    goToCategory(category) {
      this.$router.push({ name: 'category', params: { category: category } })
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: 'auto' })
      })
    },
    goToAllProducts() {
      this.$router.push({ name: 'home' })
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: 'auto' })
      })
    },
    goToItem(itemId) {
      this.$router.push({ name: 'Item', params: { itemId } })
    },
    goToTop() {
      window.scrollTo({ top: 0, behavior: 'auto' })
    }
  },
  computed: {
    groupedProducts() {
      const itemsPerSlide = 6
      const products = this.discountedProducts
      const grouped = []
      if (products.length <= itemsPerSlide) {
        grouped.push(products)
        return grouped
      }
      for (let i = 0; i < products.length; i += itemsPerSlide) {
        const group = products.slice(i, i + itemsPerSlide)
        if (
          i + itemsPerSlide >= products.length &&
          group.length < itemsPerSlide
        ) {
          const remainingItems = itemsPerSlide - group.length
          const nextGroup = products.slice(0, remainingItems)
          group.push(...nextGroup)
        }
        grouped.push(group)
      }
      return grouped
    },
    discountedProducts() {
      return this.$store.getters.filteredProducts.filter(
        product => product.discount > 0
      )
    },
    products() {
      return this.$store.getters.products
    },
    filteredProducts() {
      return this.$store.getters.filteredProducts
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
    scopes() {
      return this.$store.state.scopes
    },
    profile() {
      return this.$store.state.profile
    },
    categories() {
      return this.$store.getters.categories
    }
  }
}
</script>
