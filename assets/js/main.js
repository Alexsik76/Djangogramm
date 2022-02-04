
import {ComponentLiveIcon} from './components/like_icon_vue'
import ImagePreview from "./components/image_preview";


import {createApp} from "vue";
createApp({

    components: {
        'like-icon': ComponentLiveIcon,
        'image-preview': ImagePreview
    },


}).mount("#app")

