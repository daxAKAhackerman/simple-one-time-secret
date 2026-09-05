<template>
  <div class="secret-link">
    <b-input type="textarea" v-model="store.link" readonly> </b-input>
    <b-tooltip class="copy-button" label="Copy to clipboard">
      <b-button @click="copyToClipboard"
        ><img :src="contentCopyIcon" width="24" height="24" />
      </b-button>
    </b-tooltip>
  </div>
  <br />
  <b-button variant="outline-primary" @click="store.setLink('')">Create another secret</b-button>
</template>

<script setup lang="ts">
import { store } from '../store.js'
import { makeToast } from '../helpers.js'

import { useToast } from 'buefy'

const toast = useToast()

const contentCopyIcon = new URL('/src/assets/content-copy.svg', import.meta.url).href
console.log(contentCopyIcon)

function copyToClipboard() {
  navigator.clipboard.writeText(store.link)
  makeToast(toast, 'The link was copied to your clipboard.', 'is-primary')
}
</script>
<style scoped>
.copy-button {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  opacity: 0.25;
  filter: alpha(opacity=25);
  transition: opacity 0.25s ease-in-out;
}

.copy-button:hover {
  opacity: 0.75;
  filter: alpha(opacity=75);
}

.secret-link {
  position: relative;
}
</style>
