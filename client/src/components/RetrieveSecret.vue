<template>
  <b-collapse v-model="showSecret">
    <b-form-textarea v-model="secret" rows="10" max-rows="10" readonly></b-form-textarea>
    <br />
  </b-collapse>
  <div v-if="showError" class="error-message">
    &nbsp;Sorry, but this secret either does not exist, has already been viewed or is expired.
  </div>
  <b-button v-else block variant="outline-primary" :disabled="buttonDisabled" @click="getSecret"
    >Retrieve secret</b-button
  >
</template>

<script>
import axios from 'axios'
import { base64ToBytes, base64UrlToBytes } from '@/crypto.js'

export default {
  name: 'RetrieveSecret',
  data() {
    return {
      secret: '',
      showSecret: false,
      buttonDisabled: false,
      showError: false
    }
  },
  methods: {
    async getSecret() {
      const fragment = window.location.hash.slice(1)
      const [uuid, base64UrlKey] = fragment.split('.')

      if (!uuid || !base64UrlKey) {
        this.buttonDisabled = true
        this.showError = true
        return
      }

      try {
        const response = await axios.get(`/api/secret/${uuid}`)
        const secret = await this.decryptSecret(response.data.secret, base64UrlKey)

        this.secret = secret
        this.showSecret = true
        this.buttonDisabled = true
      } catch (error) {
        void error
        this.buttonDisabled = true
        this.showError = true
      }
    },
    async decryptSecret(ciphertextB64, base64UrlKey) {
      const keyBytes = base64UrlToBytes(base64UrlKey)
      const combined = base64ToBytes(ciphertextB64)
      const iv = combined.subarray(0, 12)
      const ciphertext = combined.subarray(12)

      const key = await crypto.subtle.importKey('raw', keyBytes, { name: 'AES-GCM' }, false, [
        'decrypt'
      ])
      const plaintext = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, ciphertext)
      return new TextDecoder().decode(plaintext)
    }
  }
}
</script>
<style scoped>
.error-message {
  font-weight: bold;
  color: #dc3545;
}
</style>
