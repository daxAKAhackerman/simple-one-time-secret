<template>
  <b-collapse v-model="showSecret">
    <b-field type="is-primary">
      <b-input type="textarea" v-model="secret" rows="10" max-rows="10" readonly></b-input>
    </b-field>
    <br />
  </b-collapse>
  <div v-if="showError" class="error-message">
    &nbsp;Sorry, but this secret either does not exist, has already been viewed or is expired.
  </div>
  <b-button v-else type="is-primary" expanded :disabled="buttonDisabled" @click="getSecret"
    >Retrieve secret</b-button
  >
</template>

<script setup lang="ts">
import axios from 'axios'
import { inflate } from 'pako'
import { ref } from 'vue'
import { b64ToUint8Array, uint8ArrayToString, arrayBufferToString } from '@/helpers'

const secret = ref('')
const showSecret = ref(false)
const buttonDisabled = ref(false)
const showError = ref(false)

async function getSecret(): Promise<void> {
  const b64String = window.location.hash.slice(1)

  const decodedString = uint8ArrayToString(inflate(b64ToUint8Array(decodeURIComponent(b64String))))

  const encryptionParams = decodedString.split(';')
  const uuid = encryptionParams[0] as string
  const iv = encryptionParams[1] as string
  const key = encryptionParams[2] as string

  axios
    .get(`/api/secret/${uuid}`)
    .then((response) => {
      decryptSecret(response.data.secret, key, iv)
        .then((decryptedSecret) => {
          const decodedSecret = arrayBufferToString(decryptedSecret)
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
async function decryptSecret(data: string, key: string, iv: string) {
  const importedKey = await self.crypto.subtle.importKey(
    'raw',
    b64ToUint8Array(key),
    { name: 'AES-GCM' },
    false,
    ['decrypt'],
  )

  return await self.crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: b64ToUint8Array(iv) },
    importedKey,
    b64ToUint8Array(data),
  )
}
</script>
<style lang="css">
.error-message {
  font-weight: bold;
  color: #bd4147;
}
</style>
