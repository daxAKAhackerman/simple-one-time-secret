<template>
  <div>
    <b-row>
      <b-col offset="2" cols="8">
        <h1>One Time Secret</h1>
        <hr />
        <b-collapse v-model="formVisible"
          ><NewSecret @link-generated="link = $event"
        /></b-collapse>
        <b-collapse v-model="linkVisible"
          ><ShowLink :link="link" @reset="reset"
        /></b-collapse>
        <b-collapse v-model="retrieveVisible"><RetrieveSecret /></b-collapse>
        <hr />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import NewSecret from "./NewSecret";
import ShowLink from "./ShowLink";
import RetrieveSecret from "./RetrieveSecret";

export default {
  name: "Index",
  components: {
    NewSecret,
    ShowLink,
    RetrieveSecret,
  },
  data() {
    return {
      link: "",
    };
  },
  computed: {
    formVisible: {
      get: function () {
        return Boolean(!this.link && !location.hash);
      },
      set: function () {},
    },
    linkVisible: {
      get: function () {
        return Boolean(this.link && !location.hash);
      },
      set: function () {},
    },
    retrieveVisible: {
      get: function () {
        return Boolean(location.hash);
      },
      set: function () {},
    },
  },
  methods: {
    reset() {
      this.link = "";
    },
  },
};
</script>

<style scoped>
</style>
