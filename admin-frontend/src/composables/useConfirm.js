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

const accept = () => {
  state.value.resolve?.(true);
  state.value.open = false;
};

const cancel = () => {
  state.value.resolve?.(false);
  state.value.open = false;
};

/**
 * ✅ Retourne un objet qui est À LA FOIS :
 *   - callable : `await useConfirm()({ title, message })`
 *   - destructurable : `const { state, accept, cancel } = useConfirm()`
 *   - avec une propriété `.confirm(...)` : `await useConfirm().confirm({...})`
 *
 * Les 3 usages fonctionnent, donc rien à changer dans les vues ni dans ConfirmDialog.vue.
 */
export function useConfirm() {
  // 1) La fonction callable
  const ask = ({ title, message, confirmText, cancelText, dangerous = false } = {}) => {
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

  // 2) On greffe les utilitaires sur la fonction
  ask.state = state;
  ask.accept = accept;
  ask.cancel = cancel;
  ask.confirm = ask; // alias rétrocompatible

  // 3) On expose aussi state/accept/cancel au niveau de l'objet retourné
  //    (utile pour `const { state, accept, cancel } = useConfirm()`)
  ask.open = ask;   // au cas où on appelle `useConfirm().open(...)` un jour

  return ask;
}