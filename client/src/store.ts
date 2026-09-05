import { reactive } from 'vue'

export const store = reactive({
  link: '',
  setLink(link: string) {
    this.link = link
  },
})
