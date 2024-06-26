<template>
  <b-form @submit="postSecret">
    <b-form-group label="Secret:" label-for="secret-textarea">
      <b-form-textarea
        id="secret-textarea"
        v-model="secret"
        rows="20"
        max-rows="20"
      ></b-form-textarea>
    </b-form-group>

    <b-form-group label="Expiration (local time):" label-for="datepicker">
      <b-row>
        <b-col>
          <b-input-group id="datepicker">
            <b-form-input
              v-model="expirationDate"
              type="text"
              placeholder="YYYY-MM-DD"
              autocomplete="off"
              required
            ></b-form-input>
            <b-input-group-append variant="primary">
              <b-form-datepicker
                v-model="expirationDate"
                button-only
                right
                locale="en-US"
                button-variant="outline-primary"
              ></b-form-datepicker>
            </b-input-group-append>
          </b-input-group>
        </b-col>
        <b-col>
          <b-input-group>
            <b-form-input
              v-model="expirationTime"
              type="text"
              placeholder="HH:mm:ss"
              required
            ></b-form-input>
            <b-input-group-append>
              <b-form-timepicker
                v-model="expirationTime"
                button-only
                right
                locale="en"
                button-variant="outline-primary"
                show-seconds
                :hour12="false"
              ></b-form-timepicker>
            </b-input-group-append>
          </b-input-group>
        </b-col>
      </b-row>
    </b-form-group>
    <b-button type="submit" block variant="outline-primary">Create secret link</b-button>
  </b-form>
  <br />
  <h2>How it works</h2>
  <p>
    Simple One Time Secret is an application that allows to securely share information using a
    single-use link. Once the secret has been viewed (or once the expiration is reached), the secret
    is deleted from the database and no longer accessible. In addition, the server only has access
    to the encrypted secret and its ID. Everything else is generated client side and is never sent
    to the server. More precisely:
  </p>
  <ol>
    <li>
      Using JavaScript, a random encryption passphrase is generated and used to encrypt the secret.
    </li>
    <li>The encrypted secret is sent to the server, along with the expiration timestamp.</li>
    <li>The server replies with the ID of the secret.</li>
    <li>
      A link is generated by adding the deflated concatenation of the ID and encryption passhprase
      to the hash data of the URL. Hash data is not sent to the server when a URL is accessed.
    </li>
    <li>
      When the secret is retrieved, the server receives the ID of the secret, deletes it from the
      database, and returns the encrypted value back to the client (if it's not expired).
    </li>
    <li>
      The secret value can then be decrypted client side using the information stored in the hash
      data.
    </li>
  </ol>
  <p>
    Want more information? Good news,
    <b-link href="https://github.com/daxAKAhackerman/simple-one-time-secret"
      >this project is open source!
    </b-link>
  </p>
</template>
<script>
import axios from 'axios'
import * as CryptoJS from 'crypto-js'
import pako from 'pako'
import { store } from '@/store.js'
import { makeToast } from '@/helpers.js'

export default {
  name: 'NewSecret',
  data() {
    return {
      secret: '',
      expirationDate: '',
      expirationTime: '00:00:00',
      store
    }
  },
  computed: {
    expirationTimestamp() {
      let expirationTime = this.expirationTime
      if (expirationTime === '') {
        expirationTime = '00:00:00'
      }
      const expirationString = `${this.expirationDate} ${expirationTime}`
      const expirationDate = new Date(expirationString)
      const expirationFormated = Math.floor(expirationDate.getTime() / 1000)

      return expirationFormated
    }
  },
  methods: {
    initNewSecret() {
      const currentDate = new Date()
      currentDate.setDate(currentDate.getDate() + 7)
      currentDate.setTime(currentDate.getTime() - currentDate.getTimezoneOffset() * 60 * 1000)

      this.expirationDate = currentDate.toISOString().split('T')[0]
      this.expirationTime = '00:00:00'
      this.secret = ''
    },
    postSecret(event) {
      event.preventDefault()
      const path = '/api/secret'

      const passphrase = this.generateString(32)
      const secret = this.encryptSecret(this.secret, passphrase)

      const payload = { expiration: this.expirationTimestamp, secret }

      axios
        .post(path, payload)
        .then((response) => {
          this.generateLink(response.data.id, passphrase)
          this.initNewSecret()
        })
        .catch((error) => {
          void error
          makeToast(
            this,
            'Something went wrong while creating your secret. Please make sure that the expiration date/time is valid.',
            'danger'
          )
        })
    },
    generateString(length) {
      let result = ''
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

      for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length))
      }

      return result
    },
    encryptSecret(secret, passphrase) {
      const encrypted = CryptoJS.AES.encrypt(secret, passphrase)

      return encrypted.toString()
    },
    generateLink(uuid, passphrase) {
      const data = encodeURIComponent(
        btoa(
          String.fromCharCode.apply(null, new Uint16Array(pako.deflate(`${uuid};${passphrase}`)))
        )
      )

      const link = `${window.location.origin}#${data}`

      this.store.setLink(link)
    }
  },
  created() {
    this.initNewSecret()
  }
}
</script>
