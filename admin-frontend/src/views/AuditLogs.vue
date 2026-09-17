<template>
  <div class="audit-layout">
    <Sidebar
      :user="auth.user"
      :is-super-it="true"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Journal d'audit"
        subtitle="Historique complet des actions (SuperIT)"
        icon="fas fa-history"
      >
        <template #actions>
          <button class="btn-secondary" @click="load" :disabled="loading">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
            Rafraîchir
          </button>
        </template>
      </TopBar>

      <section class="filters-bar">
        <select v-model="filters.action" class="filter-select">
          <option value="">Toutes les actions</option>
          <option value="CREATE">Création</option>
          <option value="UPDATE">Modification</option>
          <option value="DELETE">Suppression</option>
          <option value="LOGIN">Connexion</option>
          <option value="LOGOUT">Déconnexion</option>
          <option value="LOGIN_FAILED">Échec de connexion</option>
          <option value="SYNC">Synchronisation</option>
        </select>
        <select v-model="filters.user_id" class="filter-select">
          <option value="">Tous les utilisateurs</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.nom }}</option>
        </select>
        <button class="btn-primary" @click="load">
          <i class="fas fa-search"></i> Filtrer
        </button>
        <div class="result-count">
          <i class="fas fa-list"></i> {{ logs.length }} entrée(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="logs.length === 0" class="empty-block">
        <i class="fas fa-history"></i>
        <h3>Aucune action enregistrée</h3>
      </section>

      <section v-else class="logs-table-wrap">
        <table class="logs-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Utilisateur</th>
              <th>Action</th>
              <th>Objet</th>
              <th>Détails</th>
              <th>IP</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id">
              <td class="cell-date">{{ formatDate(log.created_at) }}</td>
              <td>
                <div class="cell-user">
                  <div class="user-avatar-sm" :class="{ it: isIT(log) }">
                    {{ getInitials(log.user_nom) }}
                  </div>
                  <span>{{ log.user_nom || 'Système' }}</span>
                </div>
              </td>
              <td>
                <span class="action-badge" :class="`action-${log.action.toLowerCase()}`">
                  <i :class="actionIcon(log.action)"></i> {{ log.action_label }}
                </span>
              </td>
              <td>
                <div v-if="log.model_name" class="cell-object">
                  <span class="object-model">{{ log.model_name }}</span>
                  <span v-if="log.object_repr" class="object-repr">{{ log.object_repr }}</span>
                </div>
                <span v-else class="empty">—</span>
              </td>
              <td class="cell-details">
                <span v-if="hasDetails(log)" class="details-text">{{ formatDetails(log.details) }}</span>
                <span v-else class="empty">—</span>
              </td>
              <td class="cell-ip">{{ log.ip_address || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>

    <Toast />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import { authAPI, adminAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const sidebarCollapsed = ref(false)
const logs = ref([])
const users = ref([])
const loading = ref(false)
const filters = ref({ action: '', user_id: '' })

const load = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.value.action) params.action = filters.value.action
    if (filters.value.user_id) params.user_id = filters.value.user_id

    const { data } = await authAPI.getAuditLogs(params)
    logs.value = Array.isArray(data) ? data : []
  } catch (err) {
    if (err.response?.status === 403) {
      toast.error('Accès réservé au SuperIT')
      router.push('/dashboard')
    } else {
      toast.error('Impossible de charger le journal')
    }
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  try {
    const { data } = await adminAPI.getUsers()
    users.value = Array.isArray(data) ? data : []
  } catch {
    logger.warn('Impossible de charger les utilisateurs')
  }
}

const actionIcon = (action) => ({
  CREATE: 'fas fa-plus-circle',
  UPDATE: 'fas fa-edit',
  DELETE: 'fas fa-trash',
  LOGIN: 'fas fa-sign-in-alt',
  LOGOUT: 'fas fa-sign-out-alt',
  LOGIN_FAILED: 'fas fa-exclamation-triangle',
  SYNC: 'fas fa-sync-alt',
  EXPORT: 'fas fa-download',
}[action] || 'fas fa-circle')

const isIT = (log) => log.user_email?.includes('it') || false

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2)
}

const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleString('fr-FR', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

const hasDetails = (log) => log.details && Object.keys(log.details).length > 0

const formatDetails = (details) => {
  if (!details) return ''
  if (details.changes) {
    return Object.entries(details.changes)
      .map(([k, v]) => `${k}: ${v.old} → ${v.new}`)
      .join(', ')
  }
  return Object.entries(details)
    .filter(([, v]) => typeof v !== 'object')
    .map(([k, v]) => `${k}: ${v}`)
    .join(', ')
}

const handleLogout = async () => {
  await auth.logout()
  router.push('/it-login')
}

onMounted(() => {
  if (!auth.isSuperIT) {
    router.push('/dashboard')
    return
  }
  loadUsers()
  load()
})
</script>

<style scoped>
.audit-layout { min-height: 100vh; background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); font-family: 'Inter', system-ui, sans-serif; }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.filters-bar { display: flex; gap: 12px; padding: 14px 18px; background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; margin-bottom: 20px; flex-wrap: wrap; align-items: center; }
.filter-select { padding: 10px 14px; border: 1.5px solid rgba(255, 255, 255, 0.1); border-radius: 10px; font-size: 13.5px; background: rgba(255, 255, 255, 0.04); color: #fff; cursor: pointer; }
.filter-select option { background: #1e1b4b; }
.result-count { font-size: 12.5px; color: #94a3b8; padding: 6px 14px; background: rgba(255, 255, 255, 0.04); border-radius: 20px; }
.result-count i { color: #818cf8; margin-right: 4px; }

.loading-block, .empty-block { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 60px 20px; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid rgba(255, 255, 255, 0.15); border-top-color: #818cf8; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-block p { color: #94a3b8; }
.empty-block i { font-size: 48px; color: #6366f1; margin-bottom: 12px; display: block; }
.empty-block h3 { color: #fff; margin: 0; }

.logs-table-wrap { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; overflow: hidden; }
.logs-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.logs-table thead { background: rgba(255, 255, 255, 0.04); }
.logs-table th { padding: 12px 16px; text-align: left; font-weight: 600; color: #94a3b8; font-size: 12px; }
.logs-table td { padding: 12px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); vertical-align: middle; color: #cbd5e1; }
.logs-table tr:last-child td { border-bottom: none; }
.logs-table tr:hover { background: rgba(255, 255, 255, 0.02); }

.cell-date { color: #94a3b8; white-space: nowrap; font-size: 12px; }
.cell-user { display: flex; align-items: center; gap: 8px; }
.user-avatar-sm { width: 28px; height: 28px; border-radius: 50%; background: #10b981; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.user-avatar-sm.it { background: #6366f1; }

.action-badge { display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.action-badge.action-create { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.action-badge.action-update { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.action-badge.action-delete { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.action-badge.action-login { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.action-badge.action-logout { background: rgba(148, 163, 184, 0.15); color: #94a3b8; }
.action-badge.action-login_failed { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.action-badge.action-sync { background: rgba(99, 102, 241, 0.15); color: #818cf8; }

.cell-object .object-model { font-weight: 600; color: #cbd5e1; display: block; }
.cell-object .object-repr { font-size: 11.5px; color: #94a3b8; }
.cell-details { max-width: 250px; }
.details-text { font-size: 12px; color: #94a3b8; font-style: italic; }
.empty { color: #64748b; }
.cell-ip { font-family: monospace; font-size: 11.5px; color: #94a3b8; }

.btn-secondary, .btn-primary { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 9px; font-size: 13.5px; font-weight: 600; border: none; cursor: pointer; }
.btn-primary { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.1); }
.btn-secondary:hover:not(:disabled) { background: rgba(255, 255, 255, 0.1); }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .logs-table { font-size: 12px; }
  .logs-table th, .logs-table td { padding: 8px 10px; }
}
</style>
