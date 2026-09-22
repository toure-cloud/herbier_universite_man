<template>
  <div class="activites">
    <!-- ==================== HERO ==================== -->
    <section class="hero-activites">
      <div class="hero-background">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
        <div class="hero-glow"></div>
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
      </div>

      <div class="hero-wave">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path fill="var(--bg-page)"
            d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z">
          </path>
        </svg>
      </div>
    </section>

    <!-- ==================== SERVICES / EXPERTISE ==================== -->
    <section class="expertise-section">
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
            :data-aos-delay="index * 80"
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
              />
              <span v-if="getServiceAllImages(service).length > 1" class="gallery-count">
                <i class="fas fa-images"></i> {{ getServiceAllImages(service).length }}
              </span>
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

            <button class="service-details-btn" type="button">
              Voir les détails
              <i class="fas fa-arrow-right"></i>
            </button>
          </article>
        </div>
      </div>
    </section>

    <!-- ==================== MÉTHODOLOGIE ==================== -->
    <section class="methodologie-section">
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
            :data-aos-delay="index * 90"
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

    <!-- ==================== IMPACT ==================== -->
    <section class="impact-section">
      <div class="container">
        <div class="impact-content">
          <div class="impact-text" data-aos="fade-right">
            <span class="section-badge light">Notre Impact</span>
            <h2>
              Des résultats
              <span class="title-accent">concrets</span>
              et mesurables
            </h2>
            <p>
              Depuis notre création, nous mesurons l'impact de nos actions à
              travers des indicateurs précis et des réalisations tangibles.
            </p>
          </div>

          <div class="impact-stats" data-aos="fade-left">
            <div v-for="(stat, index) in impactStats" :key="index" class="impact-card">
              <div class="impact-number">
                <span class="counter" :data-target="stat.value">
                  {{ stat.displayValue || stat.value }}
                </span>
                <span class="impact-unit">{{ stat.unit }}</span>
              </div>
              <div class="impact-label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== PUBLICATIONS ==================== -->
    <section class="publications-section">
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
            :data-aos-delay="index * 80"
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

    <!-- ==================== TÉMOIGNAGES ==================== -->
    <section class="testimonials-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Témoignages</span>
          <h2 class="section-title">Ils nous font confiance</h2>
          <p class="section-subtitle">Ce que nos partenaires disent de notre travail</p>
        </div>

        <div class="testimonials-grid">
          <article
            v-for="(testimonial, index) in testimonials"
            :key="index"
            class="testimonial-card"
            data-aos="fade-up"
            :data-aos-delay="index * 80"
          >
            <div class="testimonial-quote">
              <i class="fas fa-quote-left"></i>
              <p>{{ testimonial.text }}</p>
            </div>
            <div class="testimonial-author">
              <div class="author-avatar">
                <img :src="getAvatarUrl(testimonial.avatar)" :alt="testimonial.name" @error="handleAvatarError" />
              </div>
              <div class="author-info">
                <h4>{{ testimonial.name }}</h4>
                <p>{{ testimonial.position }}</p>
                <span>{{ testimonial.organization }}</span>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ==================== CTA ==================== -->
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

    <!-- ==================== MODALE DÉTAIL SERVICE ==================== -->
    <transition name="service-modal-fade">
      <div v-if="selectedService" class="service-modal" @click.self="closeService">
        <div class="service-modal-container">
          <button class="service-modal-close" @click="closeService" aria-label="Fermer">
            <i class="fas fa-times"></i>
          </button>

          <div class="service-modal-header">
            <div class="service-modal-icon">
              <i :class="selectedService.icon"></i>
            </div>
            <div class="service-modal-header-text">
              <span v-if="selectedService.titre_court" class="service-modal-kicker">
                {{ selectedService.titre_court }}
              </span>
              <h2>{{ selectedService.title }}</h2>
            </div>
          </div>

          <div class="service-modal-body">
            <div v-if="allServiceImages.length" class="service-modal-gallery">
              <div class="service-modal-gallery-main">
                <img
                  :src="getImageUrl(currentServiceImage)"
                  :alt="selectedService.title"
                  @error="handleImageError"
                />
              </div>
              <div v-if="allServiceImages.length > 1" class="service-modal-gallery-thumbs">
                <img
                  v-for="(img, i) in allServiceImages"
                  :key="i"
                  :src="getImageUrl(img)"
                  :class="{ active: i === currentServiceImageIndex }"
                  @click="currentServiceImageIndex = i"
                  @error="handleImageError"
                  :alt="`Image ${i + 1}`"
                />
              </div>
            </div>

            <p v-if="selectedService.caption" class="service-modal-caption">
              {{ selectedService.caption }}
            </p>

            <p class="service-modal-description">
              {{ selectedService.descriptionLongue || selectedService.description }}
            </p>

            <div v-if="selectedService.features && selectedService.features.length" class="service-modal-features">
              <h3>Points forts</h3>
              <ul>
                <li v-for="(feature, idx) in selectedService.features" :key="idx">
                  <i class="fas fa-check-circle"></i>
                  <span>{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="service-modal-footer">
            <button class="btn-modal-close" @click="closeService">Fermer</button>
            <router-link to="/contact" class="btn-modal-cta">
              Demander ce service <i class="fas fa-arrow-right"></i>
            </router-link>
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
      impactStats: [],
      publications: [],
      testimonials: [],
      selectedService: null,
      currentServiceImageIndex: 0,
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
  },
  mounted() {
    this.initAnimations()
    this.loadActivitesData()
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

        this.impactStats = (data.statistiques || []).map(s => ({
          value: s.valeur || '0',
          displayValue: s.valeur || '0',
          unit: s.unite || '',
          label: s.titre || ''
        }))
        if (this.impactStats.length === 0) this.impactStats = this.getDefaultImpactStats()

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
        this.impactStats = this.getDefaultImpactStats()
        this.publications = this.getDefaultPublications()
        this.testimonials = this.getDefaultTestimonials()
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.initAnimations()
          this.initCounters()
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

    openService(service) {
      this.selectedService = service
      this.currentServiceImageIndex = 0
      document.body.style.overflow = 'hidden'
    },

    closeService() {
      this.selectedService = null
      this.currentServiceImageIndex = 0
      document.body.style.overflow = ''
    },

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

    getDefaultImpactStats() {
      return [
        { value: '150', displayValue: '150', unit: '+', label: 'Projets réalisés' },
        { value: '25', displayValue: '25', unit: '', label: 'Chercheurs permanents' },
        { value: '50', displayValue: '50', unit: '+', label: 'Publications' },
        { value: '1000', displayValue: '1000', unit: '+', label: 'Étudiants formés' }
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
    },

    initCounters() {
      const counters = document.querySelectorAll('.counter')
      counters.forEach(counter => {
        const target = parseInt(counter.dataset.target)
        if (!target || isNaN(target)) return
        let current = 0
        const increment = target / 50
        const updateCounter = () => {
          if (current < target) {
            current += increment
            counter.textContent = Math.ceil(current)
            setTimeout(updateCounter, 30)
          } else {
            counter.textContent = target
          }
        }
        updateCounter()
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

/* ==================== HERO ==================== */
.hero-activites {
  position: relative;
  min-height: 520px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  background: linear-gradient(145deg, #0f2744 0%, #1a365d 45%, #1e3a5f 100%);
}

.hero-background { position: absolute; inset: 0; }

.hero-gradient {
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

.hero-glow {
  position: absolute;
  width: 480px;
  height: 480px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(66, 153, 225, 0.12), transparent 70%);
  top: -100px;
  right: -60px;
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 880px;
  margin: 0 auto;
  padding: 100px 24px 80px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  padding: 8px 18px;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 1.5rem;
}

.hero-badge i { color: #63b3ed; }

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.2rem, 4.5vw, 3.2rem);
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 1.15rem;
  letter-spacing: -0.02em;
}

.title-accent {
  background: linear-gradient(135deg, #63b3ed, #90cdf4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.1rem;
  line-height: 1.65;
  opacity: 0.9;
  margin: 0 0 2.5rem;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.hero-stat {
  text-align: center;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(10px);
  padding: 14px 22px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 140px;
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 1.7rem;
  font-weight: 700;
  color: #90cdf4;
  line-height: 1.1;
}

.stat-label {
  font-size: 0.8rem;
  opacity: 0.8;
  font-weight: 500;
  margin-top: 4px;
}

.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  line-height: 0;
}

.hero-wave svg { display: block; width: 100%; height: 70px; }

/* ==================== SERVICES ==================== */
.expertise-section { padding: 64px 0; background: white; }

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
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.service-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
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
  transition: transform 0.4s ease;
}

.service-card:hover .service-image img { transform: scale(1.05); }

.gallery-count {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  display: inline-flex;
  align-items: center;
  gap: 4px;
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

.service-card:hover .service-icon { background: var(--primary); }

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
  color: var(--primary);
  font-size: 0.85rem;
  margin-top: 2px;
  flex-shrink: 0;
}

.service-details-btn {
  margin-top: 14px;
  background: none;
  border: none;
  color: var(--primary);
  font-weight: 500;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  cursor: pointer;
  transition: gap 0.25s ease;
}

.service-card:hover .service-details-btn { gap: 12px; }

/* ==================== MÉTHODOLOGIE ==================== */
.methodologie-section { padding: 64px 0; background: var(--bg-page); }

.methodologie-timeline { max-width: 860px; margin: 0 auto; }

.timeline-step {
  display: flex;
  gap: 1.35rem;
  margin-bottom: 1.25rem;
}

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

/* ==================== IMPACT ==================== */
.impact-section {
  padding: 72px 0;
  background: linear-gradient(145deg, #0f2744 0%, #1a365d 100%);
  color: white;
}

.impact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.impact-text h2 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.7rem, 3vw, 2.15rem);
  font-weight: 700;
  margin: 12px 0 14px;
  line-height: 1.25;
}

.impact-text p { font-size: 1rem; opacity: 0.9; line-height: 1.65; margin: 0; }

.impact-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.impact-card {
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 1.6rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all var(--transition);
}

.impact-card:hover { transform: translateY(-4px); background: rgba(255, 255, 255, 0.12); }

.impact-number {
  font-family: 'Playfair Display', serif;
  font-size: 2.3rem;
  font-weight: 700;
  margin-bottom: 6px;
  line-height: 1.1;
}

.impact-unit { font-size: 1.4rem; color: #90cdf4; }

.impact-label { font-size: 0.875rem; opacity: 0.85; }

/* ==================== PUBLICATIONS ==================== */
.publications-section { padding: 64px 0; background: white; }

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

.publication-card:hover { transform: translateX(5px); background: white; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }

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

/* ==================== TÉMOIGNAGES ==================== */
.testimonials-section { padding: 64px 0; background: var(--bg-page); }

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 1.5rem;
}

.testimonial-card {
  background: white;
  border-radius: 20px;
  padding: 1.75rem;
  border: 1px solid var(--border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.testimonial-card:hover { transform: translateY(-5px); box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08); }

.testimonial-quote i {
  font-size: 1.75rem;
  color: var(--primary);
  opacity: 0.2;
  margin-bottom: 12px;
  display: block;
}

.testimonial-quote p {
  font-size: 0.95rem;
  font-style: italic;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0 0 1.35rem;
}

.testimonial-author { display: flex; align-items: center; gap: 14px; }

.author-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--primary-light);
  flex-shrink: 0;
}

.author-avatar img { width: 100%; height: 100%; object-fit: cover; }

.author-info h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 2px;
}

.author-info p { font-size: 0.8rem; color: var(--text-secondary); margin: 0; }
.author-info span { font-size: 0.75rem; color: var(--text-muted); }

/* ==================== CTA ==================== */
.cta-section { padding: 48px 0 64px; background: white; }

.cta-content {
  text-align: center;
  max-width: 680px;
  margin: 0 auto;
  padding: 2.75rem 2.25rem;
  background: linear-gradient(135deg, var(--primary) 0%, #1a365d 100%);
  border-radius: 28px;
  color: white;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
}

.cta-content h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.85rem;
  font-weight: 700;
  margin: 0 0 10px;
}

.cta-content p { font-size: 1rem; opacity: 0.9; margin: 0 0 1.75rem; line-height: 1.55; }

.cta-buttons { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

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

/* ==================== MODALE ==================== */
.service-modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 20px;
}

.service-modal-container {
  background: #fff;
  border-radius: 24px;
  max-width: 760px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
}

.service-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  color: #64748b;
  cursor: pointer;
  font-size: 0.95rem;
  z-index: 2;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.service-modal-close:hover {
  background: rgba(239, 68, 68, 0.9);
  color: #fff;
  transform: rotate(90deg);
}

.service-modal-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 28px 20px;
  border-bottom: 1px solid #e2e8f0;
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

.service-modal-body { padding: 24px 28px; }

.service-modal-gallery { margin-bottom: 20px; }

.service-modal-gallery-main {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: 14px;
  overflow: hidden;
  background: #f1f5f9;
}

.service-modal-gallery-main img { width: 100%; height: 100%; object-fit: cover; }

.service-modal-gallery-thumbs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  gap: 8px;
  margin-top: 10px;
}

.service-modal-gallery-thumbs img {
  aspect-ratio: 1;
  border-radius: 10px;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.service-modal-gallery-thumbs img.active { border-color: #2b6cb0; }

.service-modal-caption {
  font-size: 0.8rem;
  color: #94a3b8;
  font-style: italic;
  text-align: center;
  margin: 0 0 16px;
}

.service-modal-description {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.7;
  margin: 0 0 20px;
  white-space: pre-line;
}

.service-modal-features {
  background: #f8fafc;
  border-radius: 14px;
  padding: 18px 20px;
}

.service-modal-features h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 10px;
}

.service-modal-features ul { list-style: none; padding: 0; margin: 0; }

.service-modal-features li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 6px 0;
  font-size: 0.88rem;
  color: #4a5568;
}

.service-modal-features li i {
  color: #38a169;
  font-size: 0.85rem;
  margin-top: 3px;
  flex-shrink: 0;
}

.service-modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 28px 24px;
  border-top: 1px solid #e2e8f0;
}

.btn-modal-close {
  padding: 10px 20px;
  border-radius: 9999px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #4a5568;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-modal-close:hover { background: #f8fafc; }

.btn-modal-cta {
  padding: 10px 22px;
  border-radius: 9999px;
  background: #2b6cb0;
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-modal-cta:hover { background: #1a4f8a; gap: 12px; }

/* ==================== TRANSITIONS ==================== */
.service-modal-fade-enter-active,
.service-modal-fade-leave-active { transition: opacity 0.25s ease; }

.service-modal-fade-enter-active .service-modal-container,
.service-modal-fade-leave-active .service-modal-container {
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.service-modal-fade-enter-from,
.service-modal-fade-leave-to { opacity: 0; }

.service-modal-fade-enter-from .service-modal-container,
.service-modal-fade-leave-to .service-modal-container {
  transform: scale(0.94) translateY(10px);
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 992px) {
  .impact-content { grid-template-columns: 1fr; text-align: center; }
}

@media (max-width: 768px) {
  .hero-content { padding: 80px 20px 60px; }
  .services-grid { grid-template-columns: 1fr; }
  .step-card { flex-direction: column; text-align: center; }
  .impact-stats { grid-template-columns: 1fr; }
  .publications-grid, .testimonials-grid { grid-template-columns: 1fr; }
  .cta-buttons { flex-direction: column; align-items: center; }
}

@media (max-width: 600px) {
  .service-modal-header { padding: 20px 20px 16px; }
  .service-modal-body { padding: 20px; }
  .service-modal-footer {
    flex-direction: column-reverse;
    padding: 16px 20px 20px;
  }
  .btn-modal-close, .btn-modal-cta {
    width: 100%;
    justify-content: center;
  }
}
</style>