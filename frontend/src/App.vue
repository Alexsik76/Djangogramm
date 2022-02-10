
<script>
import LikeIcon from '@/components/LikeIcon.vue'
import ImagePreview from "@/components/ImagePreview.vue";
import CardHeader from "@/components/CardHeader";
import Counter from "@/components/Counter";
export default {
  name: 'App',

  compilerOptions: {
    delimiters: ["[[", "]]"]
  },
  components: {
    'like-icon': LikeIcon,
    'image-preview': ImagePreview,
    'card-header': CardHeader,
    'counter': Counter
  },
  data() {
    return {
      app_count: null,
      app_counter: this.get_count
    }
  },
  methods:{
    get_count(count) {this.app_count = count}

  },

}
</script>
