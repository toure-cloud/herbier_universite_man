<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast"
        :class="`toast-${t.type}`"
      >
        <i :class="iconFor(t.type)"></i>
        <span>{{ t.message }}</span>
        <button @click="dismiss(t.id)" aria-label="Fermer"><i class="fas fa-times"></i></button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast';
const { toasts, dismiss } = useToast();

const iconFor = (type) => ({
  success: 'fas fa-check-circle',
  error: 'fas fa-exclamation-circle',
  warning: 'fas fa-exclamation-triangle',
  info: 'fas fa-info-circle',
}[type] || 'fas fa-info-circle');
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 3000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 380px;
}
.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 10px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  font-size: 13.5px;
  font-weight: 500;
  color: #fff;
  background: #334155;
}
.toast i { font-size: 16px; }
.toast button {
  margin-left: auto;
  background: none;
  border: none;
  color: inherit;
  opacity: 0.7;
  cursor: pointer;
  font-size: 12px;
}
.toast button:hover { opacity: 1; }
.toast-success { background: #10b981; }
.toast-error { background: #ef4444; }
.toast-warning { background: #f59e0b; }
.toast-info { background: #3b82f6; }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(40px); }
.toast-leave-to { opacity: 0; transform: translateX(40px); }
</style>