<template>
  <header class="topbar">
    <div class="topbar-title">
      <div class="title-icon" v-if="icon"><i :class="icon"></i></div>
      <div>
        <h1>{{ title }}</h1>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>
    </div>

    <div class="topbar-actions">
      <slot name="actions" />
      <button v-if="showRefresh" class="btn-icon" @click="$emit('refresh')" :disabled="loading">
        <i class="fas fa-sync-alt" :class="{ spinning: loading }"></i>
      </button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' },
  showRefresh: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
});
defineEmits(['refresh']);
</script>

<style scoped>
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 18px 24px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.topbar-title { display: flex; align-items: center; gap: 14px; }
.title-icon {
  width: 44px; height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, #10b981, #059669);
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  font-size: 18px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
.topbar-title h1 { font-size: 20px; font-weight: 700; color: #0f172a; margin: 0; }
.topbar-title p { font-size: 13px; color: #64748b; margin: 2px 0 0; }

.topbar-actions { display: flex; align-items: center; gap: 10px; }

.btn-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #475569;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.btn-icon:hover:not(:disabled) { background: #f8fafc; border-color: #cbd5e1; }
.btn-icon:disabled { opacity: 0.5; cursor: not-allowed; }
.spinning { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>