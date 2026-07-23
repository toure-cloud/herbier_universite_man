<template>
  <div class="management-page">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon"><i class="fas fa-leaf"></i></div>
          <div class="logo-text">
            <span class="logo-title">Herbier Admin</span>
            <span class="logo-subtitle">Université de Man</span>
          </div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i><span>Tableau de bord</span>
        </router-link>
        <router-link to="/plantes" class="nav-item">
          <i class="fas fa-leaf"></i><span>Plantes</span>
        </router-link>
        <router-link to="/equipe" class="nav-item">
          <i class="fas fa-users"></i><span>Équipe</span>
        </router-link>
        <router-link to="/partenaires" class="nav-item">
          <i class="fas fa-handshake"></i><span>Partenaires</span>
        </router-link>
        <router-link to="/slides" class="nav-item">
          <i class="fas fa-images"></i><span>Slides</span>
        </router-link>
        <router-link to="/projets" class="nav-item active">
          <i class="fas fa-project-diagram"></i><span>Projets</span>
        </router-link>
        <router-link to="/activites" class="nav-item">
          <i class="fas fa-chart-line"></i><span>Activités</span>
        </router-link>
        <router-link to="/temoignages" class="nav-item">
          <i class="fas fa-comment-dots"></i><span>Témoignages</span>
        </router-link>
        <router-link to="/publications" class="nav-item">
          <i class="fas fa-book"></i><span>Publications</span>
        </router-link>
        <router-link to="/statistiques" class="nav-item">
          <i class="fas fa-chart-bar"></i><span>Statistiques</span>
        </router-link>
        <router-link to="/administrateurs" class="nav-item">
          <i class="fas fa-user-shield"></i><span>Administrateurs</span>
          <span class="nav-badge">Admin</span>
        </router-link>
        <router-link to="/settings" class="nav-item">
          <i class="fas fa-cog"></i><span>Paramètres</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info-sidebar">
          <div class="user-avatar-sidebar">{{ userInitials }}</div>
          <div class="user-details-sidebar">
            <span class="user-name-sidebar">{{ user?.nom || 'Admin' }}</span>
            <span class="user-role">{{ isSuperAdmin ? 'Super Admin' : 'Admin' }}</span>
          </div>
        </div>
        <button @click="confirmLogout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i><span>Déconnexion</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-bar">
        <div class="page-title">
          <h1><i class="fas fa-project-diagram"></i> Gestion des Projets</h1>
          <p>Ajoutez, modifiez ou supprimez des projets</p>
        </div>
        <button @click="openModal" class="btn-primary">
          <i class="fas fa-plus"></i> Nouveau projet
        </button>
      </header>

      <!-- Filtres -->
      <div class="filters-bar">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input type="text" v-model="searchQuery" placeholder="Rechercher un projet...">
        </div>
        <select v-model="filters.categorie" class="filter-select">
          <option value="">Toutes les catégories</option>
          <option value="recherche">🔬 Recherche</option>
          <option value="conservation">🌿 Conservation</option>
          <option value="formation">📚 Formation</option>
          <option value="developpement">💼 Développement</option>
        </select>
        <select v-model="filters.statut" class="filter-select">
          <option value="">Tous les statuts</option>
          <option value="termine">✅ Terminé</option>
          <option value="encours">🔄 En cours</option>
          <option value="planifie">📅 Planifié</option>
        </select>
        <div class="stats-badge">
          <i class="fas fa-chart-simple"></i> {{ filteredProjets.length }} projet(s)
        </div>
      </div>

      <!-- Vue Grille -->
      <div class="projects-grid">
        <div v-for="projet in filteredProjets" :key="projet.id" class="project-card">
          <div class="project-image">
            <img :src="getFullImageUrl(projet.image)" @error="handleImageError" :alt="projet.titre">
            <div class="project-category">{{ getCategorieLabel(projet.categorie) }}</div>
            <div class="project-status" :class="projet.statut">{{ getStatutLabel(projet.statut) }}</div>
            <div class="project-featured" v-if="projet.featured">
              <i class="fas fa-star"></i> À la une
            </div>
          </div>
          <div class="project-info">
            <h3>{{ projet.titre }}</h3>
            <p class="project-description">{{ truncate(projet.description, 100) }}</p>
            <div class="project-meta">
              <span><i class="fas fa-calendar"></i> {{ projet.annee || 'N/A' }}</span>
              <span><i class="fas fa-map-marker-alt"></i> {{ projet.lieu || 'N/A' }}</span>
              <span><i class="fas fa-users"></i> {{ projet.partenaires || 0 }} partenaire(s)</span>
            </div>
            <div class="project-progress" v-if="projet.progression !== undefined && projet.progression !== null">
              <div class="progress-label">
                <span>Progression</span>
                <span>{{ projet.progression }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: projet.progression + '%' }"></div>
              </div>
            </div>
            <div class="project-footer">
              <div class="project-tags" v-if="projet.tags">
                <span v-for="tag in getTagList(projet.tags).slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <div class="project-actions">
                <button @click="editItem(projet)" class="btn-edit"><i class="fas fa-edit"></i></button>
                <button @click="deleteItem(projet)" class="btn-delete"><i class="fas fa-trash"></i></button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="filteredProjets.length === 0" class="empty-state">
          <i class="fas fa-project-diagram"></i>
          <h3>Aucun projet trouvé</h3>
          <p>Essayez de modifier vos critères de recherche</p>
          <button @click="resetFilters" class="btn-primary">
            <i class="fas fa-redo-alt"></i> Réinitialiser les filtres
          </button>
        </div>
      </div>

      <!-- Modal Ajout/Modification -->
      <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
        <div class="modal-content modal-large">
          <div class="modal-header">
            <h2>{{ editingId ? 'Modifier' : 'Ajouter' }} un projet</h2>
            <button class="close" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>
          <form @submit.prevent="saveItem" class="modal-form">
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-tag"></i> Titre *</label>
                <input type="text" v-model="form.titre" required placeholder="Titre du projet">
              </div>
              <div class="form-group">
                <label><i class="fas fa-tags"></i> Catégorie *</label>
                <select v-model="form.categorie" required>
                  <option value="recherche">🔬 Recherche</option>
                  <option value="conservation">🌿 Conservation</option>
                  <option value="formation">📚 Formation</option>
                  <option value="developpement">💼 Développement</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-clock"></i> Statut *</label>
                <select v-model="form.statut">
                  <option value="termine">✅ Terminé</option>
                  <option value="encours">🔄 En cours</option>
                  <option value="planifie">📅 Planifié</option>
                </select>
              </div>
              <div class="form-group">
                <label><i class="fas fa-calendar-alt"></i> Année/Période *</label>
                <input type="text" v-model="form.annee" placeholder="2023-2024">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-map-marker-alt"></i> Lieu</label>
                <input type="text" v-model="form.lieu" placeholder="Lieu du projet">
              </div>
              <div class="form-group">
                <label><i class="fas fa-users"></i> Nombre de partenaires</label>
                <input type="number" v-model="form.partenaires" min="0">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-user-graduate"></i> Bénéficiaires</label>
                <input type="text" v-model="form.beneficiaires" placeholder="Étudiants, chercheurs...">
              </div>
              <div class="form-group">
                <label><i class="fas fa-coins"></i> Budget</label>
                <input type="text" v-model="form.budget" placeholder="10 000 000 FCFA">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-hourglass-half"></i> Durée</label>
                <input type="text" v-model="form.duree" placeholder="24 mois">
              </div>
              <div class="form-group">
                <label><i class="fas fa-chart-line"></i> Impact</label>
                <input type="text" v-model="form.impact" placeholder="Impact du projet">
              </div>
            </div>
            <div class="form-group">
              <label><i class="fas fa-percent"></i> Progression (%)</label>
              <input type="number" v-model="form.progression" min="0" max="100">
            </div>
            <div class="form-group">
              <label><i class="fas fa-align-left"></i> Description courte *</label>
              <textarea v-model="form.description" rows="3" required placeholder="Description courte du projet"></textarea>
            </div>
            <div class="form-group">
              <label><i class="fas fa-align-justify"></i> Description détaillée</label>
              <textarea v-model="form.description_longue" rows="5" placeholder="Description détaillée du projet"></textarea>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-bullseye"></i> Objectifs</label>
                <textarea v-model="form.objectifs" rows="3" placeholder="Objectifs du projet"></textarea>
              </div>
              <div class="form-group">
                <label><i class="fas fa-check-double"></i> Résultats</label>
                <textarea v-model="form.resultats" rows="3" placeholder="Résultats obtenus"></textarea>
              </div>
            </div>
            <div class="form-group">
              <label><i class="fas fa-tags"></i> Tags</label>
              <input type="text" v-model="form.tags" placeholder="biodiversité, conservation, recherche (séparés par des virgules)">
            </div>
            <div class="form-group">
              <label><i class="fas fa-image"></i> Image principale</label>
              <div class="image-upload-area" 
                   @dragover.prevent @drop.prevent="handleDrop" 
                   @click="triggerFileInput"
                   :class="{ 'has-image': form.image_preview }">
                <div v-if="form.image_preview" class="image-preview">
                  <img :src="form.image_preview" alt="Aperçu">
                  <button type="button" class="remove-image" @click.stop="removeImage">✕</button>
                </div>
                <div v-else class="upload-placeholder">
                  <i class="fas fa-cloud-upload-alt"></i>
                  <p>Cliquez ou déposez une image ici</p>
                  <span class="upload-hint">PNG, JPG, JPEG, WEBP</span>
                </div>
                <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" style="display:none">
              </div>
              <small class="form-help" v-if="form._existing_image">Image actuelle</small>
            </div>
            <div class="form-group">
              <label><i class="fas fa-images"></i> Images galerie (URLs séparées par des virgules)</label>
              <input type="text" v-model="imagesGalerieInput" placeholder="https://.../image1.jpg, https://.../image2.jpg">
            </div>
            <div class="form-group checkbox">
              <label>
                <input type="checkbox" v-model="form.featured">
                <span>Projet à la une</span>
              </label>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn-secondary" @click="closeModal">Annuler</button>
              <button type="submit" class="btn-primary" :disabled="loading">
                <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                {{ loading ? 'Enregistrement...' : 'Enregistrer' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Toast -->
      <div v-if="toastMessage" class="toast" :class="toastType">
        <i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
        <span>{{ toastMessage }}</span>
      </div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001'

export default {
  name: 'ProjetsManagement',
  data() {
    return {
      projets: [],
      searchQuery: '',
      filters: {
        categorie: '',
        statut: ''
      },
      showModal: false,
      editingId: null,
      loading: false,
      imagesGalerieInput: '',
      form: {
        titre: '',
        categorie: 'recherche',
        statut: 'encours',
        annee: '',
        lieu: '',
        partenaires: 0,
        beneficiaires: '',
        budget: '',
        duree: '',
        impact: '',
        progression: 0,
        description: '',
        description_longue: '',
        objectifs: '',
        resultats: '',
        tags: '',
        image: '',
        images_galerie: [],
        featured: false,
        image_preview: null,
        image_file: null,
        _existing_image: null
      },
      toastMessage: '',
      toastType: '',
      user: null,
      isSuperAdmin: false
    }
  },
  computed: {
    userInitials() {
      return this.user?.nom ? this.user.nom.split(' ').map(n => n[0]).join('').toUpperCase() : 'AD'
    },
    filteredProjets() {
      let filtered = this.projets
      
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        filtered = filtered.filter(p => 
          p.titre?.toLowerCase().includes(q) || 
          p.description?.toLowerCase().includes(q) ||
          p.lieu?.toLowerCase().includes(q)
        )
      }
      
      if (this.filters.categorie) {
        filtered = filtered.filter(p => p.categorie === this.filters.categorie)
      }
      
      if (this.filters.statut) {
        filtered = filtered.filter(p => p.statut === this.filters.statut)
      }
      
      return filtered
    }
  },
  mounted() {
    const auth = useAuthStore()
    this.user = auth.user
    this.isSuperAdmin = this.user?.role === 'it_admin' || this.user?.is_superuser
    this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const res = await axios.get(`${API_BASE_URL}/api/projets/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        this.projets = res.data || []
      } catch(e) {
        console.error('Erreur chargement:', e)
        this.showToast('error', 'Erreur lors du chargement des projets')
      }
    },

    getFullImageUrl(imagePath) {
      if (!imagePath) return '/src/images/projet-placeholder.jpg'
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath
      }
      if (imagePath.startsWith('/media/')) {
        return `${API_BASE_URL}${imagePath}`
      }
      if (imagePath.startsWith('media/')) {
        return `${API_BASE_URL}/${imagePath}`
      }
      return imagePath
    },

    getCategorieLabel(cat) {
      const labels = {
        recherche: '🔬 Recherche',
        conservation: '🌿 Conservation',
        formation: '📚 Formation',
        developpement: '💼 Développement'
      }
      return labels[cat] || cat
    },

    getStatutLabel(statut) {
      const labels = {
        termine: '✅ Terminé',
        encours: '🔄 En cours',
        planifie: '📅 Planifié'
      }
      return labels[statut] || statut
    },

    getTagList(tags) {
      if (!tags) return []
      return tags.split(',').map(tag => tag.trim()).filter(tag => tag)
    },

    handleImageError(e) {
      e.target.src = '/src/images/projet-placeholder.jpg'
    },

    truncate(text, len) {
      return text?.length > len ? text.substring(0, len) + '...' : text || ''
    },

    resetFilters() {
      this.searchQuery = ''
      this.filters.categorie = ''
      this.filters.statut = ''
    },

    triggerFileInput() {
      this.$refs.fileInput?.click()
    },

    handleFileSelect(event) {
      const file = event.target.files[0]
      if (!file) return
      
      if (file.size > 5 * 1024 * 1024) {
        this.showToast('error', 'L\'image ne doit pas dépasser 5MB')
        event.target.value = ''
        return
      }
      
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
      if (!validTypes.includes(file.type)) {
        this.showToast('error', 'Format d\'image non supporté')
        event.target.value = ''
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        this.form.image_preview = e.target.result
        this.form.image_file = file
        this.form._existing_image = null
      }
      reader.readAsDataURL(file)
    },

    handleDrop(event) {
      const file = event.dataTransfer.files[0]
      if (!file || !file.type.startsWith('image/')) {
        this.showToast('error', 'Veuillez déposer une image')
        return
      }
      if (file.size > 5 * 1024 * 1024) {
        this.showToast('error', 'L\'image ne doit pas dépasser 5MB')
        return
      }
      const reader = new FileReader()
      reader.onload = (e) => {
        this.form.image_preview = e.target.result
        this.form.image_file = file
        this.form._existing_image = null
      }
      reader.readAsDataURL(file)
    },

    removeImage() {
      this.form.image_preview = null
      this.form.image_file = null
      this.form._existing_image = null
      this.form.image = null
    },

    openModal() {
      this.editingId = null
      this.form = {
        titre: '',
        categorie: 'recherche',
        statut: 'encours',
        annee: '',
        lieu: '',
        partenaires: 0,
        beneficiaires: '',
        budget: '',
        duree: '',
        impact: '',
        progression: 0,
        description: '',
        description_longue: '',
        objectifs: '',
        resultats: '',
        tags: '',
        image: '',
        images_galerie: [],
        featured: false,
        image_preview: null,
        image_file: null,
        _existing_image: null
      }
      this.imagesGalerieInput = ''
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    editItem(item) {
      this.editingId = item.id
      const existingImage = item.image || ''
      this.form = {
        ...item,
        image_preview: existingImage ? this.getFullImageUrl(existingImage) : null,
        _existing_image: existingImage,
        image_file: null
      }
      this.imagesGalerieInput = (item.images_galerie || []).join(', ')
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    closeModal() {
      this.showModal = false
      this.editingId = null
      document.body.style.overflow = 'auto'
    },

    async saveItem() {
      // Validation
      if (!this.form.titre || this.form.titre.trim() === '') {
        this.showToast('error', 'Le titre est obligatoire')
        return
      }
      if (!this.form.description || this.form.description.trim() === '') {
        this.showToast('error', 'La description courte est obligatoire')
        return
      }

      this.loading = true

      try {
        // Traiter les images de galerie
        if (this.imagesGalerieInput) {
          this.form.images_galerie = this.imagesGalerieInput.split(',').map(s => s.trim()).filter(s => s)
        } else {
          this.form.images_galerie = []
        }

        const data = { ...this.form }
        
        // Nettoyer les champs temporaires
        delete data.image_preview
        delete data.image_file
        delete data._existing_image
        
        // Supprimer les champs vides
        Object.keys(data).forEach(key => {
          if (data[key] === null || data[key] === undefined || data[key] === '') {
            delete data[key]
          }
        })

        // Gérer l'image
        if (this.form.image_file instanceof File) {
          data.image = this.form.image_file
        } else if (this.editingId && this.form._existing_image) {
          data.image = this.form._existing_image
        }

        let response
        if (this.editingId) {
          response = await axios.put(
            `${API_BASE_URL}/api/projets/${this.editingId}/`,
            data,
            {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'multipart/form-data'
              }
            }
          )
          this.showToast('success', 'Projet modifié avec succès')
        } else {
          response = await axios.post(
            `${API_BASE_URL}/api/projets/`,
            data,
            {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'multipart/form-data'
              }
            }
          )
          this.showToast('success', 'Projet ajouté avec succès')
        }

        this.closeModal()
        await this.loadData()
      } catch (error) {
        console.error('Erreur sauvegarde:', error)
        const errorMsg = error.response?.data?.message || 
                        error.response?.data?.error || 
                        'Erreur lors de l\'enregistrement'
        this.showToast('error', typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg))
      } finally {
        this.loading = false
      }
    },

    async deleteItem(item) {
      if (!confirm(`Supprimer définitivement le projet "${item.titre}" ?`)) return
      
      try {
        await axios.delete(
          `${API_BASE_URL}/api/projets/${item.id}/`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        )
        this.showToast('success', 'Projet supprimé avec succès')
        await this.loadData()
      } catch (error) {
        console.error('Erreur suppression:', error)
        this.showToast('error', 'Erreur lors de la suppression')
      }
    },

    showToast(type, message) {
      this.toastType = type
      this.toastMessage = message
      setTimeout(() => {
        this.toastMessage = ''
      }, 4000)
    },

    confirmLogout() {
      if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        localStorage.removeItem('it_admin_authenticated')
        useAuthStore().logout()
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.management-page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e8 100%);
  font-family: 'Inter', sans-serif;
}

/* ============================================
   SIDEBAR
   ============================================ */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #0d3b0f 0%, #1a472a 50%, #0a2412 100%);
  color: white;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  box-shadow: 5px 0 30px rgba(0,0,0,0.1);
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 30px 24px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-icon {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(255,215,0,0.3);
}

.logo-icon i {
  font-size: 24px;
  color: #1a472a;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.logo-subtitle {
  font-size: 10px;
  opacity: 0.7;
  margin-top: 2px;
}

.sidebar-nav {
  flex: 1;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #FFD700;
  transform: scaleY(0);
  transition: transform 0.3s;
}

.nav-item:hover::before,
.nav-item.active::before {
  transform: scaleY(1);
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
  transform: translateX(5px);
}

.nav-item.active {
  background: rgba(255,215,0,0.15);
  color: #FFD700;
}

.nav-item i {
  width: 22px;
  font-size: 18px;
}

.nav-badge {
  margin-left: auto;
  font-size: 9px;
  background: rgba(255,255,255,0.2);
  padding: 2px 8px;
  border-radius: 20px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255,255,255,0.1);
  margin-top: auto;
}

.user-info-sidebar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  padding: 10px;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
}

.user-avatar-sidebar {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  color: #1a472a;
}

.user-details-sidebar {
  display: flex;
  flex-direction: column;
}

.user-name-sidebar {
  font-weight: 600;
  font-size: 14px;
}

.user-role {
  font-size: 10px;
  opacity: 0.7;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px;
  background: rgba(220,53,69,0.2);
  border: 1px solid rgba(220,53,69,0.5);
  border-radius: 12px;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.logout-btn:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(220,53,69,0.3);
}

/* ============================================
   MAIN CONTENT
   ============================================ */
.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 20px 30px;
}

.top-bar {
  background: white;
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 20px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.05);
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
}

.page-title h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a472a;
  margin-bottom: 4px;
}

.page-title h1 i {
  color: #32CD32;
  margin-right: 10px;
}

.page-title p {
  color: #666;
  font-size: 14px;
}

.btn-primary {
  padding: 10px 20px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(50,205,50,0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ============================================
   FILTERS
   ============================================ */
.filters-bar {
  display: flex;
  gap: 15px;
  padding: 15px 20px;
  background: white;
  margin: 0 0 25px 0;
  border-radius: 16px;
  flex-wrap: wrap;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.search-box {
  flex: 1;
  position: relative;
  min-width: 200px;
}

.search-box i {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.search-box input {
  width: 100%;
  padding: 10px 15px 10px 45px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
}

.filter-select {
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s;
  min-width: 160px;
}

.filter-select:focus {
  outline: none;
  border-color: #32CD32;
}

.stats-badge {
  background: #e8f5e8;
  padding: 8px 18px;
  border-radius: 30px;
  color: #32CD32;
  font-weight: 500;
  white-space: nowrap;
}

/* ============================================
   PROJECTS GRID
   ============================================ */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
}

.project-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: all 0.3s;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.project-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: #f5f5f5;
}

.project-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.project-card:hover .project-image img {
  transform: scale(1.05);
}

.project-category {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(0,0,0,0.75);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  backdrop-filter: blur(4px);
}

.project-status {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: white;
}

.project-status.termine {
  background: #28a745;
}

.project-status.encours {
  background: #ffc107;
  color: #1a472a;
}

.project-status.planifie {
  background: #17a2b8;
}

.project-featured {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #1a472a;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.project-info {
  padding: 16px 20px;
}

.project-info h3 {
  font-size: 18px;
  color: #1a472a;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-description {
  font-size: 13px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 12px;
  color: #888;
  margin-bottom: 12px;
}

.project-meta i {
  color: #32CD32;
  margin-right: 4px;
  width: 14px;
}

.project-progress {
  margin-bottom: 12px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #666;
  margin-bottom: 4px;
}

.progress-bar {
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #32CD32, #FFD700);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #eee;
  flex-wrap: wrap;
  gap: 8px;
}

.project-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  font-size: 10px;
  padding: 2px 10px;
  background: #f0f0f0;
  border-radius: 20px;
  color: #666;
}

.project-actions {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.btn-edit {
  background: #ffc107;
  color: #1a472a;
}

.btn-edit:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(255,193,7,0.3);
}

.btn-delete {
  background: #dc3545;
  color: white;
}

.btn-delete:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(220,53,69,0.3);
}

/* ============================================
   EMPTY STATE
   ============================================ */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  grid-column: 1 / -1;
}

.empty-state i {
  font-size: 60px;
  color: #ccc;
  margin-bottom: 15px;
}

.empty-state h3 {
  font-size: 20px;
  color: #1a472a;
  margin-bottom: 8px;
}

.empty-state p {
  color: #999;
  margin-bottom: 20px;
}

/* ============================================
   MODAL
   ============================================ */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  visibility: hidden;
  opacity: 0;
  transition: all 0.3s;
  backdrop-filter: blur(4px);
}

.modal.active {
  visibility: visible;
  opacity: 1;
}

.modal-content.modal-large {
  max-width: 800px;
}

.modal-content {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  background: white;
  border-radius: 24px 24px 0 0;
  z-index: 1;
}

.modal-header h2 {
  color: #1a472a;
  margin: 0;
  font-size: 20px;
}

.close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.3s;
}

.close:hover {
  color: #f44336;
  transform: rotate(90deg);
}

.modal-form {
  padding: 25px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 18px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-weight: 500;
  color: #333;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.form-group label i {
  color: #32CD32;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  width: 100%;
  transition: border-color 0.3s;
  font-family: 'Inter', sans-serif;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 60px;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.form-group.checkbox label {
  font-weight: 400;
  cursor: pointer;
}

.form-group.checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.image-upload-area {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-upload-area:hover {
  border-color: #32CD32;
  background: #f8fafc;
}

.image-upload-area.has-image {
  border-color: #32CD32;
  background: #f8fafc;
}

.image-preview {
  position: relative;
  width: 100%;
  max-height: 300px;
  overflow: hidden;
  border-radius: 8px;
}

.image-preview img {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: contain;
}

.remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.remove-image:hover {
  background: #c0392b;
}

.upload-placeholder {
  padding: 20px;
}

.upload-placeholder i {
  font-size: 48px;
  color: #32CD32;
  margin-bottom: 10px;
}

.upload-hint {
  display: block;
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.form-help {
  display: block;
  color: #888;
  font-size: 12px;
  margin-top: 5px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-secondary {
  padding: 10px 25px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

/* ============================================
   TOAST
   ============================================ */
.toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 14px 22px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1100;
  animation: slideInRight 0.3s;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  font-weight: 500;
}

.toast.success {
  background: #28a745;
  color: white;
}

.toast.error {
  background: #dc3545;
  color: white;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }

  .sidebar-nav span,
  .sidebar-footer span,
  .logo-text,
  .user-info-sidebar {
    display: none;
  }

  .nav-item {
    justify-content: center;
  }

  .main-content {
    margin-left: 80px;
    padding: 15px;
  }

  .top-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }

  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select {
    width: 100%;
  }

  .form-row {
    flex-direction: column;
  }

  .modal-content.modal-large {
    max-width: 95%;
  }
}

@media (max-width: 480px) {
  .project-image {
    height: 160px;
  }

  .project-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .project-actions {
    justify-content: center;
  }
}
</style>