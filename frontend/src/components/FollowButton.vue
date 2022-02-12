<template>
  <div class="control">
    <div class="tags has-addons">
      <span class="tag is-dark">followers</span>
      <span class="tag" :class="getTagClass">{{ count }}</span>
      <a class="tag is-link" :class="getTagClass" @click="fetch_following">Follow</a>
    </div>
  </div>
</template>

<script>
const axios = require('axios');
export default {
  name: "FollowButton",
  props: {
    target_user_id: String,
    followers_count: String,
    is_followed: String,
  },
  data() {
    console.log(this.is_followed)
    return {
      count: this.followers_count,
      followed: this.is_followed
    }
  },
  computed: {
    getTagClass() {
      console.log(this.followed)
      return this.followed ? "is-success" : "is-info"
    }
  },
  methods: {
    fetch_following() {
      axios.get(`/auth_by_email/following/${this.target_user_id}/`)
          .then((response) => {
            this.followed = response.data.is_followed;
            this.count = response.data.count;
          })
    },
  }


}
</script>

<style scoped>

</style>