<template>
  <div class="container">
    <div class="card">
      <div class="card-content">
        <h1 class="title is-1">Simple One Time Secret</h1>
        <hr />

        <b-collapse v-model="formVisible">
          <NewSecret />
        </b-collapse>
        <b-collapse v-model="linkVisible">
          <ShowLink />
        </b-collapse>
        <b-collapse v-model="retrieveVisible">
          <RetrieveSecret />
        </b-collapse>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import NewSecret from '../components/NewSecret.vue'
import RetrieveSecret from '../components/RetrieveSecret.vue'
import ShowLink from '../components/ShowLink.vue'
import { store } from '@/store'

import { computed } from 'vue'

const formVisible = computed(() => {
  return store.link === '' && location.hash === ''
})

const linkVisible = computed(() => {
  return store.link !== '' && location.hash === ''
})

const retrieveVisible = computed(() => {
  return location.hash !== ''
})
</script>
