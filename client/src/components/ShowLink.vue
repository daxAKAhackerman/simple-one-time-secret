<template>
  <div class="secret-link">
    <b-form-textarea
      rows="3"
      no-auto-shrink
      no-resize
      readonly
      v-model="store.link"
    ></b-form-textarea>
    <b-button variant="outline-secondary" class="copy-button" @click="copyToClipboard"
      ><b-icon-files></b-icon-files
    ></b-button>
  </div>
  <br />
  <b-button variant="outline-primary" @click="store.setLink('')">Create another secret</b-button>
</template>

<script>
import { store } from '@/store.js'
import { makeToast } from '@/helpers.js'

export default {
  name: 'ShowLink',
  data() {
    return {
      store
    }
  },
  methods: {
    copyToClipboard() {
      navigator.clipboard.writeText(this.store.link)
      makeToast(this, 'Link was copied to clipboard.', 'info')
    }
  }
}
</script>
<style scoped>
.copy-button {
  position: absolute;
  bottom: 9%;
  left: 95.5%;
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
