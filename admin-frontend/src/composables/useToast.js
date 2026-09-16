// src/composables/useToast.js
import { ref } from 'vue';

const toasts = ref([]);
let nextId = 1;

export function useToast() {
  const show = (message, type = 'success', duration = 4000) => {
    const id = nextId++;
    toasts.value.push({ id, message, type });
    setTimeout(() => dismiss(id), duration);
  };

  const dismiss = (id) => {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  };

  return {
    toasts,
    success: (msg, d) => show(msg, 'success', d),
    error: (msg, d) => show(msg, 'error', d),
    warning: (msg, d) => show(msg, 'warning', d),
    info: (msg, d) => show(msg, 'info', d),
    dismiss,
  };
}