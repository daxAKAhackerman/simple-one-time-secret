import { reactive } from 'vue'

export const store = reactive({
  link: '',
  setLink(link) {
    this.link = link
  }
})
