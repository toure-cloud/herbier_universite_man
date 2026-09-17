<template>
  <div class="activites-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Activités"
        subtitle="Les activités scientifiques de l'herbier"
        icon="fas fa-chart-line"
      >
        <template #actions>
          <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
            <i class="fas fa-plus"></i> Nouvelle activité
          </button>
        </template>
      </TopBar>

      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher une activité…" />
        </div>
        <div class="view-toggle">
          <button :class="{ active: view === 'grid' }" @click="view = 'grid'">
            <i class="fas fa-th-large"></i>
          </button>
          <button :class="{ active: view === 'list' }" @click="view = 'list'">
            <i class="fas fa-list"></i>
          </button>
        </div>
        <div class="result-count">
          <i class="fas fa-chart-line"></i> {{ filtered.length }} activité(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-bolt"></i>
        <h3>Aucune activité</h3>
        <p>Ajoutez la première activité de l'herbier</p>
        <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
          <i class="fas fa-plus"></i> Nouvelle activité
        </button>
      </section>

      <!-- Vue Grille -->
      <section v-else-if="view === 'grid'" class="activites-grid">
        <article v-for="a in filtered" :key="a.id" class="activite-card">
          <div class="activite-image">
            <img v-if="getMainImage(a)" :src="getMainImage(a)" :alt="a.titre" @error="onImageError" />
            <div v-else class="activite-icon-wrap">
              <i :class="a.icon || 'fas fa-leaf'"></i>
            </div>
            <span v-if="hasMultipleImages(a)" class="images-count">
              <i class="fas fa-images"></i> {{ getAllImages(a).length }}
            </span>
            <span class="status-dot" :class="{ active: a.actif }"></span>
          </div>

          <div class="activite-body">
            <div class="activite-header">
              <i :class="a.icon || 'fas fa-leaf'" class="activite-icon-inline"></i>
              <h3>{{ a.titre }}</h3>
            </div>
            <p class="activite-court">{{ a.titre_court }}</p>
            <p class="activite-desc">{{ truncate(a.description_courte, 90) }}</p>
          </div>

          <div class="activite-actions">
            <button class="btn-icon" @click="openEdit(a)"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="remove(a)"><i class="fas fa-trash"></i></button>
          </div>
        </article>
      </section>

      <!-- Vue Liste -->
      <section v-else class="activites-table-wrap">
        <table class="activites-table">
          <thead>
            <tr>
              <th>Icône</th>
              <th>Titre</th>
              <th>Titre court</th>
              <th>Description</th>
              <th>Ordre</th>
              <th>Statut</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in filtered" :key="a.id">
              <td><i :class="a.icon || 'fas fa-leaf'" class="table-icon"></i></td>
              <td><strong>{{ a.titre }}</strong></td>
              <td>{{ a.titre_court }}</td>
              <td>{{ truncate(a.description_courte, 60) }}</td>
              <td>{{ a.ordre ?? 0 }}</td>
              <td>
                <span class="status-badge" :class="a.actif ? 'active' : 'inactive'">
                  {{ a.actif ? 'Actif' : 'Inactif' }}
                </span>
              </td>
              <td class="table-actions">
                <button class="btn-icon" @click="openEdit(a)"><i class="fas fa-edit"></i></button>
                <button class="btn-icon danger" @click="remove(a)"><i class="fas fa-trash"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>

    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box modal-large">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-bolt'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouvelle' }} activité</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-row-2">
              <div class="form-group">
                <label>Titre *</label>
                <input v-model.trim="form.titre" type="text" required />
              </div>
              <div class="form-group">
                <label>Titre court *</label>
                <input v-model.trim="form.titre_court" type="text" required />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Icône (Font Awesome)</label>
                <div class="icon-input-wrap">
                  <div class="icon-preview"><i :class="form.icon || 'fas fa-leaf'"></i></div>
                  <input v-model.trim="form.icon" type="text" placeholder="fas fa-leaf" />
                </div>
              </div>
              <div class="form-group">
                <label>Ordre</label>
                <input v-model.number="form.ordre" type="number" min="0" />
              </div>
            </div>

            <div class="form-group">
              <label>Description courte *</label>
              <textarea v-model="form.description_courte" rows="3" required></textarea>
            </div>

            <div class="form-group">
              <label>Description longue</label>
              <textarea v-model="form.description_longue" rows="4"></textarea>
            </div>

            <div class="form-group">
              <ImageUploader
                v-model="form.imagesFiles"
                label="Images de l'activité"
                icon="fas fa-images"
                :multiple="true"
                :max-files="5"
                :max-size="5"
                :existing-images="form.imagesExisting"
                @files-changed="handleImagesChange"
              />
            </div>

            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.actif" />
              <span>Activité active</span>
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
import { activitesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const activites = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const view = ref('grid')
const showModal = ref(false)
const editing = ref(null)

const form = ref({
  titre: '', titre_court: '', icon: 'fas fa-leaf',
  description_courte: '', description_longue: '',
  ordre: 0, actif: true,
  imagesFiles: [], imagesExisting: [],
})

const filtered = computed(() => {
  if (!search.value) return activites.value
  const q = search.value.toLowerCase()
  return activites.value.filter(
    (a) =>
      a.titre?.toLowerCase().includes(q) ||
      a.titre_court?.toLowerCase().includes(q) ||
      a.description_courte?.toLowerCase().includes(q)
  )
})

const getAllImages = (a) => {
  if (Array.isArray(a.images) && a.images.length) return a.images
  if (Array.isArray(a.images_galerie) && a.images_galerie.length) return a.images_galerie
  if (a.image) return [a.image]
  return []
}
const getMainImage = (a) => getAllImages(a)[0] || null
const hasMultipleImages = (a) => getAllImages(a).length > 1
const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')
const onImageError = (e) => { e.target.style.display = 'none' }

const load = async () => {
  loading.value = true
  try {
    const { data } = await activitesAPI.list()
    activites.value = Array.isArray(data) ? data : data.results || []
  } catch {
    toast.error('Impossible de charger les activités')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editing.value = null
  form.value = {
    titre: '', titre_court: '', icon: 'fas fa-leaf',
    description_courte: '', description_longue: '',
    ordre: 0, actif: true,
    imagesFiles: [], imagesExisting: [],
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (a) => {
  editing.value = a
  form.value = {
    titre: a.titre || '',
    titre_court: a.titre_court || '',
    icon: a.icon || 'fas fa-leaf',
    description_courte: a.description_courte || '',
    description_longue: a.description_longue || '',
    ordre: a.ordre ?? 0,
    actif: a.actif !== false,
    imagesFiles: [],
    imagesExisting: getAllImages(a),
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

const handleImagesChange = ({ files, existing }) => {
  form.value.imagesFiles = files
  form.value.imagesExisting = existing
}

const save = async () => {
  if (!form.value.titre || !form.value.titre_court || !form.value.description_courte) {
    toast.error('Titre, titre court et description courte obligatoires')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('titre', form.value.titre)
    fd.append('titre_court', form.value.titre_court)
    fd.append('icon', form.value.icon || 'fas fa-leaf')
    fd.append('description_courte', form.value.description_courte)
    if (form.value.description_longue) fd.append('description_longue', form.value.description_longue)
    fd.append('ordre', String(form.value.ordre || 0))
    fd.append('actif', form.value.actif ? 'true' : 'false')

    form.value.imagesFiles.forEach((f) => fd.append('images', f))
    form.value.imagesExisting.forEach((u) => fd.append('existing_images', u))

    if (editing.value) {
      await activitesAPI.update(editing.value.id, fd)
      toast.success('Activité modifiée')
    } else {
      await activitesAPI.create(fd)
      toast.success('Activité ajoutée')
    }
    closeModal()
    await load()
  } catch (err) {
    logger.warn('Save activite error')
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

const remove = async (a) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${a.titre} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await activitesAPI.remove(a.id)
    toast.success('Activité supprimée')
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
   LAYOUT + THÈME
   ============================================================ */
.activites-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.activites-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.btn-create {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 10px; font-size: 13.5px;
  font-weight: 600; cursor: pointer;
  box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5);
  transition: all 0.15s;
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
.search-wrap i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 13px; }
.search-wrap input {
  width: 100%; padding: 10px 14px 10px 40px;
  border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 13.5px; font-family: inherit;
  background: #f8fafc; color: #0f172a;
  transition: all 0.15s;
}
.superit-theme .search-wrap input {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.search-wrap input:focus { outline: none; border-color: #10b981; background: #fff; }
.superit-theme .search-wrap input:focus {
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
}
.view-toggle {
  display: flex; gap: 4px; padding: 4px;
  background: #f1f5f9; border-radius: 10px;
}
.superit-theme .view-toggle { background: rgba(255, 255, 255, 0.06); }
.view-toggle button {
  padding: 6px 12px; border-radius: 7px; border: none;
  background: none; color: #64748b; cursor: pointer; font-size: 13px;
}
.superit-theme .view-toggle button { color: #94a3b8; }
.view-toggle button.active {
  background: #fff; color: #10b981;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.superit-theme .view-toggle button.active {
  background: rgba(255, 255, 255, 0.12);
  color: #c7d2fe;
}
.result-count {
  font-size: 12.5px; color: #64748b;
  padding: 6px 14px; background: #f1f5f9; border-radius: 20px;
}
.superit-theme .result-count {
  color: #94a3b8; background: rgba(255, 255, 255, 0.04);
}
.result-count i { color: #10b981; margin-right: 4px; }
.superit-theme .result-count i { color: #818cf8; }

.loading-block, .empty-block {
  background: #fff; border-radius: 12px; padding: 60px 20px;
  text-align: center;
}
.superit-theme .loading-block, .superit-theme .empty-block {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.spinner {
  width: 40px; height: 40px;
  border: 3px solid #e2e8f0; border-top-color: #10b981;
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

.activites-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
.activite-card {
  background: #fff; border-radius: 14px; overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.15s; display: flex; flex-direction: column;
}
.superit-theme .activite-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.activite-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }
.superit-theme .activite-card:hover { border-color: rgba(129, 140, 248, 0.4); }

.activite-image {
  position: relative; aspect-ratio: 16 / 10;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  overflow: hidden;
}
.superit-theme .activite-image { background: rgba(99, 102, 241, 0.08); }
.activite-image img { width: 100%; height: 100%; object-fit: cover; }
.activite-icon-wrap {
  display: flex; align-items: center; justify-content: center;
  height: 100%; color: #10b981; font-size: 48px;
}
.superit-theme .activite-icon-wrap { color: #818cf8; }
.images-count {
  position: absolute; top: 10px; right: 10px;
  padding: 4px 9px; border-radius: 20px;
  background: rgba(0, 0, 0, 0.6); color: #fff;
  font-size: 10.5px; font-weight: 600;
  display: flex; align-items: center; gap: 4px;
}
.status-dot {
  position: absolute; bottom: 10px; right: 10px;
  width: 12px; height: 12px; border-radius: 50%;
  background: #ef4444; border: 2px solid #fff;
}
.status-dot.active { background: #10b981; }

.activite-body { padding: 16px 18px 12px; flex: 1; }
.activite-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.activite-icon-inline { color: #10b981; font-size: 15px; }
.superit-theme .activite-icon-inline { color: #818cf8; }
.activite-body h3 { font-size: 15px; color: #0f172a; margin: 0; font-weight: 700; }
.superit-theme .activite-body h3 { color: #fff; }
.activite-court { font-size: 12px; color: #10b981; font-weight: 500; margin: 4px 0 8px; }
.superit-theme .activite-court { color: #818cf8; }
.activite-desc { font-size: 12.5px; color: #475569; line-height: 1.4; margin: 0; }
.superit-theme .activite-desc { color: #cbd5e1; }

.activite-actions {
  display: flex; gap: 8px; padding: 10px 18px 14px;
  border-top: 1px solid #f1f5f9;
}
.superit-theme .activite-actions { border-top-color: rgba(255, 255, 255, 0.06); }
.btn-icon {
  flex: 1; padding: 8px; border-radius: 8px;
  border: 1.5px solid #e2e8f0; background: #fff;
  color: #475569; cursor: pointer; font-size: 13px;
}
.superit-theme .btn-icon {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }

.activites-table-wrap { background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); }
.superit-theme .activites-table-wrap { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: none; }
.activites-table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.activites-table thead { background: #f8fafc; }
.superit-theme .activites-table thead { background: rgba(255, 255, 255, 0.04); }
.activites-table th { padding: 14px 16px; text-align: left; font-weight: 600; color: #475569; font-size: 12.5px; }
.superit-theme .activites-table th { color: #94a3b8; }
.activites-table td { padding: 14px 16px; border-bottom: 1px solid #f1f5f9; color: #334155; }
.superit-theme .activites-table td { border-bottom-color: rgba(255, 255, 255, 0.05); color: #cbd5e1; }
.activites-table tr:last-child td { border-bottom: none; }
.activites-table tr:hover { background: #f8fafc; }
.superit-theme .activites-table tr:hover { background: rgba(255, 255, 255, 0.02); }
.table-icon { color: #10b981; font-size: 18px; }
.superit-theme .table-icon { color: #818cf8; }
.table-actions { display: flex; gap: 6px; }
.table-actions .btn-icon { flex: none; width: 32px; padding: 7px; }
.status-badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.superit-theme .status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box { background: #fff; border-radius: 16px; width: 100%; max-width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-box.modal-large { max-width: 760px; }
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
.form-group input, .form-group textarea {
  padding: 10px 14px; border: 1.5px solid #e2e8f0;
  border-radius: 9px; font-size: 13.5px; font-family: inherit;
  background: #f8fafc; color: #0f172a; resize: vertical;
}
.superit-theme .form-group input, .superit-theme .form-group textarea {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: #10b981; background: #fff; }
.superit-theme .form-group input:focus, .superit-theme .form-group textarea:focus {
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
}
.icon-input-wrap { display: flex; align-items: center; gap: 10px; }
.icon-preview {
  width: 42px; height: 42px; flex-shrink: 0;
  border-radius: 10px; background: #ecfdf5;
  display: flex; align-items: center; justify-content: center;
  color: #10b981; font-size: 18px;
}
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

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>
