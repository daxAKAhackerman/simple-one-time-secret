import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueMoment from 'vue-moment'
import VueClipboard from 'vue-clipboard2'

import { makeToast } from './utils'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueMoment)
Vue.use(VueClipboard)

Vue.mixin({
  methods: {
      makeToast
  }
})

new Vue({
  render: h => h(App),
}).$mount('#app')
