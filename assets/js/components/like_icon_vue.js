export const ComponentLiveIcon = {
    props: ['post_id', 'post_likes_count', 'props_is_liked'],
    data() {
        return {
                is_liked: false,
                count: null,
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
            instance.get('/gramm_app/likes/1')
                .then(response => {
                        this.iconObject = response.data.likes
                    }
                )
        }

    },
    mounted () {
        console.log("mounted " + this.post_id)
        this.count = this.post_likes_count
        this.is_liked = this.props_is_liked.toLowerCase() === "true"
    },
    template: `
    <button @click="invertIsLiked" class="button m-0">
         <span class="icon-text has-text-danger">
            <i :class="getIconClass"> &nbsp
            {{ getCount }}
            </i>
        </span>
    </button>
    `
}
