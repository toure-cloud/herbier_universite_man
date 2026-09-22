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
          <button
            class="btn-create"
            :class="{ it: auth.isSuperIT }"
            @click="openCreate"
          >
            <i class="fas fa-plus"></i>
            Nouvelle activité
          </button>
        </template>
      </TopBar>

      <!-- ==================== FILTRES ==================== -->
      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input
            v-model.trim="search"
            type="text"
            placeholder="Rechercher une activité…"
          />
        </div>
        <div class="view-toggle">
          <button
            type="button"
            :class="{ active: view === 'grid' }"
            @click="view = 'grid'"
            title="Vue grille"
          >
            <i class="fas fa-th-large"></i>
          </button>
          <button
            type="button"
            :class="{ active: view === 'list' }"
            @click="view = 'list'"
            title="Vue liste"
          >
            <i class="fas fa-list"></i>
          </button>
        </div>
        <div class="result-count">
          <i class="fas fa-chart-line"></i>
          {{ filtered.length }} activité(s)
        </div>
      </section>

      <!-- ==================== LOADING ==================== -->
      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <!-- ==================== EMPTY ==================== -->
      <section v-else-if="filtered.length === 0" class="empty-block">
        <div class="empty-icon">
          <i class="fas fa-bolt"></i>
        </div>
        <h3>Aucune activité</h3>
        <p>Ajoutez la première activité de l'herbier</p>
        <button
          class="btn-create"
          :class="{ it: auth.isSuperIT }"
          @click="openCreate"
        >
          <i class="fas fa-plus"></i>
          Nouvelle activité
        </button>
      </section>

      <!-- ==================== VUE GRILLE ==================== -->
      <section v-else-if="view === 'grid'" class="activites-grid">
        <article v-for="a in filtered" :key="a.id" class="activite-card">
          <div class="activite-image">
            <img
              v-if="getMainImage(a)"
              :src="getMainImage(a)"
              :alt="a.titre"
              @error="onImageError"
              loading="lazy"
            />
            <div v-else class="activite-icon-wrap">
              <i :class="a.icon || 'fas fa-leaf'"></i>
            </div>
            <span v-if="getGalleryCount(a) > 0" class="images-count">
              <i class="fas fa-images"></i>
              {{ getGalleryCount(a) + (getMainImage(a) ? 1 : 0) }}
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
            <button type="button" class="btn-icon" @click="openEdit(a)" title="Modifier">
              <i class="fas fa-edit"></i>
            </button>
            <button type="button" class="btn-icon danger" @click="remove(a)" title="Supprimer">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>

      <!-- ==================== VUE LISTE ==================== -->
      <section v-else class="activites-table-wrap">
        <table class="activites-table">
          <thead>
            <tr>
              <th>Image</th>
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
              <td>
                <div class="table-thumb">
                  <img
                    v-if="getMainImage(a)"
                    :src="getMainImage(a)"
                    :alt="a.titre"
                    @error="onImageError"
                  />
                  <i v-else :class="a.icon || 'fas fa-leaf'" class="table-icon"></i>
                </div>
              </td>
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
                <button type="button" class="btn-icon" @click="openEdit(a)">
                  <i class="fas fa-edit"></i>
                </button>
                <button type="button" class="btn-icon danger" @click="remove(a)">
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </main>

    <!-- ==================== MODALE ==================== -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box modal-large">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-bolt'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouvelle' }} activité</h2>
            </div>
            <button type="button" class="close-btn" @click="closeModal">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <!-- Ligne 1 : Titre + Titre court -->
            <div class="form-row-2">
              <div class="form-group">
                <label>Titre *</label>
                <input v-model.trim="form.titre" type="text" required placeholder="Ex : Inventaire floristique" />
              </div>
              <div class="form-group">
                <label>Titre court *</label>
                <input v-model.trim="form.titre_court" type="text" required placeholder="Ex : Inventaire" />
              </div>
            </div>

            <!-- Ligne 2 : Icône + Ordre -->
            <div class="form-row-2">
              <div class="form-group">
                <label>Icône (Font Awesome)</label>
                <div class="icon-input-wrap">
                  <div class="icon-preview">
                    <i :class="form.icon || 'fas fa-leaf'"></i>
                  </div>
                  <input
                    v-model.trim="form.icon"
                    type="text"
                    placeholder="fas fa-leaf"
                  />
                </div>
              </div>
              <div class="form-group">
                <label>Ordre d'affichage</label>
                <input v-model.number="form.ordre" type="number" min="0" />
              </div>
            </div>

            <!-- Description courte -->
            <div class="form-group">
              <label>Description courte *</label>
              <textarea
                v-model="form.description_courte"
                rows="3"
                required
                placeholder="Courte description (une phrase)…"
              ></textarea>
            </div>

            <!-- Description longue -->
            <div class="form-group">
              <label>Description longue</label>
              <textarea
                v-model="form.description_longue"
                rows="4"
                placeholder="Description détaillée de l'activité…"
              ></textarea>
            </div>

            <!-- Caption -->
            <div class="form-group">
              <label>Légende de l'image (caption)</label>
              <input
                v-model.trim="form.caption"
                type="text"
                placeholder="Ex : Équipe en mission sur le terrain"
              />
            </div>

            <!-- Points forts -->
            <div class="form-group">
              <label>Points forts (un par ligne)</label>
              <textarea
                v-model="form.points_forts"
                rows="3"
                placeholder="Identification morphologique&#10;Base de données&#10;Expertise reconnue"
              ></textarea>
            </div>

            <!-- ==================== IMAGE PRINCIPALE ==================== -->
            <div class="form-group">
              <label>Image principale</label>
              <div class="image-uploader">
                <input
                  type="file"
                  accept="image/*"
                  @change="onMainImageChange"
                  class="file-input"
                  id="activite-main-image-input"
                />
                <label for="activite-main-image-input" class="file-label">
                  <i class="fas fa-cloud-upload-alt"></i>
                  <span v-if="!form.imageFile && !form.imageExisting">Choisir une image principale</span>
                  <span v-else-if="form.imageFile">Nouveau : {{ form.imageFile.name }}</span>
                  <span v-else>Image actuelle conservée (cliquer pour remplacer)</span>
                </label>
              </div>
              <div v-if="form.imageExisting && !form.imageFile" class="image-preview">
                <img :src="getImageUrl(form.imageExisting)" alt="Image principale" @error="onImageError" />
              </div>
              <div v-if="form.imageFile" class="image-preview">
                <img :src="previewNewFile(form.imageFile)" alt="Aperçu" />
              </div>
            </div>

            <!-- ==================== GALERIE ==================== -->
            <div class="form-group">
              <label>Galerie d'images (plusieurs)</label>
              <div class="image-uploader">
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  @change="onGalleryImagesChange"
                  class="file-input"
                  id="activite-gallery-input"
                />
                <label for="activite-gallery-input" class="file-label">
                  <i class="fas fa-images"></i>
                  <span v-if="!form.galleryFiles.length && !form.imagesExisting.length">
                    Ajouter plusieurs images à la galerie
                  </span>
                  <span v-else>
                    {{ form.galleryFiles.length }} nouvelle(s) + {{ form.imagesExisting.length }} existante(s)
                  </span>
                </label>
              </div>

              <!-- Grille des images existantes -->
              <div v-if="form.imagesExisting.length" class="gallery-grid">
                <div
                  v-for="(img, i) in form.imagesExisting"
                  :key="'existing-' + i"
                  class="gallery-item"
                >
                  <img :src="getImageUrl(img)" alt="Image galerie" @error="onImageError" />
                  <button
                    type="button"
                    class="gallery-remove"
                    @click="removeExistingImage(i)"
                    title="Retirer de la galerie"
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              </div>

              <!-- Grille des nouvelles images -->
              <div v-if="form.galleryFiles.length" class="gallery-grid">
                <div
                  v-for="(file, i) in form.galleryFiles"
                  :key="'new-' + i"
                  class="gallery-item new"
                >
                  <img :src="previewNewFile(file)" alt="Nouvelle image" />
                  <button
                    type="button"
                    class="gallery-remove"
                    @click="removeNewImage(i)"
                    title="Retirer"
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- Actif -->
            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.actif" />
              <span>Activité active (visible sur le site public)</span>
            </label>

            <!-- Actions -->
            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                Annuler
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :class="{ it: auth.isSuperIT }"
                :disabled="saving"
              >
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { activitesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8001/api').replace(
  /\/api\/?$/,
  ''
)

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

// ============================================================
// FORMULAIRE — 1 image principale + galerie multiple
// ============================================================
const form = ref({
  titre: '',
  titre_court: '',
  icon: 'fas fa-leaf',
  description_courte: '',
  description_longue: '',
  caption: '',
  points_forts: '',
  ordre: 0,
  actif: true,
  // Image principale
  imageFile: null,
  imageExisting: null,
  // Galerie
  galleryFiles: [],
  imagesExisting: [],
})

// ============================================================
// COMPUTED
// ============================================================
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

// ============================================================
// HELPERS IMAGES
// ============================================================
const getImageUrl = (path) => {
  if (!path) return ''
  if (typeof path !== 'string') return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('blob:') || path.startsWith('data:')) return path
  if (path.startsWith('/media')) return `${API_BASE}${path}`
  if (path.startsWith('media/')) return `${API_BASE}/${path}`
  if (!path.startsWith('/')) return `${API_BASE}/media/${path}`
  return path
}

const getMainImage = (a) => {
  if (!a) return null
  if (a.image) return getImageUrl(a.image)
  // Fallback : première image de la galerie
  const gal = getGalleryUrls(a)
  return gal[0] || null
}

const getGalleryUrls = (a) => {
  if (!a) return []
  const raw = []
  if (Array.isArray(a.images_galerie) && a.images_galerie.length) {
    raw.push(...a.images_galerie)
  } else if (Array.isArray(a.images) && a.images.length) {
    raw.push(...a.images)
  }
  const seen = new Set()
  return raw
    .map(getImageUrl)
    .filter((url) => {
      if (!url || seen.has(url)) return false
      seen.add(url)
      return true
    })
}

const getGalleryCount = (a) => getGalleryUrls(a).length

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')

const onImageError = (e) => {
  if (e.target.dataset.errorHandled) return
  e.target.dataset.errorHandled = 'true'
  e.target.src =
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Crect fill='%23f1f5f9' width='200' height='200'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='12' fill='%2394a3b8' text-anchor='middle' dy='.3em'%3EPas+image%3C/text%3E%3C/svg%3E"
}

const previewNewFile = (file) => {
  if (!file) return ''
  return URL.createObjectURL(file)
}

// ============================================================
// GESTION DES IMAGES DANS LE FORMULAIRE
// ============================================================
const onMainImageChange = (e) => {
  form.value.imageFile = e.target.files?.[0] || null
}

const onGalleryImagesChange = (e) => {
  const files = Array.from(e.target.files || [])
  form.value.galleryFiles.push(...files)
  e.target.value = '' // reset pour permettre de re-sélectionner le même fichier
}

const removeExistingImage = (index) => {
  form.value.imagesExisting.splice(index, 1)
}

const removeNewImage = (index) => {
  const file = form.value.galleryFiles[index]
  if (file) URL.revokeObjectURL(file)
  form.value.galleryFiles.splice(index, 1)
}

// ============================================================
// CHARGEMENT
// ============================================================
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

// ============================================================
// CRÉATION / ÉDITION
// ============================================================
const openCreate = () => {
  editing.value = null
  form.value = {
    titre: '',
    titre_court: '',
    icon: 'fas fa-leaf',
    description_courte: '',
    description_longue: '',
    caption: '',
    points_forts: '',
    ordre: 0,
    actif: true,
    imageFile: null,
    imageExisting: null,
    galleryFiles: [],
    imagesExisting: [],
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
    caption: a.caption || '',
    points_forts: a.points_forts || '',
    ordre: a.ordre ?? 0,
    actif: a.actif !== false,
    imageFile: null,
    imageExisting: a.image || null,
    galleryFiles: [],
    imagesExisting: Array.isArray(a.images_galerie) ? [...a.images_galerie] : [],
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  // Libérer les aperçus d'images
  form.value.galleryFiles.forEach((f) => URL.revokeObjectURL(f))
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

// ============================================================
// SAUVEGARDE
// ============================================================
const save = async () => {
  if (!form.value.titre || !form.value.titre_court || !form.value.description_courte) {
    toast.error('Titre, titre court et description courte obligatoires')
    return
  }

  saving.value = true
  try {
    const fd = new FormData()

    // Champs texte
    fd.append('titre', form.value.titre)
    fd.append('titre_court', form.value.titre_court)
    fd.append('icon', form.value.icon || 'fas fa-leaf')
    fd.append('description_courte', form.value.description_courte)
    if (form.value.description_longue) fd.append('description_longue', form.value.description_longue)
    if (form.value.caption) fd.append('caption', form.value.caption)
    if (form.value.points_forts) fd.append('points_forts', form.value.points_forts)
    fd.append('ordre', String(form.value.ordre || 0))
    fd.append('actif', form.value.actif ? 'true' : 'false')

    // Image principale : on n'envoie QUE si un nouveau fichier est sélectionné
    // ⚠️ Ne pas renvoyer form.value.imageExisting (URL) dans le champ 'image' :
    // le ImageField Django refuserait.
    if (form.value.imageFile) {
      fd.append('image', form.value.imageFile)
    }

    // Nouvelles images de la galerie : gallery_0, gallery_1, ...
    form.value.galleryFiles.forEach((file, i) => {
      fd.append(`gallery_${i}`, file)
    })

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
    logger.warn('Save activite error', err)
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

// ============================================================
// SUPPRESSION
// ============================================================
const remove = async (a) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${a.titre} » ? Cette action est irréversible.`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await activitesAPI.remove(a.id)
    toast.success('Activité supprimée')
    await load()
  } catch {
    toast.error('Erreur lors de la suppression')
  }
}

// ============================================================
// LOGOUT
// ============================================================
const handleLogout = async () => {
  await auth.logout()
  router.push(auth.isSuperIT ? '/it-login' : '/admin-login')
}

// ============================================================
// LIFECYCLE
// ============================================================
onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/it-login')
    return
  }
  load()
})

onBeforeUnmount(() => {
  form.value.galleryFiles.forEach((f) => URL.revokeObjectURL(f))
})
</script>

<style scoped>
/* ============================================================
   LAYOUT + THEME
   ============================================================ */
.activites-layout {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
}
.activites-layout.superit-theme {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}
.main-content {
  margin-left: 260px;
  padding: 24px 28px 40px;
  transition: margin-left 0.3s ease;
}
.main-content.expanded { margin-left: 76px; }

.btn-create {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.45);
  transition: transform 0.15s;
}
.btn-create.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.45);
}
.btn-create:hover { transform: translateY(-1px); }

/* ============================================================
   FILTRES
   ============================================================ */
.filters-bar {
  display: flex;
  gap: 12px;
  padding: 14px 18px;
  background: #fff;
  border-radius: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
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
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 13px;
}
.search-wrap input {
  width: 100%;
  padding: 10px 14px 10px 40px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13.5px;
  font-family: inherit;
  background: #f8fafc;
  color: #0f172a;
}
.superit-theme .search-wrap input {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.search-wrap input:focus {
  outline: none;
  border-color: #10b981;
  background: #fff;
}
.superit-theme .search-wrap input:focus {
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
}
.view-toggle {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: #f1f5f9;
  border-radius: 10px;
}
.superit-theme .view-toggle {
  background: rgba(255, 255, 255, 0.06);
}
.view-toggle button {
  padding: 6px 12px;
  border-radius: 7px;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  font-size: 13px;
}
.superit-theme .view-toggle button { color: #94a3b8; }
.view-toggle button.active {
  background: #fff;
  color: #10b981;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.superit-theme .view-toggle button.active {
  background: rgba(255, 255, 255, 0.12);
  color: #c7d2fe;
}
.result-count {
  font-size: 12.5px;
  color: #64748b;
  padding: 6px 14px;
  background: #f1f5f9;
  border-radius: 20px;
}
.superit-theme .result-count {
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.04);
}
.result-count i { color: #10b981; margin-right: 4px; }
.superit-theme .result-count i { color: #818cf8; }

/* ============================================================
   LOADING / EMPTY
   ============================================================ */
.loading-block,
.empty-block {
  background: #fff;
  border-radius: 12px;
  padding: 60px 20px;
  text-align: center;
}
.superit-theme .loading-block,
.superit-theme .empty-block {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
.superit-theme .spinner {
  border-color: rgba(255, 255, 255, 0.15);
  border-top-color: #818cf8;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  font-size: 24px;
  color: #94a3b8;
}
.superit-theme .empty-icon {
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
}
.empty-block h3 { color: #0f172a; margin: 0 0 6px; }
.superit-theme .empty-block h3 { color: #fff; }
.empty-block p { color: #64748b; margin: 0 0 16px; }
.superit-theme .empty-block p { color: #94a3b8; }

/* ============================================================
   GRILLE
   ============================================================ */
.activites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}
.activite-card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: transform 0.15s, box-shadow 0.15s;
  display: flex;
  flex-direction: column;
}
.superit-theme .activite-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.activite-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1);
}
.superit-theme .activite-card:hover {
  border-color: rgba(129, 140, 248, 0.4);
}

.activite-image {
  position: relative;
  aspect-ratio: 16 / 10;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  overflow: hidden;
}
.superit-theme .activite-image {
  background: rgba(99, 102, 241, 0.08);
}
.activite-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.activite-icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #10b981;
  font-size: 48px;
}
.superit-theme .activite-icon-wrap { color: #818cf8; }
.images-count {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 9px;
  border-radius: 20px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 10.5px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}
.status-dot {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ef4444;
  border: 2px solid #fff;
}
.status-dot.active { background: #10b981; }

.activite-body { padding: 16px 18px 12px; flex: 1; }
.activite-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.activite-icon-inline { color: #10b981; font-size: 15px; }
.superit-theme .activite-icon-inline { color: #818cf8; }
.activite-body h3 {
  font-size: 15px;
  color: #0f172a;
  margin: 0;
  font-weight: 700;
}
.superit-theme .activite-body h3 { color: #fff; }
.activite-court {
  font-size: 12px;
  color: #10b981;
  font-weight: 500;
  margin: 4px 0 8px;
}
.superit-theme .activite-court { color: #818cf8; }
.activite-desc {
  font-size: 12.5px;
  color: #475569;
  line-height: 1.4;
  margin: 0;
}
.superit-theme .activite-desc { color: #cbd5e1; }

.activite-actions {
  display: flex;
  gap: 8px;
  padding: 10px 18px 14px;
  border-top: 1px solid #f1f5f9;
}
.superit-theme .activite-actions {
  border-top-color: rgba(255, 255, 255, 0.06);
}
.btn-icon {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  border: 1.5px solid #e2e8f0;
  background: #fff;
  color: #475569;
  cursor: pointer;
  font-size: 13px;
}
.superit-theme .btn-icon {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
.btn-icon.danger { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.danger {
  border-color: rgba(239, 68, 68, 0.3);
}

/* ============================================================
   TABLE
   ============================================================ */
.activites-table-wrap {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.superit-theme .activites-table-wrap {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.activites-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}
.activites-table thead { background: #f8fafc; }
.superit-theme .activites-table thead {
  background: rgba(255, 255, 255, 0.04);
}
.activites-table th {
  padding: 14px 16px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  font-size: 12.5px;
}
.superit-theme .activites-table th { color: #94a3b8; }
.activites-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  vertical-align: middle;
}
.superit-theme .activites-table td {
  border-bottom-color: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
}
.activites-table tr:last-child td { border-bottom: none; }
.activites-table tr:hover { background: #f8fafc; }
.superit-theme .activites-table tr:hover {
  background: rgba(255, 255, 255, 0.02);
}
.table-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}
.table-thumb img { width: 100%; height: 100%; object-fit: cover; }
.table-icon { color: #10b981; font-size: 18px; }
.superit-theme .table-icon { color: #818cf8; }
.table-actions { display: flex; gap: 6px; }
.table-actions .btn-icon { flex: none; width: 32px; padding: 7px; }
.status-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}
.superit-theme .status-badge.inactive {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

/* ============================================================
   MODALE
   ============================================================ */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}
.superit-theme .modal-overlay {
  background: rgba(15, 23, 42, 0.8);
}
.modal-box {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-box.modal-large { max-width: 760px; }
.superit-theme .modal-box {
  background: #1e1b4b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
  position: sticky;
  top: 0;
  background: #fff;
  border-radius: 16px 16px 0 0;
  z-index: 1;
}
.superit-theme .modal-header {
  background: #1e1b4b;
  border-bottom-color: rgba(255, 255, 255, 0.08);
}
.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}
.modal-title i { font-size: 20px; color: #10b981; }
.superit-theme .modal-title i { color: #818cf8; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0; }
.superit-theme .modal-title h2 { color: #fff; }
.close-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  background: none;
  color: #94a3b8;
  cursor: pointer;
}
.close-btn:hover { background: #f1f5f9; color: #0f172a; }
.superit-theme .close-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.modal-form {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label {
  font-size: 12.5px;
  font-weight: 600;
  color: #334155;
}
.superit-theme .form-group label { color: #cbd5e1; }
.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 9px;
  font-size: 13.5px;
  font-family: inherit;
  background: #f8fafc;
  color: #0f172a;
  resize: vertical;
}
.superit-theme .form-group input,
.superit-theme .form-group select,
.superit-theme .form-group textarea {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #10b981;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
.superit-theme .form-group input:focus,
.superit-theme .form-group select:focus,
.superit-theme .form-group textarea:focus {
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
}

.icon-input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.icon-preview {
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  border-radius: 10px;
  background: #ecfdf5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #10b981;
  font-size: 18px;
}
.superit-theme .icon-preview {
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
}
.icon-input-wrap input { flex: 1; }

/* ============================================================
   UPLOADER D'IMAGES
   ============================================================ */
.image-uploader { position: relative; }
.file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  overflow: hidden;
}
.file-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 20px;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  background: #f8fafc;
  color: #475569;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.file-label:hover {
  border-color: #6366f1;
  background: #eef2ff;
  color: #4338ca;
}
.superit-theme .file-label {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.15);
  color: #cbd5e1;
}
.superit-theme .file-label:hover {
  background: rgba(99, 102, 241, 0.15);
  border-color: #818cf8;
  color: #e0e7ff;
}
.file-label i { font-size: 1.2rem; }

.image-preview {
  margin-top: 10px;
  border-radius: 12px;
  overflow: hidden;
  max-width: 200px;
}
.image-preview img { width: 100%; display: block; }

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  margin-top: 12px;
}
.gallery-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  background: #f1f5f9;
}
.gallery-item.new { border: 2px solid #6366f1; }
.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.gallery-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: none;
  background: rgba(239, 68, 68, 0.9);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  transition: transform 0.15s ease;
}
.gallery-remove:hover {
  transform: scale(1.15);
  background: #dc2626;
}

/* ============================================================
   CHECKBOX
   ============================================================ */
.checkbox-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
  cursor: pointer;
}
.superit-theme .checkbox-wrap { color: #cbd5e1; }
.checkbox-wrap input {
  width: 16px;
  height: 16px;
  accent-color: #10b981;
}
.superit-theme .checkbox-wrap input { accent-color: #6366f1; }

/* ============================================================
   ACTIONS MODALE
   ============================================================ */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
}
.superit-theme .modal-actions {
  border-top-color: rgba(255, 255, 255, 0.08);
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 9px;
  font-size: 13.5px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
.btn-primary {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
}
.btn-primary.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
}
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary {
  background: rgba(255, 255, 255, 0.06);
  color: #cbd5e1;
}
.btn-secondary:hover { background: #e2e8f0; }
.superit-theme .btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* ============================================================
   TRANSITION
   ============================================================ */
.fade-enter-active,
.fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>