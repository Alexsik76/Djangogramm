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
                iconObject: null
            }
    },
    computed: {
        getIconClass() {
            return this.is_liked ? 'fas fa-heart' : 'far fa-heart'
        },
        getCount(){
            return this.count
        },

    },
    methods: {
        invertIsLiked(){
            this.is_liked = !this.is_liked
            this.count++
        },
        getLikes() {
            http.get(`/gramm_app/likes/${this.id}`)
                .then(response => {
                        this.iconObject = response.data.likes
                    }
                )
        },
        likeIt(){
            http.post(`/gramm_app/likes/${this.id}`)
                .then(response => {
                    if(response.status ===200)
                        this.count++
                    }
                )
        }

    },
    mounted () {
        console.log("mounted new " + this.id)

    },
    template: `
    <button @click="likeIt" class="button m-0">
         <span class="icon-text has-text-danger">
            <i :class="getIconClass"> &nbsp
            {{ getCount }}
            </i>
        </span>
    </button>
    `
}
