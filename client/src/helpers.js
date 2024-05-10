export function makeToast(scope, message, variant) {
  scope.$bvToast.toast(message, {
    autoHideDelay: 3000,
    appendToast: false,
    noCloseButton: true,
    variant
  })
}
