<template>
  <b-collapse v-model="showSecret">
    <b-form-textarea v-model="secret" rows="10" max-rows="10" readonly></b-form-textarea>
    <br />
  </b-collapse>
  <b-row class="no-margin" align-v="center">
    <b-button variant="outline-primary" :disabled="buttonDisabled" @click="getSecret"
      >Retrieve secret</b-button
    >
    <div v-if="showError" class="error-message">
      &nbsp;Sorry, but this secret either does not exist, has already been viewed or is expired.
    </div>
  </b-row>
</template>

<script>
import axios from 'axios'
import pako from 'pako'
import * as CryptoJS from 'crypto-js'

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
    getSecret() {
      const b64String = window.location.hash.slice(1)

      const decodedString = String.fromCharCode.apply(
        null,
        pako.inflate(
          new Uint8Array(
            atob(decodeURIComponent(b64String))
              .split('')
              .map((x) => x.charCodeAt(0))
          )
        )
      )

      const encryptionParams = decodedString.split(';')
      const uuid = encryptionParams[0]
      const passhprase = encryptionParams[1]

      axios
        .get(`/api/secret/${uuid}`)
        .then((response) => {
          const secret = this.decryptSecret(response.data.secret, passhprase)

          if (secret !== null) {
            this.secret = secret
            this.showSecret = true
            this.buttonDisabled = true
          } else {
            throw new Error('Bad decryption')
          }
        })
        .catch((error) => {
          void error
          this.buttonDisabled = true
          this.showError = true
        })
    },
    decryptSecret(secret, passphrase) {
      console.log(secret)
      console.log(passphrase)
      try {
        return CryptoJS.AES.decrypt(secret, passphrase).toString(CryptoJS.enc.Utf8)
      } catch (error) {
        void error
        return
      }
    }
  }
}
</script>
<style scoped>
.error-message {
  font-weight: bold;
  color: red;
}

.no-margin {
  margin-left: 0px !important;
  margin-right: 0px !important;
}
</style>
