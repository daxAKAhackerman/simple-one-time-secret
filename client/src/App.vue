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

  --bulma-success-h: 153deg;
  --bulma-success-s: 53%;
  --bulma-success-l: 53%;

  --bulma-danger-h: 348deg;
  --bulma-danger-s: 86%;
  --bulma-danger-l: 61%;

  --bulma-warning-h: 44deg;
  --bulma-warning-s: 100%;
  --bulma-warning-l: 77%;

  --bulma-radius-small: 2px;
  --bulma-radius: 4px;
  --bulma-radius-large: 6px;
}

#app {
  margin-top: 60px;
  margin-bottom: 60px;
}

a {
  color: #7d4698;
}
</style>
