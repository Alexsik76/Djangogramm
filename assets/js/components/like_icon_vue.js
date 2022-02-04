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
            instance.get(`/gramm_app/likes/${this.id}`)
                .then(response => {
                        this.iconObject = response.data.likes
                    }
                )
        }

    },
    mounted () {
        console.log("mounted new " + this.id)

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
