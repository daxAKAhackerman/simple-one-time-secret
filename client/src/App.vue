<template>
  <div id="app">
    <HomeView />
  </div>
</template>

<script setup lang="ts">
import HomeView from './views/HomeView.vue'
</script>

<style lang="css">
:root {
  --bulma-primary-h: 280deg;
  --bulma-primary-s: 37%;
  --bulma-primary-l: 44%;
}

#app {
  margin-top: 60px;
  margin-bottom: 60px;
}

a {
  color: #7d4698;
}
</style>
