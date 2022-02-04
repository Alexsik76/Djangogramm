const axios = require('axios');

let http = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: "X-CSRFTOKEN",
});

export const ComponentLiveIcon = {
    props: ['payload'],
    data() {
        return {
                is_liked: (this.payload.is_liked),
                count: this.payload.likes_count,
                id: this.payload.post_id,
            }
    },
    computed: {
        getIconClass() {
            return this.is_liked ? 'fas fa-heart' : 'far fa-heart'
        },

    },
    methods: {

        invertLike(){
            http.post(`/gramm_app/likes/${this.id}`)
                .then(response => {
                    if(response.status ===200)
                        this.is_liked ? this.count-- : this.count++
                        this.is_liked = !this.is_liked
                    }
                )
        },

    },
    template: `
    <button @click="invertLike" class="button m-0">
         <span class="icon-text has-text-danger">
            <i :class="getIconClass"> &nbsp
            {{ count }}
            </i>
        </span>
    </button>
    `
}
