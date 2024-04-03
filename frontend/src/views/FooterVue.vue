<template>
  <div>
    <v-btn
      @click="goToTop"
      prepend-icon="mdi-arrow-up-bold-outline"
      variant="elevated"
      color="outlined"
      width="100%"
      style="
        margin-top: 2%;
        color: white !important;
        background-color: #6c757d !important;
        text-align: center !important;
        cursor: pointer !important;
        margin-top: 2%;
        width: 100%;
        height: 40px;
        margin-left: 0;
      "
      >Back to Top</v-btn
    >
    <section id="newsletter" class="section-p1" style="margin-top: 1%">
      <div class="newstext">
        <h4 style="margin-top: 15px">Sign Up for Newsletters</h4>
        <p>Get Email updates about our latest shop and special offers.</p>
      </div>
      <div class="form" style="margin-top: 15px">
        <input type="text" placeholder="Your email address" />
        <button class="btn normal">Sign Up</button>
      </div>
    </section>

    <footer class="section-p1">
      <div class="col">
        <a href="#">
          <img
            class="logo"
            :src="require('@/assets/eshop-logo-png.png')"
            style="
              width: 100%;
              height: 50px;
              margin-bottom: 0;
              margin-top: 0;
              padding: 0;
            "
        /></a>
        <h4>Contact</h4>
        <p><strong>Phone:</strong>+123456789, +987654321</p>
        <p><strong>Hours:</strong>10.00 - 18.00, Mon - Sat</p>
        <div class="follow">
          <h4>Follow Us</h4>
          <div class="icon">
            <i class="fab fa-facebook-f"></i>
            <i class="fab fa-instagram"></i>
            <i class="fab fa-twitter"></i>
            <i class="fab fa-youtube"></i>
            <i class="fab fa-pinterest-p"></i>
          </div>
        </div>
      </div>

      <div class="sec">
        <div class="col">
          <h4>About</h4>
          <a href="#">About Us</a>
          <a href="#">Delivery Information</a>
          <a href="#">Privacy Policy</a>
          <a href="#">Terms and Condition</a>
          <a href="#">Contact Us</a>
        </div>

        <div class="col">
          <h4>My Account</h4>
          <a href="#">View Cart</a>
          <a href="#">My Account</a>
          <a href="#">My Wishlist</a>
          <a href="#">Track my Order</a>
          <a href="#">Help</a>
        </div>

        <div class="col install">
          <h4>Install App</h4>
          <p>From App Store or Google Play</p>

          <div class="row"></div>
          <p>Secured Payment Gateways</p>
        </div>
      </div>

      <div class="coypright">
        <p>© 2024 All rights reserved!</p>
      </div>
    </footer>
  </div>
</template>
<script>
export default {
  props: ['cart', 'avatar', 'profile', 'favorites'],
  methods: {
    goToAllProducts() {
      this.$router.push({ name: 'home' })
      this.$nextTick(() => {
        window.scrollTo({ top: 0, behavior: 'auto' })
      })
    },
    goToTop() {
      window.scrollTo({ top: 0, behavior: 'auto' })
    }
  }
}
</script>
