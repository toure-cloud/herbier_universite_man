<template>
  <div class="stats-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Statistiques"
        subtitle="Chiffres clés à mettre en avant sur le site"
        icon="fas fa-chart-bar"
      >
        <template #actions>
          <button v-if="auth.isSuperIT" class="btn-create" :class="{ it: true }" @click="openCreate">
            <i class="fas fa-plus"></i> Nouvelle statistique
          </button>
        </template>
      </TopBar>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="stats.length === 0" class="empty-block">
        <i class="fas fa-chart-bar"></i>
        <h3>Aucune statistique</h3>
        <p v-if="auth.isSuperIT">Ajoutez des chiffres clés pour la page d'accueil</p>
        <p v-else>Contactez le SuperIT pour ajouter des statistiques</p>
        <button v-if="auth.isSuperIT" class="btn-create it" @click="openCreate">
          <i class="fas fa-plus"></i> Nouvelle statistique
        </button>
      </section>

      <section v-else class="stats-grid">
        <article v-for="s in stats" :key="s.id" class="stat-card">
          <div class="stat-icon">
            <i :class="s.icon || 'fas fa-chart-line'"></i>
          </div>
          <div class="stat-body">
            <span class="stat-value">{{ s.valeur }}<small v-if="s.unite">{{ s.unite }}</small></span>
            <span class="stat-label">{{ s.titre }}</span>
          </div>
          <div v-if="auth.isSuperIT" class="stat-footer">
            <span class="status-badge" :class="s.actif ? 'active' : 'inactive'">
              {{ s.actif ? 'Actif' : 'Inactif' }}
            </span>
            <div class="actions">
              <button class="btn-icon" @click="openEdit(s)"><i class="fas fa-edit"></i></button>
              <button class="btn-icon danger" @click="remove(s)"><i class="fas fa-trash"></i></button>
            </div>
          </div>
          <div v-else class="stat-footer view-only">
            <span class="status-badge" :class="s.actif ? 'active' : 'inactive'">
              {{ s.actif ? 'Visible' : 'Masqué' }}
            </span>
          </div>
        </article>
      </section>
    </main>

    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-chart-bar'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouvelle' }} statistique</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-group">
              <label>Titre *</label>
              <input v-model.trim="form.titre" type="text" required placeholder="Espèces recensées" />
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Valeur *</label>
                <input v-model.trim="form.valeur" type="text" required placeholder="1250" />
              </div>
              <div class="form-group">
                <label>Unité (optionnel)</label>
                <input v-model.trim="form.unite" type="text" placeholder="+, %, espèces…" />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Icône (Font Awesome)</label>
                <div class="icon-input-wrap">
                  <div class="icon-preview"><i :class="form.icon || 'fas fa-chart-line'"></i></div>
                  <input v-model.trim="form.icon" type="text" placeholder="fas fa-leaf" />
                </div>
              </div>
              <div class="form-group">
                <label>Ordre</label>
                <input v-model.number="form.ordre" type="number" min="0" />
              </div>
            </div>

            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.actif" />
              <span>Statistique visible</span>
            </label>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary it" :disabled="saving">
                <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                <i v-else class="fas fa-save"></i>
                {{ saving ? 'Enregistrement…' : 'Enregistrer' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { adminApi, statistiquesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const stats = ref([])
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const editing = ref(null)

const form = ref({
  titre: '', valeur: '', unite: '',
  icon: 'fas fa-chart-line', ordre: 0, actif: true,
})

const load = async () => {
  loading.value = true
  try {
    const { data } = await statistiquesAPI.list()
    const list = Array.isArray(data) ? data : data.results || []
    stats.value = list.sort((a, b) => (a.ordre ?? 0) - (b.ordre ?? 0))
  } catch {
    toast.error('Impossible de charger les statistiques')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  if (!auth.isSuperIT) return
  editing.value = null
  form.value = {
    titre: '', valeur: '', unite: '',
    icon: 'fas fa-chart-line', ordre: 0, actif: true,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (s) => {
  if (!auth.isSuperIT) return
  editing.value = s
  form.value = {
    titre: s.titre || '', valeur: s.valeur || '',
    unite: s.unite || '', icon: s.icon || 'fas fa-chart-line',
    ordre: s.ordre ?? 0, actif: s.actif !== false,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

const save = async () => {
  if (!auth.isSuperIT) return
  if (!form.value.titre || !form.value.valeur) {
    toast.error('Titre et valeur obligatoires')
    return
  }
  saving.value = true
  try {
    if (editing.value) {
      await statistiquesAPI.update(editing.value.id, form.value)
      toast.success('Statistique modifiée')
    } else {
      await statistiquesAPI.create(form.value)
      toast.success('Statistique ajoutée')
    }
    closeModal()
    await load()
  } catch (err) {
    logger.warn('Save stat error')
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

const remove = async (s) => {
  if (!auth.isSuperIT) return
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${s.titre} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await statistiquesAPI.remove(s.id)
    toast.success('Statistique supprimée')
    await load()
  } catch {
    toast.error('Erreur')
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
  load()
})
</script>

<style scoped>
.stats-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.stats-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.btn-create { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; border-radius: 10px; font-size: 13.5px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5); }
.btn-create.it { background: linear-gradient(135deg, #6366f1, #4f46e5); box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5); }
.btn-create:hover { transform: translateY(-1px); }

.loading-block, .empty-block { background: #fff; border-radius: 12px; padding: 60px 20px; text-align: center; }
.superit-theme .loading-block, .superit-theme .empty-block { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
.spinner { width: 40px; height: 40px; border: 3px solid #e2e8f0; border-top-color: #10b981; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
.superit-theme .spinner { border-color: rgba(255, 255, 255, 0.15); border-top-color: #818cf8; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-block i { font-size: 48px; color: #cbd5e1; margin-bottom: 12px; display: block; }
.superit-theme .empty-block i { color: #6366f1; }
.empty-block h3 { color: #0f172a; margin: 0 0 6px; }
.superit-theme .empty-block h3 { color: #fff; }
.empty-block p { color: #64748b; margin: 0 0 16px; }
.superit-theme .empty-block p { color: #94a3b8; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 18px; }
.stat-card { background: #fff; border-radius: 14px; padding: 20px 18px 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); transition: all 0.15s; display: flex; flex-direction: column; gap: 12px; border-top: 3px solid #10b981; }
.superit-theme .stat-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid #818cf8; box-shadow: none; }
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }

.stat-icon { width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #ecfdf5, #d1fae5); color: #10b981; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.superit-theme .stat-icon { background: rgba(99, 102, 241, 0.15); color: #818cf8; }

.stat-body { display: flex; flex-direction: column; gap: 4px; }
.stat-value { font-size: 28px; font-weight: 800; color: #0f172a; line-height: 1; }
.superit-theme .stat-value { color: #fff; }
.stat-value small { font-size: 14px; font-weight: 600; color: #10b981; margin-left: 4px; }
.superit-theme .stat-value small { color: #818cf8; }
.stat-label { font-size: 12.5px; color: #64748b; font-weight: 500; }
.superit-theme .stat-label { color: #94a3b8; }

.stat-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid #f1f5f9; }
.superit-theme .stat-footer { border-top-color: rgba(255, 255, 255, 0.06); }
.stat-footer.view-only { justify-content: center; }
.status-badge { padding: 3px 10px; border-radius: 20px; font-size: 10.5px; font-weight: 600; }
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.superit-theme .status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.actions { display: flex; gap: 6px; }
.btn-icon { width: 32px; height: 32px; border-radius: 8px; border: 1.5px solid #e2e8f0; background: #fff; color: #475569; cursor: pointer; font-size: 12px; display: flex; align-items: center; justify-content: center; }
.superit-theme .btn-icon { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #94a3b8; }
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }

.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box { background: #fff; border-radius: 16px; width: 100%; max-width: 520px; max-height: 90vh; overflow-y: auto; }
.superit-theme .modal-box { background: #1e1b4b; border: 1px solid rgba(255, 255, 255, 0.1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid #f1f5f9; }
.superit-theme .modal-header { border-bottom-color: rgba(255, 255, 255, 0.08); }
.modal-title { display: flex; align-items: center; gap: 12px; }
.modal-title i { font-size: 20px; color: #10b981; }
.superit-theme .modal-title i { color: #818cf8; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0; }
.superit-theme .modal-title h2 { color: #fff; }
.close-btn { width: 34px; height: 34px; border-radius: 50%; border: none; background: none; color: #94a3b8; cursor: pointer; }
.close-btn:hover { background: #f1f5f9; color: #0f172a; }
.superit-theme .close-btn:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }

.modal-form { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12.5px; font-weight: 600; color: #334155; }
.superit-theme .form-group label { color: #cbd5e1; }
.form-group input, .form-group select { padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 9px; font-size: 13.5px; font-family: inherit; background: #f8fafc; color: #0f172a; }
.superit-theme .form-group input, .superit-theme .form-group select { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #fff; }
.form-group input:focus { outline: none; border-color: #10b981; background: #fff; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1); }
.superit-theme .form-group input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15); }
.icon-input-wrap { display: flex; align-items: center; gap: 10px; }
.icon-preview { width: 42px; height: 42px; flex-shrink: 0; border-radius: 10px; background: #ecfdf5; display: flex; align-items: center; justify-content: center; color: #10b981; font-size: 18px; }
.superit-theme .icon-preview { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.icon-input-wrap input { flex: 1; }

.checkbox-wrap { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; cursor: pointer; }
.superit-theme .checkbox-wrap { color: #cbd5e1; }
.checkbox-wrap input { width: 16px; height: 16px; accent-color: #10b981; }
.superit-theme .checkbox-wrap input { accent-color: #6366f1; }

.modal-actions { display: flex; justify-content: flex-end; gap: 10px; padding-top: 8px; border-top: 1px solid #f1f5f9; }
.superit-theme .modal-actions { border-top-color: rgba(255, 255, 255, 0.08); }

.btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 9px; font-size: 13.5px; font-weight: 600; border: none; cursor: pointer; }
.btn-primary { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
.btn-primary.it { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; }
.btn-secondary:hover { background: #e2e8f0; }
.superit-theme .btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>
