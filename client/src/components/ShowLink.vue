<template>
  <div class="secret-link">
    <b-field type="is-primary">
      <b-input
        custom-class="show-link-textarea"
        rows="4"
        type="textarea"
        v-model="store.link"
        readonly
      >
      </b-input>
    </b-field>
    <b-tooltip class="copy-button" label="Copy to clipboard" position="is-right">
      <b-button @click="copyToClipboard" type="is-primary" outlined
        ><img src="/src/assets/content-copy.svg" width="24" height="24" />
      </b-button>
    </b-tooltip>
  </div>
  <br />
  <b-button type="is-primary" expanded @click="store.setLink('')">Create another secret</b-button>
</template>

<script setup lang="ts">
import { store } from '@/store'
import { makeToast } from '@/helpers'

import { useToast } from 'buefy'

const toast = useToast()

function copyToClipboard() {
  navigator.clipboard.writeText(store.link)
  makeToast(toast, 'The link was copied to your clipboard.', 'is-primary')
}
</script>
<style lang="css">
.copy-button {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  opacity: 0.5;
  filter: alpha(opacity=50);
  transition: opacity 0.25s ease-in-out;
}

.copy-button:hover {
  opacity: 0.75;
  filter: alpha(opacity=75);
}

.secret-link {
  position: relative;
}

.show-link-textarea {
  resize: none;
}
</style>
