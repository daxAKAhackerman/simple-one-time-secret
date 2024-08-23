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
    <b-link v-if="showTorLink" :href="torLink"
      ><b-img
        v-b-tooltip.hover
        title="Use Simple One Time Secret over TOR instead to share secrets anonymously"
        class="tor-logo"
        src="/src/assets/tor_logo.png"
      ></b-img
    ></b-link>
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
    },
    torLink() {
      return import.meta.env.VITE_TOR_LINK
    },
    showTorLink() {
      return !location.hostname.endsWith('.onion') && this.torLink
    }
  }
}
</script>
<style scoped>
.tor-logo {
  position: fixed;
  right: 20px;
  bottom: 20px;
  height: 50px;
}
</style>
