<template>
  <div class="projets">
    <!-- ==================== HERO ==================== -->
    <section class="hero-projets">
      <div class="hero-background">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
        <div class="hero-glow"></div>
      </div>

      <div class="hero-content">
        <div class="hero-badge" data-aos="fade-down">
          <i class="fas fa-project-diagram"></i>
          <span>Nos Projets</span>
        </div>

        <h1 class="hero-title" data-aos="fade-up">
          Des initiatives qui<br />
          <span class="title-accent">façonnent l'avenir</span>
        </h1>

        <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="150">
          Découvrez nos projets de recherche, conservation et développement
          engagés pour la préservation de la biodiversité
        </p>

        <div class="hero-stats" data-aos="fade-up" data-aos-delay="300">
          <div class="stat-item">
            <div class="stat-number">{{ totalTermines }}</div>
            <div class="stat-label">Projets réalisés</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ totalEncours }}</div>
            <div class="stat-label">Projets en cours</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ totalPartenaires }}</div>
            <div class="stat-label">Partenaires</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">{{ totalBeneficiaires }}</div>
            <div class="stat-label">Bénéficiaires</div>
          </div>
        </div>
      </div>

      <div class="hero-wave">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path
            fill="var(--bg-page)"
            d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"
          ></path>
        </svg>
      </div>
    </section>

    <!-- ==================== FILTRES ==================== -->
    <section class="filters-section">
      <div class="container">
        <div class="filters-wrapper" data-aos="fade-up">
          <div class="filter-buttons">
            <button
              v-for="filter in filters"
              :key="filter.value"
              :class="['filter-btn', { active: activeFilter === filter.value }]"
              @click="setFilter(filter.value)"
            >
              {{ filter.label }}
              <span class="filter-count">{{ getProjectsCount(filter.value) }}</span>
            </button>
          </div>
          <div class="filter-search">
            <i class="fas fa-search"></i>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Rechercher un projet..."
              @input="filterProjects"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== LOADING ==================== -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Chargement des projets...</p>
      </div>
    </div>

    <!-- ==================== GRID PROJETS ==================== -->
    <section v-else-if="filteredProjects.length > 0" class="projets-grid-section">
      <div class="container">
        <div class="projets-grid">
          <article
            v-for="(projet, index) in paginatedProjects"
            :key="projet.id"
            class="projet-card"
            :class="{ featured: projet.featured }"
            data-aos="fade-up"
            :data-aos-delay="(index % 3) * 80"
          >
            <div class="projet-image">
              <img
                v-if="getMainImage(projet)"
                :src="getImageUrl(getMainImage(projet))"
                :alt="projet.titre"
                @error="handleImageError"
              />
              <div v-else class="no-image"><i class="fas fa-image"></i></div>

              <div class="projet-category">{{ getCategorieLabel(projet.categorie) }}</div>
              <div class="projet-status" :class="getStatusClass(projet.statut)">
                <i :class="getStatusIcon(projet.statut)"></i>
                {{ getStatusLabel(projet.statut) }}
              </div>
              <span v-if="getAllImages(projet).length > 1" class="images-count">
                <i class="fas fa-images"></i> {{ getAllImages(projet).length }}
              </span>
              <div class="projet-overlay">
                <div class="overlay-buttons">
                  <button class="overlay-btn" @click="openDetails(projet)" title="Voir les détails">
                    <i class="fas fa-expand"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="projet-info">
              <div class="projet-header">
                <h3>{{ projet.titre }}</h3>
                <div class="projet-annee" v-if="projet.annee">
                  <i class="fas fa-calendar-alt"></i>
                  {{ projet.annee }}
                </div>
              </div>
              <p>{{ truncate(projet.description, 140) }}</p>

              <div class="projet-meta">
                <div class="meta-item" v-if="projet.lieu">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>{{ projet.lieu }}</span>
                </div>
                <div class="meta-item" v-if="projet.partenaires_count">
                  <i class="fas fa-users"></i>
                  <span>{{ projet.partenaires_count }} partenaires</span>
                </div>
              </div>

              <div class="projet-progress" v-if="projet.progression != null">
                <div class="progress-label">
                  <span>Progression</span>
                  <span>{{ projet.progression }}%</span>
                </div>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: projet.progression + '%' }"
                  ></div>
                </div>
              </div>

              <div class="projet-actions">
                <button class="btn-details" @click="openDetails(projet)">
                  En savoir plus
                  <i class="fas fa-arrow-right"></i>
                </button>
                <div class="projet-tags" v-if="getTagList(projet.tags).length">
                  <span
                    v-for="tag in getTagList(projet.tags).slice(0, 2)"
                    :key="tag"
                    class="tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </article>
        </div>

        <!-- Pagination -->
        <div class="pagination" v-if="totalPages > 1">
          <button
            class="page-btn"
            :disabled="currentPage === 1"
            @click="currentPage--"
            aria-label="Page précédente"
          >
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
          <button
            class="page-btn"
            :disabled="currentPage === totalPages"
            @click="currentPage++"
            aria-label="Page suivante"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- ==================== PROJET EN VEDETTE ==================== -->
    <section class="featured-section" v-if="featuredProject && !loading">
      <div class="container">
        <div class="featured-wrapper" data-aos="fade-up">
          <div class="featured-badge">
            <i class="fas fa-star"></i>
            Projet à la une
          </div>
          <div class="featured-content">
            <div class="featured-text">
              <h2>{{ featuredProject.titre }}</h2>
              <p class="featured-description">
                {{ featuredProject.description_longue || featuredProject.description }}
              </p>
              <div class="featured-stats">
                <div class="featured-stat" v-if="featuredProject.duree">
                  <i class="fas fa-calendar-check"></i>
                  <span>Durée : {{ featuredProject.duree }}</span>
                </div>
                <div class="featured-stat" v-if="featuredProject.budget">
                  <i class="fas fa-hand-holding-heart"></i>
                  <span>Budget : {{ featuredProject.budget }}</span>
                </div>
                <div class="featured-stat" v-if="featuredProject.impact">
                  <i class="fas fa-globe-africa"></i>
                  <span>Impact : {{ featuredProject.impact }}</span>
                </div>
              </div>
              <button class="btn-featured" @click="openDetails(featuredProject)">
                Découvrir le projet
                <i class="fas fa-arrow-right"></i>
              </button>
            </div>
            <div class="featured-image">
              <img
                v-if="getMainImage(featuredProject)"
                :src="getImageUrl(getMainImage(featuredProject))"
                :alt="featuredProject.titre"
                @error="handleImageError"
              />
              <div v-else class="no-image"><i class="fas fa-image"></i></div>
              <div class="image-caption">
                {{ featuredProject.caption || "Projet phare de l'herbier" }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TIMELINE ==================== -->
    <section class="timeline-section" v-if="timelineProjects.length > 0 && !loading">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Notre Histoire</span>
          <h2 class="section-title">Projets par année</h2>
          <p class="section-subtitle">Découvrez l'évolution de nos actions</p>
        </div>

        <div class="timeline">
          <div
            class="timeline-item"
            v-for="(item, index) in timelineProjects"
            :key="item.annee"
            data-aos="fade-up"
            :data-aos-delay="index * 80"
          >
            <div class="timeline-year">
              <div class="year-circle">{{ item.annee }}</div>
              <div class="year-line"></div>
            </div>
            <div class="timeline-projects">
              <div
                class="timeline-project"
                v-for="projet in item.projets"
                :key="projet.titre"
              >
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <h4>{{ projet.titre }}</h4>
                  <p>{{ projet.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== AUCUN RÉSULTAT ==================== -->
    <section
      v-else-if="!loading && filteredProjects.length === 0"
      class="no-results-section"
    >
      <div class="container">
        <div class="no-results-card" data-aos="fade-up">
          <div class="no-results-icon">
            <i class="fas fa-search"></i>
          </div>
          <h3>Aucun projet trouvé</h3>
          <p>Essayez de modifier vos critères de recherche</p>
          <button @click="resetFilters" class="btn-reset">
            <i class="fas fa-redo-alt"></i>
            Réinitialiser les filtres
          </button>
        </div>
      </div>
    </section>

    <!-- ==================== CTA ==================== -->
    <section class="cta-projets">
      <div class="container">
        <div class="cta-content" data-aos="zoom-in">
          <h2>Vous avez un projet ?</h2>
          <p>Collaborons ensemble pour un avenir durable</p>
          <div class="cta-buttons">
            <router-link to="/contact" class="btn-primary">
              Proposer un projet
              <i class="fas fa-paper-plane"></i>
            </router-link>
            <a href="#" class="btn-secondary">
              Télécharger notre rapport d'activités
              <i class="fas fa-download"></i>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== MODALE DÉTAIL ==================== -->
    <transition name="herbier-modal-fade">
      <div v-if="showModal && selectedProjet" class="herbier-modal" @click.self="closeModal">
        <div class="herbier-modal-container">
          <button class="herbier-modal-close" @click="closeModal" aria-label="Fermer">
            <i class="fas fa-times"></i>
          </button>

          <div class="herbier-modal-content">
            <!-- Colonne gauche : galerie -->
            <div class="herbier-modal-gallery">
              <div class="gallery-main">
                <img
                  v-if="currentGalleryImage"
                  :src="getImageUrl(currentGalleryImage)"
                  :alt="selectedProjet.titre"
                  @error="handleImageError"
                />
                <div v-else class="no-image"><i class="fas fa-image"></i></div>

                <div
                  class="herbier-modal-badge"
                  :class="getStatusClass(selectedProjet.statut)"
                >
                  {{ getStatusLabel(selectedProjet.statut) }}
                </div>
              </div>

              <div
                v-if="allGalleryImages.length > 1"
                class="gallery-thumbs"
              >
                <img
                  v-for="(img, i) in allGalleryImages"
                  :key="i"
                  :src="getImageUrl(img)"
                  :class="{ active: i === currentGalleryIndex }"
                  @click="currentGalleryIndex = i"
                  @error="handleImageError"
                  :alt="`Image ${i + 1}`"
                />
              </div>
            </div>

            <!-- Colonne droite : détails -->
            <div class="herbier-modal-info">
              <div class="modal-header-titles">
                <span v-if="selectedProjet.categorie" class="modal-kicker">
                  {{ getCategorieLabel(selectedProjet.categorie) }}
                </span>
                <h2 class="herbier-modal-title">{{ selectedProjet.titre }}</h2>
                <div class="herbier-modal-meta">
                  <span v-if="selectedProjet.annee">
                    <i class="fas fa-calendar"></i>
                    {{ selectedProjet.annee }}
                  </span>
                  <span v-if="selectedProjet.lieu">
                    <i class="fas fa-map-marker-alt"></i>
                    {{ selectedProjet.lieu }}
                  </span>
                  <span v-if="selectedProjet.duree">
                    <i class="fas fa-clock"></i>
                    {{ selectedProjet.duree }}
                  </span>
                </div>
              </div>

              <div class="herbier-modal-details">
                <div class="detail-card" v-if="selectedProjet.partenaires_count">
                  <div class="detail-icon"><i class="fas fa-users"></i></div>
                  <div class="detail-body">
                    <h4>Partenaires</h4>
                    <p>{{ selectedProjet.partenaires_count }}</p>
                  </div>
                </div>
                <div class="detail-card" v-if="selectedProjet.beneficiaires">
                  <div class="detail-icon"><i class="fas fa-user-check"></i></div>
                  <div class="detail-body">
                    <h4>Bénéficiaires</h4>
                    <p>{{ selectedProjet.beneficiaires }}</p>
                  </div>
                </div>
                <div class="detail-card" v-if="selectedProjet.budget">
                  <div class="detail-icon"><i class="fas fa-coins"></i></div>
                  <div class="detail-body">
                    <h4>Budget</h4>
                    <p>{{ selectedProjet.budget }}</p>
                  </div>
                </div>
                <div class="detail-card" v-if="selectedProjet.impact">
                  <div class="detail-icon"><i class="fas fa-globe-africa"></i></div>
                  <div class="detail-body">
                    <h4>Impact</h4>
                    <p>{{ selectedProjet.impact }}</p>
                  </div>
                </div>
              </div>

              <div class="herbier-modal-section" v-if="selectedProjet.progression != null">
                <h4><i class="fas fa-chart-line"></i> Progression</h4>
                <div class="modal-progress">
                  <div class="modal-prog-bar">
                    <div
                      class="modal-prog-fill"
                      :style="{ width: selectedProjet.progression + '%' }"
                    ></div>
                  </div>
                  <span class="modal-prog-label">{{ selectedProjet.progression }}%</span>
                </div>
              </div>

              <div
                class="herbier-modal-section"
                v-if="selectedProjet.description_longue || selectedProjet.description"
              >
                <h4><i class="fas fa-align-left"></i> Description</h4>
                <p>{{ selectedProjet.description_longue || selectedProjet.description }}</p>
              </div>

              <div class="herbier-modal-section" v-if="selectedProjet.objectifs">
                <h4><i class="fas fa-bullseye"></i> Objectifs</h4>
                <p>{{ selectedProjet.objectifs }}</p>
              </div>

              <div class="herbier-modal-section" v-if="selectedProjet.resultats">
                <h4><i class="fas fa-trophy"></i> Résultats</h4>
                <p>{{ selectedProjet.resultats }}</p>
              </div>

              <div
                class="herbier-modal-section"
                v-if="getTagList(selectedProjet.tags).length"
              >
                <h4><i class="fas fa-tags"></i> Tags</h4>
                <div class="modal-tags">
                  <span v-for="tag in getTagList(selectedProjet.tags)" :key="tag" class="modal-tag">
                    {{ tag }}
                  </span>
                </div>
              </div>

              <div class="herbier-modal-actions">
                <button class="btn-outline" @click="shareProject">
                  <i class="fas fa-share-alt"></i>
                  Partager
                </button>
                <button class="btn-primary" @click="closeModal">
                  <i class="fas fa-times"></i>
                  Fermer
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
  name: 'Projets',
  data() {
    return {
      projets: [],
      loading: true,
      activeFilter: 'all',
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 6,
      showModal: false,
      selectedProjet: null,
      currentGalleryIndex: 0,
      filters: [
        { label: 'Tous', value: 'all' },
        { label: 'Recherche', value: 'recherche' },
        { label: 'Conservation', value: 'conservation' },
        { label: 'Formation', value: 'formation' },
        { label: 'Développement', value: 'developpement' },
      ],
      statutLabels: {
        termine: 'Terminé',
        encours: 'En cours',
        planifie: 'Planifié',
      },
      categorieLabels: {
        recherche: 'Recherche',
        conservation: 'Conservation',
        formation: 'Formation',
        developpement: 'Développement',
        autre: 'Autre',
      },
    }
  },
  computed: {
    filteredProjects() {
      let filtered = [...this.projets]
      if (this.activeFilter !== 'all') {
        filtered = filtered.filter((p) => p.categorie === this.activeFilter)
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(
          (p) =>
            p.titre?.toLowerCase().includes(query) ||
            p.description?.toLowerCase().includes(query) ||
            p.lieu?.toLowerCase().includes(query) ||
            p.description_longue?.toLowerCase().includes(query)
        )
      }
      return filtered
    },
    paginatedProjects() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredProjects.slice(start, start + this.itemsPerPage)
    },
    totalPages() {
      return Math.ceil(this.filteredProjects.length / this.itemsPerPage)
    },
    displayedPages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)
      if (end - start + 1 < maxVisible) start = Math.max(1, end - maxVisible + 1)
      for (let i = start; i <= end; i++) pages.push(i)
      return pages
    },
    featuredProject() {
      return this.projets.find((p) => p.featured === true)
    },
    timelineProjects() {
      const timeline = {}
      this.projets.forEach((projet) => {
        const annee = projet.annee?.split('-')[0] || projet.annee
        if (annee && !timeline[annee]) timeline[annee] = { annee, projets: [] }
        if (annee && timeline[annee]) {
          timeline[annee].projets.push({
            titre: projet.titre,
            description: projet.description,
          })
        }
      })
      return Object.values(timeline).sort((a, b) => b.annee - a.annee)
    },
    totalTermines() {
      return this.projets.filter((p) => p.statut === 'termine').length
    },
    totalEncours() {
      return this.projets.filter((p) => p.statut === 'encours').length
    },
    totalPartenaires() {
      return this.projets.reduce(
        (sum, p) => sum + (parseInt(p.partenaires_count) || 0),
        0
      )
    },
    totalBeneficiaires() {
      const total = this.projets.reduce((sum, p) => {
        return sum + (parseInt(p.beneficiaires) || 0)
      }, 0)
      return total > 1000 ? Math.floor(total / 1000) + 'k+' : total
    },
    allGalleryImages() {
      if (!this.selectedProjet) return []
      return this.getAllImages(this.selectedProjet)
    },
    currentGalleryImage() {
      return this.allGalleryImages[this.currentGalleryIndex] || ''
    },
  },
  mounted() {
    this.fetchProjects()
    this.initAnimations()
  },
  methods: {
    async fetchProjects() {
      this.loading = true
      try {
        const response = await axios.get(config.API_ENDPOINTS.projets)
        this.projets = Array.isArray(response.data)
          ? response.data
          : response.data.results || []
      } catch (error) {
        console.error('Erreur lors du chargement des projets:', error)
        this.projets = []
      } finally {
        this.loading = false
      }
    },

    // ============================================
    // IMAGES
    // ============================================
    getAllImages(p) {
      if (!p) return []
      if (Array.isArray(p.images_galerie) && p.images_galerie.length) {
        return p.images_galerie
      }
      if (Array.isArray(p.images) && p.images.length) return p.images
      if (p.image) return [p.image]
      return []
    },

    getMainImage(p) {
      return this.getAllImages(p)[0] || null
    },

  getImageUrl(path) {
  if (!path) return ''
  if (typeof path !== 'string') return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('data:') || path.startsWith('blob:')) return path

  // ✅ Les médias sont stockés côté ADMIN-BACKEND (port 8001)
  const adminMediaUrl = import.meta.env.VITE_ADMIN_MEDIA_URL || 'http://localhost:8001'

  if (path.startsWith('/media')) return `${adminMediaUrl}${path}`
  if (path.startsWith('media/')) return `${adminMediaUrl}/${path}`
  return `${adminMediaUrl}/media/${path.replace(/^\/+/, '')}`
},

    handleImageError(e) {
      e.target.style.opacity = '0.3'
      e.target.style.background = '#f1f5f9'
    },

    // ============================================
    // LABELS
    // ============================================
    getCategorieLabel(categorie) {
      return this.categorieLabels[categorie] || categorie
    },

    getStatusLabel(statut) {
      return this.statutLabels[statut] || statut
    },

    getStatusClass(statut) {
      return {
        termine: 'termine',
        encours: 'encours',
        planifie: 'planifie',
      }[statut] || ''
    },

    getStatusIcon(statut) {
      return {
        termine: 'fas fa-check-circle',
        encours: 'fas fa-spinner fa-pulse',
        planifie: 'fas fa-clock',
      }[statut] || 'fas fa-circle'
    },

    getTagList(tags) {
      if (!tags) return []
      return tags.split(',').map((t) => t.trim()).filter(Boolean)
    },

    truncate(text, length) {
      if (!text) return ''
      return text.length > length ? text.slice(0, length) + '…' : text
    },

    getProjectsCount(category) {
      if (category === 'all') return this.projets.length
      return this.projets.filter((p) => p.categorie === category).length
    },

    setFilter(filter) {
      this.activeFilter = filter
      this.filterProjects()
    },

    filterProjects() {
      this.currentPage = 1
    },

    resetFilters() {
      this.activeFilter = 'all'
      this.searchQuery = ''
      this.currentPage = 1
    },

    initAnimations() {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.style.opacity = '1'
              entry.target.style.transform = 'translateY(0)'
            }
          })
        },
        { threshold: 0.1 }
      )
      document.querySelectorAll('[data-aos]').forEach((el) => {
        el.style.opacity = '0'
        el.style.transform = 'translateY(24px)'
        el.style.transition = 'all 0.55s cubic-bezier(0.22, 1, 0.36, 1)'
        observer.observe(el)
      })
    },

    openDetails(projet) {
      this.selectedProjet = projet
      this.currentGalleryIndex = 0
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    closeModal() {
      this.showModal = false
      this.selectedProjet = null
      this.currentGalleryIndex = 0
      document.body.style.overflow = ''
    },

    shareProject() {
      if (!this.selectedProjet) return
      const p = this.selectedProjet
      const shareData = {
        title: p.titre,
        text: p.description,
        url: window.location.href,
      }
      if (navigator.share) {
        navigator.share(shareData).catch(() => {})
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(`${p.titre} — ${window.location.href}`)
        alert('Lien copié dans le presse-papier')
      }
    },
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

/* ==================== TOKENS ==================== */
.projets {
  --primary: #2b6cb0;
  --primary-dark: #1a4f8a;
  --primary-light: #ebf4ff;
  --accent: #38a169;
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --text-muted: #718096;
  --bg-page: #f7fafc;
  --border: #e2e8f0;
  --radius-full: 9999px;
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-x: hidden;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-primary);
  background: var(--bg-page);
}

.container { max-width: 1240px; margin: 0 auto; padding: 0 24px; }

.section-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  padding: 5px 14px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 12px;
}
.section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.75rem, 3vw, 2.1rem);
  font-weight: 700;
  margin: 0 0 8px;
}
.section-subtitle { font-size: 0.95rem; color: var(--text-muted); margin: 0; }
.section-header { text-align: center; margin-bottom: 2.75rem; }

/* ==================== HERO ==================== */
.hero-projets {
  position: relative;
  min-height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  background: linear-gradient(145deg, #0f2744 0%, #1a365d 45%, #1e3a5f 100%);
  padding: 56px 0 48px;
}
.hero-background { position: absolute; inset: 0; }
.hero-gradient {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(66, 153, 225, 0.18), transparent 70%);
}
.hero-pattern {
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.6;
}
.hero-glow {
  position: absolute;
  width: 360px; height: 360px; border-radius: 50%;
  background: radial-gradient(circle, rgba(66, 153, 225, 0.12), transparent 70%);
  top: -80px; right: -40px;
}
.hero-content { position: relative; z-index: 2; max-width: 880px; margin: 0 auto; padding: 0 24px; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 500;
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
.title-accent {
  background: linear-gradient(135deg, #63b3ed, #90cdf4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle { font-size: 0.95rem; line-height: 1.55; opacity: 0.9; margin: 0 0 1.5rem; }
.hero-stats { display: flex; justify-content: center; gap: 0.85rem; flex-wrap: wrap; }
.stat-item {
  text-align: center;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(10px);
  padding: 10px 16px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 110px;
}
.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #90cdf4;
}
.stat-label { font-size: 0.7rem; opacity: 0.8; margin-top: 3px; }
.hero-wave { position: absolute; bottom: -1px; left: 0; right: 0; line-height: 0; }
.hero-wave svg { display: block; width: 100%; height: 48px; }

/* ==================== FILTRES ==================== */
.filters-section { padding: 36px 0; background: white; border-bottom: 1px solid var(--border); }
.filters-wrapper { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.filter-buttons { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-btn {
  padding: 8px 16px;
  background: #edf2f7;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  font-weight: 500;
  font-size: 0.85rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all var(--transition);
}
.filter-btn:hover { background: #e2e8f0; }
.filter-btn.active { background: var(--primary); color: white; }
.filter-count { background: rgba(0, 0, 0, 0.08); padding: 2px 8px; border-radius: var(--radius-full); font-size: 0.7rem; }
.filter-btn.active .filter-count { background: rgba(255, 255, 255, 0.25); }
.filter-search { position: relative; }
.filter-search i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
.filter-search input {
  padding: 10px 16px 10px 40px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-full);
  width: 260px;
  font-size: 0.9rem;
  font-family: inherit;
}
.filter-search input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.12); }

/* ==================== LOADING ==================== */
.loading-container {
  display: flex; align-items: center; justify-content: center;
  min-height: 380px;
}
.loading-spinner { text-align: center; }
.spinner {
  width: 44px; height: 44px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ==================== GRID ==================== */
.projets-grid-section { padding: 48px 0 64px; background: var(--bg-page); }
.projets-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.5rem; }
.projet-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  position: relative;
}
.projet-card:hover { transform: translateY(-6px); box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08); }
.projet-card.featured { border: 2px solid var(--primary); }
.projet-image { position: relative; height: 210px; overflow: hidden; background: #edf2f7; }
.projet-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.45s ease; }
.projet-card:hover .projet-image img { transform: scale(1.05); }
.no-image { display: flex; align-items: center; justify-content: center; height: 100%; color: #cbd5e1; font-size: 40px; }
.projet-category {
  position: absolute; top: 12px; left: 12px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(6px);
  color: white;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 500;
}
.projet-status {
  position: absolute; bottom: 12px; left: 12px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 600;
  color: white;
  display: flex;
  align-items: center;
  gap: 5px;
}
.projet-status.termine { background: #38a169; }
.projet-status.encours { background: #d69e2e; }
.projet-status.planifie { background: var(--primary); }
.images-count {
  position: absolute; bottom: 12px; right: 12px;
  padding: 4px 9px;
  border-radius: 20px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}
.projet-overlay {
  position: absolute; inset: 0;
  background: rgba(26, 54, 93, 0.65);
  display: flex; align-items: center; justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.projet-card:hover .projet-overlay { opacity: 1; }
.overlay-btn {
  width: 48px; height: 48px;
  background: white; border: none;
  border-radius: 50%;
  font-size: 1.1rem;
  color: var(--text-primary);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.overlay-btn:hover { background: var(--primary); color: white; transform: scale(1.08); }

.projet-info { padding: 1.35rem; }
.projet-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 10px; }
.projet-header h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.3;
}
.projet-annee {
  font-size: 0.75rem;
  color: var(--text-muted);
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 4px;
}
.projet-info p { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.55; margin: 0 0 12px; }
.projet-meta { display: flex; gap: 14px; margin-bottom: 12px; flex-wrap: wrap; }
.meta-item { display: flex; align-items: center; gap: 5px; font-size: 0.8rem; color: var(--text-muted); }
.meta-item i { color: var(--primary); }
.projet-progress { margin-bottom: 14px; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 5px; }
.progress-bar { height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--primary), #63b3ed); border-radius: 3px; }
.projet-actions { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.btn-details {
  background: none; border: none;
  color: var(--primary); font-weight: 600;
  font-size: 0.875rem; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px;
  padding: 0;
}
.projet-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag { font-size: 0.7rem; padding: 3px 10px; background: #edf2f7; border-radius: var(--radius-full); color: var(--text-secondary); }

/* ==================== PAGINATION ==================== */
.pagination { display: flex; justify-content: center; gap: 6px; margin-top: 2.5rem; }
.page-btn {
  min-width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  border: 1.5px solid var(--border);
  background: white;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
}
.page-btn:hover:not(:disabled) { border-color: var(--primary); color: var(--primary); background: var(--primary-light); }
.page-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ==================== FEATURED ==================== */
.featured-section { padding: 56px 0; background: var(--bg-page); }
.featured-wrapper {
  background: white;
  border-radius: 28px;
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
  position: relative;
}
.featured-badge {
  position: absolute; top: 20px; right: 20px;
  background: var(--primary); color: white;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 500;
  z-index: 2;
  display: flex; align-items: center; gap: 6px;
}
.featured-content { display: grid; grid-template-columns: 1fr 1fr; align-items: stretch; }
.featured-text { padding: 2.75rem; display: flex; flex-direction: column; justify-content: center; }
.featured-text h2 { font-family: 'Playfair Display', serif; font-size: 1.75rem; font-weight: 700; margin: 0 0 12px; line-height: 1.3; }
.featured-description { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.65; margin: 0 0 1.5rem; }
.featured-stats { display: flex; flex-direction: column; gap: 10px; margin-bottom: 1.75rem; }
.featured-stat { display: flex; align-items: center; gap: 10px; color: var(--text-secondary); font-size: 0.9rem; }
.featured-stat i { color: var(--primary); width: 18px; }
.btn-featured {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 22px;
  background: var(--primary); color: white;
  border: none; border-radius: var(--radius-full);
  font-weight: 500; font-size: 0.9rem;
  cursor: pointer; width: fit-content;
}
.btn-featured:hover { background: var(--primary-dark); transform: translateY(-2px); gap: 12px; }
.featured-image { position: relative; min-height: 360px; background: #edf2f7; }
.featured-image img { width: 100%; height: 100%; object-fit: cover; }
.image-caption {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.85), transparent);
  color: white; padding: 1.25rem 1rem 1rem;
  text-align: center; font-size: 0.8rem;
}

/* ==================== TIMELINE ==================== */
.timeline-section { padding: 64px 0; background: white; }
.timeline { max-width: 780px; margin: 0 auto; }
.timeline-item { display: flex; gap: 1.75rem; margin-bottom: 1.5rem; }
.timeline-year { text-align: center; min-width: 80px; flex-shrink: 0; }
.year-circle {
  width: 56px; height: 56px;
  background: var(--primary); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; font-size: 0.95rem;
  margin: 0 auto 8px;
}
.year-line {
  width: 2px; height: calc(100% - 64px);
  background: linear-gradient(to bottom, var(--primary), #bee3f8);
  margin: 0 auto;
}
.timeline-projects { flex: 1; padding-bottom: 1rem; }
.timeline-project {
  display: flex; gap: 12px;
  margin-bottom: 12px; padding: 1rem 1.15rem;
  background: var(--bg-page);
  border-radius: 16px;
  border: 1px solid var(--border);
}
.timeline-dot { width: 10px; height: 10px; background: var(--primary); border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.timeline-content h4 { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 600; margin: 0 0 4px; }
.timeline-content p { font-size: 0.85rem; color: var(--text-secondary); margin: 0; line-height: 1.5; }

/* ==================== NO RESULTS ==================== */
.no-results-section { padding: 80px 0; background: var(--bg-page); }
.no-results-card {
  text-align: center; background: white;
  border-radius: 24px; padding: 3.5rem 2.5rem;
  max-width: 440px; margin: 0 auto;
  border: 1px solid var(--border);
}
.no-results-icon {
  width: 72px; height: 72px; border-radius: 50%;
  background: #edf2f7;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1.25rem;
  font-size: 1.75rem; color: var(--text-muted);
}
.no-results-card h3 { font-family: 'Playfair Display', serif; font-size: 1.4rem; margin: 0 0 8px; }
.no-results-card p { font-size: 0.95rem; color: var(--text-secondary); margin: 0 0 1.5rem; }
.btn-reset {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 11px 22px;
  background: var(--primary); color: white;
  border: none; border-radius: var(--radius-full);
  font-weight: 500; font-size: 0.9rem; cursor: pointer;
}

/* ==================== CTA ==================== */
.cta-projets { padding: 56px 0; background: linear-gradient(145deg, #0f2744 0%, #1a365d 100%); color: white; }
.cta-content { text-align: center; max-width: 580px; margin: 0 auto; }
.cta-content h2 { font-family: 'Playfair Display', serif; font-size: 1.85rem; font-weight: 700; margin: 0 0 10px; }
.cta-content p { font-size: 1rem; opacity: 0.9; margin: 0 0 1.75rem; }
.cta-buttons { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
.btn-primary, .btn-secondary, .btn-outline {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 24px; border-radius: var(--radius-full);
  font-weight: 500; font-size: 0.9rem;
  text-decoration: none; cursor: pointer;
  transition: all var(--transition);
}
.btn-primary { background: white; color: var(--primary); border: none; }
.btn-secondary { background: rgba(255, 255, 255, 0.12); color: white; border: 1px solid rgba(255, 255, 255, 0.25); }
.btn-outline { background: transparent; color: var(--text-secondary); border: 1.5px solid var(--border); }
.btn-primary:hover, .btn-secondary:hover, .btn-outline:hover { transform: translateY(-2px); gap: 12px; }

/* ==================== MODALE ==================== */
.herbier-modal {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
  z-index: 99999; padding: 20px;
}
.herbier-modal-container {
  background: white;
  border-radius: 24px;
  max-width: 1100px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
}
.herbier-modal-close {
  position: absolute; top: 16px; right: 16px;
  width: 42px; height: 42px;
  border: none; border-radius: 50%;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer; z-index: 10;
  display: flex; align-items: center; justify-content: center;
  color: #64748b;
  transition: all 0.2s;
}
.herbier-modal-close:hover { background: #dc2626; color: white; transform: rotate(90deg); }

.herbier-modal-content { display: grid; grid-template-columns: 1.1fr 1fr; gap: 2rem; padding: 2rem; }

/* ---------- Galerie ---------- */
.herbier-modal-gallery { display: flex; flex-direction: column; gap: 12px; }
.gallery-main {
  position: relative;
  border-radius: 16px; overflow: hidden;
  background: #f1f5f9;
  aspect-ratio: 4 / 3;
}
.gallery-main img { width: 100%; height: 100%; object-fit: cover; }
.herbier-modal-badge {
  position: absolute; top: 14px; left: 14px;
  padding: 5px 12px; border-radius: 20px;
  font-size: 0.75rem; font-weight: 600; color: white;
}
.herbier-modal-badge.termine { background: #38a169; }
.herbier-modal-badge.encours { background: #d69e2e; }
.herbier-modal-badge.planifie { background: var(--primary); }

.gallery-thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  gap: 8px;
}
.gallery-thumbs img {
  aspect-ratio: 1;
  border-radius: 10px;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}
.gallery-thumbs img:hover { opacity: 0.8; }
.gallery-thumbs img.active { border-color: var(--primary); }

/* ---------- Infos ---------- */
.herbier-modal-info { padding-right: 4px; }
.modal-header-titles { margin-bottom: 20px; }
.modal-kicker {
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  display: block;
  margin-bottom: 4px;
}
.herbier-modal-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.7rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 8px;
  line-height: 1.25;
  padding-right: 36px;
}
.herbier-modal-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  font-size: 0.85rem;
  color: #718096;
}
.herbier-modal-meta i { color: var(--primary); margin-right: 4px; }

.herbier-modal-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}
.detail-card {
  display: flex; gap: 10px; padding: 12px;
  background: #f8fafc; border-radius: 12px;
}
.detail-icon {
  width: 36px; height: 36px;
  background: #ebf4ff;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: var(--primary); flex-shrink: 0;
}
.detail-body h4 {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #94a3b8;
  margin: 0 0 2px;
  font-weight: 600;
}
.detail-body p { font-size: 0.85rem; color: #1e293b; margin: 0; }

.herbier-modal-section { margin-bottom: 16px; }
.herbier-modal-section h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #334155;
  margin: 0 0 6px;
}
.herbier-modal-section h4 i { color: var(--primary); margin-right: 6px; }
.herbier-modal-section p {
  font-size: 0.9rem;
  color: #475569;
  line-height: 1.65;
  margin: 0;
  white-space: pre-line;
}

.modal-progress { display: flex; align-items: center; gap: 10px; }
.modal-prog-bar {
  flex: 1; height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}
.modal-prog-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), #63b3ed);
  border-radius: 4px;
  transition: width 0.4s;
}
.modal-prog-label { font-size: 0.85rem; font-weight: 700; color: var(--primary); }

.modal-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.modal-tag {
  font-size: 0.75rem;
  padding: 4px 12px;
  background: #ebf4ff;
  color: var(--primary);
  border-radius: var(--radius-full);
  font-weight: 500;
}

.herbier-modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}
.herbier-modal-actions .btn-outline,
.herbier-modal-actions .btn-primary {
  padding: 10px 20px;
  font-size: 0.875rem;
}

/* ==================== TRANSITIONS ==================== */
.herbier-modal-fade-enter-active,
.herbier-modal-fade-leave-active { transition: opacity 0.25s ease; }
.herbier-modal-fade-enter-active .herbier-modal-container,
.herbier-modal-fade-leave-active .herbier-modal-container {
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
.herbier-modal-fade-enter-from,
.herbier-modal-fade-leave-to { opacity: 0; }
.herbier-modal-fade-enter-from .herbier-modal-container,
.herbier-modal-fade-leave-to .herbier-modal-container {
  transform: scale(0.94) translateY(10px);
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 992px) {
  .featured-content { grid-template-columns: 1fr; }
  .featured-text { padding: 2rem; order: 2; }
  .featured-image { min-height: 260px; order: 1; }
  .herbier-modal-content { grid-template-columns: 1fr; padding: 1.5rem; }
  .herbier-modal-details { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .hero-projets { padding: 48px 0 40px; min-height: 320px; }
  .filters-wrapper { flex-direction: column; align-items: stretch; }
  .filter-buttons { justify-content: center; }
  .filter-search input { width: 100%; }
  .projets-grid { grid-template-columns: 1fr; }
  .timeline-item { flex-direction: column; gap: 12px; }
  .year-line { display: none; }
  .cta-buttons { flex-direction: column; align-items: center; }
  .herbier-modal-actions { flex-direction: column; }
  .herbier-modal-actions .btn-outline,
  .herbier-modal-actions .btn-primary {
    width: 100%;
    justify-content: center;
  }
}

@media (min-width: 769px) and (max-width: 1100px) {
  .projets-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>