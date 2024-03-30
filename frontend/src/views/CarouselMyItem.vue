<template>
  <Carousel
    id="gallery"
    :items-to-show="1"
    :wrap-around="false"
    v-model="currentSlide"
  >
    <Slide v-for="(image, index) in item.images.images" :key="index">
      <div class="carousel__item">
        <img
          :src="`${backendEndpoint}/static/img/${item.name}/${image}`"
          alt="Image"
          class="img-fluid"
        />
      </div>
    </Slide>
  </Carousel>

  <Carousel
    id="thumbnails"
    :items-to-show="4"
    :wrap-around="true"
    v-model="currentSlide"
    ref="carousel"
  >
    <Slide v-for="(image, index) in item.images.images" :key="index">
      <div class="carousel__item" @click="slideTo(index)">
        <img
          :src="`${backendEndpoint}/static/img/${item.name}/${image}`"
          alt="Image"
          class="img-thumbnail"
          style="cursor: pointer"
        />
      </div>
    </Slide>
    <template #addons>
      <Navigation />
    </template>
  </Carousel>
  <div
    class="toast"
    id="cartToast"
    role="alert"
    aria-live="assertive"
    aria-atomic="true"
    data-bs-autohide="false"
    style="
      position: fixed;
      top: 12%;
      right: 2%;
      transform: translate(0, -50%);
      width: 250px;
      z-index: 1000;
    "
  >
    <div
      class="toast-body"
      id="cartToastBody"
      style="font-weight: 500; font: 1.1rem"
    ></div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { Carousel, Navigation, Slide } from 'vue3-carousel'

import 'vue3-carousel/dist/carousel.css'

export default defineComponent({
  name: 'GalleryExample',
  props: {
    backendEndpoint: {
      type: String,
      required: true
    },
    item: {
      type: Object,
      required: true
    }
  },
  components: {
    Carousel,
    Slide,
    Navigation
  },
  data: () => ({
    currentSlide: 0
  }),
  methods: {
    slideTo(val) {
      this.currentSlide = val
    }
  }
})
</script>
<style>
:root {
  --vc-clr-primary: #2e76db;
}
.carousel__viewport {
  perspective: 2000px;
}

.carousel__prev,
.carousel__next {
  border: 1px;
  color: rgb(94, 152, 202);
  border-radius: 50%;
  margin-left: -40px !important;
  margin-right: -40px !important;
  width: 40px;
  height: 40px;
  display: flex;
}
.img-fluid {
  max-height: 550px !important;
}
.img-thumbnail {
  max-height: 100px !important;
}
</style>
