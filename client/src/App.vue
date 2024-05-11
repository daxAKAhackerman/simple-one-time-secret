<template>
  <div id="app">
    <HomeView />
  </div>
</template>

<script>
import HomeView from './views/HomeView.vue'

export default {
  components: {
    HomeView
  }
}
</script>
<style>
body {
  color: #00060d;
  background-color: #f2f8ff !important;
}

#app {
  margin-top: 60px;
  margin-bottom: 60px;
}

textarea {
  background-color: #f2f8ff !important;
}
</style>
