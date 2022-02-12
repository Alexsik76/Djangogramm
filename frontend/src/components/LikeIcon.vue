<template>
  <button @click="postLike" class="button m-0">
      <span class="icon-text has-text-danger">
            <i :class="getIconClass">
              {{" " + count }}
            </i>
        </span>
  </button>
</template>

<script>
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
                }
              }
          )
    },
  },
}
</script>
