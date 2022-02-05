const axios = require('axios');

export const ComponentLiveIcon = {
    props: ['payload'],
    data() {
        return {
            id: this.payload.post_id,
            is_liked: (this.payload.is_liked),
            count: this.payload.likes_count,
        }
    },
    computed: {
        getIconClass() {
            return this.is_liked ? 'fas fa-heart' : 'far fa-heart'
        },
    },
    methods: {

        postLike() {
            axios.get(`/gramm_app/likes/${this.id}`)
                .then(response => {
                        if (response.status === 200) {
                            this.is_liked = response.data.is_liker
                            this.count = response.data.likes_count
                        }
                    }
                )
        },
    },
    template: `
      <button @click="postLike" class="button m-0">
      <span class="icon-text has-text-danger">
            <i :class="getIconClass"> &nbsp
              {{ count }}
            </i>
        </span>
      </button>
    `
}
