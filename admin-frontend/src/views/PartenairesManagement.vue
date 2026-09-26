<template>
  <div class="partenaires-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Partenaires"
        :subtitle="auth.isSuperIT
          ? 'Gérez les partenaires de l\'herbier'
          : 'Consultation des partenaires'"
        icon="fas fa-handshake"
        :show-refresh="true"
        :loading="loading"
        @refresh="loadPartenaires"
      >
        <template #actions>
          <button
            v-if="auth.isSuperIT"
            class="btn-create it"
            @click="openCreate"
          >
            <i class="fas fa-plus"></i> Nouveau partenaire
          </button>
        </template>
      </TopBar>

      <div v-if="!auth.isSuperIT" class="readonly-banner">
        <i class="fas fa-lock"></i>
        <div>
          <strong>Mode lecture seule</strong>
          <p>
            La gestion des partenaires est réservée au
            <strong>Super Administrateur IT</strong>.
          </p>
        </div>
      </div>

      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher un partenaire…" />
        </div>
        <div class="result-count">
          <i class="fas fa-handshake"></i> {{ filtered.length }} partenaire(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-handshake-slash"></i>
        <h3>Aucun partenaire</h3>
        <p v-if="auth.isSuperIT">Ajoutez votre premier partenaire</p>
        <p v-else>Les partenaires seront bientôt disponibles.</p>
        <button v-if="auth.isSuperIT" class="btn-create it" @click="openCreate">
          <i class="fas fa-plus"></i> Nouveau partenaire
        </button>
      </section>

      <section v-else class="partenaires-grid">
        <article
          v-for="p in filtered"
          :key="p.id"
          class="partenaire-card"
          :class="{ inactive: !p.actif }"
        >
          <div class="partenaire-logo">
            <img
              v-if="p.logo"
              :src="p.logo"
              :alt="p.nom"
              @error="onImageError"
            />
            <i v-else class="fas fa-building"></i>
          </div>

          <div class="partenaire-body">
            <h3>{{ p.nom }}</h3>
            <p v-if="p.type" class="partenaire-type">{{ p.type }}</p>
            <p v-if="p.description" class="partenaire-desc">{{ truncate(p.description, 110) }}</p>

            <a
              v-if="p.site_web"
              :href="p.site_web"
              target="_blank"
              rel="noopener"
              class="partenaire-link"
            >
              <i class="fas fa-external-link-alt"></i> Site web
            </a>

            <span class="status-badge" :class="p.actif ? 'active' : 'inactive'">
              {{ p.actif ? 'Actif' : 'Inactif' }}
            </span>
          </div>

          <div v-if="auth.isSuperIT" class="partenaire-actions">
            <button class="btn-icon edit" @click="openEdit(p)" title="Modifier">
              <i class="fas fa-pen"></i>
            </button>
            <button class="btn-icon delete" @click="remove(p)" title="Supprimer">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <transition name="fade">
      <div v-if="showModal && auth.isSuperIT" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-handshake'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouveau' }} partenaire</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom *</label>
                <input v-model.trim="form.nom" type="text" required placeholder="Ex : Université de Man" />
              </div>
              <div class="form-group">
                <label>Type</label>
                <input v-model.trim="form.type" type="text" placeholder="Ex : ONG, Université" />
              </div>
            </div>

            <div class="form-group">
              <label>Site web</label>
              <input v-model.trim="form.site_web" type="url" placeholder="https://…" />
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea v-model="form.description" rows="3"></textarea>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Ordre d'affichage</label>
                <input v-model.number="form.ordre" type="number" min="0" />
              </div>
              <div class="form-group">
                <label class="checkbox-wrap">
                  <input type="checkbox" v-model="form.actif" />
                  <span>Partenaire actif</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <ImageUploader
                v-model="form.logoFile"
                label="Logo"
                icon="fas fa-building"
                :multiple="false"
                :max-size="5"
                :existing-images="form.logoExisting ? [form.logoExisting] : []"
                @files-changed="handleLogoChange"
              />
            </div>

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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import ImageUploader from '../components/ImageUploader.vue'
import { partenairesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const partenaires = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)

const form = ref({
  nom: '', type: '', site_web: '', description: '',
  ordre: 0, actif: true,
  logoFile: null, logoExisting: null,
})

const filtered = computed(() => {
  if (!search.value) return partenaires.value
  const q = search.value.toLowerCase()
  return partenaires.value.filter(
    (p) => p.nom?.toLowerCase().includes(q)
        || p.type?.toLowerCase().includes(q)
        || p.description?.toLowerCase().includes(q)
  )
})

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')
const onImageError = (e) => { e.target.style.display = 'none' }

const loadPartenaires = async () => {
  loading.value = true
  try {
    const { data } = await partenairesAPI.list()
    partenaires.value = Array.isArray(data) ? data : (data.results || [])
  } catch {
    toast.error('Impossible de charger les partenaires')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  if (!auth.isSuperIT) return
  editing.value = null
  form.value = {
    nom: '', type: '', site_web: '', description: '',
    ordre: 0, actif: true,
    logoFile: null, logoExisting: null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (p) => {
  if (!auth.isSuperIT) return
  editing.value = p
  form.value = {
    nom: p.nom || '',
    type: p.type || '',
    site_web: p.site_web || '',
    description: p.description || '',
    ordre: p.ordre ?? 0,
    actif: p.actif !== false,
    logoFile: null,
    logoExisting: p.logo || null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

const handleLogoChange = ({ files, existing }) => {
  form.value.logoFile = files[0] || null
  form.value.logoExisting = existing[0] || null
}

const save = async () => {
  if (!auth.isSuperIT) return
  if (!form.value.nom) {
    toast.error('Le nom est obligatoire')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('nom', form.value.nom)
    if (form.value.type) fd.append('type', form.value.type)
    if (form.value.site_web) fd.append('site_web', form.value.site_web)
    if (form.value.description) fd.append('description', form.value.description)
    fd.append('ordre', String(form.value.ordre ?? 0))
    fd.append('actif', form.value.actif ? 'true' : 'false')

    if (form.value.logoFile) fd.append('logo', form.value.logoFile)
    else if (form.value.logoExisting) fd.append('logo', form.value.logoExisting)

    if (editing.value) {
      await partenairesAPI.update(editing.value.id, fd)
      toast.success('Partenaire mis à jour')
    } else {
      await partenairesAPI.create(fd)
      toast.success('Partenaire ajouté')
    }
    closeModal()
    await loadPartenaires()
  } catch (err) {
    logger.warn('Save partenaire error')
    toast.error(err.response?.data?.error || 'Erreur lors de l\'enregistrement')
  } finally {
    saving.value = false
  }
}

const remove = async (p) => {
  if (!auth.isSuperIT) return
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer le partenaire « ${p.nom} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await partenairesAPI.remove(p.id)
    toast.success('Partenaire supprimé')
    await loadPartenaires()
  } catch {
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
  loadPartenaires()
})
</script>

<style scoped>
/* ============================================================
   LAYOUT + THEME
   ============================================================ */
.partenaires-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.partenaires-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.readonly-banner {
  display: flex; gap: 14px; align-items: flex-start;
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  border-left: 4px solid #f59e0b;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 20px;
  color: #78350f;
}
.readonly-banner i { font-size: 22px; color: #d97706; flex-shrink: 0; margin-top: 2px; }
.readonly-banner strong { font-size: 14px; display: block; margin-bottom: 2px; }
.readonly-banner p { margin: 0; font-size: 13px; line-height: 1.5; }

.btn-create {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; color: #fff;
  border: none; border-radius: 10px;
  font-size: 13.5px; font-weight: 600; cursor: pointer;
}
.btn-create.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5);
}
.btn-create:hover { transform: translateY(-1px); }

.filters-bar {
  display: flex; gap: 12px; padding: 14px 18px;
  background: #fff; border-radius: 12px; margin-bottom: 20px;
  flex-wrap: wrap; align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.superit-theme .filters-bar {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.search-wrap { flex: 1; min-width: 200px; position: relative; }
.search-wrap i {
  position: absolute; left: 14px; top: 50%;
  transform: translateY(-50%); color: #94a3b8; font-size: 13px;
}
.search-wrap input {
  width: 100%; padding: 10px 14px 10px 40px;
  border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 13.5px; font-family: inherit;
  background: #f8fafc; color: #0f172a;
}
.superit-theme .search-wrap input {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.search-wrap input:focus { outline: none; border-color: #6366f1; background: #fff; }
.superit-theme .search-wrap input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); }
.result-count {
  font-size: 12.5px; color: #64748b;
  padding: 6px 14px; background: #f1f5f9; border-radius: 20px;
}
.superit-theme .result-count { color: #94a3b8; background: rgba(255, 255, 255, 0.04); }
.result-count i { color: #6366f1; margin-right: 4px; }
.superit-theme .result-count i { color: #818cf8; }

.loading-block, .empty-block {
  background: #fff; border-radius: 12px; padding: 60px 20px; text-align: center;
}
.superit-theme .loading-block, .superit-theme .empty-block {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.spinner {
  width: 40px; height: 40px;
  border: 3px solid #e2e8f0; border-top-color: #6366f1;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
.superit-theme .spinner { border-color: rgba(255, 255, 255, 0.15); border-top-color: #818cf8; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-block i { font-size: 48px; color: #cbd5e1; margin-bottom: 12px; display: block; }
.superit-theme .empty-block i { color: #6366f1; }
.empty-block h3 { color: #0f172a; margin: 0 0 6px; }
.superit-theme .empty-block h3 { color: #fff; }
.empty-block p { color: #64748b; margin: 0 0 16px; }
.superit-theme .empty-block p { color: #94a3b8; }

.partenaires-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 18px;
}
.partenaire-card {
  background: #fff; border-radius: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.15s;
  display: flex; gap: 16px; padding: 18px;
  position: relative;
}
.superit-theme .partenaire-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.partenaire-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }
.superit-theme .partenaire-card:hover { border-color: rgba(129, 140, 248, 0.4); }
.partenaire-card.inactive { opacity: 0.55; }

.partenaire-logo {
  width: 64px; height: 64px; flex-shrink: 0;
  border-radius: 12px; overflow: hidden;
  background: #f1f5f9;
  display: flex; align-items: center; justify-content: center;
}
.superit-theme .partenaire-logo { background: rgba(255, 255, 255, 0.08); }
.partenaire-logo img { width: 100%; height: 100%; object-fit: contain; padding: 6px; }
.partenaire-logo i { font-size: 30px; color: #cbd5e1; }
.superit-theme .partenaire-logo i { color: #6366f1; }

.partenaire-body { flex: 1; min-width: 0; }
.partenaire-body h3 { font-size: 15px; color: #0f172a; margin: 0 0 4px; font-weight: 700; }
.superit-theme .partenaire-body h3 { color: #fff; }
.partenaire-type {
  font-size: 11px; color: #6366f1; margin: 0 0 8px;
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}
.superit-theme .partenaire-type { color: #818cf8; }
.partenaire-desc { font-size: 12.5px; color: #475569; line-height: 1.4; margin: 0 0 8px; }
.superit-theme .partenaire-desc { color: #cbd5e1; }
.partenaire-link {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; color: #6366f1; text-decoration: none;
  font-weight: 600; margin-bottom: 8px;
}
.partenaire-link:hover { text-decoration: underline; }

.status-badge {
  padding: 3px 10px; border-radius: 20px;
  font-size: 10.5px; font-weight: 600; display: inline-block;
}
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.superit-theme .status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.partenaire-actions {
  position: absolute; top: 12px; right: 12px;
  display: flex; gap: 6px;
}
.btn-icon {
  width: 32px; height: 32px; border-radius: 8px;
  border: 1.5px solid #e2e8f0; background: #fff;
  color: #475569; cursor: pointer; font-size: 12px;
  display: flex; align-items: center; justify-content: center;
}
.superit-theme .btn-icon {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.edit:hover { color: #6366f1; border-color: #c7d2fe; }
.btn-icon.delete { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.delete { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }
.btn-icon.delete:hover { background: #fee2e2; }

/* MODALE */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000; padding: 20px;
}
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box {
  background: #fff; border-radius: 16px;
  width: 100%; max-width: 620px; max-height: 90vh; overflow-y: auto;
}
.superit-theme .modal-box {
  background: #1e1b4b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px; border-bottom: 1px solid #f1f5f9;
  position: sticky; top: 0; background: #fff;
  border-radius: 16px 16px 0 0; z-index: 1;
}
.superit-theme .modal-header {
  background: #1e1b4b;
  border-bottom-color: rgba(255, 255, 255, 0.08);
}
.modal-title { display: flex; align-items: center; gap: 12px; }
.modal-title i { font-size: 20px; color: #6366f1; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0; }
.superit-theme .modal-title h2 { color: #fff; }
.close-btn {
  width: 34px; height: 34px; border-radius: 50%;
  border: none; background: none; color: #94a3b8; cursor: pointer;
}
.close-btn:hover { background: #f1f5f9; color: #0f172a; }
.superit-theme .close-btn:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }

.modal-form { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12.5px; font-weight: 600; color: #334155; }
.superit-theme .form-group label { color: #cbd5e1; }
.form-group input,
.form-group textarea {
  padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 9px;
  font-size: 13.5px; font-family: inherit;
  background: #f8fafc; color: #0f172a; resize: vertical;
}
.superit-theme .form-group input,
.superit-theme .form-group textarea {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.form-group input:focus { outline: none; border-color: #6366f1; background: #fff; }
.superit-theme .form-group input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); }

.checkbox-wrap { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; cursor: pointer; }
.superit-theme .checkbox-wrap { color: #cbd5e1; }
.checkbox-wrap input { width: 16px; height: 16px; accent-color: #6366f1; }

.modal-actions {
  display: flex; justify-content: flex-end; gap: 10px;
  padding-top: 8px; border-top: 1px solid #f1f5f9;
}
.superit-theme .modal-actions { border-top-color: rgba(255, 255, 255, 0.08); }

.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 9px;
  font-size: 13.5px; font-weight: 600; border: none; cursor: pointer;
}
.btn-primary { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; }
.btn-secondary:hover { background: #e2e8f0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>