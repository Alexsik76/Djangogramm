<template>
  <button @click="postLike" class="button m-0">
      <span class="icon-text has-text-danger">
        <transition>
            <i :id="`animated-icon-${this.id}`" :class="getIconClass">
              {{" " + count }}
            </i>
          </transition>
        </span>
  </button>
</template>

<script>
import {gsap} from "gsap";

const axios = require('axios');
export default {
  name: 'LikeIcon',
  props: {
    post_id: Number,
    likes_count: Number,
    is_liked: Boolean
  },
  data() {
    return {
      id: this.post_id,
      count: this.likes_count,
      liked: this.is_liked,
    }
  },
  computed: {
    getIconClass() {
    return this.liked ? 'fas fa-heart' : 'far fa-heart';
    },
  },
  methods: {
    postLike() {
      axios.get(`/gramm_app/likes/${this.id}`)
          .then(response => {
                if (response.status === 200) {
                  this.liked = response.data.is_liker;
                  this.count = response.data.likes_count;
                  this.animate_blink()
                }
              }
          )
    },
    animate_blink() {
      gsap.to(`#animated-icon-${this.id}`, {scale: 1.4, clearProps:"scale", duration:0.08})
    },
  },
}
</script>

<!--<style>-->
<!--.v-enter-active,-->
<!--.v-leave-active {-->
<!--  transition: opacity 0.5s ease;-->
<!--}-->

<!--.v-enter-from,-->
<!--.v-leave-to {-->
<!--  opacity: 0;-->
<!--}-->
<!--</style>-->
