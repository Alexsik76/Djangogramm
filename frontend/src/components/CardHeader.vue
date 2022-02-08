<template>
  <header class="card-header">
                <h3 class="card-header-title is-size-2 has-text-grey-light">{{ title }}</h3>
                <a class="delete" :href= "closeUrl" ></a>
    </header>
  </template>
<script>

const CardHeader = {
  props:
      ['closeUrl', 'title'],
}
export default CardHeader
</script>

