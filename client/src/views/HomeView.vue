<template>
    <b-row>
        <b-col offset="2" cols="8">
            <h1>Simple One Time Secret</h1>
            <hr />
            <b-collapse :visible="formVisible">
                <NewSecret />
            </b-collapse>
            <b-collapse :visible="linkVisible">
                <ShowLink />
            </b-collapse>
            <!-- <b-collapse :visible="retrieveVisible">
                <RetrieveSecret />
            </b-collapse> -->
            <hr />
        </b-col>
    </b-row>
</template>

<script>
import NewSecret from '../components/NewSecret.vue';
// import RetrieveSecret from '../components/RetrieveSecret.vue';
import ShowLink from '../components/ShowLink.vue';
import { store } from '@/store.js'


export default {
    components: {
        NewSecret,
        ShowLink,
        // RetrieveSecret,
    },
    data() {
        return {
            store
        }
    },
    computed: {
        formVisible() {
            return this.store.link === '' && !location.hash;
        },
        linkVisible() {
            return this.store.link !== '' && !location.hash;
        },
        retrieveVisible() {
            return location.hash;
        },
    },
}

</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin-top: 60px;
}

textarea {
    background-color: #edf6ff !important;
}
</style>
