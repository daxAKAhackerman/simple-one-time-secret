import { ToastProgrammatic } from "buefy"

export function makeToast(toast: ToastProgrammatic, message: string, variant: string) {
  toast.open({
    message,
    duration: 3000,
    queue: false,
    type: variant,
    position: 'is-top-right',
  })
}
