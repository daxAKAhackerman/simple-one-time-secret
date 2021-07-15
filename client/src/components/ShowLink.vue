<template>
  <div>
    <div class="secret-link">
      <b-form-textarea
        rows="3"
        no-auto-shrink
        no-resize
        disabled
        v-model="link"
      ></b-form-textarea>
      <b-button
        variant="outline-secondary"
        v-clipboard:copy="link"
        class="copy-button"
        @click="makeToast('Link was copied to clipboard.')"
        ><b-icon-files></b-icon-files
      ></b-button>
    </div>
    <br />
    <b-button variant="outline-primary" @click="$emit('reset')"
      >Create an other secret</b-button
    >
  </div>
</template>

<script>
export default {
  name: "ShowLink",
  props: ["link"],
  data() {
    return {};
  },
  methods: {
    makeToast(message) {
      this.$root.$bvToast.toast(message, {
        autoHideDelay: 2000,
        appendToast: false,
        variant: "outline-success",
        noCloseButton: true,
      });
    },
  },
};
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