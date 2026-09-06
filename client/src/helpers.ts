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

export function copyToClipboard(text: string, toast: ToastProgrammatic | undefined): void {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      if (toast) {
        makeToast(toast, 'The text was copied to your clipboard.', 'is-primary')
      }
    })
    .catch((error) => {
      void error
    })
}

export function uint8ArrayToArrayBuffer(data: Uint8Array): ArrayBuffer {
  return data.slice().buffer
}

export function stringToUint8Array(data: string): Uint8Array<ArrayBuffer> {
  return new TextEncoder().encode(data)
}

export function uint8ArrayToString(data: Uint8Array): string {
  return new TextDecoder('utf-8').decode(data)
}

export function uint8ArrayToB64(data: Uint8Array): string {
  let binary = ''
  for (const byte of data) {
    binary += String.fromCharCode(byte)
  }
  return btoa(binary)
}

export function b64ToUint8Array(data: string): Uint8Array<ArrayBuffer> {
  const binary = atob(data)
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i)
  }
  return bytes
}

export function arrayBufferToB64(data: ArrayBuffer): string {
  return uint8ArrayToB64(new Uint8Array(data))
}

export function arrayBufferToString(data: ArrayBuffer): string {
  return uint8ArrayToString(new Uint8Array(data))
}
