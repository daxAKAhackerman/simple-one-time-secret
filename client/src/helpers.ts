import { ToastProgrammatic } from 'buefy'

export function makeToast(toast: ToastProgrammatic, message: string, variant: string): void {
  toast.open({
    message,
    duration: 3000,
    queue: false,
    type: variant,
    position: 'is-top-right',
  })
}

export function copyToClipboard(text: string, toast: ToastProgrammatic | undefined) {
  navigator.clipboard.writeText(text)
  if (toast) {
    makeToast(toast, 'The text was copied to your clipboard.', 'is-primary')
  }
}

export function uint8ArrayToArrayBuffer(data: Uint8Array): ArrayBuffer {
  return data.slice().buffer
}

export function stringToUint8Array(data: string): Uint8Array<ArrayBuffer> {
  return Uint8Array.from(data, (c) => c.charCodeAt(0))
}

export function uint8ArrayToString(data: Uint8Array): string {
  return String.fromCharCode(...Array.from(data))
}

export function uint8ArrayToB64(data: Uint8Array): string {
  return btoa(uint8ArrayToString(data))
}

export function arrayBufferToB64(data: ArrayBuffer): string {
  return uint8ArrayToB64(new Uint8Array(data))
}

export function arrayBufferToString(data: ArrayBuffer): string {
  return uint8ArrayToString(new Uint8Array(data))
}

export function b64ToUint8Array(data: string): Uint8Array<ArrayBuffer> {
  return stringToUint8Array(atob(data))
}
