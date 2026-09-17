<template>
  <div class="stat-card" :class="`stat-${color}`">
    <div class="stat-icon"><i :class="icon"></i></div>
    <div class="stat-body">
      <span class="stat-value">{{ value }}</span>
      <span class="stat-label">{{ label }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  value: { type: [Number, String], required: true },
  label: { type: String, required: true },
  icon: { type: String, default: 'fas fa-chart-bar' },
  color: { type: String, default: 'green' },
})
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  border-left: 4px solid #10b981;
  transition: transform 0.15s;
}
.stat-card:hover { transform: translateY(-2px); }

.stat-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #ecfdf5;
  color: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.stat-body { display: flex; flex-direction: column; }
.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
}
.stat-label {
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}

/* ---------- Couleurs disponibles ---------- */

/* Vert (défaut) */
.stat-green { border-left-color: #10b981; }
.stat-green .stat-icon { background: #ecfdf5; color: #10b981; }

/* Bleu */
.stat-blue { border-left-color: #3b82f6; }
.stat-blue .stat-icon { background: #eff6ff; color: #3b82f6; }

/* Violet */
.stat-purple { border-left-color: #8b5cf6; }
.stat-purple .stat-icon { background: #f5f3ff; color: #8b5cf6; }

/* Orange */
.stat-orange { border-left-color: #f59e0b; }
.stat-orange .stat-icon { background: #fffbeb; color: #f59e0b; }

/* Turquoise */
.stat-teal { border-left-color: #14b8a6; }
.stat-teal .stat-icon { background: #f0fdfa; color: #14b8a6; }

/* Rouge */
.stat-red { border-left-color: #ef4444; }
.stat-red .stat-icon { background: #fef2f2; color: #ef4444; }

/* ✅ Indigo (SuperIT) */
.stat-indigo { border-left-color: #6366f1; }
.stat-indigo .stat-icon { background: #eef2ff; color: #6366f1; }

/* ✅ Rose (bonus) */
.stat-pink { border-left-color: #ec4899; }
.stat-pink .stat-icon { background: #fdf2f8; color: #ec4899; }

/* ✅ Ambre (bonus) */
.stat-amber { border-left-color: #f59e0b; }
.stat-amber .stat-icon { background: #fffbeb; color: #f59e0b; }
</style>
