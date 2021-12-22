import {ComponentLiveIcon} from './components/like_icon_vue'
import ImagePreview from "./components/image_preview";
// let http = axios.create({
//     xsrfCookieName: 'csrftoken',
//     xsrfHeaderName: "X-CSRFTOKEN",
// });
import {createApp} from "vue";
export const app = createApp({

    components: {
        'like-icon': ComponentLiveIcon,
        'image-preview': ImagePreview
    },


}).mount("#app")