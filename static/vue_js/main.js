import './components/_globals.js'
let http = axios.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: "X-CSRFTOKEN",
});
export const app = new Vue({
    delimiters: ['[[', ']]'],

}).$mount("#app")