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
import pako from 'pako'

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
      const b64String = window.location.hash.slice(1)

      const decodedString = atob(
        pako.inflate(Uint8Array.fromBase64(decodeURIComponent(b64String))).toBase64()
      )

      const encryptionParams = decodedString.split(';')
      const uuid = encryptionParams[0]
      const iv = encryptionParams[1]
      const key = encryptionParams[2]

      axios
        .get(`/api/secret/${uuid}`)
        .then((response) => {
          this.decryptSecret(response.data.secret, key, iv)
            .then((secret) => {
              const decodedSecret = atob(new Uint8Array(secret).toBase64())
              this.secret = decodedSecret
              this.showSecret = true
              this.buttonDisabled = true
            })
            .catch((error) => {
              void error
              throw new Error('Bad decryption')
            })
        })
        .catch((error) => {
          void error
          this.buttonDisabled = true
          this.showError = true
        })
    },
    async decryptSecret(data, key, iv) {
      const importedKey = await self.crypto.subtle.importKey(
        'raw',
        Uint8Array.fromBase64(key),
        { name: 'AES-GCM' },
        false,
        ['decrypt']
      )

      return await self.crypto.subtle.decrypt(
        { name: 'AES-GCM', iv: Uint8Array.fromBase64(iv) },
        importedKey,
        Uint8Array.fromBase64(data)
      )
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
