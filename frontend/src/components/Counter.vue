<template>
  <slot></slot>
</template>
<script>
export default {
  name: "Counter",

  props:{
    count: Number,
    app_counter: Function,
  },


  mounted() {

  this.app_counter(this.count)
  }
}
</script>

<!--<style scoped>-->

<!--</style>-->