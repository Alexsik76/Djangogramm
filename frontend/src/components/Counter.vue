<template>
  <div>
    <slot></slot>
  </div>
</template>
<script>
export default {
  name: "Counter",

  props: {
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