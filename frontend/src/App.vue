<script>
import LikeIcon from '@/components/LikeIcon.vue'
import ImagePreview from "@/components/ImagePreview.vue";
import CardHeader from "@/components/CardHeader";
import FollowButton from "@/components/FollowButton";

export default {
  name: 'App',

  compilerOptions: {
    delimiters: ["[[", "]]"]
  },
  components: {
    'like-icon': LikeIcon,
    'image-preview': ImagePreview,
    'card-header': CardHeader,
    'follow-button': FollowButton
  },
}
</script>
