<template>
  <b-container>
    <b-card>
      <h1>Simple One Time Secret</h1>
      <hr />
      <b-collapse :visible="formVisible">
        <NewSecret />
      </b-collapse>
      <b-collapse :visible="linkVisible">
        <ShowLink />
      </b-collapse>
      <b-collapse :visible="retrieveVisible">
        <RetrieveSecret />
      </b-collapse>
      <hr />
    </b-card>
  </b-container>
</template>

<script>
import NewSecret from '../components/NewSecret.vue'
import RetrieveSecret from '../components/RetrieveSecret.vue'
import ShowLink from '../components/ShowLink.vue'
import { store } from '@/store.js'

export default {
  components: {
    NewSecret,
    ShowLink,
    RetrieveSecret
  },
  data() {
    return {
      store
    }
  },
  computed: {
    formVisible() {
      return this.store.link === '' && location.hash === ''
    },
    linkVisible() {
      return this.store.link !== '' && location.hash === ''
    },
    retrieveVisible() {
      return location.hash !== ''
    }
  }
}
</script>
