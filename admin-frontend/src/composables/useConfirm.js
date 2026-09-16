// src/composables/useConfirm.js
import { ref } from 'vue';

const state = ref({
  open: false,
  title: '',
  message: '',
  confirmText: 'Confirmer',
  cancelText: 'Annuler',
  dangerous: false,
  resolve: null,
});

export function useConfirm() {
  const confirm = ({ title, message, confirmText, cancelText, dangerous = false }) => {
    return new Promise((resolve) => {
      state.value = {
        open: true,
        title: title || 'Confirmation',
        message: message || '',
        confirmText: confirmText || 'Confirmer',
        cancelText: cancelText || 'Annuler',
        dangerous,
        resolve,
      };
    });
  };

  const accept = () => {
    state.value.resolve?.(true);
    state.value.open = false;
  };

  const cancel = () => {
    state.value.resolve?.(false);
    state.value.open = false;
  };

  return { state, confirm, accept, cancel };
}