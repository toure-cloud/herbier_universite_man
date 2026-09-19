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

      <!-- ==================== FILTRES ==================== -->
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
          <option value="">Tous les statuts UICN</option>
          <option v-for="s in statutsConservation" :key="s.value" :value="s.value">{{ s.label }}</option>
        </select>
        <div class="result-count">
          <i class="fas fa-leaf"></i> {{ filtered.length }} plante(s)
        </div>
      </section>

      <!-- ==================== LOADING ==================== -->
      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <!-- ==================== EMPTY ==================== -->
      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-seedling"></i>
        <h3>Aucune plante trouvée</h3>
        <p>Ajoutez votre première plante</p>
        <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
          <i class="fas fa-plus"></i> Nouvelle plante
        </button>
      </section>

      <!-- ==================== GRILLE ==================== -->
      <section v-else class="plantes-grid">
        <article v-for="p in filtered" :key="p.id" class="plante-card">
          <div class="plante-image">
            <img v-if="getMainImage(p)" :src="getImageUrl(getMainImage(p))" :alt="p.nom_scientifique" @error="onImageError" />
            <div v-else class="no-image"><i class="fas fa-leaf"></i></div>
            <span v-if="p.statut_conservation" class="statut-badge" :class="getStatutClass(p.statut_conservation)">
              {{ p.statut_conservation_label || p.statut_conservation }}
            </span>
            <span v-if="p.images_galerie && p.images_galerie.length" class="gallery-count">
              <i class="fas fa-images"></i> {{ p.images_galerie.length }}
            </span>
          </div>
          <div class="plante-body">
            <h3 class="plante-nom-scientifique">{{ p.nom_scientifique }}</h3>
            <p v-if="p.nom_vernaculaire" class="plante-vernaculaire">{{ p.nom_vernaculaire }}</p>
            <p class="plante-famille" v-if="p.famille"><i class="fas fa-tag"></i> {{ p.famille }}</p>
            <p class="plante-desc" v-if="p.description">{{ truncate(p.description, 100) }}</p>
            <div class="plante-meta">
              <span class="status-badge" :class="p.actif ? 'active' : 'inactive'">
                {{ p.actif ? 'Actif' : 'Inactif' }}
              </span>
              <span v-if="p.lieu_collecte" class="meta-lieu"><i class="fas fa-map-marker-alt"></i> {{ truncate(p.lieu_collecte, 30) }}</span>
            </div>
          </div>
          <div class="plante-actions">
            <button class="btn-icon" @click="openEdit(p)"><i class="fas fa-edit"></i></button>
            <button class="btn-icon danger" @click="remove(p)"><i class="fas fa-trash"></i></button>
          </div>
        </article>
      </section>
    </main>

    <!-- ==================== MODALE CRÉATION / ÉDITION ==================== -->
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
            <!-- Ligne 1 : Noms -->
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom scientifique *</label>
                <input v-model.trim="form.nom_scientifique" type="text" required placeholder="Ex : Khaya senegalensis" />
              </div>
              <div class="form-group">
                <label>Nom vernaculaire</label>
                <input v-model.trim="form.nom_vernaculaire" type="text" placeholder="Ex : Caïlcédrat" />
              </div>
            </div>

            <!-- Ligne 2 : Famille + Type morphologique -->
            <div class="form-row-2">
              <div class="form-group">
                <label>Famille</label>
                <input v-model.trim="form.famille" type="text" placeholder="Ex : Meliaceae" />
              </div>
              <div class="form-group">
                <label>Type morphologique</label>
                <input v-model.trim="form.type_morphologique" type="text" placeholder="Arbre, arbuste, herbe…" />
              </div>
            </div>

            <!-- Ligne 3 : Type biologique + Affinité chorologique -->
            <div class="form-row-2">
              <div class="form-group">
                <label>Type biologique</label>
                <input v-model.trim="form.type_biologique" type="text" placeholder="Phanérophyte, thérophyte…" />
              </div>
              <div class="form-group">
                <label>Affinité chorologique</label>
                <input v-model.trim="form.affinite_chorologique" type="text" placeholder="Soudano-zambézienne…" />
              </div>
            </div>

            <!-- Ligne 4 : Affinité écologique + Statut UICN -->
            <div class="form-row-2">
              <div class="form-group">
                <label>Affinité écologique</label>
                <input v-model.trim="form.affinite_ecologique" type="text" placeholder="Mésophile, xérophile…" />
              </div>
              <div class="form-group">
                <label>Statut de conservation (UICN)</label>
                <select v-model="form.statut_conservation">
                  <option v-for="s in statutsConservation" :key="s.value" :value="s.value">
                    {{ s.label }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Lieu de collecte -->
            <div class="form-group">
              <label>Lieu de collecte</label>
              <input v-model.trim="form.lieu_collecte" type="text" placeholder="Ex : Mont Tonkoui, Man" />
            </div>

            <!-- Habitat -->
            <div class="form-group">
              <label>Habitat</label>
              <textarea v-model="form.habitat" rows="2" placeholder="Description de l'habitat…"></textarea>
            </div>

            <!-- Description -->
            <div class="form-group">
              <label>Description</label>
              <textarea v-model="form.description" rows="4" placeholder="Description botanique…"></textarea>
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
                  id="main-image-input"
                />
                <label for="main-image-input" class="file-label">
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
                  id="gallery-input"
                />
                <label for="gallery-input" class="file-label">
                  <i class="fas fa-images"></i>
                  <span v-if="!form.galleryFiles.length && !form.imagesExisting.length">
                    Ajouter plusieurs images à la galerie
                  </span>
                  <span v-else>
                    {{ form.galleryFiles.length }} nouvelle(s) + {{ form.imagesExisting.length }} existante(s)
                  </span>
                </label>
              </div>

              <!-- Grille des images existantes (à conserver) -->
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

              <!-- Grille des nouvelles images (à uploader) -->
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
              <span>Plante active (visible sur le site public)</span>
            </label>

            <!-- Actions -->
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { plantesAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
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

// ============================================================
// STATUTS UICN
// ============================================================
const statutsConservation = [
  { value: 'CR', label: 'En danger critique' },
  { value: 'EN', label: 'En danger' },
  { value: 'VU', label: 'Vulnérable' },
  { value: 'NT', label: 'Quasi menacé' },
  { value: 'LC', label: 'Préoccupation mineure' },
  { value: 'NE', label: 'Non évaluée' },
]

// ============================================================
// FORMULAIRE
// ============================================================
const form = ref({
  nom_scientifique: '',
  nom_vernaculaire: '',
  famille: '',
  type_morphologique: '',
  type_biologique: '',
  affinite_chorologique: '',
  affinite_ecologique: '',
  statut_conservation: 'NE',
  lieu_collecte: '',
  habitat: '',
  description: '',
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
const famillesList = computed(() => {
  const set = new Set(plantes.value.map((p) => p.famille).filter(Boolean))
  return [...set].sort()
})

const filtered = computed(() => {
  let list = plantes.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(
      (p) =>
        p.nom_scientifique?.toLowerCase().includes(q) ||
        p.nom_vernaculaire?.toLowerCase().includes(q) ||
        p.famille?.toLowerCase().includes(q) ||
        p.lieu_collecte?.toLowerCase().includes(q)
    )
  }
  if (filterFamille.value) list = list.filter((p) => p.famille === filterFamille.value)
  if (filterStatut.value) list = list.filter((p) => p.statut_conservation === filterStatut.value)
  return list
})

// ============================================================
// HELPERS
// ============================================================
const getMainImage = (p) => p.image || null

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')

const onImageError = (e) => {
  e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Crect fill='%23f1f5f9' width='200' height='200'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='12' fill='%2394a3b8' text-anchor='middle' dy='.3em'%3EPas+image%3C/text%3E%3C/svg%3E"
}

const getImageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  if (path.startsWith('/media')) {
    // Le base URL de l'admin est sur /api, donc on enlève /api pour les médias
    const base = (import.meta.env.VITE_API_URL || 'http://localhost:8001/api').replace(/\/api$/, '')
    return `${base}${path}`
  }
  return path
}

const previewNewFile = (file) => {
  if (!file) return ''
  return URL.createObjectURL(file)
}

const getStatutClass = (s) => {
  return {
    CR: 'critical',
    EN: 'endangered',
    VU: 'vulnerable',
    NT: 'near-threatened',
    LC: 'least-concern',
    NE: 'not-evaluated',
  }[s] || 'not-evaluated'
}

// ============================================================
// CHARGEMENT
// ============================================================
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

// ============================================================
// MODALE CRÉATION / ÉDITION
// ============================================================
const openCreate = () => {
  editing.value = null
  form.value = {
    nom_scientifique: '',
    nom_vernaculaire: '',
    famille: '',
    type_morphologique: '',
    type_biologique: '',
    affinite_chorologique: '',
    affinite_ecologique: '',
    statut_conservation: 'NE',
    lieu_collecte: '',
    habitat: '',
    description: '',
    actif: true,
    imageFile: null,
    imageExisting: null,
    galleryFiles: [],
    imagesExisting: [],
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (p) => {
  editing.value = p
  form.value = {
    nom_scientifique: p.nom_scientifique || '',
    nom_vernaculaire: p.nom_vernaculaire || '',
    famille: p.famille || '',
    type_morphologique: p.type_morphologique || '',
    type_biologique: p.type_biologique || '',
    affinite_chorologique: p.affinite_chorologique || '',
    affinite_ecologique: p.affinite_ecologique || '',
    statut_conservation: p.statut_conservation || 'NE',
    lieu_collecte: p.lieu_collecte || '',
    habitat: p.habitat || '',
    description: p.description || '',
    actif: p.actif !== false,
    imageFile: null,
    imageExisting: p.image || null,
    galleryFiles: [],
    imagesExisting: Array.isArray(p.images_galerie) ? [...p.images_galerie] : [],
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
// GESTION DES IMAGES
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
// SAUVEGARDE
// ============================================================
const save = async () => {
  if (!form.value.nom_scientifique) {
    toast.error('Le nom scientifique est obligatoire')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()

    // Champs texte
    fd.append('nom_scientifique', form.value.nom_scientifique)
    if (form.value.nom_vernaculaire) fd.append('nom_vernaculaire', form.value.nom_vernaculaire)
    if (form.value.famille) fd.append('famille', form.value.famille)
    if (form.value.type_morphologique) fd.append('type_morphologique', form.value.type_morphologique)
    if (form.value.type_biologique) fd.append('type_biologique', form.value.type_biologique)
    if (form.value.affinite_chorologique) fd.append('affinite_chorologique', form.value.affinite_chorologique)
    if (form.value.affinite_ecologique) fd.append('affinite_ecologique', form.value.affinite_ecologique)
    fd.append('statut_conservation', form.value.statut_conservation || 'NE')
    if (form.value.lieu_collecte) fd.append('lieu_collecte', form.value.lieu_collecte)
    if (form.value.habitat) fd.append('habitat', form.value.habitat)
    if (form.value.description) fd.append('description', form.value.description)
    fd.append('actif', form.value.actif ? 'true' : 'false')

    // Image principale
    if (form.value.imageFile) {
      fd.append('image', form.value.imageFile)
    }

    // Nouvelles images galerie : gallery_0, gallery_1, ...
    form.value.galleryFiles.forEach((file, i) => {
      fd.append(`gallery_${i}`, file)
    })

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
    logger.warn('Save plante error', err)
    toast.error(err.response?.data?.error || "Erreur lors de l'enregistrement")
  } finally {
    saving.value = false
  }
}

// ============================================================
// SUPPRESSION
// ============================================================
const remove = async (p) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${p.nom_scientifique} » ? Cette action est irréversible.`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await plantesAPI.remove(p.id)
    toast.success('Plante supprimée')
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
.plantes-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.plantes-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.btn-create {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; border: none; border-radius: 10px;
  font-size: 13.5px; font-weight: 600; cursor: pointer;
  box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5);
}
.btn-create.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5);
}
.btn-create:hover { transform: translateY(-1px); }

/* ============================================================
   FILTRES
   ============================================================ */
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
.search-wrap input:focus { outline: none; border-color: #10b981; background: #fff; }
.superit-theme .search-wrap input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); }
.filter-select {
  padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 13.5px; background: #f8fafc; cursor: pointer; color: #0f172a;
}
.superit-theme .filter-select {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.superit-theme .filter-select option { background: #1e1b4b; }
.result-count {
  font-size: 12.5px; color: #64748b;
  padding: 6px 14px; background: #f1f5f9; border-radius: 20px;
}
.superit-theme .result-count { color: #94a3b8; background: rgba(255, 255, 255, 0.04); }
.result-count i { color: #10b981; margin-right: 4px; }
.superit-theme .result-count i { color: #818cf8; }

/* ============================================================
   LOADING / EMPTY
   ============================================================ */
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

/* ============================================================
   GRILLE
   ============================================================ */
.plantes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}
.plante-card {
  background: #fff; border-radius: 14px; overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.15s;
  display: flex; flex-direction: column;
}
.superit-theme .plante-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.plante-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }
.superit-theme .plante-card:hover { border-color: rgba(129, 140, 248, 0.4); }

.plante-image {
  position: relative; aspect-ratio: 4 / 3;
  background: #f1f5f9; overflow: hidden;
}
.superit-theme .plante-image { background: rgba(255, 255, 255, 0.03); }
.plante-image img { width: 100%; height: 100%; object-fit: cover; }
.no-image {
  display: flex; align-items: center; justify-content: center;
  height: 100%; color: #cbd5e1; font-size: 40px;
}
.superit-theme .no-image { color: #6366f1; }

.statut-badge {
  position: absolute; top: 10px; left: 10px;
  padding: 4px 10px; border-radius: 20px;
  font-size: 10.5px; font-weight: 600; color: #fff;
}
.statut-badge.critical { background: rgba(220, 38, 38, 0.9); }
.statut-badge.endangered { background: rgba(234, 88, 12, 0.9); }
.statut-badge.vulnerable { background: rgba(245, 158, 11, 0.9); color: #1a1a1a; }
.statut-badge.near-threatened { background: rgba(59, 130, 246, 0.9); }
.statut-badge.least-concern { background: rgba(16, 185, 129, 0.9); }
.statut-badge.not-evaluated { background: rgba(148, 163, 184, 0.9); }

.gallery-count {
  position: absolute; bottom: 10px; right: 10px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff; padding: 4px 10px;
  border-radius: 20px; font-size: 10.5px;
  display: inline-flex; align-items: center; gap: 4px;
}

.plante-body { padding: 16px 18px 12px; flex: 1; }
.plante-nom-scientifique {
  font-size: 15px; color: #0f172a; margin: 0 0 4px;
  font-weight: 700; font-style: italic;
}
.superit-theme .plante-nom-scientifique { color: #fff; }
.plante-vernaculaire { font-size: 13px; color: #64748b; margin: 0 0 6px; }
.superit-theme .plante-vernaculaire { color: #94a3b8; }
.plante-famille {
  font-size: 12px; color: #10b981; margin: 0 0 6px; font-weight: 500;
}
.superit-theme .plante-famille { color: #818cf8; }
.plante-desc {
  font-size: 12.5px; color: #475569; line-height: 1.4; margin: 0 0 12px;
}
.superit-theme .plante-desc { color: #cbd5e1; }
.plante-meta {
  display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
}
.status-badge {
  padding: 3px 10px; border-radius: 20px;
  font-size: 10.5px; font-weight: 600;
}
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.superit-theme .status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.meta-lieu { font-size: 10.5px; color: #64748b; }
.superit-theme .meta-lieu { color: #94a3b8; }

.plante-actions {
  display: flex; gap: 8px;
  padding: 10px 18px 14px;
  border-top: 1px solid #f1f5f9;
}
.superit-theme .plante-actions { border-top-color: rgba(255, 255, 255, 0.06); }
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

/* ============================================================
   MODALE
   ============================================================ */
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
  width: 100%; max-width: 640px;
  max-height: 90vh; overflow-y: auto;
}
.modal-box.modal-large { max-width: 760px; }
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
.modal-title i { font-size: 20px; color: #10b981; }
.superit-theme .modal-title i { color: #818cf8; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0; }
.superit-theme .modal-title h2 { color: #fff; }
.close-btn {
  width: 34px; height: 34px; border-radius: 50%;
  border: none; background: none; color: #94a3b8; cursor: pointer;
}
.close-btn:hover { background: #f1f5f9; color: #0f172a; }
.superit-theme .close-btn:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }

.modal-form {
  padding: 24px;
  display: flex; flex-direction: column; gap: 16px;
}
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label {
  font-size: 12.5px; font-weight: 600; color: #334155;
}
.superit-theme .form-group label { color: #cbd5e1; }
.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 14px; border: 1.5px solid #e2e8f0;
  border-radius: 9px; font-size: 13.5px;
  font-family: inherit; background: #f8fafc; color: #0f172a;
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
  outline: none; border-color: #10b981;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
.superit-theme .form-group input:focus,
.superit-theme .form-group select:focus,
.superit-theme .form-group textarea:focus {
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
}
.form-group select option { background: #fff; color: #0f172a; }
.superit-theme .form-group select option { background: #1e1b4b; color: #fff; }

/* ============================================================
   UPLOADER D'IMAGES
   ============================================================ */
.image-uploader { position: relative; }
.file-input {
  position: absolute; width: 1px; height: 1px;
  opacity: 0; overflow: hidden;
}
.file-label {
  display: flex; align-items: center; justify-content: center;
  gap: 10px; padding: 14px 20px;
  border: 2px dashed #cbd5e1; border-radius: 12px;
  background: #f8fafc; color: #475569;
  font-size: 0.9rem; cursor: pointer;
  transition: all 0.2s ease;
}
.file-label:hover {
  border-color: #6366f1; background: #eef2ff; color: #4338ca;
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
  margin-top: 10px; border-radius: 12px;
  overflow: hidden; max-width: 200px;
}
.image-preview img { width: 100%; display: block; }

.gallery-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px; margin-top: 12px;
}
.gallery-item {
  position: relative; aspect-ratio: 1;
  border-radius: 10px; overflow: hidden;
  border: 1px solid #e2e8f0; background: #f1f5f9;
}
.gallery-item.new { border: 2px solid #6366f1; }
.gallery-item img {
  width: 100%; height: 100%; object-fit: cover;
}
.gallery-remove {
  position: absolute; top: 4px; right: 4px;
  width: 24px; height: 24px; border-radius: 50%;
  border: none; background: rgba(239, 68, 68, 0.9);
  color: #fff; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem;
  transition: transform 0.15s ease;
}
.gallery-remove:hover { transform: scale(1.15); background: #dc2626; }

/* ============================================================
   CHECKBOX
   ============================================================ */
.checkbox-wrap {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; color: #475569; cursor: pointer;
}
.superit-theme .checkbox-wrap { color: #cbd5e1; }
.checkbox-wrap input {
  width: 16px; height: 16px; accent-color: #10b981;
}
.superit-theme .checkbox-wrap input { accent-color: #6366f1; }

/* ============================================================
   ACTIONS MODALE
   ============================================================ */
.modal-actions {
  display: flex; justify-content: flex-end; gap: 10px;
  padding-top: 8px; border-top: 1px solid #f1f5f9;
}
.superit-theme .modal-actions { border-top-color: rgba(255, 255, 255, 0.08); }
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 9px;
  font-size: 13.5px; font-weight: 600;
  border: none; cursor: pointer;
}
.btn-primary { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
.btn-primary.it { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; }
.btn-secondary:hover { background: #e2e8f0; }
.superit-theme .btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }

/* ============================================================
   TRANSITION
   ============================================================ */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>