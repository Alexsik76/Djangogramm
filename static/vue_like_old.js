let instance = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: "X-CSRFTOKEN",
});
Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            iconObject: {
                my_icon: '',
                liked_count: '',
            }
        }
    },
    computed: {
        getLikes() {
            instance.get('/gramm_app/likes/1')
                .then(response => {
                        this.iconObject = response.data.likes
                    }
                )
            return this.liked_count
        }
    },
}).mount("#vue-icon")
