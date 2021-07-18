<template>
  <div>
    <b-row>
      <b-col offset="2" cols="8">
        <h1>Simple One Time Secret</h1>
        <hr />
        <b-collapse :visible="formVisible"
          ><NewSecret @link-generated="link = $event"
        /></b-collapse>
        <b-collapse :visible="linkVisible"
          ><ShowLink :link="link" @reset="link = ''"
        /></b-collapse>
        <b-collapse :visible="retrieveVisible"><RetrieveSecret /></b-collapse>
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
    formVisible: function () {
      return Boolean(!this.link && !location.hash);
    },
    linkVisible: function () {
      return Boolean(this.link && !location.hash);
    },
    retrieveVisible: function () {
      return Boolean(location.hash);
    },
  },
};
</script>
