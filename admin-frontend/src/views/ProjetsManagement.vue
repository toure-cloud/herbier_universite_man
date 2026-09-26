<template>
  <div class="projets-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Projets"
        subtitle="Gérez les projets de recherche et de conservation"
        icon="fas fa-project-diagram"
      >
        <template #actions>
          <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
            <i class="fas fa-plus"></i> Nouveau projet
          </button>
        </template>
      </TopBar>

      <!-- Filtres -->
      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher un projet…" />
        </div>
        <select v-model="filterCategorie" class="filter-select">
          <option value="">Toutes les catégories</option>
          <option v-for="c in categories" :key="c.value" :value="c.value">{{ c.label }}</option>
        </select>
        <select v-model="filterStatut" class="filter-select">
          <option value="">Tous les statuts</option>
          <option v-for="s in statuts" :key="s.value" :value="s.value">{{ s.label }}</option>
        </select>
        <div class="result-count">
          <i class="fas fa-project-diagram"></i> {{ filtered.length }} projet(s)
        </div>
      </section>

      <!-- États -->
      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-folder-open"></i>
        <h3>Aucun projet trouvé</h3>
        <p>Ajoutez un nouveau projet ou modifiez vos filtres</p>
        <button class="btn-create" :class="{ it: auth.isSuperIT }" @click="openCreate">
          <i class="fas fa-plus"></i> Nouveau projet
        </button>
      </section>

      <!-- Grille -->
      <section v-else class="projets-grid">
        <article v-for="p in filtered" :key="p.id" class="projet-card">
          <div class="projet-image">
            <img
              v-if="getMainImage(p)"
              :src="getImageUrl(getMainImage(p))"
              :alt="p.titre"
              @error="onImageError"
            />
            <div v-else class="no-image"><i class="fas fa-image"></i></div>

            <span v-if="p.categorie" class="cat-badge">{{ getCategorieLabel(p.categorie) }}</span>
            <span
              v-if="p.statut"
              class="statut-badge"
              :class="`statut-${p.statut}`"
            >
              {{ getStatutLabel(p.statut) }}
            </span>
            <span v-if="hasMultipleImages(p)" class="images-count">
              <i class="fas fa-images"></i> {{ getAllImages(p).length }}
            </span>
          </div>

          <div class="projet-body">
            <h3>{{ p.titre }}</h3>
            <p class="projet-desc">{{ truncate(p.description, 110) }}</p>
            <div class="projet-meta">
              <span v-if="p.annee"><i class="fas fa-calendar"></i> {{ p.annee }}</span>
              <span v-if="p.lieu"><i class="fas fa-map-marker-alt"></i> {{ p.lieu }}</span>
            </div>
            <div v-if="p.progression != null" class="progression">
              <div class="prog-bar">
                <div class="prog-fill" :style="{ width: `${p.progression}%` }"></div>
              </div>
              <span class="prog-label">{{ p.progression }}%</span>
            </div>
          </div>

          <div class="projet-actions">
            <button class="btn-icon" @click="openEdit(p)" title="Modifier">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon danger" @click="remove(p)" title="Supprimer">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <!-- Modal création/édition -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box modal-large">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-project-diagram'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouveau' }} projet</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-group">
              <label>Titre *</label>
              <input v-model.trim="form.titre" type="text" placeholder="Titre du projet" required />
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Catégorie *</label>
                <select v-model="form.categorie" required>
                  <option v-for="c in categories" :key="c.value" :value="c.value">{{ c.label }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Statut *</label>
                <select v-model="form.statut" required>
                  <option v-for="s in statuts" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </div>
            </div>

            <div class="form-row-3">
              <div class="form-group">
                <label>Année / Période</label>
                <input v-model.trim="form.annee" type="text" placeholder="2023-2024" />
              </div>
              <div class="form-group">
                <label>Lieu</label>
                <input v-model.trim="form.lieu" type="text" placeholder="Man, Côte d'Ivoire" />
              </div>
              <div class="form-group">
                <label>Progression (%)</label>
                <input v-model.number="form.progression" type="number" min="0" max="100" />
              </div>
            </div>

            <div class="form-group">
              <label>Description courte *</label>
              <textarea v-model="form.description" rows="3" required placeholder="Résumé du projet…"></textarea>
            </div>

            <div class="form-group">
              <label>Description détaillée</label>
              <textarea v-model="form.description_longue" rows="4" placeholder="Détails, objectifs…"></textarea>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Partenaires</label>
                <input v-model.number="form.partenaires_count" type="number" min="0" placeholder="0" />
              </div>
              <div class="form-group">
                <label>Budget</label>
                <input v-model.trim="form.budget" type="text" placeholder="10 000 000 FCFA" />
              </div>
            </div>

            <div class="form-group">
              <label>À la une</label>
              <label class="checkbox-wrap">
                <input type="checkbox" v-model="form.featured" />
                <span>Mettre ce projet en avant sur la page d'accueil</span>
              </label>
            </div>

            <div class="form-group">
              <ImageUploader
                v-model="form.imagesFiles"
                label="Images du projet"
                icon="fas fa-images"
                :multiple="true"
                :max-files="8"
                :max-size="5"
                :existing-images="form.imagesExisting"
                @files-changed="handleImagesChange"
              />
              <p class="help-text">La première image servira de couverture.</p>
            </div>

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
import { projetsAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const projets = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const filterCategorie = ref('')
const filterStatut = ref('')
const showModal = ref(false)
const editing = ref(null)

const categories = [
  { value: 'recherche', label: '🔬 Recherche' },
  { value: 'conservation', label: '🌿 Conservation' },
  { value: 'formation', label: '📚 Formation' },
  { value: 'developpement', label: '💼 Développement' },
]

const statuts = [
  { value: 'termine', label: '✅ Terminé' },
  { value: 'encours', label: '🔄 En cours' },
  { value: 'planifie', label: '📅 Planifié' },
]

const form = ref({
  titre: '',
  categorie: 'recherche',
  statut: 'encours',
  annee: '',
  lieu: '',
  progression: 0,
  description: '',
  description_longue: '',
  partenaires_count: 0,
  budget: '',
  featured: false,
  imagesFiles: [],
  imagesExisting: [],
})

const filtered = computed(() => {
  let list = projets.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(
      (p) =>
        p.titre?.toLowerCase().includes(q) ||
        p.description?.toLowerCase().includes(q) ||
        p.lieu?.toLowerCase().includes(q)
    )
  }
  if (filterCategorie.value) list = list.filter((p) => p.categorie === filterCategorie.value)
  if (filterStatut.value) list = list.filter((p) => p.statut === filterStatut.value)
  return list
})

const getCategorieLabel = (v) => categories.find((c) => c.value === v)?.label || v
const getStatutLabel = (v) => statuts.find((s) => s.value === v)?.label || v

// ✅ Renvoie la liste des chemins d'images (relatifs ou absolus)
const getAllImages = (p) => {
  if (Array.isArray(p.images) && p.images.length) return p.images
  if (Array.isArray(p.images_galerie) && p.images_galerie.length) return p.images_galerie
  if (p.image) return [p.image]
  return []
}

const getMainImage = (p) => getAllImages(p)[0] || null
const hasMultipleImages = (p) => getAllImages(p).length > 1

// ✅ Construit une URL absolue pour afficher l'image
//    - Si l'URL est déjà absolue (http/https) → on la garde
//    - Si c'est un chemin /media/... → on préfixe avec l'URL de base du backend admin
//    - Sinon → on renvoie tel quel
const getImageUrl = (path) => {
  if (!path) return ''
  if (typeof path !== 'string') return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('data:') || path.startsWith('blob:')) return path

  // Base URL du backend admin (sans /api)
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'
  const baseUrl = apiUrl.replace(/\/api\/?$/, '')

  if (path.startsWith('/media')) {
    return `${baseUrl}${path}`
  }
  if (path.startsWith('media/')) {
    return `${baseUrl}/${path}`
  }
  // Cas par défaut : on suppose un chemin relatif sous /media/
  return `${baseUrl}/media/${path.replace(/^\/+/, '')}`
}

const onImageError = (e) => {
  e.target.style.display = 'none'
}

const truncate = (t, n) => (t?.length > n ? t.slice(0, n) + '…' : t || '')

const load = async () => {
  loading.value = true
  try {
    const { data } = await projetsAPI.list()
    projets.value = Array.isArray(data) ? data : data.results || []
  } catch {
    toast.error('Impossible de charger les projets')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editing.value = null
  form.value = {
    titre: '', categorie: 'recherche', statut: 'encours',
    annee: '', lieu: '', progression: 0,
    description: '', description_longue: '',
    partenaires_count: 0, budget: '',
    featured: false,
    imagesFiles: [], imagesExisting: [],
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (p) => {
  editing.value = p
  form.value = {
    titre: p.titre || '',
    categorie: p.categorie || 'recherche',
    statut: p.statut || 'encours',
    annee: p.annee || '',
    lieu: p.lieu || '',
    progression: p.progression ?? 0,
    description: p.description || '',
    description_longue: p.description_longue || '',
    partenaires_count: p.partenaires_count ?? 0,
    budget: p.budget || '',
    featured: p.featured === true,
    imagesFiles: [],
    imagesExisting: getAllImages(p),
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
  if (!form.value.titre || !form.value.description) {
    toast.error('Titre et description obligatoires')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('titre', form.value.titre)
    fd.append('categorie', form.value.categorie)
    fd.append('statut', form.value.statut)
    if (form.value.annee) fd.append('annee', form.value.annee)
    if (form.value.lieu) fd.append('lieu', form.value.lieu)
    fd.append('progression', String(form.value.progression || 0))
    fd.append('description', form.value.description)
    if (form.value.description_longue) fd.append('description_longue', form.value.description_longue)
    fd.append('partenaires_count', String(form.value.partenaires_count || 0))
    if (form.value.budget) fd.append('budget', form.value.budget)
    fd.append('featured', form.value.featured ? 'true' : 'false')

    // Nouvelles images
    form.value.imagesFiles.forEach((f) => fd.append('images', f))

    // Images existantes conservées (JSON)
    if (form.value.imagesExisting.length) {
      fd.append('existing_images', JSON.stringify(form.value.imagesExisting))
    }

    if (editing.value) {
      await projetsAPI.update(editing.value.id, fd)
      toast.success('Projet modifié')
    } else {
      await projetsAPI.create(fd)
      toast.success('Projet ajouté')
    }
    closeModal()
    await load()
  } catch (err) {
    logger.warn('Save projet error')
    toast.error(err.response?.data?.error || 'Erreur lors de l\'enregistrement')
  } finally {
    saving.value = false
  }
}

const remove = async (p) => {
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer définitivement « ${p.titre} » ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await projetsAPI.remove(p.id)
    toast.success('Projet supprimé')
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
   LAYOUT
   ============================================================ */
.projets-layout {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', system-ui, sans-serif;
}
.projets-layout.superit-theme {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}
.main-content {
  margin-left: 260px;
  padding: 24px 28px 40px;
  transition: margin-left 0.3s ease;
}
.main-content.expanded { margin-left: 76px; }

/* ============================================================
   BOUTON CRÉER
   ============================================================ */
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
  font-family: inherit;
  transition: all 0.15s;
  box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5);
}
.btn-create:hover { transform: translateY(-1px); }
.btn-create.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5);
}

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
  transition: all 0.15s;
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
.filter-select {
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13.5px;
  background: #f8fafc;
  font-family: inherit;
  cursor: pointer;
  color: #0f172a;
}
.superit-theme .filter-select {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.filter-select:focus { outline: none; border-color: #10b981; }
.superit-theme .filter-select:focus { border-color: #818cf8; }
.superit-theme .filter-select option {
  background: #1e1b4b;
  color: #fff;
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
.loading-block, .empty-block {
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
@keyframes spin { to { transform: rotate(360deg); } }
.loading-block p { color: #94a3b8; margin: 0; }
.empty-block i {
  font-size: 48px;
  color: #cbd5e1;
  margin-bottom: 12px;
  display: block;
}
.superit-theme .empty-block i { color: #6366f1; }
.empty-block h3 { color: #0f172a; margin: 0 0 6px; font-size: 16px; }
.superit-theme .empty-block h3 { color: #fff; }
.empty-block p { color: #64748b; font-size: 13px; margin: 0 0 16px; }
.superit-theme .empty-block p { color: #94a3b8; }

/* ============================================================
   GRILLE PROJETS
   ============================================================ */
.projets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 18px;
}
.projet-card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.15s;
  display: flex;
  flex-direction: column;
}
.superit-theme .projet-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.projet-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1);
}
.superit-theme .projet-card:hover {
  border-color: rgba(129, 140, 248, 0.4);
  box-shadow: 0 12px 30px -8px rgba(99, 102, 241, 0.3);
}

.projet-image {
  position: relative;
  aspect-ratio: 16 / 10;
  background: #f1f5f9;
  overflow: hidden;
}
.superit-theme .projet-image { background: rgba(255, 255, 255, 0.03); }
.projet-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.projet-card:hover .projet-image img { transform: scale(1.04); }
.no-image {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #cbd5e1;
  font-size: 40px;
}
.superit-theme .no-image { color: #6366f1; }

.cat-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10.5px;
  font-weight: 600;
  color: #fff;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
}
.statut-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 10.5px;
  font-weight: 600;
  color: #fff;
  backdrop-filter: blur(4px);
}
.statut-termine { background: rgba(16, 185, 129, 0.9); }
.statut-encours { background: rgba(245, 158, 11, 0.9); color: #1a1a1a; }
.statut-planifie { background: rgba(59, 130, 246, 0.9); }

.images-count {
  position: absolute;
  bottom: 10px;
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

.projet-body { padding: 16px 18px 12px; flex: 1; }
.projet-body h3 {
  font-size: 15px;
  color: #0f172a;
  margin: 0 0 6px;
  font-weight: 700;
}
.superit-theme .projet-body h3 { color: #fff; }
.projet-desc {
  font-size: 12.5px;
  color: #475569;
  line-height: 1.4;
  margin: 0 0 10px;
}
.superit-theme .projet-desc { color: #cbd5e1; }
.projet-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 10px;
}
.superit-theme .projet-meta { color: #94a3b8; }
.projet-meta i { color: #94a3b8; font-size: 11px; margin-right: 3px; }

.progression { display: flex; align-items: center; gap: 10px; }
.prog-bar {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}
.superit-theme .prog-bar { background: rgba(255, 255, 255, 0.08); }
.prog-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #f59e0b);
  border-radius: 3px;
  transition: width 0.4s;
}
.superit-theme .prog-fill {
  background: linear-gradient(90deg, #818cf8, #facc15);
}
.prog-label {
  font-size: 11px;
  font-weight: 600;
  color: #10b981;
}
.superit-theme .prog-label { color: #818cf8; }

.projet-actions {
  display: flex;
  gap: 8px;
  padding: 10px 18px 14px;
  border-top: 1px solid #f1f5f9;
}
.superit-theme .projet-actions {
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
  transition: all 0.15s;
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
.btn-icon.danger {
  color: #ef4444;
  border-color: #fecaca;
}
.superit-theme .btn-icon.danger {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}
.btn-icon.danger:hover { background: #fef2f2; }
.superit-theme .btn-icon.danger:hover {
  background: rgba(239, 68, 68, 0.15);
}

/* ============================================================
   MODAL
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
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
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
.modal-title { display: flex; align-items: center; gap: 12px; }
.modal-title i { font-size: 20px; color: #10b981; }
.superit-theme .modal-title i { color: #818cf8; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0; font-weight: 700; }
.superit-theme .modal-title h2 { color: #fff; }
.close-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  background: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 15px;
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
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-row-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
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
  transition: all 0.15s;
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
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

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

.help-text {
  font-size: 11.5px;
  color: #94a3b8;
  margin: 0;
}

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
  font-family: inherit;
  transition: all 0.15s;
}
.btn-primary {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
}
.btn-primary.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 12px -4px rgba(99, 102, 241, 0.5);
}
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary {
  background: rgba(255, 255, 255, 0.06);
  color: #cbd5e1;
}
.btn-secondary:hover { background: #e2e8f0; }
.superit-theme .btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2, .form-row-3 { grid-template-columns: 1fr; }
}
</style>