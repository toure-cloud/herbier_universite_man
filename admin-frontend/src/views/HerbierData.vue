<template>
  <div class="herbier-layout">
    <Sidebar
      :user="auth.user"
      :is-super-it="true"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Données de l'Herbier"
        subtitle="Synchronisation avec le site public (SuperIT)"
        icon="fas fa-database"
      >
        <template #actions>
          <button class="btn-secondary" @click="refresh" :disabled="loading">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
            Rafraîchir
          </button>
          <button class="btn-primary" @click="syncNow" :disabled="syncing">
            <i class="fas fa-cloud-upload-alt" :class="{ 'fa-spin': syncing }"></i>
            {{ syncing ? 'Synchronisation…' : 'Synchroniser' }}
          </button>
        </template>
      </TopBar>

      <section class="overview-grid">
        <div v-for="s in overview" :key="s.key" class="overview-card">
          <div class="ov-icon" :class="s.color"><i :class="s.icon"></i></div>
          <div class="ov-body">
            <span class="ov-value">{{ s.count }}</span>
            <span class="ov-label">{{ s.label }}</span>
          </div>
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else class="data-sections">
        <article v-for="section in sections" :key="section.key" class="data-card">
          <header class="data-card-header">
            <div class="header-left">
              <i :class="section.icon"></i>
              <h3>{{ section.label }}</h3>
            </div>
            <span class="badge">{{ (section.items || []).length }}</span>
          </header>

          <div class="data-preview">
            <div v-if="!section.items?.length" class="preview-empty">
              <i class="fas fa-inbox"></i>
              <p>Aucune donnée</p>
            </div>
            <ul v-else class="preview-list">
              <li v-for="(item, i) in section.items.slice(0, 5)" :key="item.id ?? i">
                <span class="preview-name">{{ previewName(item, section.key) }}</span>
                <span class="preview-extra">{{ previewExtra(item, section.key) }}</span>
              </li>
              <li v-if="section.items.length > 5" class="preview-more">
                + {{ section.items.length - 5 }} autre(s)
              </li>
            </ul>
          </div>
        </article>
      </section>

      <section class="sync-history">
        <div class="sync-head">
          <i class="fas fa-history"></i>
          <h3>Dernière synchronisation</h3>
        </div>
        <div class="sync-body">
          <span v-if="lastSync" class="sync-date">
            <i class="fas fa-check-circle"></i> {{ lastSync }}
          </span>
          <span v-else class="sync-empty">
            <i class="fas fa-clock"></i> Jamais synchronisé
          </span>
        </div>

        <div v-if="syncing" class="progress-wrap">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
          </div>
          <span class="progress-label">{{ progress }}%</span>
        </div>
      </section>
    </main>

    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { adminApi, publicApi } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const loading = ref(false)
const syncing = ref(false)
const progress = ref(0)
const lastSync = ref(localStorage.getItem('last_sync_date') || '')

const data = ref({
  plantes: [], equipe: [], partenaires: [], slides: [],
  projets: [], activites: [], temoignages: [],
  publications: [], faqs: [], statistiques: [], methodologie: [],
})

const sections = computed(() => [
  { key: 'plantes', label: 'Plantes', icon: 'fas fa-leaf', items: data.value.plantes },
  { key: 'equipe', label: 'Équipe', icon: 'fas fa-users', items: data.value.equipe },
  { key: 'partenaires', label: 'Partenaires', icon: 'fas fa-handshake', items: data.value.partenaires },
  { key: 'projets', label: 'Projets', icon: 'fas fa-project-diagram', items: data.value.projets },
  { key: 'activites', label: 'Activités', icon: 'fas fa-chart-line', items: data.value.activites },
  { key: 'temoignages', label: 'Témoignages', icon: 'fas fa-comment-dots', items: data.value.temoignages },
  { key: 'publications', label: 'Publications', icon: 'fas fa-book', items: data.value.publications },
  { key: 'faqs', label: 'FAQs', icon: 'fas fa-question-circle', items: data.value.faqs },
  { key: 'statistiques', label: 'Statistiques', icon: 'fas fa-chart-bar', items: data.value.statistiques },
])

const overview = computed(() =>
  [
    { key: 'plantes', label: 'Plantes', icon: 'fas fa-leaf', color: 'green' },
    { key: 'equipe', label: 'Équipe', icon: 'fas fa-users', color: 'blue' },
    { key: 'partenaires', label: 'Partenaires', icon: 'fas fa-handshake', color: 'teal' },
    { key: 'projets', label: 'Projets', icon: 'fas fa-project-diagram', color: 'purple' },
    { key: 'publications', label: 'Publications', icon: 'fas fa-book', color: 'orange' },
    { key: 'temoignages', label: 'Témoignages', icon: 'fas fa-comment-dots', color: 'pink' },
  ].map((s) => ({ ...s, count: (data.value[s.key] || []).length }))
)

const previewName = (item, key) => {
  if (key === 'publications') return item.titre || '—'
  if (key === 'faqs') return item.question || '—'
  return item.nom || item.titre || '—'
}

const previewExtra = (item, key) => {
  if (key === 'plantes') return item.famille || ''
  if (key === 'equipe') return item.poste || ''
  if (key === 'partenaires') return item.type || ''
  if (key === 'projets') return item.categorie || ''
  if (key === 'publications') return item.annee || ''
  if (key === 'temoignages') return item.organisation || ''
  return ''
}

const refresh = async () => {
  loading.value = true
  try {
    const endpoints = [
      ['plantes', 'plantes'], ['equipe', 'equipe'], ['partenaires', 'partenaires'],
      ['projets', 'projets'], ['activites', 'activites'], ['temoignages', 'temoignages'],
      ['publications', 'publications'], ['faqs', 'faqs'],
      ['statistiques', 'statistiques'], ['methodologie', 'methodologie'],
    ]

    const results = await Promise.allSettled(
      endpoints.map(([, path]) => adminApi.get(`/${path}/`))
    )

    endpoints.forEach(([key], i) => {
      const res = results[i]
      if (res.status === 'fulfilled') {
        const payload = res.value.data
        data.value[key] = Array.isArray(payload) ? payload : payload.results || []
      } else {
        data.value[key] = []
      }
    })
  } catch {
    toast.error('Impossible de charger les données')
  } finally {
    loading.value = false
  }
}

const syncNow = async () => {
  const ok = await askConfirm({
    title: 'Synchroniser',
    message: 'Pousser toutes les données vers le site public ?',
  })
  if (!ok) return

  syncing.value = true
  progress.value = 0

  const tick = setInterval(() => {
    if (progress.value < 90) progress.value += Math.random() * 15
    if (progress.value > 90) progress.value = 90
  }, 200)

  try {
    await adminApi.post('/sync-all/', { source: 'admin' })

    try {
      await publicApi.post('/sync-herbier-data/', {
        ...data.value,
        sync_date: new Date().toISOString(),
      })
    } catch {
      logger.warn('Sync public API échoué, admin OK')
    }

    progress.value = 100
    const now = new Date().toLocaleString('fr-FR')
    lastSync.value = now
    localStorage.setItem('last_sync_date', now)
    toast.success('Synchronisation réussie')
  } catch {
    toast.error('Erreur lors de la synchronisation')
  } finally {
    clearInterval(tick)
    setTimeout(() => {
      syncing.value = false
      progress.value = 0
    }, 800)
  }
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
  refresh()
})
</script>

<style scoped>
.herbier-layout { min-height: 100vh; background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); font-family: 'Inter', system-ui, sans-serif; }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.overview-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-bottom: 24px; }
.overview-card { display: flex; align-items: center; gap: 12px; padding: 14px 16px; background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; transition: transform 0.15s; }
.overview-card:hover { transform: translateY(-2px); }
.ov-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.ov-icon.green { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.ov-icon.blue { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.ov-icon.teal { background: rgba(20, 184, 166, 0.15); color: #14b8a6; }
.ov-icon.purple { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }
.ov-icon.orange { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.ov-icon.pink { background: rgba(236, 72, 153, 0.15); color: #ec4899; }
.ov-body { display: flex; flex-direction: column; }
.ov-value { font-size: 22px; font-weight: 700; color: #fff; line-height: 1; }
.ov-label { font-size: 11.5px; color: #94a3b8; margin-top: 3px; }

.loading-block { background: rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 60px; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid rgba(255, 255, 255, 0.15); border-top-color: #818cf8; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-block p { color: #94a3b8; }

.data-sections { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px; }
.data-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; overflow: hidden; transition: all 0.15s; }
.data-card:hover { transform: translateY(-2px); border-color: rgba(129, 140, 248, 0.4); }
.data-card-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: rgba(255, 255, 255, 0.02); border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
.header-left { display: flex; align-items: center; gap: 10px; }
.header-left i { font-size: 15px; color: #818cf8; }
.header-left h3 { font-size: 13.5px; color: #fff; margin: 0; font-weight: 700; }
.badge { background: rgba(99, 102, 241, 0.15); color: #c7d2fe; font-weight: 700; padding: 3px 10px; border-radius: 20px; font-size: 11px; }
.data-preview { padding: 10px 16px 14px; }
.preview-empty { text-align: center; padding: 20px 0; color: #64748b; }
.preview-empty i { font-size: 24px; margin-bottom: 6px; display: block; }
.preview-empty p { margin: 0; font-size: 12px; }
.preview-list { list-style: none; padding: 0; margin: 0; }
.preview-list li { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.04); font-size: 12.5px; }
.preview-list li:last-child { border-bottom: none; }
.preview-name { color: #cbd5e1; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.preview-extra { color: #94a3b8; font-size: 11.5px; flex-shrink: 0; }
.preview-more { justify-content: center !important; color: #818cf8 !important; font-weight: 600; font-size: 11.5px; }

.sync-history { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px 22px; display: flex; flex-direction: column; gap: 12px; }
.sync-head { display: flex; align-items: center; gap: 10px; }
.sync-head i { color: #818cf8; font-size: 16px; }
.sync-head h3 { font-size: 14px; color: #fff; margin: 0; font-weight: 700; }
.sync-body { display: flex; align-items: center; gap: 8px; }
.sync-date { font-size: 13px; color: #10b981; display: inline-flex; align-items: center; gap: 6px; font-weight: 500; }
.sync-empty { font-size: 13px; color: #94a3b8; display: inline-flex; align-items: center; gap: 6px; }
.progress-wrap { display: flex; align-items: center; gap: 12px; margin-top: 4px; }
.progress-bar { flex: 1; height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #818cf8, #facc15); border-radius: 4px; transition: width 0.3s; }
.progress-label { font-size: 12px; font-weight: 700; color: #818cf8; min-width: 40px; text-align: right; }

.btn-primary, .btn-secondary { display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 9px; font-size: 13.5px; font-weight: 600; border: none; cursor: pointer; transition: all 0.15s; }
.btn-primary { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.1); }
.btn-secondary:hover:not(:disabled) { background: rgba(255, 255, 255, 0.1); }
.btn-secondary:disabled { opacity: 0.6; cursor: not-allowed; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .overview-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
