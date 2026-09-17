<template>
  <div class="dashboard-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <!-- ============ TOP BAR ============ -->
      <TopBar
        :title="greeting"
        :subtitle="auth.isSuperIT ? 'Console SuperIT — Contrôle total' : 'Espace administrateur'"
        :icon="auth.isSuperIT ? 'fas fa-shield-alt' : 'fas fa-leaf'"
        :show-refresh="true"
        :loading="loading"
        @refresh="loadAll"
      >
        <template #actions>
          <div
            v-if="auth.isSuperIT"
            class="live-indicator"
            :title="`${onlineCount} admin(s) actif(s)`"
          >
            <span class="pulse"></span>
            <span>{{ onlineCount }} en ligne</span>
          </div>
        </template>
      </TopBar>

      <!-- ============ ONGLETS INTERNES ============ -->
      <nav class="dashboard-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="tab-btn"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          <i :class="tab.icon"></i>
          <span>{{ tab.label }}</span>
          <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
        </button>
      </nav>

      <!-- ============ CHARGEMENT ============ -->
      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <template v-else>
        <!-- ============================================================ -->
        <!-- ONGLET 1 : VUE D'ENSEMBLE                                     -->
        <!-- ============================================================ -->
        <div v-show="activeTab === 'overview'">
          <!-- ✅ CARTES DE STATISTIQUES -->
          <section class="stats-grid">
            <StatCard
              v-for="s in currentStats"
              :key="s.label"
              :value="s.value"
              :label="s.label"
              :icon="s.icon"
              :color="s.color"
            />
          </section>

          <!-- Actions rapides -->
          <section class="quick-actions" :class="{ 'superit-actions': auth.isSuperIT }">
            <div class="section-head">
              <h2><i class="fas fa-bolt"></i> Actions rapides</h2>
            </div>
            <div class="actions-grid">
              <router-link
                v-for="action in quickActions"
                :key="action.to"
                :to="action.to"
                class="action-card"
              >
                <i :class="action.icon"></i>
                <div>
                  <span class="action-title">{{ action.title }}</span>
                  <span class="action-desc">{{ action.desc }}</span>
                </div>
              </router-link>
            </div>
          </section>

          <!-- Vue d'ensemble du contenu — SUPERIT UNIQUEMENT -->
          <section v-if="auth.isSuperIT" class="panel content-overview">
            <div class="panel-head">
              <h3><i class="fas fa-layer-group"></i> Vue d'ensemble du contenu</h3>
            </div>
            <div class="content-grid">
              <router-link to="/plantes" class="content-item">
                <i class="fas fa-leaf"></i>
                <span class="content-value">{{ stats.total_plantes || 0 }}</span>
                <span class="content-label">Plantes</span>
              </router-link>
              <router-link to="/projets" class="content-item">
                <i class="fas fa-project-diagram"></i>
                <span class="content-value">{{ stats.total_projets || 0 }}</span>
                <span class="content-label">Projets</span>
              </router-link>
              <router-link to="/activites" class="content-item">
                <i class="fas fa-chart-line"></i>
                <span class="content-value">{{ stats.total_activites || 0 }}</span>
                <span class="content-label">Activités</span>
              </router-link>
              <router-link to="/publications" class="content-item">
                <i class="fas fa-book"></i>
                <span class="content-value">{{ stats.total_publications || 0 }}</span>
                <span class="content-label">Publications</span>
              </router-link>
              <router-link to="/equipe" class="content-item">
                <i class="fas fa-users"></i>
                <span class="content-value">{{ stats.total_equipe || 0 }}</span>
                <span class="content-label">Équipe</span>
              </router-link>
              <router-link to="/partenaires" class="content-item">
                <i class="fas fa-handshake"></i>
                <span class="content-value">{{ stats.total_partenaires || 0 }}</span>
                <span class="content-label">Partenaires</span>
              </router-link>
            </div>
          </section>

          <!-- Bandeau bienvenue — ADMIN UNIQUEMENT -->
          <section v-else class="welcome-card">
            <i class="fas fa-info-circle"></i>
            <div>
              <h3>{{ greeting }}, content de vous revoir</h3>
              <p>
                Vous pouvez gérer les <strong>plantes</strong>, <strong>projets</strong>,
                <strong>activités</strong> et <strong>publications</strong>.
                Chaque modification est tracée automatiquement.
              </p>
            </div>
          </section>
        </div>

        <!-- ============================================================ -->
        <!-- ONGLET 2 : ACTIVITÉ                                           -->
        <!-- ============================================================ -->
        <div v-show="activeTab === 'activity'">
          <!-- Alertes (SuperIT) -->
          <section v-if="auth.isSuperIT && alerts.length" class="alerts-panel">
            <div class="alert-head">
              <i class="fas fa-exclamation-triangle"></i>
              <h3>Alertes de sécurité ({{ alerts.length }})</h3>
            </div>
            <ul class="alert-list">
              <li v-for="alert in alerts" :key="alert.id" class="alert-item">
                <i :class="alert.icon"></i>
                <span>{{ alert.message }}</span>
                <span class="alert-time">{{ formatRelativeTime(alert.created_at) }}</span>
              </li>
            </ul>
          </section>

          <!-- Graphique 7 jours (SuperIT) -->
          <section v-if="auth.isSuperIT" class="panel chart-panel">
            <div class="panel-head">
              <h3><i class="fas fa-chart-area"></i> Activité des 7 derniers jours</h3>
            </div>
            <div class="chart-wrap">
              <div
                v-for="(bar, i) in weeklyActivity"
                :key="i"
                class="chart-bar"
                :title="`${bar.count} action(s) le ${bar.day}`"
              >
                <div class="bar-value">{{ bar.count }}</div>
                <div class="bar-track">
                  <div
                    class="bar-fill"
                    :style="{ height: `${(bar.count / maxWeekly) * 100}%` }"
                  ></div>
                </div>
                <div class="bar-label">{{ bar.day }}</div>
              </div>
            </div>
          </section>

          <!-- 2 colonnes (SuperIT) -->
          <div v-if="auth.isSuperIT" class="two-columns">
            <section class="panel">
              <div class="panel-head">
                <h3><i class="fas fa-stream"></i> Dernières actions</h3>
                <router-link to="/audit" class="link-see-all">Voir tout →</router-link>
              </div>
              <ul v-if="recentActivities.length" class="activity-list">
                <li v-for="log in recentActivities" :key="log.id" class="activity-item">
                  <div class="activity-icon" :class="log.action.toLowerCase()">
                    <i :class="actionIcon(log.action)"></i>
                  </div>
                  <div class="activity-body">
                    <p class="activity-message">
                      <strong>{{ log.user_nom || 'Système' }}</strong>
                      · {{ log.action_label }}
                      <span v-if="log.object_repr" class="activity-obj">
                        : {{ log.object_repr }}
                      </span>
                    </p>
                    <span class="activity-time">
                      {{ formatRelativeTime(log.created_at) }}
                    </span>
                  </div>
                </li>
              </ul>
              <p v-else class="empty-text">Aucune action récente</p>
            </section>

            <section class="panel">
              <div class="panel-head">
                <h3><i class="fas fa-users"></i> Administrateurs en ligne</h3>
                <router-link to="/administrateurs" class="link-see-all">Gérer →</router-link>
              </div>
              <ul v-if="admins.length" class="admin-list">
                <li
                  v-for="a in admins.slice(0, 5)"
                  :key="a.id"
                  class="admin-item"
                  :class="{ online: isOnline(a) }"
                >
                  <div class="admin-avatar" :class="{ super: a.role === 'it_admin' }">
                    {{ getInitials(a.nom) }}
                    <span v-if="isOnline(a)" class="online-dot"></span>
                  </div>
                  <div class="admin-info">
                    <span class="admin-name">{{ a.nom }}</span>
                    <span class="admin-role">
                      {{ a.role === 'it_admin' ? 'SuperIT' : 'Admin' }}
                      <span v-if="isOnline(a)" class="online-label">· En ligne</span>
                    </span>
                  </div>
                  <span class="admin-status" :class="a.is_active ? 'active' : 'inactive'">
                    {{ a.is_active ? 'Actif' : 'Inactif' }}
                  </span>
                </li>
              </ul>
              <p v-else class="empty-text">Aucun administrateur</p>
            </section>
          </div>

          <!-- Mes activités — ADMIN UNIQUEMENT -->
          <section v-else class="panel my-activity-panel">
            <div class="panel-head">
              <h3><i class="fas fa-user-clock"></i> Mes dernières actions</h3>
            </div>
            <ul v-if="myActivities.length" class="activity-list">
              <li v-for="log in myActivities" :key="log.id" class="activity-item">
                <div class="activity-icon" :class="log.action.toLowerCase()">
                  <i :class="actionIcon(log.action)"></i>
                </div>
                <div class="activity-body">
                  <p class="activity-message">
                    {{ log.action_label }}
                    <span v-if="log.object_repr" class="activity-obj">
                      : {{ log.object_repr }}
                    </span>
                  </p>
                  <span class="activity-time">
                    {{ formatRelativeTime(log.created_at) }}
                  </span>
                </div>
              </li>
            </ul>
            <p v-else class="empty-text">
              Aucune activité récente. Commencez par créer du contenu.
            </p>
          </section>
        </div>
      </template>
    </main>

    <Toast />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import StatCard from '../components/StatCard.vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { adminApi, adminAPI, authAPI } from '../utils/api'
import { logger } from '../utils/logger'
import { getGreetingFor } from '../utils/greeting'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const sidebarCollapsed = ref(false)
const loading = ref(false)
const activeTab = ref('overview')

const tabs = computed(() => ([
  { id: 'overview', label: "Vue d'ensemble", icon: 'fas fa-th-large' },
  { id: 'activity', label: 'Activité',       icon: 'fas fa-wave-square' },
]))

const stats = ref({})
const recentActivities = ref([])
const myActivities = ref([])
const admins = ref([])
const onlineUsers = ref([])
const alerts = ref([])
let refreshInterval = null

const greeting = computed(() => getGreetingFor(auth.user))

/* ============================================================
   STATS — SUPERIT (8 cartes) vs ADMIN (4 cartes)
   ============================================================ */
const superitStats = computed(() => [
  { label: 'Plantes',         value: stats.value.total_plantes ?? 0,        icon: 'fas fa-leaf',            color: 'green' },
  { label: 'Projets',         value: stats.value.total_projets ?? 0,        icon: 'fas fa-project-diagram', color: 'purple' },
  { label: 'Activités',       value: stats.value.total_activites ?? 0,      icon: 'fas fa-chart-line',      color: 'orange' },
  { label: 'Publications',    value: stats.value.total_publications ?? 0,   icon: 'fas fa-book',            color: 'blue' },
  { label: 'Équipe',          value: stats.value.total_equipe ?? 0,         icon: 'fas fa-users',           color: 'teal' },
  { label: 'Partenaires',     value: stats.value.total_partenaires ?? 0,    icon: 'fas fa-handshake',       color: 'amber' },
  { label: 'Administrateurs', value: admins.value.length,                   icon: 'fas fa-users-cog',       color: 'indigo' },
  { label: 'En ligne',        value: onlineCount.value,                     icon: 'fas fa-signal',          color: 'red' },
])

// ✅ Admin : uniquement le contenu qu'il gère (ni équipe, ni partenaires, ni admins)
const adminStats = computed(() => [
  { label: 'Plantes',      value: stats.value.total_plantes ?? 0,      icon: 'fas fa-leaf',            color: 'green' },
  { label: 'Projets',      value: stats.value.total_projets ?? 0,      icon: 'fas fa-project-diagram', color: 'purple' },
  { label: 'Activités',    value: stats.value.total_activites ?? 0,    icon: 'fas fa-chart-line',      color: 'orange' },
  { label: 'Publications', value: stats.value.total_publications ?? 0, icon: 'fas fa-book',            color: 'blue' },
])

const currentStats = computed(() => (auth.isSuperIT ? superitStats.value : adminStats.value))
const onlineCount = computed(() => onlineUsers.value.length)

const quickActions = computed(() => {
  if (auth.isSuperIT) {
    return [
      { to: '/administrateurs', title: 'Nouvel admin',       desc: 'Créer un compte',    icon: 'fas fa-user-plus' },
      { to: '/audit',           title: "Journal d'audit",    desc: 'Toutes les actions', icon: 'fas fa-history' },
      { to: '/maintenance',     title: 'Maintenance',        desc: 'Backup & export',    icon: 'fas fa-tools' },
      { to: '/herbier-data',    title: 'Synchronisation',    desc: 'Site public',        icon: 'fas fa-database' },
    ]
  }
  return [
    { to: '/plantes',       title: 'Plantes',       desc: `${stats.value.total_plantes || 0} enregistrées`,  icon: 'fas fa-leaf' },
    { to: '/projets',       title: 'Projets',       desc: `${stats.value.total_projets || 0} actifs`,        icon: 'fas fa-project-diagram' },
    { to: '/activites',     title: 'Activités',     desc: `${stats.value.total_activites || 0} publiées`,    icon: 'fas fa-chart-line' },
    { to: '/publications',  title: 'Publications',  desc: `${stats.value.total_publications || 0} articles`, icon: 'fas fa-book' },
  ]
})

const weeklyActivity = computed(() => {
  const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
  const result = []
  for (let i = 6; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    const dayIndex = (date.getDay() + 6) % 7
    const dayLabel = days[dayIndex]
    const dayStr = date.toISOString().slice(0, 10)
    const count = recentActivities.value.filter((a) => a.created_at?.startsWith(dayStr)).length
    result.push({ day: dayLabel, count })
  }
  return result
})

const maxWeekly = computed(() => Math.max(...weeklyActivity.value.map((b) => b.count), 1))

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2)
}

const isOnline = (admin) => onlineUsers.value.some((u) => u.id === admin.id)

const actionIcon = (action) => ({
  CREATE: 'fas fa-plus-circle', UPDATE: 'fas fa-edit', DELETE: 'fas fa-trash',
  LOGIN: 'fas fa-sign-in-alt', LOGOUT: 'fas fa-sign-out-alt',
  LOGIN_FAILED: 'fas fa-exclamation-triangle', SYNC: 'fas fa-sync-alt', EXPORT: 'fas fa-download',
}[action] || 'fas fa-circle')

const formatRelativeTime = (d) => {
  if (!d) return ''
  const diff = (Date.now() - new Date(d).getTime()) / 1000
  if (diff < 60) return "à l'instant"
  if (diff < 3600) return `il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `il y a ${Math.floor(diff / 3600)} h`
  if (diff < 604800) return `il y a ${Math.floor(diff / 86400)} j`
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

const maskEmail = (email) => {
  if (!email) return 'inconnu'
  const [user, domain] = email.split('@')
  if (!domain) return 'inconnu'
  return `${user.slice(0, 2)}***@${domain}`
}

/* ============================================================
   CHARGEMENTS
   ============================================================ */
const loadStats = async () => {
  try {
    const { data } = await adminApi.get('/stats/')
    stats.value = data
  } catch {
    logger.warn('Erreur stats')
  }
}

const loadRecentActivities = async () => {
  if (!auth.isSuperIT) return
  try {
    const { data } = await adminAPI.getAuditLogs({ limit: 50 })
    recentActivities.value = Array.isArray(data) ? data : []
  } catch {
    logger.warn('Erreur audit')
  }
}

const loadMyActivities = async () => {
  if (auth.isSuperIT) return
  try {
    const { data } = await adminApi.get('/me/activity/', { params: { limit: 10 } })
    myActivities.value = Array.isArray(data) ? data : []
  } catch {
    logger.warn('Erreur mes activités')
  }
}

const loadAdmins = async () => {
  if (!auth.isSuperIT) return
  try {
    const { data } = await adminAPI.getUsers()
    admins.value = Array.isArray(data) ? data : []
    const thirtyMinAgo = Date.now() - 30 * 60 * 1000
    onlineUsers.value = admins.value.filter(
      (a) => a.last_login && new Date(a.last_login).getTime() > thirtyMinAgo
    )
  } catch {
    logger.warn('Erreur admins')
  }
}

const loadAlerts = async () => {
  if (!auth.isSuperIT) return
  try {
    const { data } = await adminAPI.getAuditLogs({ action: 'LOGIN_FAILED', limit: 5 })
    alerts.value = (Array.isArray(data) ? data : []).map((log) => ({
      id: log.id,
      level: 'danger',
      icon: 'fas fa-exclamation-triangle',
      message: `Tentative de connexion échouée : ${maskEmail(log.details?.email)}`,
      created_at: log.created_at,
    }))
  } catch {
    logger.warn('Erreur alertes')
  }
}

const loadAll = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadStats(),
      loadRecentActivities(),
      loadMyActivities(),
      loadAdmins(),
      loadAlerts(),
    ])
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  await auth.logout()
  router.push(auth.isSuperIT ? '/it-login' : '/admin-login')
}

onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/it-login')
    return
  }
  loadAll()
  if (auth.isSuperIT) {
    refreshInterval = setInterval(() => {
      loadRecentActivities()
      loadAdmins()
      loadAlerts()
    }, 30000)
  }
})

onBeforeUnmount(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<style scoped>
/* ============================================================
   ONGLETS INTERNES
   ============================================================ */
.dashboard-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 6px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow-x: auto;
}
.superit-theme .dashboard-tabs {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  border-radius: 10px;
  border: none;
  background: none;
  font-family: inherit;
  font-size: 13.5px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.tab-btn i { font-size: 14px; }
.tab-btn:hover { background: #f8fafc; color: #0f172a; }
.superit-theme .tab-btn { color: #94a3b8; }
.superit-theme .tab-btn:hover { background: rgba(255, 255, 255, 0.06); color: #fff; }
.tab-btn.active { background: #ecfdf5; color: #059669; }
.superit-theme .tab-btn.active { background: rgba(99, 102, 241, 0.15); color: #c7d2fe; }
.tab-badge {
  font-size: 10px;
  background: #f59e0b;
  color: #1a1a1a;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 700;
}

/* ============================================================
   LAYOUT
   ============================================================ */
.dashboard-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

/* ============================================================
   LOADING
   ============================================================ */
.loading-block { background: rgba(255, 255, 255, 0.05); border-radius: 14px; padding: 80px 20px; text-align: center; }
.superit-theme .loading-block { border: 1px solid rgba(255, 255, 255, 0.1); }
.spinner {
  width: 44px; height: 44px;
  border: 3px solid rgba(255, 255, 255, 0.15);
  border-top-color: #818cf8;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-block p { color: #94a3b8; margin: 0; }

/* ============================================================
   ALERTES
   ============================================================ */
.alerts-panel {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 20px;
}
.alert-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.alert-head i { color: #ef4444; font-size: 18px; }
.alert-head h3 { font-size: 14px; color: #fecaca; margin: 0; font-weight: 700; }
.alert-list { list-style: none; padding: 0; margin: 0; }
.alert-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(239, 68, 68, 0.1);
  font-size: 13px; color: #fca5a5;
}
.alert-item:last-child { border-bottom: none; }
.alert-item i { color: #ef4444; font-size: 13px; }
.alert-time { margin-left: auto; font-size: 11px; color: #f87171; opacity: 0.7; }

/* ============================================================
   STATS
   ============================================================ */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }

/* ============================================================
   PANELS
   ============================================================ */
.panel {
  background: #fff;
  border-radius: 14px;
  padding: 20px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
}
.superit-theme .panel {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.panel-head {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px; padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
.superit-theme .panel-head { border-bottom-color: rgba(255, 255, 255, 0.08); }
.panel-head h3 {
  font-size: 14.5px; color: #0f172a; margin: 0; font-weight: 700;
  display: flex; align-items: center; gap: 8px;
}
.superit-theme .panel-head h3 { color: #e2e8f0; }
.superit-theme .panel-head h3 i { color: #818cf8; }
.link-see-all { font-size: 12.5px; color: #10b981; text-decoration: none; font-weight: 600; }
.superit-theme .link-see-all { color: #818cf8; }

/* ============================================================
   GRAPHIQUE
   ============================================================ */
.chart-panel { margin-bottom: 20px; }
.chart-wrap {
  display: flex; align-items: flex-end; justify-content: space-between;
  gap: 12px; height: 180px; padding: 10px 0;
}
.chart-bar {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  gap: 6px; height: 100%; justify-content: flex-end; cursor: help;
}
.bar-value { font-size: 11px; font-weight: 700; color: #818cf8; }
.bar-track {
  width: 100%; flex: 1;
  background: rgba(99, 102, 241, 0.08);
  border-radius: 6px 6px 0 0;
  display: flex; align-items: flex-end; overflow: hidden;
}
.bar-fill {
  width: 100%;
  background: linear-gradient(180deg, #818cf8, #6366f1);
  border-radius: 6px 6px 0 0;
  transition: height 0.4s ease;
  min-height: 4px;
}
.bar-label { font-size: 11px; color: #94a3b8; font-weight: 500; }

/* ============================================================
   ACTIONS RAPIDES
   ============================================================ */
.quick-actions {
  background: #fff; border-radius: 14px;
  padding: 20px 24px; margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.superit-theme .quick-actions {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.section-head { margin-bottom: 16px; }
.section-head h2 {
  font-size: 16px; color: #0f172a; margin: 0; font-weight: 700;
  display: flex; align-items: center; gap: 8px;
}
.superit-theme .section-head h2 { color: #e2e8f0; }
.superit-theme .section-head h2 i { color: #facc15; }
.actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.action-card {
  display: flex; align-items: center; gap: 14px;
  padding: 16px 18px; border-radius: 12px;
  background: #f8fafc; border: 1px solid #e2e8f0;
  color: #334155; text-decoration: none; transition: all 0.15s;
}
.action-card:hover {
  background: #ecfdf5; border-color: #10b981;
  color: #059669; transform: translateY(-2px);
}
.action-card i { font-size: 20px; color: #10b981; flex-shrink: 0; }
.action-card > div { display: flex; flex-direction: column; }
.action-title { font-size: 13.5px; font-weight: 600; line-height: 1.2; }
.action-desc { font-size: 11.5px; color: #64748b; margin-top: 2px; }
.superit-actions .action-card {
  background: rgba(99, 102, 241, 0.08);
  border-color: rgba(99, 102, 241, 0.2);
  color: #c7d2fe;
}
.superit-actions .action-card:hover {
  background: rgba(99, 102, 241, 0.18);
  border-color: #818cf8;
  color: #e0e7ff; transform: translateY(-2px);
}
.superit-actions .action-card i { color: #818cf8; }
.superit-actions .action-desc { color: #a5b4fc; }

/* ============================================================
   TWO COLUMNS
   ============================================================ */
.two-columns { display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; margin-bottom: 20px; }
@media (max-width: 1024px) { .two-columns { grid-template-columns: 1fr; } }

/* ============================================================
   ACTIVITÉS
   ============================================================ */
.activity-list { list-style: none; padding: 0; margin: 0; }
.activity-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}
.superit-theme .activity-item { border-bottom-color: rgba(255, 255, 255, 0.05); }
.activity-item:last-child { border-bottom: none; }
.activity-icon {
  width: 34px; height: 34px;
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; font-size: 13px;
}
.activity-icon.create { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.activity-icon.update { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.activity-icon.delete { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.activity-icon.login { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.activity-icon.login_failed { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.activity-icon.sync { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.activity-body { flex: 1; min-width: 0; }
.activity-message { font-size: 13px; color: #334155; margin: 0; line-height: 1.4; }
.superit-theme .activity-message { color: #cbd5e1; }
.activity-message strong { color: #0f172a; font-weight: 600; }
.superit-theme .activity-message strong { color: #fff; }
.activity-obj { color: #64748b; font-style: italic; }
.superit-theme .activity-obj { color: #94a3b8; }
.activity-time { font-size: 11px; color: #94a3b8; margin-top: 2px; display: block; }

/* ============================================================
   ADMINS
   ============================================================ */
.admin-list { list-style: none; padding: 0; margin: 0; }
.admin-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}
.superit-theme .admin-item { border-bottom-color: rgba(255, 255, 255, 0.05); }
.admin-item:last-child { border-bottom: none; }
.admin-avatar {
  position: relative; width: 38px; height: 38px; border-radius: 50%;
  background: linear-gradient(135deg, #64748b, #475569);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px; flex-shrink: 0;
}
.admin-avatar.super { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.online-dot {
  position: absolute; bottom: 0; right: 0;
  width: 11px; height: 11px; background: #10b981;
  border: 2px solid #1e1b4b; border-radius: 50%;
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
  50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
}
.admin-info { flex: 1; min-width: 0; }
.admin-name { font-size: 13.5px; font-weight: 600; color: #0f172a; display: block; }
.superit-theme .admin-name { color: #fff; }
.admin-role { font-size: 11.5px; color: #64748b; display: block; margin-top: 1px; }
.superit-theme .admin-role { color: #94a3b8; }
.online-label { color: #10b981; font-weight: 600; }
.admin-status { font-size: 10.5px; padding: 3px 8px; border-radius: 10px; font-weight: 600; flex-shrink: 0; }
.admin-status.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.admin-status.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

/* ============================================================
   CONTENT OVERVIEW
   ============================================================ */
.content-overview { margin-bottom: 20px; }
.content-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; }
.content-item {
  display: flex; flex-direction: column; align-items: center;
  padding: 18px 12px; background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px; text-decoration: none; transition: all 0.15s;
}
.content-item:hover {
  background: rgba(99, 102, 241, 0.12);
  border-color: #818cf8; transform: translateY(-2px);
}
.content-item i { font-size: 22px; color: #818cf8; margin-bottom: 8px; }
.content-value { font-size: 24px; font-weight: 700; color: #fff; line-height: 1; }
.content-label { font-size: 11.5px; color: #94a3b8; margin-top: 4px; font-weight: 500; }

/* ============================================================
   WELCOME (Admin)
   ============================================================ */
.welcome-card {
  display: flex; gap: 16px; align-items: flex-start;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  border-radius: 14px; padding: 20px 24px; margin-bottom: 20px;
  border-left: 4px solid #10b981;
}
.welcome-card i { font-size: 26px; color: #059669; flex-shrink: 0; margin-top: 2px; }
.welcome-card h3 { font-size: 15px; color: #0f172a; margin: 0 0 6px; font-weight: 700; }
.welcome-card p { font-size: 13px; color: #475569; margin: 0; line-height: 1.5; }
.welcome-card strong { color: #059669; }
.my-activity-panel { margin-bottom: 20px; }

/* ============================================================
   LIVE INDICATOR
   ============================================================ */
.live-indicator {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px; background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 20px; font-size: 12.5px; font-weight: 600;
  color: #10b981; cursor: help;
}
.pulse {
  width: 8px; height: 8px; background: #10b981;
  border-radius: 50%; animation: pulse-live 1.5s infinite;
}
@keyframes pulse-live {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

/* ============================================================
   EMPTY
   ============================================================ */
.empty-text { text-align: center; color: #94a3b8; font-size: 13px; padding: 24px 0; margin: 0; }

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .actions-grid { grid-template-columns: 1fr; }
  .content-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>