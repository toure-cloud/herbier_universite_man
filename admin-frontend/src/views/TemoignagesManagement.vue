<template>
  <div class="temoignages-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Témoignages"
        subtitle="Les avis et retours sur l'herbier"
        icon="fas fa-comment-dots"
      >
        <template #actions>
          <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
            <i class="fas fa-plus"></i> Nouveau témoignage
          </button>
        </template>
      </TopBar>

      <section class="stats-row">
        <div class="stat-pill">
          <i class="fas fa-comment-dots"></i>
          <div>
            <span class="stat-value">{{ temoignages.length }}</span>
            <span class="stat-label">Total</span>
          </div>
        </div>
        <div class="stat-pill green">
          <i class="fas fa-check-circle"></i>
          <div>
            <span class="stat-value">{{ actifs }}</span>
            <span class="stat-label">Publiés</span>
          </div>
        </div>
        <div class="stat-pill gold">
          <i class="fas fa-star"></i>
          <div>
            <span class="stat-value">{{ moyenneNote }}/5</span>
            <span class="stat-label">Note moyenne</span>
          </div>
        </div>
      </section>

      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher un témoignage…" />
        </div>
        <select v-model="filterNote" class="filter-select">
          <option value="">Toutes les notes</option>
          <option v-for="n in [5, 4, 3, 2, 1]" :key="n" :value="n">{{ n }} ★</option>
        </select>
        <select v-model="filterStatus" class="filter-select">
          <option value="">Tous les statuts</option>
          <option value="true">Publié</option>
          <option value="false">Masqué</option>
        </select>
        <div class="result-count">
          <i class="fas fa-comment-dots"></i> {{ filtered.length }} témoignage(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-comment-dots"></i>
        <h3>Aucun témoignage</h3>
        <p>Ajoutez les retours de vos visiteurs</p>
        <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
          <i class="fas fa-plus"></i> Nouveau témoignage
        </button>
      </section>

      <section v-else class="temoignages-grid">
        <article v-for="t in filtered" :key="t.id" class="temoignage-card">
          <div class="quote-icon"><i class="fas fa-quote-left"></i></div>

          <div class="temoignage-header">
            <div class="avatar">
              <img v-if="t.photo || t.image" :src="t.photo || t.image" :alt="t.nom" @error="onImageError" />
              <span v-else>{{ getInitials(t.nom) }}</span>
            </div>
            <div class="author-info">
              <h3>{{ t.nom }}</h3>
              <p class="author-role">
                {{ t.poste }}<span v-if="t.organisation"> · {{ t.organisation }}</span>
              </p>
            </div>
            <span class="status-dot" :class="{ active: t.actif }"></span>
          </div>

          <div class="rating">
            <i v-for="n in 5" :key="n" class="fas fa-star" :class="{ filled: n <= (t.note || 5) }"></i>
          </div>

          <p class="temoignage-text">« {{ truncate(t.texte, 180) }} »</p>

          <div class="temoignage-actions">
            <button class="btn-icon" @click="openEdit(t)" title="Modifier">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" :class="t.actif ? 'danger' : 'success'" @click="toggleStatus(t)">
              <i :class="t.actif ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
            <button class="btn-icon danger" @click="remove(t)" title="Supprimer">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-comment-dots'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouveau' }} témoignage</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom *</label>
                <input v-model.trim="form.nom" type="text" required placeholder="Jean Kouassi" />
              </div>
              <div class="form-group">
                <label>Poste *</label>
                <input v-model.trim="form.poste" type="text" required placeholder="Directeur…" />
              </div>
            </div>

            <div class="form-group">
              <label>Organisation</label>
              <input v-model.trim="form.organisation" type="text" placeholder="Université de Man" />
            </div>

            <div class="form-group">
              <label>Témoignage *</label>
              <textarea v-model="form.texte" rows="4" required></textarea>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Note (1 à 5)</label>
                <select v-model.number="form.note">
                  <option v-for="n in [5, 4, 3, 2, 1]" :key="n" :value="n">{{ '★'.repeat(n) }} ({{ n }})</option>
                </select>
              </div>
              <div class="form-group">
                <label>Ordre</label>
                <input v-model.number="form.ordre" type="number" min="0" />
              </div>
            </div>

            <div class="form-group">
              <ImageUploader
                v-model="form.photoFile"
                label="Photo (optionnelle)"
                icon="fas fa-camera"
                :multiple="false"
                :max-size="3"
                :existing-images="form.photoExisting ? [form.photoExisting] : []"
                @files-changed="handlePhotoChange"
              />
            </div>

            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.actif" />
              <span>Témoignage publié</span>
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
import { temoignagesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const temoignages = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const filterNote = ref('')
const filterStatus = ref('')
const showModal = ref(false)
const editing = ref(null)

const form = ref({
  nom: '', poste: '', organisation: '', texte: '',
  note: 5, ordre: 0, actif: true,
  photoFile: null, photoExisting: null,
})

const actifs = computed(() => temoignages.value.filter((t) => t.actif).length)

const moyenneNote = computed(() => {
  if (!temoignages.value.length) return 0
  const sum = temoignages.value.reduce((acc, t) => acc + (t.note || 5), 0)
  return (sum / temoignages.value.length).toFixed(1)
})

const filtered = computed(() => {
  let list = temoignages.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(
      (t) =>
        t.nom?.toLowerCase().includes(q) ||
        t.organisation?.toLowerCase().includes(q) ||
        t.texte?.toLowerCase().includes(q)
    )
  }
  if (filterNote.value) list = list.filter((t) => (t.note || 5) === Number(filterNote.value))
  if (filterStatus.value) {
    const active = filterStatus.value === 'true'
    list = list.filter((t) => t.actif === active)
  }
  return list.sort((a, b) => (a.ordre ?? 0) - (b.ordre ?? 0))
})

const getInitials = (name) =>
  name ? name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2) : '?'

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')
const onImageError = (e) => { e.target.style.display = 'none' }

const load = async () => {
  loading.value = true
  try {
    const { data } = await temoignagesAPI.list()
    temoignages.value = Array.isArray(data) ? data : data.results || []
  } catch {
    toast.error('Impossible de charger les témoignages')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editing.value = null
  form.value = {
    nom: '', poste: '', organisation: '', texte: '',
    note: 5, ordre: 0, actif: true,
    photoFile: null, photoExisting: null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (t) => {
  editing.value = t
  form.value = {
    nom: t.nom || '', poste: t.poste || '',
    organisation: t.organisation || '', texte: t.texte || '',
    note: t.note ?? 5, ordre: t.ordre ?? 0,
    actif: t.actif !== false,
    photoFile: null, photoExisting: t.photo || t.image || null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

const handlePhotoChange = ({ files, existing }) => {
  form.value.photoFile = files[0] || null
  form.value.photoExisting = existing[0] || null
}

const save = async () => {
  if (!form.value.nom || !form.value.poste || !form.value.texte) {
    toast.error('Nom, poste et témoignage obligatoires')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('nom', form.value.nom)
    fd.append('poste', form.value.poste)
    if (form.value.organisation) fd.append('organisation', form.value.organisation)
    fd.append('texte', form.value.texte)
    fd.append('note', String(form.value.note || 5))
    fd.append('ordre', String(form.value.ordre || 0))
    fd.append('actif', form.value.actif ? 'true' : 'false')

    if (form.value.photoFile) fd.append('photo', form.value.photoFile)
    else if (form.value.photoExisting) fd.append('photo', form.value.photoExisting)

    if (editing.value) {
      await temoignagesAPI.update(editing.value.id, fd)
      toast.success('Témoignage modifié')
    } else {
      await temoignagesAPI.create(fd)
      toast.success('Témoignage ajouté')
    }
    closeModal()
    await load()
  } catch (err) {
    logger.warn('Save témoignage error')
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

const toggleStatus = async (t) => {
  try {
    await temoignagesAPI.patch(t.id, { actif: !t.actif })
    toast.success(t.actif ? 'Témoignage masqué' : 'Témoignage publié')
    await load()
  } catch {
    toast.error('Erreur')
  }
}

const remove = async (t) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer le témoignage de « ${t.nom} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await temoignagesAPI.remove(t.id)
    toast.success('Témoignage supprimé')
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
.temoignages-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.temoignages-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 20px; }
.stat-pill { display: flex; align-items: center; gap: 12px; padding: 14px 18px; background: #fff; border-radius: 12px; border-left: 4px solid #3b82f6; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); }
.superit-theme .stat-pill { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 4px solid #818cf8; box-shadow: none; }
.stat-pill.green { border-left-color: #10b981; }
.stat-pill.gold { border-left-color: #f59e0b; }
.stat-pill i { font-size: 20px; color: #3b82f6; }
.stat-pill.green i { color: #10b981; }
.stat-pill.gold i { color: #f59e0b; }
.stat-value { font-size: 20px; font-weight: 700; color: #0f172a; line-height: 1; }
.superit-theme .stat-value { color: #fff; }
.stat-label { font-size: 11.5px; color: #64748b; }
.superit-theme .stat-label { color: #94a3b8; }

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

.temoignages-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; }
.temoignage-card { position: relative; background: #fff; border-radius: 14px; padding: 22px 20px 16px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); transition: all 0.15s; border-top: 3px solid #10b981; display: flex; flex-direction: column; }
.superit-theme .temoignage-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-top: 3px solid #818cf8; box-shadow: none; }
.temoignage-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }

.quote-icon { position: absolute; top: 14px; right: 18px; font-size: 34px; color: #ecfdf5; z-index: 0; }
.superit-theme .quote-icon { color: rgba(99, 102, 241, 0.15); }

.temoignage-header { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; position: relative; z-index: 1; }
.avatar { width: 48px; height: 48px; border-radius: 50%; flex-shrink: 0; background: linear-gradient(135deg, #10b981, #059669); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; overflow: hidden; }
.superit-theme .avatar { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.avatar img { width: 100%; height: 100%; object-fit: cover; }
.author-info { flex: 1; min-width: 0; }
.author-info h3 { font-size: 14.5px; color: #0f172a; margin: 0 0 2px; font-weight: 700; }
.superit-theme .author-info h3 { color: #fff; }
.author-role { font-size: 11.5px; color: #64748b; margin: 0; }
.superit-theme .author-role { color: #94a3b8; }
.status-dot { width: 10px; height: 10px; border-radius: 50%; background: #ef4444; flex-shrink: 0; }
.status-dot.active { background: #10b981; }

.rating { margin-bottom: 10px; font-size: 13px; }
.rating i { color: #e2e8f0; margin-right: 2px; }
.superit-theme .rating i { color: rgba(255, 255, 255, 0.15); }
.rating i.filled { color: #f59e0b; }

.temoignage-text { font-size: 13px; color: #475569; line-height: 1.6; margin: 0 0 14px; font-style: italic; flex: 1; }
.superit-theme .temoignage-text { color: #cbd5e1; }

.temoignage-actions { display: flex; gap: 6px; padding-top: 12px; border-top: 1px solid #f1f5f9; }
.superit-theme .temoignage-actions { border-top-color: rgba(255, 255, 255, 0.06); }
.btn-icon { flex: 1; padding: 8px; border-radius: 8px; border: 1.5px solid #e2e8f0; background: #fff; color: #475569; cursor: pointer; font-size: 12px; }
.superit-theme .btn-icon { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #94a3b8; }
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.success { color: #10b981; border-color: #a7f3d0; }
.superit-theme .btn-icon.success { color: #10b981; border-color: rgba(16, 185, 129, 0.3); }
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }

.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box { background: #fff; border-radius: 16px; width: 100%; max-width: 580px; max-height: 90vh; overflow-y: auto; }
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
