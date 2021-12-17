let instance = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: "X-CSRFTOKEN",
});
const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            my_icon: ''
        }
    },
    methods: {
        async getIconClass() {
            await instance
                .get(post_url)
                .then((response) => {
                this.my_icon = response.data.likes ? "fas fa-heart" : "far fa-heart";
            })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    mounted() {
        this.getIconClass();
    }

}).mount("#vue-icon")
