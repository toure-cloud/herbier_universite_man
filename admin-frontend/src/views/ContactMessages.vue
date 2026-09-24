<template>
  <div class="messages-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Messages de contact"
        subtitle="Consultez et gérez les messages reçus"
        icon="fas fa-envelope"
      >
        <template #actions>
          <button class="btn-refresh" @click="loadMessages" :disabled="loading">
            <i class="fas fa-sync-alt" :class="{ spinning: loading }"></i>
            Rafraîchir
          </button>
        </template>
      </TopBar>

      <!-- Stats -->
      <section class="stats-bar">
        <div class="stat-pill" :class="{ active: filter === 'all' }" @click="setFilter('all')">
          <i class="fas fa-inbox"></i>
          <span>Tous</span>
          <span class="stat-count">{{ stats.total }}</span>
        </div>
        <div class="stat-pill" :class="{ active: filter === 'unread' }" @click="setFilter('unread')">
          <i class="fas fa-envelope"></i>
          <span>Non lus</span>
          <span class="stat-count urgent">{{ stats.non_lus }}</span>
        </div>
        <div class="stat-pill" :class="{ active: filter === 'read' }" @click="setFilter('read')">
          <i class="fas fa-envelope-open"></i>
          <span>Lus</span>
          <span class="stat-count">{{ stats.total - stats.non_lus }}</span>
        </div>
      </section>

      <!-- Recherche -->
      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher par nom, email, message…" />
        </div>
      </section>

      <!-- Loading -->
      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement des messages…</p>
      </section>

      <!-- Empty -->
      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-envelope-open"></i>
        <h3>Aucun message</h3>
        <p>{{ emptyMessage }}</p>
      </section>

      <!-- Liste -->
      <section v-else class="messages-list">
        <article
          v-for="msg in filtered"
          :key="msg.id"
          class="message-card"
          :class="{ unread: !msg.lu }"
          @click="openMessage(msg)"
        >
          <div class="message-avatar" :class="{ unread: !msg.lu }">
            {{ getInitials(msg.nom) }}
          </div>

          <div class="message-body">
            <div class="message-header">
              <h3>{{ msg.nom }}</h3>
              <span v-if="!msg.lu" class="unread-dot"></span>
              <span class="message-date">{{ formatDate(msg.date_envoi) }}</span>
            </div>
            <p class="message-email">
              <i class="fas fa-envelope"></i> {{ msg.email }}
            </p>
            <div class="message-sujet">
              <i class="fas fa-tag"></i> {{ msg.sujet_label }}
            </div>
            <p class="message-preview">{{ truncate(msg.message, 130) }}</p>
          </div>

          <div class="message-actions" @click.stop>
            <button
              class="btn-icon"
              :title="msg.lu ? 'Marquer non lu' : 'Marquer lu'"
              @click="toggleRead(msg)"
            >
              <i :class="msg.lu ? 'fas fa-envelope' : 'fas fa-envelope-open'"></i>
            </button>
            <button class="btn-icon danger" title="Supprimer" @click="removeMessage(msg)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <!-- ==================== MODALE DÉTAIL ==================== -->
    <transition name="fade">
      <div v-if="selectedMessage" class="modal-overlay" @click.self="closeMessage">
        <div class="modal-box modal-large">
          <div class="modal-header">
            <div class="modal-title">
              <div class="modal-avatar" :class="{ unread: !selectedMessage.lu }">
                {{ getInitials(selectedMessage.nom) }}
              </div>
              <div>
                <h2>{{ selectedMessage.nom }}</h2>
                <span class="modal-subtitle">
                  <i class="fas fa-envelope"></i> {{ selectedMessage.email }}
                </span>
              </div>
            </div>
            <button class="close-btn" @click="closeMessage">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <div class="detail-row">
              <span class="detail-label">Téléphone</span>
              <span class="detail-value">{{ selectedMessage.telephone || '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Sujet</span>
              <span class="detail-value badge">{{ selectedMessage.sujet_label }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Date</span>
              <span class="detail-value">{{ formatDateFull(selectedMessage.date_envoi) }}</span>
            </div>

            <div class="detail-message">
              <h4><i class="fas fa-comment"></i> Message</h4>
              <p>{{ selectedMessage.message }}</p>
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-secondary" @click="closeMessage">
              Fermer
            </button>
            <a
              :href="`mailto:${selectedMessage.email}?subject=Re: ${selectedMessage.sujet_label}`"
              class="btn btn-primary"
              @click="markAsRead(selectedMessage)"
            >
              <i class="fas fa-reply"></i> Répondre
            </a>
          </div>
        </div>
      </div>
    </transition>

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
import { adminApi } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const messages = ref([])
const stats = ref({ total: 0, non_lus: 0 })
const loading = ref(false)
const filter = ref('all')
const search = ref('')
const selectedMessage = ref(null)

const filtered = computed(() => {
  let list = messages.value

  if (filter.value === 'unread') list = list.filter(m => !m.lu)
  if (filter.value === 'read')   list = list.filter(m => m.lu)

  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(m =>
      m.nom?.toLowerCase().includes(q) ||
      m.email?.toLowerCase().includes(q) ||
      m.message?.toLowerCase().includes(q)
    )
  }
  return list
})

const emptyMessage = computed(() => {
  if (search.value) return 'Aucun message ne correspond à votre recherche.'
  if (filter.value === 'unread') return 'Aucun message non lu.'
  if (filter.value === 'read')   return 'Aucun message lu.'
  return 'Vous n\'avez reçu aucun message pour le moment.'
})

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')

const formatDate = (iso) => {
  if (!iso) return ''
  const date = new Date(iso)
  const now = new Date()
  const diff = (now - date) / 1000

  if (diff < 60) return "À l'instant"
  if (diff < 3600) return `Il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `Il y a ${Math.floor(diff / 3600)} h`

  return date.toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'short',
    hour: '2-digit', minute: '2-digit'
  })
}

const formatDateFull = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

const loadStats = async () => {
  try {
    const { data } = await adminApi.get('/contact-messages/stats/')
    stats.value = data
  } catch (err) {
    logger.warn('Erreur stats messages', err)
  }
}

const loadMessages = async () => {
  loading.value = true
  try {
    const { data } = await adminApi.get('/contact-messages/')
    messages.value = Array.isArray(data) ? data : []
    await loadStats()
  } catch (err) {
    logger.warn('Erreur chargement messages', err)
    toast.error('Impossible de charger les messages')
  } finally {
    loading.value = false
  }
}

const setFilter = (value) => { filter.value = value }

const openMessage = async (msg) => {
  selectedMessage.value = msg
  document.body.style.overflow = 'hidden'
  if (!msg.lu) {
    await markAsRead(msg)
  }
}

const closeMessage = () => {
  selectedMessage.value = null
  document.body.style.overflow = ''
}

const markAsRead = async (msg) => {
  if (msg.lu) return
  try {
    await adminApi.patch(`/contact-messages/${msg.id}/`, { lu: true })
    msg.lu = true
    await loadStats()
  } catch (err) {
    logger.warn('Erreur marquage lu', err)
  }
}

const toggleRead = async (msg) => {
  try {
    const newLu = !msg.lu
    await adminApi.patch(`/contact-messages/${msg.id}/`, { lu: newLu })
    msg.lu = newLu
    await loadStats()
  } catch (err) {
    logger.warn('Erreur toggle lu', err)
    toast.error('Erreur')
  }
}

const removeMessage = async (msg) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer le message de « ${msg.nom} » ? Cette action est irréversible.`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return

  try {
    await adminApi.delete(`/contact-messages/${msg.id}/`)
    toast.success('Message supprimé')
    if (selectedMessage.value?.id === msg.id) closeMessage()
    await loadMessages()
  } catch (err) {
    logger.warn('Erreur suppression message', err)
    toast.error('Erreur lors de la suppression')
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
  loadMessages()
})
</script>

<style scoped>
.messages-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.messages-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

/* ==================== BOUTON RAFRAÎCHIR ==================== */
.btn-refresh {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px; border: none; border-radius: 10px;
  background: #fff; color: #475569; font-size: 13.5px; font-weight: 600;
  cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.superit-theme .btn-refresh { background: rgba(255,255,255,0.08); color: #c7d2fe; }
.btn-refresh:hover { background: #f8fafc; }
.btn-refresh:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-refresh .spinning { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ==================== STATS BAR ==================== */
.stats-bar {
  display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;
}
.stat-pill {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 10px 18px; border-radius: 12px;
  background: #fff; cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: all 0.15s;
  font-size: 13.5px; color: #334155;
}
.superit-theme .stat-pill {
  background: rgba(255,255,255,0.05); color: #cbd5e1;
}
.stat-pill:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.stat-pill.active { background: #6366f1; color: #fff; }
.stat-pill i { font-size: 14px; }
.stat-count {
  background: #e2e8f0; color: #475569;
  padding: 2px 8px; border-radius: 10px;
  font-size: 11px; font-weight: 700;
}
.superit-theme .stat-count { background: rgba(255,255,255,0.12); color: #e0e7ff; }
.stat-pill.active .stat-count { background: rgba(255,255,255,0.25); color: #fff; }
.stat-count.urgent { background: #fee2e2; color: #b91c1c; }
.superit-theme .stat-count.urgent { background: rgba(239,68,68,0.2); color: #fca5a5; }

/* ==================== FILTRES ==================== */
.filters-bar {
  display: flex; gap: 12px; padding: 14px 18px;
  background: #fff; border-radius: 12px; margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.superit-theme .filters-bar {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: none;
}
.search-wrap { flex: 1; position: relative; }
.search-wrap i {
  position: absolute; left: 14px; top: 50%;
  transform: translateY(-50%); color: #94a3b8; font-size: 13px;
}
.search-wrap input {
  width: 100%; padding: 10px 14px 10px 40px;
  border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 13.5px; font-family: inherit; background: #f8fafc; color: #0f172a;
}
.superit-theme .search-wrap input {
  background: rgba(255,255,255,0.04);
  border-color: rgba(255,255,255,0.1); color: #fff;
}
.search-wrap input:focus { outline: none; border-color: #6366f1; background: #fff; }
.superit-theme .search-wrap input:focus { border-color: #818cf8; background: rgba(255,255,255,0.08); }

/* ==================== LOADING / EMPTY ==================== */
.loading-block, .empty-block {
  background: #fff; border-radius: 14px; padding: 60px 20px; text-align: center;
}
.superit-theme .loading-block, .superit-theme .empty-block {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.08);
}
.spinner {
  width: 40px; height: 40px;
  border: 3px solid #e2e8f0; border-top-color: #6366f1;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
.superit-theme .spinner { border-color: rgba(255,255,255,0.15); border-top-color: #818cf8; }
.empty-block i { font-size: 48px; color: #cbd5e1; margin-bottom: 12px; display: block; }
.superit-theme .empty-block i { color: #6366f1; }
.empty-block h3 { color: #0f172a; margin: 0 0 6px; }
.superit-theme .empty-block h3 { color: #fff; }
.empty-block p { color: #64748b; margin: 0; }
.superit-theme .empty-block p { color: #94a3b8; }

/* ==================== LISTE DES MESSAGES ==================== */
.messages-list {
  display: flex; flex-direction: column; gap: 12px;
}
.message-card {
  display: flex; gap: 16px; align-items: flex-start;
  padding: 18px 20px; background: #fff;
  border-radius: 14px; border-left: 4px solid transparent;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: all 0.15s ease;
  cursor: pointer;
}
.superit-theme .message-card {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: none;
}
.message-card:hover { transform: translateX(3px); box-shadow: 0 8px 20px rgba(0,0,0,0.06); }
.superit-theme .message-card:hover { border-color: rgba(129,140,248,0.4); }
.message-card.unread {
  border-left-color: #6366f1;
  background: #f8faff;
}
.superit-theme .message-card.unread { background: rgba(99,102,241,0.08); }

.message-avatar {
  width: 48px; height: 48px; flex-shrink: 0;
  border-radius: 50%; background: #e2e8f0; color: #475569;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 15px;
}
.message-avatar.unread { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }

.message-body { flex: 1; min-width: 0; }
.message-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 4px;
}
.message-header h3 { font-size: 15px; color: #0f172a; margin: 0; font-weight: 700; }
.superit-theme .message-header h3 { color: #fff; }
.unread-dot {
  width: 8px; height: 8px; border-radius: 50%; background: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.2);
}
.message-date { margin-left: auto; font-size: 11.5px; color: #94a3b8; }
.message-email {
  font-size: 12.5px; color: #64748b; margin: 0 0 6px;
  display: flex; align-items: center; gap: 6px;
}
.superit-theme .message-email { color: #94a3b8; }
.message-email i { color: #6366f1; font-size: 11px; }
.message-sujet {
  display: inline-block; font-size: 11px; font-weight: 600;
  color: #6366f1; background: #eef2ff;
  padding: 3px 10px; border-radius: 20px; margin-bottom: 8px;
}
.superit-theme .message-sujet { background: rgba(99,102,241,0.15); color: #a5b4fc; }
.message-sujet i { margin-right: 4px; font-size: 10px; }
.message-preview {
  font-size: 13px; color: #475569; line-height: 1.5; margin: 0;
}
.superit-theme .message-preview { color: #cbd5e1; }

.message-actions { display: flex; gap: 6px; flex-shrink: 0; }
.btn-icon {
  width: 36px; height: 36px; border-radius: 9px;
  border: 1.5px solid #e2e8f0; background: #fff;
  color: #475569; cursor: pointer; font-size: 13px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.superit-theme .btn-icon {
  background: rgba(255,255,255,0.04);
  border-color: rgba(255,255,255,0.1); color: #94a3b8;
}
.btn-icon:hover { background: #f8fafc; color: #0f172a; }
.superit-theme .btn-icon:hover { background: rgba(255,255,255,0.08); color: #fff; }
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger { border-color: rgba(239,68,68,0.3); }
.btn-icon.danger:hover { background: #fee2e2; }

/* ==================== MODALE ==================== */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(15,23,42,0.5); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000; padding: 20px;
}
.superit-theme .modal-overlay { background: rgba(15,23,42,0.8); }
.modal-box {
  background: #fff; border-radius: 16px;
  width: 100%; max-width: 640px; max-height: 90vh; overflow-y: auto;
}
.modal-box.modal-large { max-width: 720px; }
.superit-theme .modal-box {
  background: #1e1b4b; border: 1px solid rgba(255,255,255,0.1);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px; border-bottom: 1px solid #f1f5f9;
  position: sticky; top: 0; background: #fff;
  border-radius: 16px 16px 0 0; z-index: 1;
}
.superit-theme .modal-header {
  background: #1e1b4b; border-bottom-color: rgba(255,255,255,0.08);
}
.modal-title { display: flex; align-items: center; gap: 14px; }
.modal-avatar {
  width: 52px; height: 52px; border-radius: 50%;
  background: #e2e8f0; color: #475569;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 17px; flex-shrink: 0;
}
.modal-avatar.unread { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0 0 2px; }
.superit-theme .modal-title h2 { color: #fff; }
.modal-subtitle { font-size: 12.5px; color: #64748b; display: flex; align-items: center; gap: 6px; }
.superit-theme .modal-subtitle { color: #94a3b8; }
.modal-subtitle i { font-size: 11px; color: #6366f1; }
.close-btn {
  width: 34px; height: 34px; border-radius: 50%;
  border: none; background: none; color: #94a3b8; cursor: pointer;
}
.close-btn:hover { background: #f1f5f9; color: #0f172a; }
.superit-theme .close-btn:hover { background: rgba(255,255,255,0.08); color: #fff; }

.modal-body { padding: 24px; }
.detail-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid #f1f5f9;
}
.superit-theme .detail-row { border-bottom-color: rgba(255,255,255,0.08); }
.detail-label { font-size: 12.5px; color: #94a3b8; font-weight: 600; }
.detail-value { font-size: 13.5px; color: #334155; font-weight: 500; }
.superit-theme .detail-value { color: #cbd5e1; }
.detail-value.badge {
  background: #eef2ff; color: #6366f1;
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 600;
}
.superit-theme .detail-value.badge { background: rgba(99,102,241,0.15); color: #a5b4fc; }

.detail-message {
  margin-top: 20px; padding: 18px;
  background: #f8fafc; border-radius: 12px;
}
.superit-theme .detail-message { background: rgba(255,255,255,0.04); }
.detail-message h4 {
  font-size: 13px; color: #334155; margin: 0 0 10px;
  display: flex; align-items: center; gap: 8px;
}
.superit-theme .detail-message h4 { color: #cbd5e1; }
.detail-message h4 i { color: #6366f1; }
.detail-message p {
  font-size: 14px; color: #334155; line-height: 1.7; margin: 0;
  white-space: pre-line;
}
.superit-theme .detail-message p { color: #e2e8f0; }

.modal-actions {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 16px 24px; border-top: 1px solid #f1f5f9;
}
.superit-theme .modal-actions { border-top-color: rgba(255,255,255,0.08); }
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 9px;
  font-size: 13.5px; font-weight: 600;
  border: none; cursor: pointer; text-decoration: none;
}
.btn-primary { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.btn-primary:hover { transform: translateY(-1px); }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary { background: rgba(255,255,255,0.06); color: #cbd5e1; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .message-card { flex-direction: column; }
  .message-actions { align-self: flex-end; }
}
</style>