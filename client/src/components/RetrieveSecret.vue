<template>
  <h1>test</h1>
  <!-- <b-collapse v-model="showSecret">
    <b-form-textarea v-model="secret" rows="10" max-rows="10" readonly></b-form-textarea>
    <br />
  </b-collapse>
  <div v-if="showError" class="error-message">
    &nbsp;Sorry, but this secret either does not exist, has already been viewed or is expired.
  </div>
  <b-button v-else block variant="outline-primary" :disabled="buttonDisabled" @click="getSecret"
    >Retrieve secret</b-button
  > -->
</template>

<script setup lang="ts">
import axios from 'axios'
import { inflate } from 'pako'
import { ref } from 'vue'

const secret = ref('')
const showSecret = ref(false)
const buttonDisabled = ref(false)
const showError = ref(false)

async function getSecret() {
  const b64String = window.location.hash.slice(1)

  const decodedString = String.fromCharCode(
    ...inflate(Uint8Array.from(decodeURIComponent(atob(b64String)), (c) => c.charCodeAt(0))),
  )

  const encryptionParams = decodedString.split(';')
  const uuid = encryptionParams[0]
  const iv = encryptionParams[1]
  const key = encryptionParams[2]

  axios
    .get(`/api/secret/${uuid}`)
    .then((response) => {
      decryptSecret(response.data.secret, key, iv)
        .then((decryptedSecret) => {
          const decodedSecret = String.fromCharCode(...new Uint8Array(decryptedSecret))
          secret.value = decodedSecret
          showSecret.value = true
          buttonDisabled.value = true
        })
        .catch((error) => {
          void error
          throw new Error('Bad decryption')
        })
    })
    .catch((error) => {
      void error
      buttonDisabled.value = true
      showError.value = true
    })
}
async function decryptSecret(data, key, iv) {
  const importedKey = await self.crypto.subtle.importKey(
    'raw',
    Uint8Array.fromBase64(key),
    { name: 'AES-GCM' },
    false,
    ['decrypt'],
  )

  return await self.crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: Uint8Array.fromBase64(iv) },
    importedKey,
    Uint8Array.fromBase64(data),
  )
}
</script>
<style scoped>
.error-message {
  font-weight: bold;
  color: #dc3545;
}
</style>
