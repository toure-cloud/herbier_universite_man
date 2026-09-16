<template>
  <transition name="fade">
    <div v-if="state.open" class="modal-overlay" @click.self="cancel">
      <div class="modal-box">
        <div class="modal-icon" :class="{ dangerous: state.dangerous }">
          <i :class="state.dangerous ? 'fas fa-exclamation-triangle' : 'fas fa-question-circle'"></i>
        </div>
        <h3>{{ state.title }}</h3>
        <p>{{ state.message }}</p>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancel">{{ state.cancelText }}</button>
          <button
            class="btn"
            :class="state.dangerous ? 'btn-danger' : 'btn-primary'"
            @click="accept"
          >
            {{ state.confirmText }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useConfirm } from '../composables/useConfirm';
const { state, accept, cancel } = useConfirm();
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2500;
  padding: 20px;
}
.modal-box {
  background: #fff;
  border-radius: 16px;
  padding: 32px 28px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
.modal-icon {
  width: 60px; height: 60px;
  border-radius: 50%;
  background: #dbeafe;
  color: #2563eb;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  margin: 0 auto 16px;
}
.modal-icon.dangerous { background: #fee2e2; color: #dc2626; }
.modal-box h3 { font-size: 18px; color: #0f172a; margin: 0 0 8px; }
.modal-box p { font-size: 14px; color: #64748b; margin: 0 0 24px; line-height: 1.5; }
.modal-actions { display: flex; gap: 10px; justify-content: center; }
.btn {
  padding: 10px 22px;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-secondary { background: #f1f5f9; color: #334155; }
.btn-secondary:hover { background: #e2e8f0; }
.btn-primary { background: #10b981; color: #fff; }
.btn-primary:hover { background: #059669; }
.btn-danger { background: #ef4444; color: #fff; }
.btn-danger:hover { background: #dc2626; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>