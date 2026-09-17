<template>
  <div class="publications-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Publications"
        subtitle="Articles et publications scientifiques"
        icon="fas fa-book"
      >
        <template #actions>
          <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
            <i class="fas fa-plus"></i> Nouvelle publication
          </button>
        </template>
      </TopBar>

      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher une publication…" />
        </div>
        <select v-model="filterAnnee" class="filter-select">
          <option value="">Toutes les années</option>
          <option v-for="a in anneesDisponibles" :key="a" :value="a">{{ a }}</option>
        </select>
        <div class="result-count">
          <i class="fas fa-book"></i> {{ filtered.length }} publication(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-book"></i>
        <h3>Aucune publication</h3>
        <p>Ajoutez votre première publication</p>
        <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
          <i class="fas fa-plus"></i> Nouvelle publication
        </button>
      </section>

      <section v-else class="pub-list">
        <article v-for="p in filtered" :key="p.id" class="pub-card">
          <div class="pub-icon"><i class="fas fa-file-alt"></i></div>
          <div class="pub-body">
            <h3>{{ p.titre }}</h3>
            <p class="pub-auteurs"><i class="fas fa-user-edit"></i> {{ p.auteurs }}</p>
            <p class="pub-journal"><i class="fas fa-book"></i> {{ p.journal }} — {{ p.annee }}</p>
            <p v-if="p.resume" class="pub-resume">{{ truncate(p.resume, 160) }}</p>
            <div class="pub-links">
              <a v-if="p.lien" :href="p.lien" target="_blank" rel="noopener" class="pub-link">
                <i class="fas fa-external-link-alt"></i> Voir l'article
              </a>
              <span v-if="p.doi" class="pub-doi">
                <i class="fas fa-fingerprint"></i> {{ p.doi }}
              </span>
            </div>
          </div>
          <div class="pub-actions">
            <button class="btn-icon" @click="openEdit(p)"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="remove(p)"><i class="fas fa-trash"></i></button>
          </div>
        </article>
      </section>
    </main>

    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box modal-large">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-book'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouvelle' }} publication</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-group">
              <label>Titre *</label>
              <input v-model.trim="form.titre" type="text" required placeholder="Titre de l'article" />
            </div>

            <div class="form-group">
              <label>Auteurs *</label>
              <input v-model.trim="form.auteurs" type="text" required placeholder="Kouassi J., Konan M., …" />
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Journal / Revue *</label>
                <input v-model.trim="form.journal" type="text" required placeholder="Nom du journal" />
              </div>
              <div class="form-group">
                <label>Année *</label>
                <input v-model.number="form.annee" type="number" min="1900" :max="currentYear" required />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>DOI</label>
                <input v-model.trim="form.doi" type="text" placeholder="10.xxxx/xxxxx" />
              </div>
              <div class="form-group">
                <label>Lien URL</label>
                <input v-model.trim="form.lien" type="url" placeholder="https://…" />
              </div>
            </div>

            <div class="form-group">
              <label>Résumé</label>
              <textarea v-model="form.resume" rows="5"></textarea>
            </div>

            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.actif" />
              <span>Publication active</span>
            </label>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary" :class="{ it: auth.isSuperIT }" :disabled="saving">
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { publicationsAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const publications = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const filterAnnee = ref('')
const showModal = ref(false)
const editing = ref(null)
const currentYear = new Date().getFullYear()

const form = ref({
  titre: '', auteurs: '', journal: '', annee: currentYear,
  doi: '', lien: '', resume: '', actif: true,
})

const anneesDisponibles = computed(() => {
  const set = new Set(publications.value.map((p) => p.annee).filter(Boolean))
  return [...set].sort((a, b) => b - a)
})

const filtered = computed(() => {
  let list = publications.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(
      (p) =>
        p.titre?.toLowerCase().includes(q) ||
        p.auteurs?.toLowerCase().includes(q) ||
        p.journal?.toLowerCase().includes(q)
    )
  }
  if (filterAnnee.value) list = list.filter((p) => p.annee == filterAnnee.value)
  return list.sort((a, b) => (b.annee || 0) - (a.annee || 0))
})

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')

const load = async () => {
  loading.value = true
  try {
    const { data } = await publicationsAPI.list()
    publications.value = Array.isArray(data) ? data : data.results || []
  } catch {
    toast.error('Impossible de charger les publications')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editing.value = null
  form.value = {
    titre: '', auteurs: '', journal: '', annee: currentYear,
    doi: '', lien: '', resume: '', actif: true,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (p) => {
  editing.value = p
  form.value = {
    titre: p.titre || '', auteurs: p.auteurs || '',
    journal: p.journal || '', annee: p.annee || currentYear,
    doi: p.doi || '', lien: p.lien || '',
    resume: p.resume || '', actif: p.actif !== false,
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
  if (!form.value.titre || !form.value.auteurs || !form.value.journal || !form.value.annee) {
    toast.error('Titre, auteurs, journal et année obligatoires')
    return
  }
  saving.value = true
  try {
    const payload = { ...form.value }
    if (editing.value) {
      await publicationsAPI.update(editing.value.id, payload)
      toast.success('Publication modifiée')
    } else {
      await publicationsAPI.create(payload)
      toast.success('Publication ajoutée')
    }
    closeModal()
    await load()
  } catch (err) {
    logger.warn('Save publication error')
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

const remove = async (p) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${p.titre} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await publicationsAPI.remove(p.id)
    toast.success('Publication supprimée')
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
.publications-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.publications-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.btn-create { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; border-radius: 10px; font-size: 13.5px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5); }
.btn-create.it { background: linear-gradient(135deg, #6366f1, #4f46e5); box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5); }
.btn-create:hover { transform: translateY(-1px); }

.filters-bar { display: flex; gap: 12px; padding: 14px 18px; background: #fff; border-radius: 12px; margin-bottom: 20px; flex-wrap: wrap; align-items: center; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); }
.superit-theme .filters-bar { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: none; }
.search-wrap { flex: 1; min-width: 200px; position: relative; }
.search-wrap i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 13px; }
.search-wrap input { width: 100%; padding: 10px 14px 10px 40px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 13.5px; font-family: inherit; background: #f8fafc; color: #0f172a; }
.superit-theme .search-wrap input { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #fff; }
.search-wrap input:focus { outline: none; border-color: #10b981; background: #fff; }
.superit-theme .search-wrap input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); }
.filter-select { padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 13.5px; background: #f8fafc; cursor: pointer; color: #0f172a; }
.superit-theme .filter-select { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #fff; }
.superit-theme .filter-select option { background: #1e1b4b; }
.result-count { font-size: 12.5px; color: #64748b; padding: 6px 14px; background: #f1f5f9; border-radius: 20px; }
.superit-theme .result-count { color: #94a3b8; background: rgba(255, 255, 255, 0.04); }
.result-count i { color: #10b981; margin-right: 4px; }
.superit-theme .result-count i { color: #818cf8; }

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

.pub-list { display: flex; flex-direction: column; gap: 12px; }
.pub-card { display: flex; gap: 16px; padding: 18px 20px; background: #fff; border-radius: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); transition: all 0.15s; border-left: 4px solid #10b981; }
.superit-theme .pub-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 4px solid #818cf8; box-shadow: none; }
.pub-card:hover { transform: translateX(3px); }

.pub-icon { width: 46px; height: 46px; border-radius: 12px; background: #ecfdf5; color: #10b981; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.superit-theme .pub-icon { background: rgba(99, 102, 241, 0.15); color: #818cf8; }

.pub-body { flex: 1; min-width: 0; }
.pub-body h3 { font-size: 15px; color: #0f172a; margin: 0 0 6px; font-weight: 700; line-height: 1.35; }
.superit-theme .pub-body h3 { color: #fff; }
.pub-auteurs { font-size: 12.5px; color: #475569; margin: 0 0 4px; }
.superit-theme .pub-auteurs { color: #cbd5e1; }
.pub-auteurs i { color: #94a3b8; margin-right: 5px; }
.pub-journal { font-size: 12.5px; color: #64748b; margin: 0 0 6px; font-style: italic; }
.superit-theme .pub-journal { color: #94a3b8; }
.pub-journal i { color: #94a3b8; margin-right: 5px; }
.pub-resume { font-size: 12.5px; color: #475569; line-height: 1.5; margin: 8px 0; }
.superit-theme .pub-resume { color: #cbd5e1; }
.pub-links { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px; align-items: center; }
.pub-link { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; color: #10b981; text-decoration: none; font-weight: 600; }
.superit-theme .pub-link { color: #818cf8; }
.pub-link:hover { text-decoration: underline; }
.pub-doi { font-size: 11.5px; color: #94a3b8; display: inline-flex; align-items: center; gap: 4px; }

.pub-actions { display: flex; flex-direction: column; gap: 6px; flex-shrink: 0; }
.btn-icon { width: 32px; height: 32px; border-radius: 8px; border: 1.5px solid #e2e8f0; background: #fff; color: #475569; cursor: pointer; font-size: 12px; display: flex; align-items: center; justify-content: center; }
.superit-theme .btn-icon { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #94a3b8; }
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }

.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box { background: #fff; border-radius: 16px; width: 100%; max-width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-box.modal-large { max-width: 700px; }
.superit-theme .modal-box { background: #1e1b4b; border: 1px solid rgba(255, 255, 255, 0.1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid #f1f5f9; position: sticky; top: 0; background: #fff; border-radius: 16px 16px 0 0; z-index: 1; }
.superit-theme .modal-header { background: #1e1b4b; border-bottom-color: rgba(255, 255, 255, 0.08); }
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
.form-group input, .form-group select, .form-group textarea { padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 9px; font-size: 13.5px; font-family: inherit; background: #f8fafc; color: #0f172a; resize: vertical; }
.superit-theme .form-group input, .superit-theme .form-group select, .superit-theme .form-group textarea { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #fff; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #10b981; background: #fff; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1); }
.superit-theme .form-group input:focus, .superit-theme .form-group select:focus, .superit-theme .form-group textarea:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15); }

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
  .pub-card { flex-direction: column; }
  .pub-actions { flex-direction: row; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>
