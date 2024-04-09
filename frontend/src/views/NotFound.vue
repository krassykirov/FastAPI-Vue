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
      :total="total"
      :user="user"
      :profile="profile"
      :favorites="favorites"
    />
    <div>
      <img
        :src="require('@/assets/404.jpg')"
        style="width: 100%; height: 80%"
      />
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/MyNavbar.vue'

export default {
  components: {
    NavBar
  },
  props: ['cart', 'avatar', 'favorites', 'catchAll', 'profile'],
  name: 'NotFound',
  created() {
    this.$store.dispatch('fetchCategories')
  },
  computed: {
    categories() {
      return this.$store.getters.categories
    }
  }
}
</script>
