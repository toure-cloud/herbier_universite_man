<template>
  <div class="plantes-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Plantes"
        subtitle="Gérez la collection botanique"
        icon="fas fa-leaf"
      >
        <template #actions>
          <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
            <i class="fas fa-plus"></i> Nouvelle plante
          </button>
        </template>
      </TopBar>

      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher une plante…" />
        </div>
        <select v-model="filterFamille" class="filter-select">
          <option value="">Toutes les familles</option>
          <option v-for="f in famillesList" :key="f" :value="f">{{ f }}</option>
        </select>
        <select v-model="filterStatut" class="filter-select">
          <option value="">Tous les statuts</option>
          <option v-for="s in statutsConservation" :key="s" :value="s">{{ s }}</option>
        </select>
        <div class="result-count">
          <i class="fas fa-leaf"></i> {{ filtered.length }} plante(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-seedling"></i>
        <h3>Aucune plante trouvée</h3>
        <p>Ajoutez votre première plante</p>
        <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
          <i class="fas fa-plus"></i> Nouvelle plante
        </button>
      </section>

      <section v-else class="plantes-grid">
        <article v-for="p in filtered" :key="p.id" class="plante-card">
          <div class="plante-image">
            <img v-if="getMainImage(p)" :src="getMainImage(p)" :alt="p.nom" @error="onImageError" />
            <div v-else class="no-image"><i class="fas fa-leaf"></i></div>
            <span v-if="p.statut_conservation" class="statut-badge" :class="getStatutClass(p.statut_conservation)">
              {{ p.statut_conservation }}
            </span>
          </div>
          <div class="plante-body">
            <h3>{{ p.nom }}</h3>
            <p class="plante-famille" v-if="p.famille"><i class="fas fa-tag"></i> {{ p.famille }}</p>
            <p class="plante-desc" v-if="p.description">{{ truncate(p.description, 100) }}</p>
            <div class="plante-meta">
              <span class="status-badge" :class="p.actif ? 'active' : 'inactive'">
                {{ p.actif ? 'Actif' : 'Inactif' }}
              </span>
            </div>
          </div>
          <div class="plante-actions">
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
              <i :class="editing ? 'fas fa-edit' : 'fas fa-leaf'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouvelle' }} plante</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>
          <form @submit.prevent="save" class="modal-form">
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom *</label>
                <input v-model.trim="form.nom" type="text" required placeholder="Nom commun" />
              </div>
              <div class="form-group">
                <label>Famille</label>
                <input v-model.trim="form.famille" type="text" placeholder="Fabaceae…" />
              </div>
            </div>
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom scientifique</label>
                <input v-model.trim="form.nom_scientifique" type="text" placeholder="Nom latin" />
              </div>
              <div class="form-group">
                <label>Statut de conservation</label>
                <select v-model="form.statut_conservation">
                  <option value="">Non spécifié</option>
                  <option v-for="s in statutsConservation" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Description</label>
              <textarea v-model="form.description" rows="3"></textarea>
            </div>
            <div class="form-group">
              <label>Habitat</label>
              <input v-model.trim="form.habitat" type="text" placeholder="Forêt, savane…" />
            </div>
            <div class="form-group">
              <ImageUploader
                v-model="form.imageFile"
                label="Image"
                icon="fas fa-image"
                :multiple="false"
                :max-size="5"
                :existing-images="form.imageExisting ? [form.imageExisting] : []"
                @files-changed="handleImageChange"
              />
            </div>
            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.actif" />
              <span>Plante active</span>
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
import ImageUploader from '../components/ImageUploader.vue'
import { plantesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

// ✅ Renommé de `confirm` à `askConfirm` pour ne PAS écraser window.confirm
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const plantes = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const filterFamille = ref('')
const filterStatut = ref('')
const showModal = ref(false)
const editing = ref(null)

const statutsConservation = [
  'En danger critique', 'En danger', 'Vulnérable',
  'Quasi menacé', 'Préoccupation mineure', 'Non évaluée',
]

const form = ref({
  nom: '', famille: '', nom_scientifique: '', description: '',
  habitat: '', statut_conservation: '', actif: true,
  imageFile: null, imageExisting: null,
})

const famillesList = computed(() => {
  const set = new Set(plantes.value.map((p) => p.famille).filter(Boolean))
  return [...set].sort()
})

const filtered = computed(() => {
  let list = plantes.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(
      (p) => p.nom?.toLowerCase().includes(q) || p.famille?.toLowerCase().includes(q)
    )
  }
  if (filterFamille.value) list = list.filter((p) => p.famille === filterFamille.value)
  if (filterStatut.value) list = list.filter((p) => p.statut_conservation === filterStatut.value)
  return list
})

const getMainImage = (p) => p.image || null
const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')
const onImageError = (e) => { e.target.style.display = 'none' }

const getStatutClass = (s) => {
  const v = (s || '').toLowerCase()
  if (v.includes('critique')) return 'critical'
  if (v.includes('danger')) return 'endangered'
  if (v.includes('vulnérable')) return 'vulnerable'
  if (v.includes('quasi')) return 'near-threatened'
  return 'least-concern'
}

const load = async () => {
  loading.value = true
  try {
    const { data } = await plantesAPI.list()
    plantes.value = Array.isArray(data) ? data : data.results || []
  } catch {
    toast.error('Impossible de charger les plantes')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editing.value = null
  form.value = {
    nom: '', famille: '', nom_scientifique: '', description: '',
    habitat: '', statut_conservation: '', actif: true,
    imageFile: null, imageExisting: null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (p) => {
  editing.value = p
  form.value = {
    nom: p.nom || '', famille: p.famille || '',
    nom_scientifique: p.nom_scientifique || '',
    description: p.description || '', habitat: p.habitat || '',
    statut_conservation: p.statut_conservation || '',
    actif: p.actif !== false,
    imageFile: null, imageExisting: p.image || null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

const handleImageChange = ({ files, existing }) => {
  form.value.imageFile = files[0] || null
  form.value.imageExisting = existing[0] || null
}

const save = async () => {
  if (!form.value.nom) {
    toast.error('Le nom est obligatoire')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('nom', form.value.nom)
    if (form.value.famille) fd.append('famille', form.value.famille)
    if (form.value.nom_scientifique) fd.append('nom_scientifique', form.value.nom_scientifique)
    if (form.value.description) fd.append('description', form.value.description)
    if (form.value.habitat) fd.append('habitat', form.value.habitat)
    if (form.value.statut_conservation) fd.append('statut_conservation', form.value.statut_conservation)
    fd.append('actif', form.value.actif ? 'true' : 'false')
    if (form.value.imageFile) fd.append('image', form.value.imageFile)
    else if (form.value.imageExisting) fd.append('image', form.value.imageExisting)

    if (editing.value) {
      await plantesAPI.update(editing.value.id, fd)
      toast.success('Plante modifiée')
    } else {
      await plantesAPI.create(fd)
      toast.success('Plante ajoutée')
    }
    closeModal()
    await load()
  } catch (err) {
    logger.warn('Save plante error')
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

// ✅ Utilise askConfirm, pas confirm
const remove = async (p) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${p.nom} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await plantesAPI.remove(p.id)
    toast.success('Plante supprimée')
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
/* ============================================================
   LAYOUT + THEME
   ============================================================ */
.plantes-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.plantes-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
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

.plantes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
.plante-card { background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); transition: all 0.15s; display: flex; flex-direction: column; }
.superit-theme .plante-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: none; }
.plante-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }
.superit-theme .plante-card:hover { border-color: rgba(129, 140, 248, 0.4); }

.plante-image { position: relative; aspect-ratio: 4 / 3; background: #f1f5f9; overflow: hidden; }
.superit-theme .plante-image { background: rgba(255, 255, 255, 0.03); }
.plante-image img { width: 100%; height: 100%; object-fit: cover; }
.no-image { display: flex; align-items: center; justify-content: center; height: 100%; color: #cbd5e1; font-size: 40px; }
.superit-theme .no-image { color: #6366f1; }

.statut-badge { position: absolute; top: 10px; left: 10px; padding: 4px 10px; border-radius: 20px; font-size: 10.5px; font-weight: 600; color: #fff; }
.statut-badge.critical { background: rgba(220, 38, 38, 0.9); }
.statut-badge.endangered { background: rgba(234, 88, 12, 0.9); }
.statut-badge.vulnerable { background: rgba(245, 158, 11, 0.9); color: #1a1a1a; }
.statut-badge.near-threatened { background: rgba(59, 130, 246, 0.9); }
.statut-badge.least-concern { background: rgba(16, 185, 129, 0.9); }

.plante-body { padding: 16px 18px 12px; flex: 1; }
.plante-body h3 { font-size: 15px; color: #0f172a; margin: 0 0 6px; font-weight: 700; }
.superit-theme .plante-body h3 { color: #fff; }
.plante-famille { font-size: 12px; color: #10b981; margin: 0 0 6px; font-weight: 500; }
.superit-theme .plante-famille { color: #818cf8; }
.plante-desc { font-size: 12.5px; color: #475569; line-height: 1.4; margin: 0 0 12px; }
.superit-theme .plante-desc { color: #cbd5e1; }
.plante-meta { display: flex; gap: 6px; }
.status-badge { padding: 3px 10px; border-radius: 20px; font-size: 10.5px; font-weight: 600; }
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.superit-theme .status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.plante-actions { display: flex; gap: 8px; padding: 10px 18px 14px; border-top: 1px solid #f1f5f9; }
.superit-theme .plante-actions { border-top-color: rgba(255, 255, 255, 0.06); }
.btn-icon { flex: 1; padding: 8px; border-radius: 8px; border: 1.5px solid #e2e8f0; background: #fff; color: #475569; cursor: pointer; font-size: 13px; }
.superit-theme .btn-icon { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #94a3b8; }
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box { background: #fff; border-radius: 16px; width: 100%; max-width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-box.modal-large { max-width: 720px; }
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
.form-group select option { background: #fff; color: #0f172a; }
.superit-theme .form-group select option { background: #1e1b4b; color: #fff; }

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