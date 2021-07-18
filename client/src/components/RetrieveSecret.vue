<template>
  <div>
    <b-collapse v-model="showSecret">
      <b-form-textarea
        v-model="secret"
        rows="10"
        max-rows="10"
        readonly
      ></b-form-textarea>
      <br />
    </b-collapse>
    <b-row class="no-margin" align-v="center">
      <b-button
        variant="outline-primary"
        :disabled="buttonDisabled"
        @click="getSecret"
        >Retrieve secret</b-button
      >
      <div v-if="showError" class="error-message">
        &nbsp;Sorry, but this secret either does not exist, has already been
        viewed or is expired.
      </div>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
import pako from "pako";
import crypto from "crypto";

export default {
  name: "RetrieveSecret",
  data() {
    return {
      secret: "",
      showSecret: false,
      buttonDisabled: false,
      showError: false,
    };
  },
  methods: {
    decryptSecret(secret, key, iv) {
      const decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
      try {
        let decrypted = decipher.update(secret, "base64", "utf8");
        decrypted += decipher.final("utf8");
        return decrypted;
      } catch (error) {
        void error;
        return null;
      }
    },
    getSecret() {
      const b64String = window.location.hash.slice(1);

      const decodedString = String.fromCharCode.apply(
        null,
        pako.inflate(
          new Uint8Array(
            atob(decodeURIComponent(b64String))
              .split("")
              .map((x) => x.charCodeAt(0))
          )
        )
      );

      const encryptionParams = decodedString.split(";");
      const uuid = encryptionParams[0];
      const key = encryptionParams[1];
      const iv = encryptionParams[2];

      axios
        .get(`/api/secret/${uuid}`)
        .then((response) => {
          const secret = this.decryptSecret(response.data.secret, key, iv);

          if (secret !== null) {
            this.secret = secret;
            this.showSecret = true;
            this.buttonDisabled = true;
          } else {
            throw new Error("Bad decrypt");
          }
        })
        .catch((error) => {
          void error;
          this.buttonDisabled = true;
          this.showError = true;
        });
    },
  },
};
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
