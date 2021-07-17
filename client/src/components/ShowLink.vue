<template>
  <div>
    <div class="secret-link">
      <b-form-textarea
        rows="3"
        no-auto-shrink
        no-resize
        readonly
        v-model="link"
      ></b-form-textarea>
      <b-button
        variant="outline-secondary"
        v-clipboard:copy="link"
        class="copy-button"
        @click="makeToast('Link was copied to clipboard.', 'info', 2000)"
        ><b-icon-files></b-icon-files
      ></b-button>
    </div>
    <br />
    <b-button variant="outline-primary" @click="$emit('reset')"
      >Create another secret</b-button
    >
  </div>
</template>

<script>
export default {
  name: "ShowLink",
  props: ["link"],
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
