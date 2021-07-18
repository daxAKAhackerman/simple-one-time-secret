export const makeToast = function(message, variant, delay) {
  this.$root.$bvToast.toast(message, {
    autoHideDelay: delay,
    appendToast: false,
    variant: variant,
    noCloseButton: true,
  });
}
