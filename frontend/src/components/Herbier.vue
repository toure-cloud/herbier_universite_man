<template>
  <div class="herbier">
    <!-- ==================== HERO ==================== -->
    <section class="hero-herbier">
      <div class="hero-background">
        <div class="hero-overlay"></div>
        <div class="hero-pattern"></div>
      </div>
      <div class="hero-content">
        <div class="hero-badge" data-aos="fade-down">
          <i class="fas fa-database"></i>
          <span>Collection Botanique</span>
        </div>
        <h1 class="hero-title" data-aos="fade-up">L'Herbier Numérique</h1>
        <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="200">
          Explorez notre collection de <span class="highlight">{{ totalPlants }}+ spécimens</span><br>
          classifiés scientifiquement
        </p>
        <div class="hero-stats" data-aos="fade-up" data-aos-delay="400">
          <div class="stat-card">
            <div class="stat-number">{{ totalPlants }}</div>
            <div class="stat-label">Spécimens</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ uniqueFamilies }}</div>
            <div class="stat-label">Familles</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ plantsWithImagesCount }}</div>
            <div class="stat-label">Illustrations</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ endangeredSpecies }}</div>
            <div class="stat-label">Espèces menacées</div>
          </div>
        </div>
      </div>
      <div class="hero-wave">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
          <path fill="#ffffff" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
        </svg>
      </div>
    </section>

    <!-- ==================== RECHERCHE ==================== -->
    <section class="search-section">
      <div class="container">
        <div class="search-card" data-aos="fade-up">
          <div class="search-header">
            <i class="fas fa-search"></i>
            <h3>Recherche</h3>
          </div>
          <div class="search-main">
            <div class="search-input-wrapper">
              <i class="fas fa-search"></i>
              <input
                v-model="searchQuery"
                @input="debouncedSearch"
                type="text"
                placeholder="Rechercher par nom scientifique, famille, vernaculaire, habitat, lieu de collecte..."
                class="search-input"
              />
              <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="search-filters">
              <div class="filter-group">
                <label><i class="fas fa-tag"></i> Famille</label>
                <select v-model="selectedFamily" @change="filterPlants" class="filter-select">
                  <option value="">Toutes les familles</option>
                  <option v-for="f in familiesList" :key="f" :value="f">{{ f }}</option>
                </select>
              </div>
              <div class="filter-group">
                <label><i class="fas fa-leaf"></i> Statut UICN</label>
                <select v-model="selectedConservation" @change="filterPlants" class="filter-select">
                  <option value="">Tous</option>
                  <option value="CR">En danger critique</option>
                  <option value="EN">En danger</option>
                  <option value="VU">Vulnérable</option>
                  <option value="NT">Quasi menacé</option>
                  <option value="LC">Préoccupation mineure</option>
                  <option value="NE">Non évaluée</option>
                </select>
              </div>
              <div class="view-toggle">
                <button
                  :class="['view-btn', { active: viewMode === 'grid' }]"
                  @click="viewMode = 'grid'"
                  title="Vue en grille">
                  <i class="fas fa-th"></i>
                </button>
                <button
                  :class="['view-btn', { active: viewMode === 'list' }]"
                  @click="viewMode = 'list'"
                  title="Vue en liste">
                  <i class="fas fa-list"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="search-results-info">
            <div class="results-count">
              <i class="fas fa-leaf"></i>
              <span>{{ filteredPlants.length }} résultat(s)</span>
              <span v-if="hasActiveFilters" class="filter-badge">Filtres actifs</span>
            </div>
            <button v-if="hasActiveFilters" @click="resetFilters" class="reset-btn">
              <i class="fas fa-redo-alt"></i> Réinitialiser
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== LOADING ==================== -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Chargement de l'herbier…</p>
      </div>
    </div>

    <!-- ==================== GRILLE ==================== -->
    <template v-else-if="filteredPlants.length > 0">
      <!-- Vue grille -->
      <section class="plants-section" v-if="viewMode === 'grid'">
        <div class="container">
          <div class="plants-grid">
            <div
              v-for="plant in paginatedPlants"
              :key="plant.id"
              class="plant-card"
              @click="openPlantModal(plant)"
            >
              <div class="plant-image">
                <img
                  :src="getImageUrl(plant.image)"
                  :alt="plant.nom_scientifique"
                  @error="handleImageError"
                />
                <div
                  class="plant-badge"
                  :class="getConservationClass(plant.statut_conservation)"
                  v-if="plant.statut_conservation"
                >
                  {{ plant.statut_conservation_label || plant.statut_conservation }}
                </div>
                <div v-if="hasGallery(plant)" class="gallery-count">
                  <i class="fas fa-images"></i> {{ plant.images_galerie.length }}
                </div>
                <div class="plant-overlay">
                  <span class="quick-view">
                    <i class="fas fa-eye"></i> Voir les détails
                  </span>
                </div>
              </div>
              <div class="plant-details">
                <h3 class="plant-name">{{ plant.nom_scientifique }}</h3>
                <p class="plant-vernaculaire" v-if="plant.nom_vernaculaire">
                  {{ plant.nom_vernaculaire }}
                </p>
                <div class="plant-family" v-if="plant.famille">
                  <i class="fas fa-tag"></i><span>{{ plant.famille }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Vue liste -->
      <section class="plants-section" v-if="viewMode === 'list'">
        <div class="container">
          <div class="plants-list">
            <div
              v-for="plant in paginatedPlants"
              :key="plant.id"
              class="plant-list-item"
              @click="openPlantModal(plant)"
            >
              <div class="list-image">
                <img
                  :src="getImageUrl(plant.image)"
                  :alt="plant.nom_scientifique"
                  @error="handleImageError"
                />
              </div>
              <div class="list-content">
                <h3 class="list-name">{{ plant.nom_scientifique }}</h3>
                <p class="list-vernaculaire" v-if="plant.nom_vernaculaire">
                  {{ plant.nom_vernaculaire }}
                </p>
                <div class="list-family" v-if="plant.famille">
                  <i class="fas fa-tag"></i> {{ plant.famille }}
                </div>
                <div class="list-meta">
                  <span v-if="plant.type_morphologique">
                    <i class="fas fa-tree"></i> {{ plant.type_morphologique }}
                  </span>
                  <span v-if="plant.lieu_collecte">
                    <i class="fas fa-map-marker-alt"></i> {{ plant.lieu_collecte }}
                  </span>
                  <span
                    class="status-badge"
                    :class="getConservationClass(plant.statut_conservation)"
                    v-if="plant.statut_conservation"
                  >
                    {{ plant.statut_conservation_label || plant.statut_conservation }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Pagination -->
      <div class="container">
        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" :disabled="currentPage === 1" @click="currentPage--">
            <i class="fas fa-chevron-left"></i>
          </button>
          <button
            v-for="page in displayedPages"
            :key="page"
            :class="['page-btn', { active: currentPage === page }]"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </template>

    <!-- ==================== AUCUN RÉSULTAT ==================== -->
    <section v-else class="no-results-section">
      <div class="container">
        <div class="no-results-card" data-aos="fade-up">
          <div class="no-results-icon">
            <i class="fas fa-seedling"></i>
          </div>
          <h3>Aucune plante trouvée</h3>
          <p>Nous n'avons pas trouvé de spécimens correspondant à vos critères.</p>
          <button @click="resetFilters" class="btn-primary">
            <i class="fas fa-redo-alt"></i> Réinitialiser la recherche
          </button>
        </div>
      </div>
    </section>

    <!-- ==================== MODALE DÉTAIL ==================== -->
    <transition name="herbier-modal-fade">
      <div v-if="showModal" class="herbier-modal" @click.self="closeModal">
        <div class="herbier-modal-container">
          <button class="herbier-modal-close" @click="closeModal" aria-label="Fermer">
            <i class="fas fa-times"></i>
          </button>

          <div class="herbier-modal-content" v-if="selectedPlant">
            <!-- Colonne gauche : galerie -->
            <div class="herbier-modal-gallery">
              <!-- Image principale -->
              <div class="herbier-modal-gallery-main">
                <img
                  :src="getImageUrl(currentGalleryImage)"
                  :alt="selectedPlant.nom_scientifique"
                  @error="handleImageError"
                />
                <div
                  class="herbier-modal-badge"
                  :class="getConservationClass(selectedPlant.statut_conservation)"
                  v-if="selectedPlant.statut_conservation"
                >
                  {{ selectedPlant.statut_conservation_label || selectedPlant.statut_conservation }}
                </div>
                <div class="herbier-modal-image-counter" v-if="allImages.length > 1">
                  {{ currentGalleryIndex + 1 }} / {{ allImages.length }}
                </div>
              </div>

              <!-- Miniatures secondaires — même taille, alignées horizontalement -->
              <div class="herbier-modal-gallery-thumbs" v-if="allImages.length > 1">
                <button
                  v-for="(img, i) in allImages"
                  :key="i"
                  type="button"
                  class="herbier-modal-thumb"
                  :class="{ active: i === currentGalleryIndex }"
                  @click="currentGalleryIndex = i"
                  :aria-label="`Photo ${i + 1}`"
                >
                  <img
                    :src="getImageUrl(img)"
                    @error="handleImageError"
                    :alt="`Photo ${i + 1}`"
                  />
                </button>
              </div>
            </div>

            <!-- Colonne droite : détails -->
            <div class="herbier-modal-info">
              <header class="herbier-modal-header">
                <h2 class="herbier-modal-title">{{ selectedPlant.nom_scientifique }}</h2>
                <p v-if="selectedPlant.nom_vernaculaire" class="herbier-modal-vernaculaire">
                  <i class="fas fa-language"></i>
                  <span>{{ selectedPlant.nom_vernaculaire }}</span>
                </p>
              </header>

              <!-- Grille des détails -->
              <div class="herbier-modal-details">
                <div class="herbier-modal-detail-card" v-if="selectedPlant.famille">
                  <div class="herbier-modal-detail-icon"><i class="fas fa-tag"></i></div>
                  <div class="herbier-modal-detail-body">
                    <span class="herbier-modal-detail-label">Famille</span>
                    <span class="herbier-modal-detail-value">{{ selectedPlant.famille }}</span>
                  </div>
                </div>

                <div class="herbier-modal-detail-card" v-if="selectedPlant.type_morphologique">
                  <div class="herbier-modal-detail-icon"><i class="fas fa-tree"></i></div>
                  <div class="herbier-modal-detail-body">
                    <span class="herbier-modal-detail-label">Type morphologique</span>
                    <span class="herbier-modal-detail-value">{{ selectedPlant.type_morphologique }}</span>
                  </div>
                </div>

                <div class="herbier-modal-detail-card" v-if="selectedPlant.type_biologique">
                  <div class="herbier-modal-detail-icon"><i class="fas fa-seedling"></i></div>
                  <div class="herbier-modal-detail-body">
                    <span class="herbier-modal-detail-label">Type biologique</span>
                    <span class="herbier-modal-detail-value">{{ selectedPlant.type_biologique }}</span>
                  </div>
                </div>

                <div class="herbier-modal-detail-card" v-if="selectedPlant.affinite_chorologique">
                  <div class="herbier-modal-detail-icon"><i class="fas fa-globe-africa"></i></div>
                  <div class="herbier-modal-detail-body">
                    <span class="herbier-modal-detail-label">Affinité chorologique</span>
                    <span class="herbier-modal-detail-value">{{ selectedPlant.affinite_chorologique }}</span>
                  </div>
                </div>

                <div class="herbier-modal-detail-card" v-if="selectedPlant.affinite_ecologique">
                  <div class="herbier-modal-detail-icon"><i class="fas fa-mountain"></i></div>
                  <div class="herbier-modal-detail-body">
                    <span class="herbier-modal-detail-label">Affinité écologique</span>
                    <span class="herbier-modal-detail-value">{{ selectedPlant.affinite_ecologique }}</span>
                  </div>
                </div>

                <div class="herbier-modal-detail-card" v-if="selectedPlant.lieu_collecte">
                  <div class="herbier-modal-detail-icon"><i class="fas fa-map-marker-alt"></i></div>
                  <div class="herbier-modal-detail-body">
                    <span class="herbier-modal-detail-label">Lieu de collecte</span>
                    <span class="herbier-modal-detail-value">{{ selectedPlant.lieu_collecte }}</span>
                  </div>
                </div>
              </div>

              <!-- Habitat -->
              <div class="herbier-modal-section" v-if="selectedPlant.habitat">
                <h4 class="herbier-modal-section-title">
                  <i class="fas fa-home"></i> Habitat
                </h4>
                <p class="herbier-modal-section-text">{{ selectedPlant.habitat }}</p>
              </div>

              <!-- Description -->
              <div class="herbier-modal-section" v-if="selectedPlant.description">
                <h4 class="herbier-modal-section-title">
                  <i class="fas fa-align-left"></i> Description
                </h4>
                <p class="herbier-modal-section-text">{{ selectedPlant.description }}</p>
              </div>

              <!-- Actions -->
              <div class="herbier-modal-actions">
                <button class="btn-primary" @click="sharePlant">
                  <i class="fas fa-share-alt"></i> Partager
                </button>
                <button class="btn-outline" @click="closeModal">
                  <i class="fas fa-times"></i> Fermer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios'
import config from '../config.js'

export default {
  name: 'Herbier',
  data() {
    return {
      plants: [],
      filteredPlants: [],
      searchQuery: '',
      selectedFamily: '',
      selectedConservation: '',
      viewMode: 'grid',
      currentPage: 1,
      itemsPerPage: 12,
      loading: true,
      showModal: false,
      selectedPlant: null,
      currentGalleryIndex: 0,
      searchTimeout: null,
    }
  },
  computed: {
    totalPlants() {
      return this.plants.length
    },
    uniqueFamilies() {
      const set = new Set(this.plants.map(p => p.famille).filter(Boolean))
      return set.size
    },
    plantsWithImagesCount() {
      return this.plants.filter(p => p.image).length
    },
    endangeredSpecies() {
      return this.plants.filter(p => ['CR', 'EN', 'VU'].includes(p.statut_conservation)).length
    },
    familiesList() {
      const families = [...new Set(this.plants.map(p => p.famille).filter(Boolean))]
      return families.sort()
    },
    hasActiveFilters() {
      return this.searchQuery !== '' || this.selectedFamily !== '' || this.selectedConservation !== ''
    },
    paginatedPlants() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredPlants.slice(start, start + this.itemsPerPage)
    },
    totalPages() {
      return Math.ceil(this.filteredPlants.length / this.itemsPerPage)
    },
    displayedPages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }
      for (let i = start; i <= end; i++) pages.push(i)
      return pages
    },
    /** Toutes les images de la plante sélectionnée (principale + galerie, dédoublonnées) */
    allImages() {
      if (!this.selectedPlant) return []
      const imgs = []
      if (this.selectedPlant.image) imgs.push(this.selectedPlant.image)
      if (Array.isArray(this.selectedPlant.images_galerie)) {
        imgs.push(...this.selectedPlant.images_galerie)
      }
      return [...new Set(imgs)]
    },
    /** Image courante affichée dans la galerie de la modale */
    currentGalleryImage() {
      return this.allImages[this.currentGalleryIndex] || this.selectedPlant?.image || ''
    },
  },
  mounted() {
    this.fetchPlants()
  },
  methods: {
    // ============================================
    // CHARGEMENT
    // ============================================
    async fetchPlants() {
      this.loading = true
      try {
        const response = await axios.get(config.API_ENDPOINTS.plantes)
        this.plants = Array.isArray(response.data) ? response.data : (response.data.results || [])
        this.filteredPlants = [...this.plants]
      } catch (error) {
        console.error('Erreur chargement plantes :', error)
        this.plants = []
        this.filteredPlants = []
      } finally {
        this.loading = false
      }
    },

    // ============================================
    // RECHERCHE ET FILTRES
    // ============================================
    debouncedSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => this.filterPlants(), 300)
    },

    filterPlants() {
      let filtered = [...this.plants]

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        filtered = filtered.filter(p =>
          p.nom_scientifique?.toLowerCase().includes(q) ||
          p.nom_vernaculaire?.toLowerCase().includes(q) ||
          p.famille?.toLowerCase().includes(q) ||
          p.habitat?.toLowerCase().includes(q) ||
          p.description?.toLowerCase().includes(q) ||
          p.lieu_collecte?.toLowerCase().includes(q) ||
          p.type_morphologique?.toLowerCase().includes(q) ||
          p.type_biologique?.toLowerCase().includes(q) ||
          p.affinite_chorologique?.toLowerCase().includes(q) ||
          p.affinite_ecologique?.toLowerCase().includes(q)
        )
      }

      if (this.selectedFamily) {
        filtered = filtered.filter(p => p.famille === this.selectedFamily)
      }

      if (this.selectedConservation) {
        filtered = filtered.filter(p => p.statut_conservation === this.selectedConservation)
      }

      this.filteredPlants = filtered
      this.currentPage = 1
    },

    clearSearch() {
      this.searchQuery = ''
      this.filterPlants()
    },

    resetFilters() {
      this.searchQuery = ''
      this.selectedFamily = ''
      this.selectedConservation = ''
      this.filterPlants()
    },

    // ============================================
    // IMAGES
    // ============================================
    /**
     * ✅ Les médias sont uploadés côté ADMIN-BACKEND (port 8001).
     * Le backend public (port 8000) n'a pas les fichiers.
     * On pointe donc vers l'admin pour les URLs /media/.
     */
    getImageUrl(path) {
      if (!path) return ''
      if (path.startsWith('http')) return path
      if (path.startsWith('/media')) {
        const adminBase = (import.meta.env.VITE_ADMIN_MEDIA_URL || 'http://localhost:8001').replace(/\/+$/, '')
        return `${adminBase}${path}`
      }
      return path
    },

    /**
     * ✅ Remplace une image cassée par un placeholder discret.
     * Anti-boucle : marque l'image pour ne pas re-déclencher sur le placeholder.
     */
    handleImageError(e) {
      if (e.target.dataset.errorHandled) return
      e.target.dataset.errorHandled = 'true'
      e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Crect fill='%23f1f5f9' width='80' height='80'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='24' fill='%23cbd5e1' text-anchor='middle' dy='.3em'%3E%3F%3C/text%3E%3C/svg%3E"
    },

    hasGallery(plant) {
      return Array.isArray(plant.images_galerie) && plant.images_galerie.length > 0
    },

    // ============================================
    // STATUT UICN
    // ============================================
    getConservationClass(statut) {
      const classes = {
        CR: 'critical',
        EN: 'endangered',
        VU: 'vulnerable',
        NT: 'near-threatened',
        LC: 'least-concern',
        NE: 'not-evaluated',
      }
      return classes[statut] || 'not-evaluated'
    },

    // ============================================
    // MODALE
    // ============================================
    openPlantModal(plant) {
      this.selectedPlant = plant
      this.currentGalleryIndex = 0
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    closeModal() {
      this.showModal = false
      this.selectedPlant = null
      this.currentGalleryIndex = 0
      document.body.style.overflow = ''
    },

    // ============================================
    // PARTAGE
    // ============================================
    sharePlant() {
      const plant = this.selectedPlant
      if (!plant) return

      const text = `${plant.nom_scientifique}${plant.nom_vernaculaire ? ` (${plant.nom_vernaculaire})` : ''}`
      const url = window.location.href

      if (navigator.share) {
        navigator.share({ title: plant.nom_scientifique, text, url }).catch(() => {})
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(`${text} — ${url}`)
        alert('Informations copiées dans le presse-papier')
      } else {
        alert(text)
      }
    },
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

/* ==================== BASE ==================== */
.herbier {
  overflow-x: hidden;
  font-family: 'Inter', system-ui, sans-serif;
  color: #1a202c;
  background: #f7fafc;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ==================== HERO ==================== */
.hero-herbier {
  position: relative;
  min-height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  background: linear-gradient(145deg, #0f2744 0%, #1a365d 45%, #1e3a5f 100%);
}

.hero-background { position: absolute; inset: 0; }

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(66, 153, 225, 0.18), transparent 70%);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.6;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 880px;
  padding: 56px 24px 48px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 0.8rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 1rem;
}

.hero-badge i { color: #63b3ed; }

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.75rem, 3.5vw, 2.5rem);
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 0.75rem;
}

.hero-subtitle {
  font-size: 0.95rem;
  line-height: 1.55;
  opacity: 0.9;
  margin: 0 0 1.5rem;
}

.highlight {
  color: #90cdf4;
  font-weight: 600;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.stat-card {
  text-align: center;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(10px);
  padding: 10px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 110px;
  transition: all 0.25s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-3px);
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #90cdf4;
}

.stat-label {
  font-size: 0.7rem;
  opacity: 0.85;
  margin-top: 3px;
}

.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  line-height: 0;
}

.hero-wave svg { display: block; width: 100%; height: 48px; }

/* ==================== RECHERCHE ==================== */
.search-section {
  padding: 48px 0;
  background: #f7fafc;
}

.search-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.search-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-header i { color: #2b6cb0; }
.search-header h3 { margin: 0; font-size: 1.05rem; }

.search-main { padding: 20px 24px; }

.search-input-wrapper {
  position: relative;
  margin-bottom: 16px;
}

.search-input-wrapper i {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 12px 44px 12px 44px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #2b6cb0;
  box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.1);
}

.clear-btn {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
}

.search-filters {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 0.85rem;
  color: #4a5568;
  font-weight: 500;
}

.filter-select {
  padding: 8px 16px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  font-family: inherit;
  background: white;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #2b6cb0;
}

.view-toggle {
  display: flex;
  gap: 4px;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 10px;
  margin-left: auto;
}

.view-btn {
  padding: 8px 14px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.view-btn.active {
  background: #2b6cb0;
  color: white;
}

.search-results-info {
  padding: 14px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.results-count {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #475569;
}

.results-count i { color: #2b6cb0; }

.filter-badge {
  background: #ebf4ff;
  color: #2b6cb0;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
}

.reset-btn {
  background: white;
  border: 1px solid #e2e8f0;
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85rem;
  color: #64748b;
}

.reset-btn:hover { background: #f1f5f9; }

/* ==================== LOADING ==================== */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-spinner { text-align: center; }

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #e2e8f0;
  border-top-color: #2b6cb0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin { to { transform: rotate(360deg); } }
.loading-spinner p { color: #64748b; }

/* ==================== GRILLE ==================== */
.plants-section {
  padding: 40px 0 60px;
  background: #f7fafc;
}

.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.plant-card {
  background: white;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.plant-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.12);
}

.plant-image {
  position: relative;
  height: 220px;
  overflow: hidden;
  background: #f1f5f9;
}

.plant-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.plant-card:hover .plant-image img { transform: scale(1.05); }

.plant-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  color: white;
}

.plant-badge.critical { background: #dc2626; }
.plant-badge.endangered { background: #ea580c; }
.plant-badge.vulnerable { background: #d97706; }
.plant-badge.near-threatened { background: #2563eb; }
.plant-badge.least-concern { background: #16a34a; }
.plant-badge.not-evaluated { background: #94a3b8; }

.gallery-count {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.plant-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.plant-card:hover .plant-overlay { opacity: 1; }

.quick-view {
  background: white;
  color: #1e293b;
  padding: 8px 18px;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 500;
}

.plant-details { padding: 18px 20px; }

.plant-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 4px;
  font-style: italic;
}

.plant-vernaculaire {
  font-size: 0.85rem;
  color: #718096;
  margin: 0 0 8px;
}

.plant-family {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #2b6cb0;
}

.plant-family i { font-size: 0.75rem; }

/* ==================== LISTE ==================== */
.plants-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.plant-list-item {
  display: flex;
  gap: 1.25rem;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.2s;
}

.plant-list-item:hover {
  transform: translateX(4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.list-image {
  width: 140px;
  height: 140px;
  flex-shrink: 0;
  overflow: hidden;
  background: #f1f5f9;
}

.list-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.list-content {
  flex: 1;
  padding: 16px 20px 16px 0;
}

.list-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  font-style: italic;
  margin: 0 0 4px;
}

.list-vernaculaire {
  font-size: 0.85rem;
  color: #718096;
  margin: 0 0 8px;
}

.list-family {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #2b6cb0;
  margin-bottom: 8px;
}

.list-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  font-size: 0.8rem;
  color: #64748b;
}

.list-meta i { color: #2b6cb0; margin-right: 4px; }

.status-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  color: white;
}

.status-badge.critical { background: #dc2626; }
.status-badge.endangered { background: #ea580c; }
.status-badge.vulnerable { background: #d97706; }
.status-badge.near-threatened { background: #2563eb; }
.status-badge.least-concern { background: #16a34a; }
.status-badge.not-evaluated { background: #94a3b8; }

/* ==================== PAGINATION ==================== */
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 3rem;
}

.page-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  color: #475569;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) { background: #f1f5f9; }
.page-btn.active {
  background: #2b6cb0;
  color: white;
  border-color: #2b6cb0;
}
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ==================== NO RESULTS ==================== */
.no-results-section { padding: 80px 0; }

.no-results-card {
  text-align: center;
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  max-width: 480px;
  margin: 0 auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.no-results-icon {
  font-size: 3.5rem;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.no-results-card h3 {
  font-family: 'Playfair Display', serif;
  color: #1a202c;
  margin-bottom: 8px;
}

.no-results-card p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.btn-primary {
  background: #2b6cb0;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #1a4f8a;
  transform: translateY(-2px);
}

/* ==================== MODALE (préfixée herbier-modal-*) ==================== */
.herbier-modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.72);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 24px;
}

.herbier-modal-container {
  background: #ffffff;
  border-radius: 20px;
  max-width: 1080px;
  width: 100%;
  max-height: 92vh;
  overflow-y: auto;
  position: relative;
  box-shadow:
    0 0 0 1px rgba(15, 23, 42, 0.06),
    0 25px 50px -12px rgba(0, 0, 0, 0.35);
}

.herbier-modal-close {
  position: absolute;
  top: 18px;
  right: 18px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-size: 0.95rem;
}

.herbier-modal-close:hover {
  background: #fee2e2;
  border-color: #fecaca;
  color: #dc2626;
}

.herbier-modal-content {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
  gap: 0;
  min-height: 0;
}

/* ---------- Galerie ---------- */
.herbier-modal-gallery {
  display: flex;
  flex-direction: column;
  gap: 0;
  background: #0f172a;
  border-radius: 20px 0 0 20px;
  overflow: hidden;
  padding: 20px 20px 18px;
}

.herbier-modal-gallery-main {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #1e293b;
  aspect-ratio: 4 / 3;
  max-height: 420px;
  flex-shrink: 0;
}

.herbier-modal-gallery-main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.herbier-modal-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: white;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.herbier-modal-badge.critical { background: #dc2626; }
.herbier-modal-badge.endangered { background: #ea580c; }
.herbier-modal-badge.vulnerable { background: #d97706; }
.herbier-modal-badge.near-threatened { background: #2563eb; }
.herbier-modal-badge.least-concern { background: #16a34a; }
.herbier-modal-badge.not-evaluated { background: #64748b; }

.herbier-modal-image-counter {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(15, 23, 42, 0.75);
  color: #e2e8f0;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.03em;
  z-index: 2;
}

/* Miniatures secondaires : même dimension, alignées en ligne horizontale */
.herbier-modal-gallery-thumbs {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  gap: 10px;
  margin-top: 14px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 4px;
  scrollbar-width: thin;
  scrollbar-color: #475569 transparent;
}

.herbier-modal-gallery-thumbs::-webkit-scrollbar {
  height: 4px;
}

.herbier-modal-gallery-thumbs::-webkit-scrollbar-track {
  background: transparent;
}

.herbier-modal-gallery-thumbs::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 4px;
}

.herbier-modal-thumb {
  flex: 0 0 auto;
  width: 72px;
  height: 72px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: #1e293b;
  transition: border-color 0.2s ease, opacity 0.2s ease, box-shadow 0.2s ease;
  opacity: 0.7;
}

.herbier-modal-thumb:hover {
  opacity: 1;
  border-color: #64748b;
}

.herbier-modal-thumb.active {
  opacity: 1;
  border-color: #60a5fa;
  box-shadow: 0 0 0 1px #60a5fa;
}

.herbier-modal-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ---------- Infos ---------- */
.herbier-modal-info {
  display: flex;
  flex-direction: column;
  padding: 28px 32px 28px 28px;
  overflow-y: auto;
  max-height: 92vh;
  background: #ffffff;
}

.herbier-modal-header {
  margin-bottom: 22px;
  padding-right: 36px;
}

.herbier-modal-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.65rem;
  font-weight: 700;
  font-style: italic;
  color: #0f172a;
  margin: 0 0 8px;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.herbier-modal-vernaculaire {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
}

.herbier-modal-vernaculaire i {
  color: #3b82f6;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.herbier-modal-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 24px;
}

.herbier-modal-detail-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  transition: border-color 0.15s ease;
}

.herbier-modal-detail-card:hover {
  border-color: #cbd5e1;
}

.herbier-modal-detail-icon {
  width: 34px;
  height: 34px;
  background: #eff6ff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
  flex-shrink: 0;
  font-size: 0.85rem;
}

.herbier-modal-detail-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.herbier-modal-detail-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  color: #94a3b8;
  font-weight: 600;
  letter-spacing: 0.05em;
  line-height: 1.2;
}

.herbier-modal-detail-value {
  font-size: 0.9rem;
  color: #1e293b;
  font-weight: 500;
  line-height: 1.35;
  word-break: break-word;
}

.herbier-modal-section {
  margin-bottom: 18px;
  min-width: 0;
  max-width: 100%;
}

.herbier-modal-section-text,
.herbier-modal-section p {
  font-size: 0.925rem;
  color: #475569;
  line-height: 1.7;
  margin: 0;
  white-space: pre-wrap;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;

  /* Force le retour à la ligne — aucun débordement hors du cadre */
  overflow-wrap: anywhere;
  word-break: break-word;
  word-wrap: break-word;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

/* Important pour les grilles CSS : autorise le shrink des colonnes */
.herbier-modal-content,
.herbier-modal-info,
.herbier-modal-gallery {
  min-width: 0;
}

.herbier-modal-info {
  overflow-x: hidden;
}

.herbier-modal-section-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: #334155;
  margin: 0 0 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.herbier-modal-section-title i {
  color: #3b82f6;
  font-size: 0.85rem;
}

.herbier-modal-section-text {
  font-size: 0.925rem;
  color: #475569;
  line-height: 1.7;
  margin: 0;
  white-space: pre-line;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;
}

.herbier-modal-actions {
  display: flex;
  gap: 12px;
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.btn-outline {
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  color: #475569;
}

.btn-outline:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
  color: #1e293b;
}

.herbier-modal-actions .btn-primary {
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 0.9rem;
}

/* ==================== TRANSITION MODALE ==================== */
.herbier-modal-fade-enter-active,
.herbier-modal-fade-leave-active {
  transition: opacity 0.22s ease;
}

.herbier-modal-fade-enter-active .herbier-modal-container,
.herbier-modal-fade-leave-active .herbier-modal-container {
  transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1);
}

.herbier-modal-fade-enter-from,
.herbier-modal-fade-leave-to {
  opacity: 0;
}

.herbier-modal-fade-enter-from .herbier-modal-container,
.herbier-modal-fade-leave-to .herbier-modal-container {
  transform: scale(0.96) translateY(12px);
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 900px) {
  .herbier-modal-content {
    grid-template-columns: 1fr;
  }

  .herbier-modal-gallery {
    border-radius: 20px 20px 0 0;
    padding: 16px 16px 14px;
  }

  .herbier-modal-gallery-main {
    max-height: 280px;
    aspect-ratio: 16 / 10;
  }

  .herbier-modal-info {
    padding: 22px 20px 24px;
    max-height: none;
  }

  .herbier-modal-details {
    grid-template-columns: 1fr;
  }

  .herbier-modal-thumb {
    width: 64px;
    height: 64px;
  }
}

@media (max-width: 768px) {
  .plants-grid {
    grid-template-columns: 1fr;
  }

  .plant-list-item {
    flex-direction: column;
  }

  .list-image {
    width: 100%;
    height: 180px;
  }

  .list-content {
    padding: 16px;
  }

  .search-filters {
    flex-direction: column;
    align-items: stretch;
  }

  .view-toggle {
    margin-left: 0;
    justify-content: center;
  }

  .herbier-modal {
    padding: 12px;
  }

  .herbier-modal-container {
    border-radius: 16px;
    max-height: 96vh;
  }

  .herbier-modal-gallery {
    border-radius: 16px 16px 0 0;
  }

  .herbier-modal-title {
    font-size: 1.4rem;
  }

  .herbier-modal-actions {
    flex-direction: column;
  }

  .herbier-modal-actions .btn-primary,
  .herbier-modal-actions .btn-outline {
    width: 100%;
    justify-content: center;
  }
}
</style>