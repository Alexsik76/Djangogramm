import { createApp } from 'vue/dist/vue.esm-bundler.js';
import App from './App.vue'

const app = createApp(App);
app.config.productionTip = false;
createApp(App).mount('#app')