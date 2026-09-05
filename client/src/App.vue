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

.copy-button {
  position: absolute;
  right: 0.5rem;
  opacity: 0.5;
  filter: alpha(opacity=50);
  transition: opacity 0.25s ease-in-out;
}

.copy-button:hover {
  opacity: 0.75;
  filter: alpha(opacity=75);
}
</style>
