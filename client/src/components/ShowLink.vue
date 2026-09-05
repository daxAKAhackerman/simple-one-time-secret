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
    <b-tooltip class="copy-button copy-button-link" label="Copy to clipboard" position="is-right">
      <b-button @click="copyToClipboard(store.link, toast)" type="is-primary" outlined
        ><img src="/src/assets/content-copy.svg" width="24" height="24" />
      </b-button>
    </b-tooltip>
  </div>
  <br />
  <b-button type="is-primary" expanded @click="store.setLink('')">Create another secret</b-button>
</template>

<script setup lang="ts">
import { store } from '@/store'
import { copyToClipboard } from '@/helpers'
import { useToast } from 'buefy'

const toast = useToast()
</script>

<style lang="css">
.copy-button-link {
  bottom: 0.5rem;
}

.secret-link {
  position: relative;
}

.show-link-textarea {
  resize: none;
}
</style>
