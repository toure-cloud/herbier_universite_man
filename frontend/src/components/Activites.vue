<template>
  <div class="activites">
    <!-- ============================================================
         BARRE DE NAVIGATION STICKY (scroll-spy)
         ============================================================ -->
    <nav class="sticky-nav" :class="{ visible: showStickyNav }">
      <div class="sticky-nav-inner">
        <button
          v-for="section in sections"
          :key="section.id"
          :class="['sticky-nav-btn', { active: activeSection === section.id }]"
          @click="scrollToSection(section.id)"
        >
          <i :class="section.icon"></i>
          <span>{{ section.label }}</span>
        </button>
      </div>
    </nav>

    <!-- ============================================================
         HERO
         ============================================================ -->
    <section id="hero" class="hero-activites">
      <div class="hero-background">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
        <div class="hero-glow hero-glow-1"></div>
        <div class="hero-glow hero-glow-2"></div>
      </div>

      <div class="hero-content" data-aos="fade-up">
        <div class="hero-badge">
          <i class="fas fa-seedling"></i>
          <span>Notre Engagement</span>
        </div>

        <h1 class="hero-title">
          Des actions concrètes<br />
          pour <span class="title-accent">la biodiversité</span>
        </h1>

        <p class="hero-subtitle">
          Découvrez comment nous agissons quotidiennement pour la recherche,
          la conservation et la formation en botanique
        </p>

        <div class="hero-stats">
          <div class="hero-stat" v-for="stat in heroStats" :key="stat.label">
            <div class="stat-number">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>

        <button class="hero-scroll-hint" @click="scrollToSection('services')">
          <i class="fas fa-chevron-down"></i>
        </button>
      </div>

      <div class="hero-wave">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path fill="var(--bg-page)"
            d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z">
          </path>
        </svg>
      </div>
    </section>

    <!-- ============================================================
         SERVICES
         ============================================================ -->
    <section id="services" class="expertise-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Nos Services</span>
          <h2 class="section-title">Domaines d'Expertise</h2>
          <p class="section-subtitle">
            Des compétences scientifiques de haut niveau au service de la botanique
          </p>
        </div>

        <div v-if="loading" class="loading-block">
          <div class="spinner"></div>
          <p>Chargement des services...</p>
        </div>

        <div v-else class="services-grid">
          <article
            v-for="(service, index) in services"
            :key="index"
            class="service-card"
            :class="{ 'has-image': getServiceMainImage(service) }"
            data-aos="fade-up"
            :data-aos-delay="Math.min(index * 60, 300)"
            @click="openService(service)"
            role="button"
            tabindex="0"
            @keydown.enter="openService(service)"
          >
            <div v-if="getServiceMainImage(service)" class="service-image">
              <img
                :src="getImageUrl(getServiceMainImage(service))"
                :alt="service.title"
                @error="handleImageError"
                loading="lazy"
              />
              <span v-if="getServiceAllImages(service).length > 1" class="gallery-count">
                <i class="fas fa-images"></i> {{ getServiceAllImages(service).length }}
              </span>
              <div class="image-overlay-hint">
                <i class="fas fa-expand"></i>
              </div>
            </div>

            <div class="service-icon">
              <i :class="service.icon"></i>
            </div>

            <h3>{{ service.title }}</h3>
            <p>{{ service.description }}</p>

            <ul class="service-features" v-if="service.features && service.features.length">
              <li v-for="(feature, idx) in service.features.slice(0, 3)" :key="idx">
                <i class="fas fa-check-circle"></i>
                <span>{{ feature }}</span>
              </li>
            </ul>

            <div class="service-details-btn">
              Voir les détails
              <i class="fas fa-arrow-right"></i>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ============================================================
         MÉTHODOLOGIE
         ============================================================ -->
    <section id="methodologie" class="methodologie-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Notre Processus</span>
          <h2 class="section-title">Méthodologie de travail</h2>
          <p class="section-subtitle">Une approche rigoureuse et structurée</p>
        </div>

        <div class="methodologie-timeline">
          <div
            v-for="(step, index) in methodologie"
            :key="index"
            class="timeline-step"
            data-aos="fade-up"
            :data-aos-delay="Math.min(index * 80, 320)"
          >
            <div class="step-marker">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-line" v-if="index < methodologie.length - 1"></div>
            </div>
            <div class="step-card">
              <div class="step-icon">
                <i :class="step.icon"></i>
              </div>
              <div class="step-content">
                <h3>{{ step.title }}</h3>
                <p>{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================
         PUBLICATIONS
         ============================================================ -->
    <section id="publications" class="publications-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Recherche</span>
          <h2 class="section-title">Publications scientifiques</h2>
          <p class="section-subtitle">Nos contributions à la science botanique</p>
        </div>

        <div class="publications-grid">
          <article
            v-for="(pub, index) in publications"
            :key="index"
            class="publication-card"
            data-aos="fade-up"
            :data-aos-delay="Math.min(index * 60, 240)"
          >
            <div class="publication-icon">
              <i class="fas fa-file-alt"></i>
            </div>
            <div class="publication-details">
              <h3>{{ pub.title }}</h3>
              <p class="publication-authors">{{ pub.authors }}</p>
              <p class="publication-journal">{{ pub.journal }} • {{ pub.year }}</p>
              <a v-if="pub.link" :href="pub.link" class="publication-link" target="_blank" rel="noopener">
                Lire l'article <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ============================================================
         TÉMOIGNAGES — Carrousel
         ============================================================ -->
    <section id="temoignages" class="testimonials-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Témoignages</span>
          <h2 class="section-title">Ils nous font confiance</h2>
          <p class="section-subtitle">Ce que nos partenaires disent de notre travail</p>
        </div>

        <div class="testimonials-carousel" data-aos="fade-up">
          <button class="carousel-nav prev" @click="prevTestimonial" aria-label="Précédent">
            <i class="fas fa-chevron-left"></i>
          </button>

          <transition name="testimonial-fade" mode="out-in">
            <article class="testimonial-card" :key="currentTestimonialIndex">
              <div class="testimonial-quote">
                <i class="fas fa-quote-left"></i>
                <p>{{ currentTestimonial?.text }}</p>
              </div>
              <div class="testimonial-author">
                <div class="author-avatar">
                  <img
                    :src="getAvatarUrl(currentTestimonial?.avatar)"
                    :alt="currentTestimonial?.name"
                    @error="handleAvatarError"
                  />
                </div>
                <div class="author-info">
                  <h4>{{ currentTestimonial?.name }}</h4>
                  <p>{{ currentTestimonial?.position }}</p>
                  <span>{{ currentTestimonial?.organization }}</span>
                </div>
              </div>
            </article>
          </transition>

          <button class="carousel-nav next" @click="nextTestimonial" aria-label="Suivant">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>

        <!-- Indicateurs -->
        <div class="carousel-dots" v-if="testimonials.length > 1">
          <button
            v-for="(_, i) in testimonials"
            :key="i"
            :class="['dot', { active: i === currentTestimonialIndex }]"
            @click="currentTestimonialIndex = i"
            :aria-label="`Témoignage ${i + 1}`"
          ></button>
        </div>
      </div>
    </section>

    <!-- ============================================================
         CTA
         ============================================================ -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content" data-aos="zoom-in">
          <h2>Vous avez un projet ?</h2>
          <p>
            Collaborons ensemble pour un avenir durable et la préservation de
            notre patrimoine végétal
          </p>
          <div class="cta-buttons">
            <router-link to="/contact" class="btn-primary">
              Proposer un projet <i class="fas fa-arrow-right"></i>
            </router-link>
            <a href="#" class="btn-secondary">
              Télécharger notre brochure <i class="fas fa-download"></i>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================
         MODAL DÉTAIL SERVICE — PREMIUM
         ============================================================ -->
    <transition name="modal-fade">
      <div
        v-if="selectedService"
        class="service-modal"
        @click.self="closeService"
        role="dialog"
        aria-modal="true"
      >
        <div class="service-modal-container">
          <!-- Bouton fermer -->
          <button class="service-modal-close" @click="closeService" aria-label="Fermer">
            <i class="fas fa-times"></i>
          </button>

          <!-- En-tête -->
          <header class="service-modal-header">
            <div class="service-modal-icon">
              <i :class="selectedService.icon"></i>
            </div>
            <div class="service-modal-header-text">
              <span v-if="selectedService.titre_court" class="service-modal-kicker">
                {{ selectedService.titre_court }}
              </span>
              <h2>{{ selectedService.title }}</h2>
            </div>

            <div class="service-modal-nav" v-if="services.length > 1">
              <button @click="navService(-1)" aria-label="Service précédent" title="Précédent">
                <i class="fas fa-chevron-left"></i>
              </button>
              <button @click="navService(1)" aria-label="Service suivant" title="Suivant">
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          </header>

          <!-- Corps -->
          <div class="service-modal-body">
            <!-- Galerie -->
            <div v-if="allServiceImages.length" class="service-modal-gallery">
              <div class="service-modal-gallery-main">
                <img
                  :src="getImageUrl(currentServiceImage)"
                  :alt="selectedService.title"
                  @error="handleImageError"
                />
                <div class="gallery-main-overlay"></div>

                <!-- Compteur -->
                <div class="gallery-counter" v-if="allServiceImages.length > 1">
                  <i class="fas fa-image"></i>
                  {{ currentServiceImageIndex + 1 }} / {{ allServiceImages.length }}
                </div>

                <!-- Navigation -->
                <button
                  v-if="allServiceImages.length > 1"
                  class="gallery-nav prev"
                  @click.stop="prevServiceImage"
                  aria-label="Image précédente"
                >
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button
                  v-if="allServiceImages.length > 1"
                  class="gallery-nav next"
                  @click.stop="nextServiceImage"
                  aria-label="Image suivante"
                >
                  <i class="fas fa-chevron-right"></i>
                </button>
              </div>

              <!-- Miniatures -->
              <div v-if="allServiceImages.length > 1" class="service-modal-gallery-thumbs">
                <button
                  v-for="(img, i) in allServiceImages"
                  :key="i"
                  :class="['thumb', { active: i === currentServiceImageIndex }]"
                  @click="currentServiceImageIndex = i"
                  :aria-label="`Image ${i + 1}`"
                >
                  <img :src="getImageUrl(img)" @error="handleImageError" :alt="`Image ${i + 1}`" />
                </button>
              </div>
            </div>

            <!-- Caption -->
            <p v-if="selectedService.caption" class="service-modal-caption">
              <i class="fas fa-camera"></i>
              {{ selectedService.caption }}
            </p>

            <!-- Description -->
            <div class="service-modal-section">
              <h3 class="modal-section-title">
                <span class="title-icon"><i class="fas fa-align-left"></i></span>
                Description
              </h3>
              <p class="service-modal-description">
                {{ selectedService.descriptionLongue || selectedService.description }}
              </p>
            </div>

            <!-- Points forts -->
            <div
              v-if="selectedService.features && selectedService.features.length"
              class="service-modal-section"
            >
              <h3 class="modal-section-title">
                <span class="title-icon"><i class="fas fa-star"></i></span>
                Points forts
              </h3>
              <ul class="service-modal-features">
                <li v-for="(feature, idx) in selectedService.features" :key="idx">
                  <i class="fas fa-check-circle"></i>
                  <span>{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Pied -->
          <footer class="service-modal-footer">
            <div class="modal-footer-actions">
              <button class="btn-modal-share" @click="shareService" title="Partager">
                <i class="fas fa-share-alt"></i>
              </button>
              <button class="btn-modal-close" @click="closeService">
                Fermer
              </button>
              <!-- <router-link to="/contact" class="btn-modal-cta">
                Demander ce service <i class="fas fa-arrow-right"></i>
              </router-link> -->
            </div>
            <div class="modal-keyboard-hint">
              <kbd>←</kbd> <kbd>→</kbd> naviguer · <kbd>Échap</kbd> fermer
            </div>
          </footer>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios'
import config from '../config.js'

export default {
  name: 'Activites',
  data() {
    return {
      loading: true,
      heroStats: [
        { value: '10+', label: "Années d'expertise" },
        { value: '5000+', label: 'Spécimens étudiés' },
        { value: '150+', label: 'Espèces identifiées' },
        { value: '25+', label: 'Chercheurs' }
      ],
      services: [],
      methodologie: [],
      publications: [],
      testimonials: [],
      selectedService: null,
      currentServiceImageIndex: 0,
      // Nouveaux
      showStickyNav: false,
      activeSection: 'hero',
      currentTestimonialIndex: 0,
      testimonialTimer: null,
      sections: [
        { id: 'hero', label: 'Accueil', icon: 'fas fa-home' },
        { id: 'services', label: 'Services', icon: 'fas fa-th-large' },
        { id: 'methodologie', label: 'Méthode', icon: 'fas fa-tasks' },
        { id: 'publications', label: 'Recherche', icon: 'fas fa-book' },
        { id: 'temoignages', label: 'Avis', icon: 'fas fa-quote-left' },
      ],
    }
  },
  computed: {
    allServiceImages() {
      if (!this.selectedService) return []
      return this.getServiceAllImages(this.selectedService)
    },
    currentServiceImage() {
      return this.allServiceImages[this.currentServiceImageIndex] || ''
    },
    currentTestimonial() {
      return this.testimonials[this.currentTestimonialIndex] || {}
    },
  },
  mounted() {
    this.initAnimations()
    this.loadActivitesData()
    window.addEventListener('scroll', this.handleScroll, { passive: true })
    window.addEventListener('keydown', this.handleKeydown)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
    window.removeEventListener('keydown', this.handleKeydown)
    this.stopTestimonialTimer()
  },
  methods: {
    async loadActivitesData() {
      try {
        const { data } = await axios.get(config.API_ENDPOINTS.activitesData)

        this.services = (data.activites || []).map(a => ({
          id: a.id,
          icon: a.icon || 'fas fa-leaf',
          title: a.titre || '',
          titre_court: a.titre_court || '',
          description: a.description_courte || '',
          descriptionLongue: a.description_longue || '',
          image: a.image || '',
          images_galerie: Array.isArray(a.images_galerie) ? a.images_galerie : [],
          caption: a.caption || '',
          features: (a.points_forts || '')
            .split('\n')
            .map(p => p.trim())
            .filter(Boolean)
        }))
        if (this.services.length === 0) this.services = this.getDefaultServices()

        this.methodologie = (data.methodologie || []).map(m => ({
          icon: m.icon || 'fas fa-clipboard-list',
          title: m.titre || '',
          description: m.description || ''
        }))
        if (this.methodologie.length === 0) this.methodologie = this.getDefaultMethodologie()

        this.publications = (data.publications || []).map(p => ({
          title: p.titre || '',
          authors: p.auteurs || '',
          journal: p.journal || '',
          year: p.annee || '',
          link: p.lien || ''
        }))
        if (this.publications.length === 0) this.publications = this.getDefaultPublications()

        this.testimonials = (data.temoignages || []).map(t => ({
          text: t.texte || '',
          name: t.nom || '',
          position: t.poste || '',
          organization: t.organisation || '',
          avatar: t.photo || ''
        }))
        if (this.testimonials.length === 0) this.testimonials = this.getDefaultTestimonials()
      } catch (error) {
        console.error('Erreur chargement activités:', error)
        this.services = this.getDefaultServices()
        this.methodologie = this.getDefaultMethodologie()
        this.publications = this.getDefaultPublications()
        this.testimonials = this.getDefaultTestimonials()
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.initAnimations()
          this.startTestimonialTimer()
        })
      }
    },

    getServiceMainImage(service) {
      if (!service) return ''
      if (service.image) return service.image
      if (Array.isArray(service.images_galerie) && service.images_galerie.length) {
        return service.images_galerie[0]
      }
      return ''
    },

    getServiceAllImages(service) {
      if (!service) return []
      const imgs = []
      if (service.image) imgs.push(service.image)
      if (Array.isArray(service.images_galerie)) {
        imgs.push(...service.images_galerie)
      }
      return [...new Set(imgs)]
    },

    getImageUrl(path) {
      if (!path) return ''
      if (path.startsWith('http')) return path
      if (path.startsWith('/media')) {
        const adminBase = (import.meta.env.VITE_ADMIN_MEDIA_URL || 'http://localhost:8001').replace(/\/+$/, '')
        return `${adminBase}${path}`
      }
      return path
    },

    getAvatarUrl(path) {
      return this.getImageUrl(path)
    },

    handleImageError(e) {
      if (e.target.dataset.errorHandled) return
      e.target.dataset.errorHandled = 'true'
      e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Crect fill='%23f1f5f9' width='80' height='80'/%3E%3Ctext x='50%25' y='50%25' font-family='Arial' font-size='24' fill='%23cbd5e1' text-anchor='middle' dy='.3em'%3E%3F%3C/text%3E%3C/svg%3E"
    },

    handleAvatarError(e) {
      e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect fill='%23e2e8f0' width='100' height='100'/%3E%3Ccircle cx='50' cy='40' r='20' fill='%2394a3b8'/%3E%3Cpath d='M20,90 Q50,60 80,90' fill='%2394a3b8'/%3E%3C/svg%3E"
    },

    // ============================================================
    // MODAL SERVICE
    // ============================================================
    openService(service) {
      this.selectedService = service
      this.currentServiceImageIndex = 0
      document.body.style.overflow = 'hidden'
      this.stopTestimonialTimer()
    },

    closeService() {
      this.selectedService = null
      this.currentServiceImageIndex = 0
      document.body.style.overflow = ''
      this.startTestimonialTimer()
    },

    nextServiceImage() {
      if (this.allServiceImages.length > 1) {
        this.currentServiceImageIndex =
          (this.currentServiceImageIndex + 1) % this.allServiceImages.length
      }
    },

    prevServiceImage() {
      if (this.allServiceImages.length > 1) {
        this.currentServiceImageIndex =
          (this.currentServiceImageIndex - 1 + this.allServiceImages.length) %
          this.allServiceImages.length
      }
    },

    navService(direction) {
      const currentIndex = this.services.findIndex(s => s.id === this.selectedService?.id)
      if (currentIndex === -1) return
      const nextIndex = (currentIndex + direction + this.services.length) % this.services.length
      this.openService(this.services[nextIndex])
    },

    shareService() {
      if (!this.selectedService) return
      const data = {
        title: this.selectedService.title,
        text: this.selectedService.description,
        url: window.location.href,
      }
      if (navigator.share) {
        navigator.share(data).catch(() => {})
      } else {
        navigator.clipboard?.writeText(window.location.href)
        alert('Lien copié dans le presse-papiers')
      }
    },

    // ============================================================
    // NAVIGATION STICKY + SCROLL-SPY
    // ============================================================
    handleScroll() {
      this.showStickyNav = window.scrollY > 400

      // Scroll-spy
      const scrollPos = window.scrollY + 200
      for (const section of this.sections) {
        const el = document.getElementById(section.id)
        if (el) {
          const top = el.offsetTop
          const bottom = top + el.offsetHeight
          if (scrollPos >= top && scrollPos < bottom) {
            this.activeSection = section.id
            break
          }
        }
      }
    },

    scrollToSection(id) {
      const el = document.getElementById(id)
      if (el) {
        const offset = 80
        window.scrollTo({ top: el.offsetTop - offset, behavior: 'smooth' })
      }
    },

    // ============================================================
    // CARROUSEL TÉMOIGNAGES
    // ============================================================
    nextTestimonial() {
      if (this.testimonials.length > 1) {
        this.currentTestimonialIndex =
          (this.currentTestimonialIndex + 1) % this.testimonials.length
      }
    },

    prevTestimonial() {
      if (this.testimonials.length > 1) {
        this.currentTestimonialIndex =
          (this.currentTestimonialIndex - 1 + this.testimonials.length) % this.testimonials.length
      }
    },

    startTestimonialTimer() {
      this.stopTestimonialTimer()
      if (this.testimonials.length > 1) {
        this.testimonialTimer = setInterval(() => this.nextTestimonial(), 6000)
      }
    },

    stopTestimonialTimer() {
      if (this.testimonialTimer) {
        clearInterval(this.testimonialTimer)
        this.testimonialTimer = null
      }
    },

    // ============================================================
    // CLAVIER
    // ============================================================
    handleKeydown(e) {
      if (!this.selectedService) return
      if (e.key === 'Escape') this.closeService()
      if (e.key === 'ArrowRight') this.nextServiceImage()
      if (e.key === 'ArrowLeft') this.prevServiceImage()
    },

    // ============================================================
    // FALLBACKS
    // ============================================================
    getDefaultServices() {
      return [
        { icon: 'fas fa-leaf', title: 'Identification des plantes', description: "Service expert d'identification botanique.", features: ['Identification morphologique', 'Base de données', 'Expertise reconnue'] },
        { icon: 'fas fa-graduation-cap', title: 'Formations aux inventaires', description: "Programmes de formation complets.", features: ['Formations pratiques', 'Modules certifiants', 'Suivi personnalisé'] },
        { icon: 'fas fa-chart-line', title: 'Inventaire floristique', description: "Inventaires exhaustifs.", features: ['Protocoles scientifiques', 'Équipe expérimentée', 'Rapports détaillés'] },
        { icon: 'fas fa-industry', title: "Études d'impact", description: "Évaluations environnementales.", features: ['Conformité internationale', 'Expertise pluridisciplinaire', "Mesures d'atténuation"] },
        { icon: 'fas fa-box', title: "Réalisation d'herbier", description: "Collections d'herbier scientifiques.", features: ['Collecte et séchage', 'Étiquetage', 'Conservation optimale'] },
        { icon: 'fas fa-globe-africa', title: 'Gestion durable', description: 'Stratégies de gestion durable.', features: ['Conservation in situ', 'Plan de gestion', 'Suivi'] }
      ]
    },

    getDefaultMethodologie() {
      return [
        { icon: 'fas fa-clipboard-list', title: 'Phase préparatoire', description: "Analyse des besoins et définition des protocoles." },
        { icon: 'fas fa-hiking', title: 'Travail de terrain', description: 'Collecte des données et relevés botaniques.' },
        { icon: 'fas fa-microscope', title: 'Analyse en laboratoire', description: 'Identification et analyses statistiques.' },
        { icon: 'fas fa-chart-bar', title: 'Rapport et valorisation', description: 'Rédaction et présentation des résultats.' }
      ]
    },

    getDefaultPublications() {
      return [
        { title: 'Diversité floristique des Montagnes de Man', authors: 'Kouassi J., Konan M., Yao P.', journal: 'Journal of Tropical Botany', year: 2023, link: '#' }
      ]
    },

    getDefaultTestimonials() {
      return [
        { text: 'Une équipe exceptionnelle.', name: 'Dr. Bernard Amani', position: 'Directeur', organization: 'Parc National de Taï', avatar: '' }
      ]
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
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

/* ==================== BASE ==================== */
.activites {
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
  --radius-full: 9999px;
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
.section-badge.light {
  background: rgba(99, 179, 237, 0.2);
  color: #90cdf4;
}

.section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.75rem, 3vw, 2.15rem);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
  line-height: 1.25;
}

.section-subtitle {
  font-size: 0.95rem;
  color: var(--text-muted);
  margin: 0 auto;
  max-width: 560px;
}

.section-header {
  text-align: center;
  margin-bottom: 2.75rem;
}

/* ==================== STICKY NAV ==================== */
.sticky-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 900;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  transform: translateY(-100%);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.sticky-nav.visible { transform: translateY(0); }

.sticky-nav-inner {
  max-width: 1240px;
  margin: 0 auto;
  padding: 10px 24px;
  display: flex;
  gap: 6px;
  overflow-x: auto;
  scrollbar-width: none;
}
.sticky-nav-inner::-webkit-scrollbar { display: none; }

.sticky-nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 500;
  border-radius: var(--radius-full);
  cursor: pointer;
  white-space: nowrap;
  transition: all var(--transition);
  font-family: inherit;
}
.sticky-nav-btn i { font-size: 0.75rem; }
.sticky-nav-btn:hover {
  background: #f1f5f9;
  color: var(--text-primary);
}
.sticky-nav-btn.active {
  background: var(--primary);
  color: #fff;
  box-shadow: 0 4px 12px rgba(43, 108, 176, 0.25);
}

/* ==================== HERO ==================== */
.hero-activites {
  position: relative;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  background: linear-gradient(145deg, #0a1e36 0%, #1a365d 45%, #1e3a5f 100%);
}

.hero-background { position: absolute; inset: 0; }

.hero-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(66, 153, 225, 0.22), transparent 70%);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.6;
}

.hero-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(60px);
}
.hero-glow-1 {
  width: 280px;
  height: 280px;
  background: radial-gradient(circle, rgba(66, 153, 225, 0.25), transparent 70%);
  top: -80px;
  right: -40px;
}
.hero-glow-2 {
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(56, 161, 105, 0.2), transparent 70%);
  bottom: -60px;
  left: -30px;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 24px 32px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 0.75rem;
}
.hero-badge i { color: #63b3ed; }

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.6rem, 3vw, 2.25rem);
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}

.title-accent {
  background: linear-gradient(135deg, #63b3ed, #90cdf4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 0.9rem;
  line-height: 1.5;
  opacity: 0.9;
  margin: 0 auto 1.15rem;
  max-width: 540px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 0.7rem;
  flex-wrap: wrap;
}

.hero-stat {
  text-align: center;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(10px);
  padding: 8px 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 100px;
  transition: all var(--transition);
}
.hero-stat:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: #90cdf4;
  line-height: 1.1;
}
.stat-label {
  font-size: 0.65rem;
  opacity: 0.8;
  font-weight: 500;
  margin-top: 2px;
}

.hero-scroll-hint {
  margin-top: 1rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  animation: bounce 2s infinite;
  transition: all var(--transition);
  font-size: 0.75rem;
}
.hero-scroll-hint:hover { background: rgba(255, 255, 255, 0.18); }
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(5px); }
}

.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  line-height: 0;
}
.hero-wave svg { display: block; width: 100%; height: 36px; }

/* ==================== SERVICES ==================== */
.expertise-section { padding: 72px 0; background: white; }

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.service-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 1.75rem;
  border: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  outline: none;
}

.service-card:focus-visible {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.15);
}

.service-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(43, 108, 176, 0.15);
  border-color: transparent;
}

.service-image {
  position: relative;
  width: 100%;
  height: 180px;
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 16px;
  background: #f1f5f9;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}

.service-card:hover .service-image img { transform: scale(1.07); }

.image-overlay-hint {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.5rem;
  opacity: 0;
  transition: opacity 0.3s;
}
.service-card:hover .image-overlay-hint { opacity: 1; }

.gallery-count {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

.service-icon {
  width: 56px;
  height: 56px;
  background: var(--primary-light);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
  transition: all var(--transition);
}

.service-card:hover .service-icon {
  background: var(--primary);
  transform: rotate(-6deg) scale(1.05);
}

.service-icon i {
  font-size: 1.3rem;
  color: var(--primary);
  transition: color var(--transition);
}
.service-card:hover .service-icon i { color: white; }
.service-card.has-image .service-icon { display: none; }

.service-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 10px;
}

.service-card > p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0 0 1.15rem;
}

.service-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.service-features li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 5px 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.service-features li i {
  color: var(--accent);
  font-size: 0.85rem;
  margin-top: 2px;
  flex-shrink: 0;
}

.service-details-btn {
  margin-top: 14px;
  color: var(--primary);
  font-weight: 500;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: gap 0.25s ease;
}
.service-card:hover .service-details-btn { gap: 12px; }

/* ==================== MÉTHODOLOGIE ==================== */
.methodologie-section { padding: 72px 0; background: var(--bg-page); }

.methodologie-timeline { max-width: 860px; margin: 0 auto; }

.timeline-step { display: flex; gap: 1.35rem; margin-bottom: 1.25rem; }

.step-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.step-number {
  width: 46px;
  height: 46px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 12px rgba(43, 108, 176, 0.3);
  z-index: 2;
}

.step-line {
  width: 2px;
  flex: 1;
  background: linear-gradient(to bottom, var(--primary), #bee3f8);
  margin: 8px 0 0;
  min-height: 24px;
}

.step-card {
  flex: 1;
  background: white;
  border-radius: 20px;
  padding: 1.35rem 1.5rem;
  display: flex;
  gap: 1.15rem;
  border: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all var(--transition);
}
.step-card:hover { transform: translateX(6px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }

.step-icon {
  width: 48px;
  height: 48px;
  background: var(--primary-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.step-icon i { font-size: 1.25rem; color: var(--primary); }

.step-content h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px;
}
.step-content p { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.55; margin: 0; }

/* ==================== PUBLICATIONS ==================== */
.publications-section { padding: 72px 0; background: white; }

.publications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}

.publication-card {
  display: flex;
  gap: 1.15rem;
  background: var(--bg-page);
  border-radius: 20px;
  padding: 1.35rem;
  border: 1px solid var(--border);
  transition: all var(--transition);
}
.publication-card:hover {
  transform: translateX(5px);
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.publication-icon {
  width: 48px;
  height: 48px;
  background: var(--primary-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.publication-icon i { font-size: 1.2rem; color: var(--primary); }

.publication-details h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px;
  line-height: 1.35;
}
.publication-authors { font-size: 0.8rem; color: var(--text-secondary); margin: 0 0 4px; }
.publication-journal { font-size: 0.75rem; color: var(--text-muted); margin: 0 0 10px; }
.publication-link {
  font-size: 0.8rem;
  color: var(--primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  transition: gap var(--transition);
}
.publication-link:hover { gap: 10px; }

/* ==================== TÉMOIGNAGES — Carrousel ==================== */
.testimonials-section { padding: 72px 0; background: var(--bg-page); }

.testimonials-carousel {
  position: relative;
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.testimonial-card {
  flex: 1;
  background: white;
  border-radius: 24px;
  padding: 2.25rem 2rem;
  border: 1px solid var(--border);
  box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.testimonial-quote i {
  font-size: 2rem;
  color: var(--primary);
  opacity: 0.2;
  margin-bottom: 16px;
  display: block;
}

.testimonial-quote p {
  font-size: 1.05rem;
  font-style: italic;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0 0 1.75rem;
}

.testimonial-author {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
}

.author-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--primary-light);
  flex-shrink: 0;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.author-avatar img { width: 100%; height: 100%; object-fit: cover; }

.author-info { text-align: left; }
.author-info h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px;
}
.author-info p { font-size: 0.8rem; color: var(--text-secondary); margin: 0; }
.author-info span { font-size: 0.75rem; color: var(--text-muted); }

.carousel-nav {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: white;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.carousel-nav:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  transform: scale(1.08);
}

.carousel-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 1.5rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: none;
  background: #cbd5e1;
  cursor: pointer;
  transition: all var(--transition);
  padding: 0;
}
.dot.active {
  background: var(--primary);
  width: 24px;
  border-radius: 4px;
}

.testimonial-fade-enter-active,
.testimonial-fade-leave-active { transition: opacity 0.35s ease, transform 0.35s ease; }
.testimonial-fade-enter-from { opacity: 0; transform: translateX(20px); }
.testimonial-fade-leave-to { opacity: 0; transform: translateX(-20px); }

/* ==================== CTA ==================== */
.cta-section { padding: 56px 0 72px; background: white; }

.cta-content {
  text-align: center;
  max-width: 680px;
  margin: 0 auto;
  padding: 2.75rem 2.25rem;
  background: linear-gradient(135deg, var(--primary) 0%, #1a365d 100%);
  border-radius: 28px;
  color: white;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}
.cta-content::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(99, 179, 237, 0.15), transparent 70%);
  top: -150px;
  right: -100px;
  border-radius: 50%;
}

.cta-content h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.85rem;
  font-weight: 700;
  margin: 0 0 10px;
  position: relative;
}
.cta-content p { font-size: 1rem; opacity: 0.9; margin: 0 0 1.75rem; line-height: 1.55; position: relative; }

.cta-buttons { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; position: relative; }

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
  transition: all var(--transition);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.btn-primary:hover { gap: 12px; transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15); }

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
.btn-secondary:hover { background: rgba(255, 255, 255, 0.22); transform: translateY(-2px); }

/* ==================== LOADING ==================== */
.loading-block { text-align: center; padding: 60px 0; }
.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-block p { color: var(--text-muted); font-size: 0.9rem; }

/* ==================== MODAL SERVICE ==================== */
.service-modal {
  position: fixed;
  inset: 0;
  background: rgba(10, 20, 35, 0.75);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 20px;
}

.service-modal-container {
  background: #fff;
  border-radius: 24px;
  max-width: 800px;
  width: 100%;
  max-height: 92vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
}

.service-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  color: #64748b;
  cursor: pointer;
  font-size: 0.95rem;
  z-index: 10;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.service-modal-close:hover {
  background: #e53e3e;
  color: #fff;
  transform: rotate(90deg);
}

.service-modal-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 26px 28px 20px;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 5;
  border-radius: 24px 24px 0 0;
}

.service-modal-icon {
  width: 56px;
  height: 56px;
  background: #ebf4ff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.service-modal-icon i { font-size: 1.4rem; color: #2b6cb0; }

.service-modal-header-text { flex: 1; min-width: 0; }

.service-modal-kicker {
  font-size: 0.7rem;
  font-weight: 600;
  color: #2b6cb0;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  display: block;
  margin-bottom: 4px;
}

.service-modal-header-text h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  line-height: 1.25;
}

.service-modal-nav {
  display: flex;
  gap: 4px;
  margin-right: 50px;
}
.service-modal-nav button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #64748b;
  cursor: pointer;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}
.service-modal-nav button:hover {
  background: #2b6cb0;
  color: #fff;
  border-color: #2b6cb0;
}

.service-modal-body { padding: 24px 28px; }

/* Galerie modal */
.service-modal-gallery { margin-bottom: 24px; }

.service-modal-gallery-main {
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: 16px;
  overflow: hidden;
  background: #f1f5f9;
  position: relative;
}

.service-modal-gallery-main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.gallery-main-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.15), transparent 30%, transparent 70%, rgba(0, 0, 0, 0.35));
  pointer-events: none;
}

.gallery-counter {
  position: absolute;
  bottom: 14px;
  right: 14px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  color: #fff;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  color: #1a202c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.gallery-nav:hover {
  background: #2b6cb0;
  color: #fff;
  transform: translateY(-50%) scale(1.1);
}
.gallery-nav.prev { left: 12px; }
.gallery-nav.next { right: 12px; }

.service-modal-gallery-thumbs {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: thin;
}
.service-modal-gallery-thumbs::-webkit-scrollbar { height: 6px; }
.service-modal-gallery-thumbs::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.thumb {
  flex-shrink: 0;
  width: 76px;
  height: 60px;
  border-radius: 10px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  padding: 0;
  background: #f1f5f9;
  transition: all var(--transition);
  opacity: 0.65;
}
.thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.thumb:hover { opacity: 0.9; transform: translateY(-2px); }
.thumb.active {
  border-color: #2b6cb0;
  opacity: 1;
  box-shadow: 0 0 0 3px rgba(43, 108, 176, 0.15);
}

.service-modal-caption {
  font-size: 0.82rem;
  color: #94a3b8;
  font-style: italic;
  text-align: center;
  margin: 0 0 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.service-modal-section { margin-bottom: 1.5rem; }
.service-modal-section:last-child { margin-bottom: 0; }

.modal-section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #1a202c;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin: 0 0 12px;
}

.title-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: #ebf4ff;
  color: #2b6cb0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  flex-shrink: 0;
}

.service-modal-description {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.75;
  margin: 0;
  white-space: pre-line;
}

.service-modal-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 8px;
}

.service-modal-features li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 14px;
  font-size: 0.88rem;
  color: #4a5568;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.service-modal-features li i {
  color: #38a169;
  font-size: 0.85rem;
  margin-top: 3px;
  flex-shrink: 0;
}

.service-modal-footer {
  padding: 16px 28px 24px;
  border-top: 1px solid #e2e8f0;
  position: sticky;
  bottom: 0;
  background: #fff;
  border-radius: 0 0 24px 24px;
}

.modal-footer-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  align-items: center;
}

.btn-modal-share {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}
.btn-modal-share:hover {
  background: #ebf4ff;
  color: #2b6cb0;
  border-color: #2b6cb0;
}

.btn-modal-close {
  padding: 10px 22px;
  border-radius: var(--radius-full);
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #4a5568;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition);
  font-family: inherit;
}
.btn-modal-close:hover { background: #f8fafc; }

.btn-modal-cta {
  padding: 10px 22px;
  border-radius: var(--radius-full);
  background: #2b6cb0;
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition);
  box-shadow: 0 4px 12px rgba(43, 108, 176, 0.25);
}
.btn-modal-cta:hover { background: #1a4f8a; gap: 12px; transform: translateY(-1px); }

.modal-keyboard-hint {
  text-align: center;
  font-size: 0.72rem;
  color: #94a3b8;
  margin-top: 12px;
}
.modal-keyboard-hint kbd {
  display: inline-block;
  padding: 2px 6px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-family: 'SF Mono', Menlo, monospace;
  font-size: 0.7rem;
  color: #64748b;
  margin: 0 2px;
}

/* ==================== TRANSITIONS ==================== */
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.28s ease; }

.modal-fade-enter-active .service-modal-container,
.modal-fade-leave-active .service-modal-container {
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.28s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }

.modal-fade-enter-from .service-modal-container,
.modal-fade-leave-to .service-modal-container {
  transform: scale(0.94) translateY(20px);
  opacity: 0;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
  .hero-content { padding: 32px 20px 28px; }
  .services-grid { grid-template-columns: 1fr; }
  .step-card { flex-direction: column; text-align: center; }
  .step-icon { align-self: center; }
  .publications-grid { grid-template-columns: 1fr; }
  .cta-buttons { flex-direction: column; align-items: center; }
  .testimonials-carousel { flex-direction: column; }
  .carousel-nav { display: none; }
  .sticky-nav-btn span { display: none; }
  .sticky-nav-btn { padding: 8px 12px; }
  .service-modal-nav { display: none; }
}

@media (max-width: 600px) {
  .service-modal-header { padding: 20px 20px 16px; flex-wrap: wrap; }
  .service-modal-body { padding: 20px; }
  .service-modal-footer { padding: 16px 20px 20px; }
  .modal-footer-actions { flex-direction: column-reverse; }
  .btn-modal-close, .btn-modal-cta { width: 100%; justify-content: center; }
  .service-modal-gallery-main { aspect-ratio: 4 / 3; }
  .service-modal-features { grid-template-columns: 1fr; }
}
</style>