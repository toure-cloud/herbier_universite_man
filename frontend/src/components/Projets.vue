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
                :src="getImageUrl(projet.image)"
                :alt="projet.titre"
                @error="handleImageError"
              />
              <div class="projet-category">{{ getCategorieLabel(projet.categorie) }}</div>
              <div class="projet-status" :class="getStatusClass(projet.statut)">
                <i :class="getStatusIcon(projet.statut)"></i>
                {{ getStatusLabel(projet.statut) }}
              </div>
              <div class="projet-overlay">
                <div class="overlay-buttons">
                  <button class="overlay-btn" @click="openGallery(projet)" title="Galerie">
                    <i class="fas fa-images"></i>
                  </button>
                  <button class="overlay-btn" @click="openDetails(projet)" title="Détails">
                    <i class="fas fa-expand"></i>
                  </button>
                </div>
              </div>
            </div>

            <div class="projet-info">
              <div class="projet-header">
                <h3>{{ projet.titre }}</h3>
                <div class="projet-annee">
                  <i class="fas fa-calendar-alt"></i>
                  {{ projet.annee }}
                </div>
              </div>
              <p>{{ projet.description }}</p>

              <div class="projet-meta">
                <div class="meta-item" v-if="projet.lieu">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>{{ projet.lieu }}</span>
                </div>
                <div class="meta-item" v-if="projet.partenaires">
                  <i class="fas fa-users"></i>
                  <span>{{ projet.partenaires }} partenaires</span>
                </div>
              </div>

              <div class="projet-progress" v-if="projet.progression">
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
                :src="getImageUrl(featuredProject.image)"
                :alt="featuredProject.titre"
                @error="handleImageError"
              />
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

    <!-- ==================== MODAL ==================== -->
    <div
      class="modal"
      :class="{ active: showModal }"
      @click.self="closeModal"
      role="dialog"
      aria-modal="true"
    >
      <div class="modal-container">
        <button class="modal-close" @click="closeModal" aria-label="Fermer">
          <i class="fas fa-times"></i>
        </button>

        <div class="modal-content" v-if="selectedProjet">
          <div class="modal-image">
            <img
              :src="getImageUrl(selectedProjet.image)"
              :alt="selectedProjet.titre"
              @error="handleImageError"
            />
            <div
              class="modal-badge"
              :class="getStatusClass(selectedProjet.statut)"
            >
              {{ getStatusLabel(selectedProjet.statut) }}
            </div>
          </div>

          <div class="modal-info">
            <h2 class="modal-title">{{ selectedProjet.titre }}</h2>
            <div class="modal-meta">
              <span v-if="selectedProjet.annee">
                <i class="fas fa-calendar"></i>
                {{ selectedProjet.annee }}
              </span>
              <span v-if="selectedProjet.lieu">
                <i class="fas fa-map-marker-alt"></i>
                {{ selectedProjet.lieu }}
              </span>
              <span v-if="selectedProjet.categorie">
                <i class="fas fa-tag"></i>
                {{ getCategorieLabel(selectedProjet.categorie) }}
              </span>
            </div>

            <div
              class="modal-section"
              v-if="selectedProjet.description_longue || selectedProjet.description"
            >
              <h4><i class="fas fa-align-left"></i> Description</h4>
              <p>
                {{ selectedProjet.description_longue || selectedProjet.description }}
              </p>
            </div>

            <div class="modal-section" v-if="selectedProjet.objectifs">
              <h4><i class="fas fa-bullseye"></i> Objectifs</h4>
              <p>{{ selectedProjet.objectifs }}</p>
            </div>

            <div class="modal-section" v-if="selectedProjet.resultats">
              <h4><i class="fas fa-chart-line"></i> Résultats</h4>
              <p>{{ selectedProjet.resultats }}</p>
            </div>

            <div class="modal-stats">
              <div class="modal-stat" v-if="selectedProjet.partenaires">
                <div class="stat-title">Partenaires</div>
                <div class="stat-value">{{ selectedProjet.partenaires }}</div>
              </div>
              <div class="modal-stat" v-if="selectedProjet.beneficiaires">
                <div class="stat-title">Bénéficiaires</div>
                <div class="stat-value">{{ selectedProjet.beneficiaires }}</div>
              </div>
              <div class="modal-stat" v-if="selectedProjet.budget">
                <div class="stat-title">Budget</div>
                <div class="stat-value">{{ selectedProjet.budget }}</div>
              </div>
            </div>

            <div class="modal-actions">
              <button
                class="btn-primary"
                v-if="selectedProjet.lien_rapport"
              >
                <i class="fas fa-download"></i>
                Télécharger le rapport
              </button>
              <button class="btn-outline" @click="shareProject">
                <i class="fas fa-share-alt"></i>
                Partager
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
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
      filters: [
        { label: 'Tous', value: 'all' },
        { label: 'Recherche', value: 'recherche' },
        { label: 'Conservation', value: 'conservation' },
        { label: 'Formation', value: 'formation' },
        { label: 'Développement', value: 'developpement' }
      ],
      statutLabels: {
        termine: 'Terminé',
        encours: 'En cours',
        planifie: 'Planifié'
      },
      categorieLabels: {
        recherche: 'Recherche',
        conservation: 'Conservation',
        formation: 'Formation',
        developpement: 'Développement',
        autre: 'Autre'
      }
    }
  },
  computed: {
    filteredProjects() {
      let filtered = [...this.projets]

      if (this.activeFilter !== 'all') {
        filtered = filtered.filter(p => p.categorie === this.activeFilter)
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(
          p =>
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
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }
      for (let i = start; i <= end; i++) pages.push(i)
      return pages
    },
    featuredProject() {
      return this.projets.find(p => p.featured === true)
    },
    timelineProjects() {
      const timeline = {}
      this.projets.forEach(projet => {
        const annee = projet.annee?.split('-')[0] || projet.annee
        if (annee && !timeline[annee]) {
          timeline[annee] = { annee, projets: [] }
        }
        if (annee && timeline[annee]) {
          timeline[annee].projets.push({
            titre: projet.titre,
            description: projet.description
          })
        }
      })
      return Object.values(timeline).sort((a, b) => b.annee - a.annee)
    },
    totalTermines() {
      return this.projets.filter(p => p.statut === 'termine').length
    },
    totalEncours() {
      return this.projets.filter(p => p.statut === 'encours').length
    },
    totalPartenaires() {
      return this.projets.reduce((sum, p) => sum + (p.partenaires || 0), 0)
    },
    totalBeneficiaires() {
      const total = this.projets.reduce((sum, p) => {
        return sum + (parseInt(p.beneficiaires) || 0)
      }, 0)
      return total > 1000 ? Math.floor(total / 1000) + 'k+' : total
    }
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
        this.projets = response.data || []
      } catch (error) {
        console.error('Erreur lors du chargement des projets:', error)
        this.projets = []
      } finally {
        this.loading = false
      }
    },

    getImageUrl(imagePath) {
      if (!imagePath) return '/images/placeholder-project.jpg'
      if (imagePath.startsWith('http')) return imagePath
      if (imagePath.startsWith('/media')) {
        return `${config.API_URL.replace(/\/api$/, '')}${imagePath}`
      }
      return imagePath
    },

    handleImageError(e) {
      e.target.src =
        'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="250"%3E%3Crect fill="%23e2e8f0" width="400" height="250"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="14" fill="%2394a3b8" text-anchor="middle" dy=".3em"%3EPas d\'image%3C/text%3E%3C/svg%3E'
    },

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
        planifie: 'planifie'
      }[statut] || ''
    },

    getStatusIcon(statut) {
      return {
        termine: 'fas fa-check-circle',
        encours: 'fas fa-spinner fa-pulse',
        planifie: 'fas fa-clock'
      }[statut] || 'fas fa-circle'
    },

    getTagList(tags) {
      if (!tags) return []
      return tags.split(',').map(tag => tag.trim()).filter(Boolean)
    },

    getProjectsCount(category) {
      if (category === 'all') return this.projets.length
      return this.projets.filter(p => p.categorie === category).length
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
        entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.style.opacity = '1'
              entry.target.style.transform = 'translateY(0)'
            }
          })
        },
        { threshold: 0.1 }
      )

      document.querySelectorAll('[data-aos]').forEach(el => {
        el.style.opacity = '0'
        el.style.transform = 'translateY(24px)'
        el.style.transition = 'all 0.55s cubic-bezier(0.22, 1, 0.36, 1)'
        observer.observe(el)
      })
    },

    openDetails(projet) {
      this.selectedProjet = projet
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    closeModal() {
      this.showModal = false
      this.selectedProjet = null
      document.body.style.overflow = 'auto'
    },

    openGallery(projet) {
      console.log('Ouvrir galerie du projet:', projet.titre)
    },

    shareProject() {
      if (navigator.share && this.selectedProjet) {
        navigator.share({
          title: this.selectedProjet.titre,
          text: this.selectedProjet.description,
          url: window.location.href
        })
      } else {
        alert('Fonctionnalité de partage à venir')
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

/* ==================== DESIGN TOKENS ==================== */
.projets {
  --primary: #2b6cb0;
  --primary-dark: #1a4f8a;
  --primary-light: #ebf4ff;
  --accent: #38a169;
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --text-muted: #718096;
  --bg-page: #f7fafc;
  --bg-card: #ffffff;
  --border: #e2e8f0;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.05), 0 2px 4px rgba(0, 0, 0, 0.03);
  --shadow-lg: 0 12px 28px rgba(0, 0, 0, 0.08), 0 4px 10px rgba(0, 0, 0, 0.04);
  --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);

  overflow-x: hidden;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-primary);
  background: var(--bg-page);
}

.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ==================== SECTION HEADER ==================== */
.section-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  padding: 5px 14px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  margin-bottom: 12px;
}

.section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.75rem, 3vw, 2.1rem);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
}

.section-subtitle {
  font-size: 0.95rem;
  color: var(--text-muted);
  margin: 0;
}

.section-header {
  text-align: center;
  margin-bottom: 2.75rem;
}

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

.hero-background {
  position: absolute;
  inset: 0;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 80% 60% at 50% 0%,
    rgba(66, 153, 225, 0.18),
    transparent 70%
  );
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.6;
}

.hero-glow {
  position: absolute;
  width: 360px;
  height: 360px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(66, 153, 225, 0.12), transparent 70%);
  top: -80px;
  right: -40px;
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 880px;
  margin: 0 auto;
  padding: 0 24px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 1rem;
}

.hero-badge i {
  color: #63b3ed;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.75rem, 3.5vw, 2.5rem);
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 0.75rem;
  letter-spacing: -0.02em;
}

.title-accent {
  background: linear-gradient(135deg, #63b3ed, #90cdf4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 0.95rem;
  line-height: 1.55;
  opacity: 0.9;
  margin: 0 0 1.5rem;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 10px 16px;
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 110px;
  transition: all var(--transition);
}

.stat-item:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-3px);
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #90cdf4;
  line-height: 1.1;
}

.stat-label {
  font-size: 0.7rem;
  opacity: 0.8;
  font-weight: 500;
  margin-top: 3px;
}

.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  line-height: 0;
}

.hero-wave svg {
  display: block;
  width: 100%;
  height: 48px;
}

/* ==================== FILTRES ==================== */
.filters-section {
  padding: 36px 0;
  background: white;
  border-bottom: 1px solid var(--border);
}

.filters-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  background: #edf2f7;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition);
  font-weight: 500;
  font-size: 0.85rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-btn:hover {
  background: #e2e8f0;
  color: var(--text-primary);
}

.filter-btn.active {
  background: var(--primary);
  color: white;
  box-shadow: 0 2px 8px rgba(43, 108, 176, 0.3);
}

.filter-count {
  background: rgba(0, 0, 0, 0.08);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
}

.filter-btn.active .filter-count {
  background: rgba(255, 255, 255, 0.25);
}

.filter-search {
  position: relative;
}

.filter-search i {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 0.9rem;
}

.filter-search input {
  padding: 10px 16px 10px 40px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-full);
  width: 260px;
  outline: none;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all var(--transition);
}

.filter-search input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.12);
}

/* ==================== LOADING ==================== */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 380px;
  background: var(--bg-page);
}

.loading-spinner {
  text-align: center;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-spinner p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* ==================== GRID PROJETS ==================== */
.projets-grid-section {
  padding: 48px 0 64px;
  background: var(--bg-page);
}

.projets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

.projet-card {
  background: white;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  position: relative;
}

.projet-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
}

.projet-card.featured {
  border: 2px solid var(--primary);
}

.projet-card.featured::before {
  content: '★ Projet phare';
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--primary);
  color: white;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 600;
  z-index: 3;
}

.projet-image {
  position: relative;
  height: 210px;
  overflow: hidden;
  background: #edf2f7;
}

.projet-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.45s ease;
}

.projet-card:hover .projet-image img {
  transform: scale(1.05);
}

.projet-category {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(6px);
  color: white;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 500;
  z-index: 2;
}

.projet-status {
  position: absolute;
  bottom: 12px;
  left: 12px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 600;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 5px;
  color: white;
}

.projet-status.termine {
  background: #38a169;
}
.projet-status.encours {
  background: #d69e2e;
}
.projet-status.planifie {
  background: var(--primary);
}

.projet-overlay {
  position: absolute;
  inset: 0;
  background: rgba(26, 54, 93, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.projet-card:hover .projet-overlay {
  opacity: 1;
}

.overlay-buttons {
  display: flex;
  gap: 12px;
}

.overlay-btn {
  width: 44px;
  height: 44px;
  background: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}

.overlay-btn:hover {
  background: var(--primary);
  color: white;
  transform: scale(1.08);
}

.projet-info {
  padding: 1.35rem;
}

.projet-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
}

.projet-header h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-primary);
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

.projet-info p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0 0 12px;
}

.projet-meta {
  display: flex;
  gap: 14px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.meta-item i {
  color: var(--primary);
  width: 14px;
}

.projet-progress {
  margin-bottom: 14px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 5px;
}

.progress-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), #63b3ed);
  border-radius: 3px;
  transition: width 0.8s ease;
}

.projet-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.btn-details {
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  transition: gap var(--transition);
}

.btn-details:hover {
  gap: 10px;
}

.projet-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  font-size: 0.7rem;
  padding: 3px 10px;
  background: #edf2f7;
  border-radius: var(--radius-full);
  color: var(--text-secondary);
}

/* ==================== PAGINATION ==================== */
.pagination {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 2.5rem;
}

.page-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid var(--border);
  background: white;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-light);
}

.page-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  box-shadow: 0 2px 8px rgba(43, 108, 176, 0.3);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ==================== FEATURED ==================== */
.featured-section {
  padding: 56px 0;
  background: var(--bg-page);
}

.featured-wrapper {
  background: white;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
  position: relative;
}

.featured-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  background: var(--primary);
  color: white;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.8rem;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 10px rgba(43, 108, 176, 0.3);
}

.featured-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  align-items: stretch;
}

.featured-text {
  padding: 2.75rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.featured-text h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px;
  line-height: 1.3;
}

.featured-description {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0 0 1.5rem;
}

.featured-stats {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 1.75rem;
}

.featured-stat {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.featured-stat i {
  color: var(--primary);
  width: 18px;
}

.btn-featured {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 22px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: 0 2px 8px rgba(43, 108, 176, 0.25);
  width: fit-content;
}

.btn-featured:hover {
  background: var(--primary-dark);
  gap: 12px;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(43, 108, 176, 0.35);
}

.featured-image {
  position: relative;
  min-height: 360px;
  background: #edf2f7;
}

.featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.85), transparent);
  color: white;
  padding: 1.25rem 1rem 1rem;
  text-align: center;
  font-size: 0.8rem;
}

/* ==================== TIMELINE ==================== */
.timeline-section {
  padding: 64px 0;
  background: white;
}

.timeline {
  max-width: 780px;
  margin: 0 auto;
}

.timeline-item {
  display: flex;
  gap: 1.75rem;
  margin-bottom: 1.5rem;
}

.timeline-year {
  text-align: center;
  min-width: 80px;
  flex-shrink: 0;
}

.year-circle {
  width: 56px;
  height: 56px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  margin: 0 auto 8px;
  box-shadow: 0 4px 12px rgba(43, 108, 176, 0.3);
}

.year-line {
  width: 2px;
  height: calc(100% - 64px);
  background: linear-gradient(to bottom, var(--primary), #bee3f8);
  margin: 0 auto;
}

.timeline-projects {
  flex: 1;
  padding-bottom: 1rem;
}

.timeline-project {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  padding: 1rem 1.15rem;
  background: var(--bg-page);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  transition: all var(--transition);
}

.timeline-project:hover {
  transform: translateX(5px);
  background: white;
  box-shadow: var(--shadow-sm);
  border-color: transparent;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  background: var(--primary);
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}

.timeline-content h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px;
}

.timeline-content p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

/* ==================== NO RESULTS ==================== */
.no-results-section {
  padding: 80px 0;
  background: var(--bg-page);
}

.no-results-card {
  text-align: center;
  background: white;
  border-radius: 24px;
  padding: 3.5rem 2.5rem;
  max-width: 440px;
  margin: 0 auto;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.no-results-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #edf2f7;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
  font-size: 1.75rem;
  color: var(--text-muted);
}

.no-results-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px;
}

.no-results-card p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0 0 1.5rem;
}

.btn-reset {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 22px;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition);
}

.btn-reset:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

/* ==================== CTA ==================== */
.cta-projets {
  padding: 56px 0;
  background: linear-gradient(145deg, #0f2744 0%, #1a365d 100%);
  color: white;
}

.cta-content {
  text-align: center;
  max-width: 580px;
  margin: 0 auto;
}

.cta-content h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.85rem;
  font-weight: 700;
  margin: 0 0 10px;
}

.cta-content p {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0 0 1.75rem;
}

.cta-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: var(--primary);
  text-decoration: none;
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.9rem;
  border: none;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  gap: 12px;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.12);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.9rem;
  border: 1px solid rgba(255, 255, 255, 0.25);
  transition: all var(--transition);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.22);
  transform: translateY(-2px);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 22px;
  background: transparent;
  color: var(--text-secondary);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition);
}

.btn-outline:hover {
  background: #f7fafc;
  border-color: var(--border);
  color: var(--text-primary);
}

/* ==================== MODAL ==================== */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  padding: 20px;
}

.modal.active {
  opacity: 1;
  visibility: visible;
}

.modal-container {
  background: white;
  border-radius: 24px;
  max-width: 960px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: var(--shadow-lg);
  transform: scale(0.96) translateY(12px);
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.modal.active .modal-container {
  transform: scale(1) translateY(0);
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid var(--border);
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--transition);
  box-shadow: var(--shadow-sm);
}

.modal-close:hover {
  background: #e53e3e;
  border-color: #e53e3e;
  color: white;
  transform: scale(1.08);
}

.modal-content {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  gap: 0;
}

.modal-image {
  position: relative;
  background: #edf2f7;
  min-height: 320px;
}

.modal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  min-height: 320px;
}

.modal-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.modal-badge.termine {
  background: #38a169;
}
.modal-badge.encours {
  background: #d69e2e;
}
.modal-badge.planifie {
  background: var(--primary);
}

.modal-info {
  padding: 2rem 1.75rem 2rem 1.5rem;
  display: flex;
  flex-direction: column;
}

.modal-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px;
  line-height: 1.3;
  padding-right: 36px;
}

.modal-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 1.35rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.modal-meta i {
  color: var(--primary);
  margin-right: 4px;
}

.modal-section {
  margin-bottom: 1.25rem;
}

.modal-section h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-section h4 i {
  color: var(--primary);
}

.modal-section p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0;
}

.modal-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin: 1.25rem 0;
  padding: 1.15rem;
  background: var(--bg-page);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
}

.modal-stat {
  text-align: center;
}

.stat-title {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.stat-value {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--primary);
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: auto;
  padding-top: 8px;
  flex-wrap: wrap;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 992px) {
  .featured-content {
    grid-template-columns: 1fr;
  }

  .featured-text {
    padding: 2rem;
    order: 2;
  }

  .featured-image {
    min-height: 260px;
    order: 1;
  }

  .modal-content {
    grid-template-columns: 1fr;
  }

  .modal-image img {
    min-height: 240px;
    max-height: 280px;
  }
}

@media (max-width: 768px) {
  .hero-projets {
    padding: 48px 0 40px;
    min-height: 320px;
  }

  .hero-stats {
    gap: 8px;
  }

  .stat-item {
    min-width: 100px;
    padding: 8px 12px;
  }

  .filters-wrapper {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-buttons {
    justify-content: center;
  }

  .filter-search input {
    width: 100%;
  }

  .projets-grid {
    grid-template-columns: 1fr;
  }

  .timeline-item {
    flex-direction: column;
    gap: 12px;
  }

  .year-line {
    display: none;
  }

  .modal-stats {
    grid-template-columns: 1fr;
  }

  .modal-actions {
    flex-direction: column;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .cta-content h2 {
    font-size: 1.5rem;
  }
}

@media (min-width: 769px) and (max-width: 1100px) {
  .projets-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>