<template>
  <div class="accueil">
    <!-- ==================== HERO SLIDESHOW ==================== -->
    <section class="hero-section">
      <div class="slideshow-container">
        <div
          class="slide"
          v-for="(slide, index) in slides"
          :key="index"
          :class="{ active: currentSlide === index }"
        >
          <img
            :src="getImageUrl(slide.image)"
            :alt="slide.titre"
            @error="handleImageError"
          />
          <div class="slide-overlay"></div>
          <div class="slide-content">
            <span class="slide-badge">{{ slide.titre }}</span>
            <h2 class="slide-title">{{ slide.titre }}</h2>
            <p class="slide-text">{{ slide.texte_botanique }}</p>
          </div>
        </div>

        <button class="nav-btn prev" @click="changeSlide(-1)" aria-label="Slide précédent">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button class="nav-btn next" @click="changeSlide(1)" aria-label="Slide suivant">
          <i class="fas fa-chevron-right"></i>
        </button>

        <div class="slide-dots">
          <button
            v-for="(slide, index) in slides"
            :key="'dot-' + index"
            :class="['dot', { active: currentSlide === index }]"
            @click="goToSlide(index)"
            :aria-label="'Aller au slide ' + (index + 1)"
          ></button>
        </div>
      </div>

      <div class="hero-scroll" @click="scrollToContent">
        <div class="scroll-mouse">
          <div class="scroll-wheel"></div>
        </div>
        <span>Découvrir</span>
      </div>
    </section>

    <!-- ==================== PRÉSIDENT ==================== -->
    <section class="president-section" id="content">
      <div class="container">
        <div class="president-grid">
          <!-- Carte Président -->
          <div class="president-card" data-aos="fade-right">
            <div class="president-image-wrapper">
              <div class="president-image">
                <img
                  src="/images/president.png"
                  alt="Président de l'Université de Man"
                  @error="handleImageError"
                />
                <div class="honor-badge">
                  <i class="fas fa-graduation-cap"></i>
                  Honoraire
                </div>
                <div class="president-social">
                  <a href="#" class="social-link" aria-label="LinkedIn">
                    <i class="fab fa-linkedin-in"></i>
                  </a>
                  <a href="#" class="social-link" aria-label="Twitter">
                    <i class="fab fa-twitter"></i>
                  </a>
                  <a href="#" class="social-link" aria-label="Google Scholar">
                    <i class="fas fa-graduation-cap"></i>
                  </a>
                </div>
              </div>
              <div class="president-info">
                <h3>Prof. Coulibaly Lacina</h3>
                <p class="president-role">Président de l'Université de Man</p>
                <div class="president-stats">
                  <div class="president-stat">
                    <span class="stat-num">15+</span>
                    <span class="stat-label">Années</span>
                  </div>
                  <div class="president-stat">
                    <span class="stat-num">50+</span>
                    <span class="stat-label">Publications</span>
                  </div>
                  <div class="president-stat">
                    <span class="stat-num">10+</span>
                    <span class="stat-label">Projets</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Message du Président -->
          <div class="message-card" data-aos="fade-left">
            <div class="message-header">
              <div class="quote-icon">
                <i class="fas fa-quote-right"></i>
              </div>
              <span class="message-badge">Mot du Président</span>
              <h2>
                Un engagement pour la préservation<br />
                de notre patrimoine botanique
              </h2>
            </div>

            <div class="message-body">
              <p>
                C'est avec une grande fierté que je présente l'Herbier de
                l'Université de Man, un projet ambitieux qui incarne notre
                engagement pour la préservation de la biodiversité végétale en
                Côte d'Ivoire.
              </p>
              <p>
                Depuis sa création, notre herbier s'est imposé comme un centre
                d'excellence dédié à l'étude, la conservation et la valorisation
                de la flore de notre belle région montagneuse. Grâce au
                dévouement de nos chercheurs et à la qualité de nos partenariats
                scientifiques, nous avons pu développer des programmes de
                recherche innovants et former une nouvelle génération de
                botanistes passionnés.
              </p>
              <p>
                Cet outil numérique que nous vous proposons aujourd'hui
                témoigne de notre volonté de partager nos connaissances et de
                rendre accessible à tous ce patrimoine scientifique unique. Je
                vous invite à découvrir la richesse de notre collection et à
                nous rejoindre dans cette aventure passionnante au service de la
                nature.
              </p>
            </div>

            <div class="message-footer">
              <div class="signature">
                <div class="signature-line"></div>
                <p class="signature-name">Prof. Coulibaly Lacina</p>
                <p class="signature-title">Président de l'Université de Man</p>
              </div>
              <div class="signature-date">
                <i class="fas fa-calendar-alt"></i>
                <span>Man, 2026</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== EXPERTISE ==================== -->
    <section class="expertise-section">
      <div class="container">
        <div class="expertise-content">
          <div class="expertise-text" data-aos="fade-right">
            <span class="section-badge">Notre Expertise</span>
            <h2>Une équipe de<br />botanistes passionnés</h2>
            <p>
              Fort d'une expérience de plus de 10 ans dans le domaine de la
              botanique tropicale, notre équipe met son savoir-faire au service
              de la connaissance et de la préservation de la flore.
            </p>

            <div class="expertise-features">
              <div class="feature">
                <i class="fas fa-check-circle"></i>
                <span>Expertise reconnue internationalement</span>
              </div>
              <div class="feature">
                <i class="fas fa-check-circle"></i>
                <span>Équipe pluridisciplinaire</span>
              </div>
              <div class="feature">
                <i class="fas fa-check-circle"></i>
                <span>Partenariats scientifiques</span>
              </div>
              <div class="feature">
                <i class="fas fa-check-circle"></i>
                <span>Approche innovante</span>
              </div>
            </div>

            <router-link to="/activites" class="btn-primary">
              Découvrir nos activités
              <i class="fas fa-arrow-right"></i>
            </router-link>
          </div>

          <div class="expertise-stats" data-aos="fade-left">
            <div class="stat-big">
              <div class="stat-number">10+</div>
              <div class="stat-label">Années d'existence</div>
            </div>
            <div class="stat-big">
              <div class="stat-number">5000+</div>
              <div class="stat-label">Spécimens</div>
            </div>
            <div class="stat-big">
              <div class="stat-number">150+</div>
              <div class="stat-label">Espèces</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== SERVICES ==================== -->
    <section class="services-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Nos Services</span>
          <h2 class="section-title">Solutions sur mesure</h2>
          <p class="section-subtitle">
            Des prestations adaptées à vos besoins spécifiques
          </p>
        </div>

        <div class="services-grid">
          <div
            class="service-card"
            v-for="(service, index) in services"
            :key="index"
            data-aos="fade-up"
            :data-aos-delay="index * 80"
          >
            <div class="service-icon">
              <i :class="service.icon"></i>
            </div>
            <h3>{{ service.titre }}</h3>
            <p>{{ service.description }}</p>
            <router-link to="/activites" class="service-link">
              En savoir plus
              <i class="fas fa-arrow-right"></i>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== ÉQUIPE ==================== -->
    <section class="team-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Notre Équipe</span>
          <h2 class="section-title">Des experts à votre service</h2>
          <p class="section-subtitle">Des chercheurs passionnés et dévoués</p>
        </div>

        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <p>Chargement de l'équipe...</p>
        </div>

        <div v-else-if="equipe.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-users"></i>
          </div>
          <p>Aucun membre de l'équipe disponible</p>
        </div>

        <div v-else class="team-grid">
          <div
            class="team-card"
            v-for="(membre, index) in equipe"
            :key="membre.id"
            data-aos="fade-up"
            :data-aos-delay="index * 80"
          >
            <div class="team-image">
              <img
                :src="getImageUrl(membre.photo || membre.image)"
                :alt="membre.nom"
                @error="handleImageError"
              />
              
            </div>
            <div class="team-info">
              <h3>{{ membre.nom }}</h3>
              <p class="team-poste">{{ membre.poste }}</p>
              <p class="team-specialite">{{ membre.specialite || '—' }}</p>
              <div class="team-contact" v-if="membre.email">
                <i class="fas fa-envelope"></i>
                <span>{{ membre.email }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== PARTENAIRES ==================== -->
    <section class="partenaires-section">
      <div class="container">
        <div class="section-header" data-aos="fade-up">
          <span class="section-badge">Partenaires</span>
          <h2 class="section-title">Ils nous accompagnent</h2>
          <p class="section-subtitle">Un réseau de collaborateurs engagés</p>
        </div>

        <div v-if="partenairesLoading" class="loading-container">
          <div class="spinner"></div>
          <p>Chargement des partenaires...</p>
        </div>

        <div v-else-if="partenaires.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-handshake"></i>
          </div>
          <p>Aucun partenaire disponible pour le moment</p>
        </div>

        <div v-else class="partenaires-grid">
          <div
            class="partenaire-card"
            v-for="(partenaire, index) in partenaires"
            :key="partenaire.id"
            data-aos="fade-up"
            :data-aos-delay="index * 80"
          >
            <div class="partenaire-logo">
              <img
                :src="getPartenaireLogo(partenaire)"
                :alt="partenaire.nom"
                @error="handleImageError"
              />
            </div>
            <div class="partenaire-info">
              <h4>{{ partenaire.nom }}</h4>
              <p>
                {{
                  partenaire.description ||
                  "Partenaire de l'Université de Man"
                }}
              </p>
              <span v-if="partenaire.type" class="partenaire-type">
                <i class="fas fa-tag"></i>
                {{ partenaire.type }}
              </span>
              <a
                v-if="partenaire.site_web"
                :href="partenaire.site_web"
                target="_blank"
                rel="noopener"
                class="partenaire-link"
              >
                Visiter le site
                <i class="fas fa-external-link-alt"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== NEWSLETTER ==================== -->
    <section class="newsletter-section">
      <div class="container">
        <div class="newsletter-content" data-aos="zoom-in">
          <div class="newsletter-icon">
            <i class="fas fa-envelope-open-text"></i>
          </div>
          <h2>Restez connectés</h2>
          <p>Recevez nos actualités et nos découvertes botaniques</p>
          <form class="newsletter-form" @submit.prevent="subscribeNewsletter">
            <input
              type="email"
              placeholder="Votre adresse email"
              required
              aria-label="Adresse email"
            />
            <button type="submit">
              S'abonner
              <i class="fas fa-paper-plane"></i>
            </button>
          </form>
        </div>
      </div>
    </section>

    <!-- ==================== CTA ==================== -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content" data-aos="fade-up">
          <div class="cta-text">
            <h2>Prêt à collaborer avec nous ?</h2>
            <p>Contactez notre équipe pour discuter de vos projets</p>
          </div>
          <router-link to="/contact" class="btn-cta">
            Nous contacter
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import config from '../config.js'

export default {
  name: 'Accueil',
  data() {
    return {
      currentSlide: 0,
      slideInterval: null,
      slides: [],
      equipe: [],
      partenaires: [],
      loading: true,
      partenairesLoading: true,
      services: [
        {
          titre: 'Identification',
          description:
            "Service expert d'identification botanique précis et fiable.",
          icon: 'fas fa-leaf'
        },
        {
          titre: 'Formation',
          description:
            'Programmes de formation sur mesure adaptés à vos besoins.',
          icon: 'fas fa-graduation-cap'
        },
        {
          titre: 'Inventaire',
          description:
            'Inventaires floristiques exhaustifs et cartographie.',
          icon: 'fas fa-chart-line'
        },
        {
          titre: "Études d'impact",
          description: 'Évaluations environnementales rigoureuses.',
          icon: 'fas fa-file-alt'
        },
        {
          titre: 'Herbier',
          description: "Création et maintenance de collections d'herbier.",
          icon: 'fas fa-box'
        },
        {
          titre: 'Conseil',
          description: 'Accompagnement personnalisé pour vos projets.',
          icon: 'fas fa-comments'
        }
      ]
    }
  },
  mounted() {
    this.fetchSlides()
    this.fetchEquipe()
    this.fetchPartenaires()
    this.startSlideShow()
    this.initAnimations()
  },
  beforeUnmount() {
    this.stopSlideShow()
  },
  methods: {
    async fetchSlides() {
      try {
        const response = await axios.get(config.API_ENDPOINTS.slides, {
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          }
        })
        if (response.data && response.data.length > 0) {
          this.slides = response.data
        } else {
          this.setDefaultSlides()
        }
      } catch (error) {
        console.error('Erreur chargement slides:', error)
        this.setDefaultSlides()
      }
    },

    setDefaultSlides() {
      this.slides = [
        {
          image: '/images/slide1.jpg',
          titre: 'La Biodiversité des Montagnes',
          texte_botanique:
            'Les montagnes de Man abritent une flore unique et diversifiée avec des espèces endémiques remarquables.'
        },
        {
          image: '/images/slide2.jpg',
          titre: 'Collection Botanique',
          texte_botanique:
            'Notre herbier conserve plus de 5000 spécimens de plantes de la région du Tonkpi.'
        },
        {
          image: '/images/slide3.jpg',
          titre: 'Recherche et Conservation',
          texte_botanique:
            'Engagés dans la préservation de la flore pour les générations futures.'
        }
      ]
    },

    async fetchEquipe() {
      this.loading = true
      try {
        const response = await axios.get(config.API_ENDPOINTS.equipe, {
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          }
        })
        this.equipe =
          response.data && response.data.length > 0 ? response.data : []
      } catch (error) {
        console.error('Erreur chargement équipe:', error)
        this.equipe = []
      } finally {
        this.loading = false
      }
    },

    async fetchPartenaires() {
      this.partenairesLoading = true
      try {
        const response = await axios.get(config.API_ENDPOINTS.partenaires, {
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
          }
        })
        if (response.data) {
          if (Array.isArray(response.data)) {
            this.partenaires = response.data
          } else if (
            response.data.results &&
            Array.isArray(response.data.results)
          ) {
            this.partenaires = response.data.results
          } else if (typeof response.data === 'object') {
            this.partenaires = [response.data]
          } else {
            this.partenaires = []
          }
        } else {
          this.partenaires = []
        }
      } catch (error) {
        console.error('Erreur chargement partenaires:', error)
        this.partenaires = []
      } finally {
        this.partenairesLoading = false
      }
    },

    getImageUrl(imagePath) {
      if (!imagePath) return ''

      // URL absolue
      if (imagePath.startsWith('http')) return imagePath

      // Media depuis l'API
      if (imagePath.startsWith('/media')) {
        const baseUrl = config.API_URL.replace(/\/api$/, '')
        return `${baseUrl}${imagePath}`
      }

      // Chemins locaux
      if (imagePath.startsWith('/images/')) return imagePath

      // Extension d'image seule
      if (imagePath.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
        return `/images/${imagePath}`
      }

      return imagePath
    },

    getPartenaireLogo(partenaire) {
      if (!partenaire) return ''
      const logoSource =
        partenaire.logo_url || partenaire.logo || partenaire.image || ''
      if (!logoSource) {
        return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f1f5f9" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="11" fill="%2394a3b8" text-anchor="middle" dy=".3em"%3ELogo%3C/text%3E%3C/svg%3E'
      }
      return this.getImageUrl(logoSource)
    },

    handleImageError(event) {
      event.target.src =
        'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"%3E%3Crect fill="%23f1f5f9" width="200" height="200"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="13" fill="%2394a3b8" text-anchor="middle" dy=".3em"%3EPas d\'image%3C/text%3E%3C/svg%3E'
      event.target.style.objectFit = 'contain'
      event.target.style.padding = '16px'
    },

    startSlideShow() {
      if (this.slides.length > 0) {
        this.slideInterval = setInterval(() => {
          this.currentSlide = (this.currentSlide + 1) % this.slides.length
        }, 5500)
      }
    },

    stopSlideShow() {
      if (this.slideInterval) {
        clearInterval(this.slideInterval)
      }
    },

    changeSlide(direction) {
      if (this.slides.length === 0) return
      this.currentSlide =
        (this.currentSlide + direction + this.slides.length) %
        this.slides.length
      this.stopSlideShow()
      this.startSlideShow()
    },

    goToSlide(index) {
      this.currentSlide = index
      this.stopSlideShow()
      this.startSlideShow()
    },

    scrollToContent() {
      const el = document.getElementById('content')
      if (el) el.scrollIntoView({ behavior: 'smooth' })
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

    subscribeNewsletter() {
      alert(
        'Merci pour votre abonnement ! Vous recevrez bientôt nos actualités.'
      )
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

/* ==================== DESIGN TOKENS ==================== */
.accueil {
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
  line-height: 1.25;
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
.hero-section {
  position: relative;
  height: 48vh;
  min-height: 360px;
  max-height: 480px;
  overflow: hidden;
}

.slideshow-container {
  position: relative;
  height: 100%;
}

.slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 1s ease-in-out;
  pointer-events: none;
}

.slide.active {
  opacity: 1;
  pointer-events: auto;
}

.slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
}

/* Overlay plus léger pour laisser voir l'image */

.slide-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(15, 39, 68, 0.15) 0%,
    rgba(26, 54, 93, 0.08) 100%
  );
}
.slide-content {
  position: absolute;
  bottom: 14%;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 560px;
  text-align: center;
  animation: slideUp 0.7s cubic-bezier(0.22, 1, 0.36, 1);
}
.slide-badge {
  display: inline-block;
  background: rgba(43, 108, 176, 0.9);
  color: white;
  padding: 4px 14px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  margin-bottom: 10px;
}

.slide-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.4rem, 3vw, 1.85rem);
  font-weight: 700;
  color: white;
  margin: 0 0 8px;
  line-height: 1.25;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
}

.slide-text {
  font-size: 0.9rem;
  color: rgba(242, 239, 239, 0.9);
  line-height: 1.5;
  max-width: 420px;
  margin: 0 auto;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}

.nav-btn:hover {
  background: var(--primary);
  border-color: var(--primary);
  transform: translateY(-50%) scale(1.06);
}

.prev {
  left: 18px;
}
.next {
  right: 18px;
}

.slide-dots {
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 10;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  border: none;
  cursor: pointer;
  padding: 0;
  transition: all var(--transition);
}

.dot.active {
  background: white;
  width: 22px;
  border-radius: 4px;
}

.hero-scroll {
  position: absolute;
  bottom: 14px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  cursor: pointer;
  z-index: 10;
  animation: bounce 2.2s infinite;
}

.scroll-mouse {
  width: 20px;
  height: 30px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  margin: 0 auto 4px;
  position: relative;
}

.scroll-wheel {
  width: 3px;
  height: 6px;
  background: white;
  border-radius: 2px;
  position: absolute;
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
  animation: scrollWheel 2s infinite;
}

@keyframes scrollWheel {
  0% {
    top: 5px;
    opacity: 1;
  }
  100% {
    top: 16px;
    opacity: 0;
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(5px);
  }
}

.hero-scroll span {
  font-size: 0.65rem;
  color: rgba(255, 255, 255, 0.85);
  letter-spacing: 0.04em;
}

/* ==================== PRÉSIDENT ==================== */
.president-section {
  padding: 56px 0 64px;
  background: white;
  position: relative;
}

.president-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--accent), var(--primary));
  background-size: 200% 100%;
  animation: gradientMove 4s ease infinite;
}

@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.president-grid {
  display: grid;
  grid-template-columns: 1fr 1.25fr;
  gap: 2.5rem;
  align-items: start;
}

.president-card {
  position: sticky;
  top: 100px;
}

.president-image-wrapper {
  background: var(--bg-page);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
  transition: all 0.35s ease;
}

.president-image-wrapper:hover {
  box-shadow: 0 20px 50px rgba(43, 108, 176, 0.12);
  border-color: rgba(43, 108, 176, 0.2);
}

.president-image {
  position: relative;
  background: linear-gradient(145deg, #1a365d 0%, #0f2744 100%);
}

.president-image img {
  width: 100%;
  height: auto;
  min-height: 260px;
  object-fit: cover;
  display: block;
  transition: transform 0.5s ease;
}

.president-card:hover .president-image img {
  transform: scale(1.03);
}

.honor-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(255, 215, 0, 0.95);
  color: #1a365d;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

.president-social {
  position: absolute;
  bottom: 14px;
  left: 14px;
  display: flex;
  gap: 8px;
}

.social-link {
  width: 34px;
  height: 34px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  font-size: 0.8rem;
  transition: all var(--transition);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.social-link:hover {
  background: var(--primary);
  color: white;
  transform: translateY(-3px);
}

.president-info {
  padding: 1.25rem 1.35rem 1.5rem;
  text-align: center;
  background: white;
}

.president-info h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px;
}

.president-info h3::after {
  content: '';
  display: block;
  width: 36px;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  margin: 8px auto 0;
  border-radius: 2px;
}

.president-role {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
  margin: 8px 0 12px;
}

.president-stats {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.president-stat {
  text-align: center;
}

.stat-num {
  display: block;
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Message */
.message-card {
  background: var(--bg-page);
  border-radius: var(--radius-xl);
  padding: 2rem;
  border: 1px solid var(--border);
  transition: all var(--transition);
}

.message-card:hover {
  border-color: rgba(43, 108, 176, 0.2);
  box-shadow: var(--shadow-md);
}

.message-header {
  margin-bottom: 1.5rem;
}

.quote-icon {
  font-size: 2.25rem;
  color: var(--primary);
  opacity: 0.12;
  margin-bottom: 8px;
}

.message-badge {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary);
  padding: 4px 14px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  margin-bottom: 12px;
}

.message-header h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.35;
  margin: 0;
}

.message-body p {
  font-size: 0.925rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0 0 12px;
}

.message-body p:last-child {
  margin-bottom: 0;
}

.message-body p::first-letter {
  font-size: 1.15em;
  font-weight: 600;
  color: var(--primary);
}

.message-footer {
  margin-top: 1.75rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 1rem;
}

.signature-line {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  margin-bottom: 10px;
  border-radius: 2px;
}

.signature-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 2px;
}

.signature-title {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin: 0;
}

.signature-date {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.signature-date i {
  color: var(--primary);
}

/* ==================== EXPERTISE ==================== */
.expertise-section {
  padding: 64px 0;
  background: var(--bg-page);
}

.expertise-content {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 3rem;
  align-items: center;
}

.expertise-text h2 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.7rem, 3vw, 2rem);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1rem;
  line-height: 1.3;
}

.expertise-text p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0 0 1.25rem;
}

.expertise-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 1.75rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.feature i {
  color: var(--primary);
  font-size: 0.95rem;
  flex-shrink: 0;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 22px;
  background: var(--primary);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-full);
  font-size: 0.9rem;
  font-weight: 500;
  transition: all var(--transition);
  box-shadow: 0 2px 8px rgba(43, 108, 176, 0.25);
}

.btn-primary:hover {
  background: var(--primary-dark);
  gap: 12px;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(43, 108, 176, 0.35);
}

.expertise-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: white;
  padding: 2rem;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
  min-width: 180px;
}

.stat-big {
  text-align: center;
}

.stat-number {
  font-family: 'Playfair Display', serif;
  font-size: 2.1rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1.1;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* ==================== SERVICES ==================== */
.services-section {
  padding: 64px 0;
  background: white;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.35rem;
}

.service-card {
  background: white;
  padding: 1.75rem 1.5rem;
  border-radius: var(--radius-xl);
  text-align: center;
  border: 1px solid var(--border);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.service-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
}

.service-icon {
  width: 56px;
  height: 56px;
  background: var(--primary-light);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.1rem;
  transition: all var(--transition);
}

.service-card:hover .service-icon {
  background: var(--primary);
}

.service-icon i {
  font-size: 1.25rem;
  color: var(--primary);
  transition: color var(--transition);
}

.service-card:hover .service-icon i {
  color: white;
}

.service-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px;
}

.service-card p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0 0 14px;
}

.service-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--primary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: gap var(--transition);
}

.service-card:hover .service-link {
  gap: 10px;
}

/* ==================== TEAM ==================== */
.team-section {
  padding: 64px 0;
  background: var(--bg-page);
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.team-card {
  background: white;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.team-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
}

.team-image {
  position: relative;
  height: 250px;
  overflow: hidden;
  background: #edf2f7;
}

.team-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.45s ease;
}

.team-card:hover .team-image img {
  transform: scale(1.06);
}

.team-overlay {
  position: absolute;
  inset: 0;
  background: rgba(43, 108, 176, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.team-card:hover .team-overlay {
  opacity: 1;
}

.team-social {
  display: flex;
  gap: 12px;
}

.team-social-link {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 0.95rem;
  transition: all var(--transition);
}

.team-social-link:hover {
  background: var(--text-primary);
  color: white;
  transform: translateY(-3px);
}

.team-info {
  padding: 1.25rem;
  text-align: center;
}

.team-info h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px;
}

.team-poste {
  font-size: 0.8rem;
  color: var(--primary);
  font-weight: 500;
  margin: 0 0 4px;
}

.team-specialite {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin: 0 0 10px;
}

.team-contact {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.team-contact i {
  color: var(--primary);
}

/* ==================== PARTENAIRES ==================== */
.partenaires-section {
  padding: 64px 0;
  background: white;
}

.partenaires-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}

.partenaire-card {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  background: var(--bg-page);
  padding: 1.15rem 1.35rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}

.partenaire-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: rgba(43, 108, 176, 0.25);
  background: white;
}

.partenaire-logo {
  width: 68px;
  height: 68px;
  flex-shrink: 0;
  background: white;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.partenaire-logo img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.partenaire-card:hover .partenaire-logo img {
  transform: scale(1.06);
}

.partenaire-info {
  flex: 1;
  min-width: 0;
}

.partenaire-info h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px;
}

.partenaire-info p {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0 0 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.partenaire-type {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.7rem;
  color: var(--primary);
  background: var(--primary-light);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  margin-bottom: 6px;
}

.partenaire-link {
  font-size: 0.75rem;
  color: var(--primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  transition: gap var(--transition);
}

.partenaire-link:hover {
  gap: 8px;
  text-decoration: underline;
}

/* ==================== LOADING / EMPTY ==================== */
.loading-container {
  text-align: center;
  padding: 3rem 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
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

.loading-container p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  background: var(--bg-page);
  border-radius: var(--radius-xl);
  border: 1px dashed var(--border);
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #edf2f7;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
  color: var(--text-muted);
}

.empty-state p {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin: 0;
}

/* ==================== NEWSLETTER ==================== */
.newsletter-section {
  padding: 64px 0;
  background: linear-gradient(145deg, #0f2744 0%, #1a365d 100%);
  color: white;
}

.newsletter-content {
  text-align: center;
  max-width: 520px;
  margin: 0 auto;
}

.newsletter-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: rgba(99, 179, 237, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
  font-size: 1.5rem;
  color: #63b3ed;
}

.newsletter-content h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 8px;
}

.newsletter-content p {
  margin: 0 0 1.5rem;
  opacity: 0.85;
  font-size: 0.95rem;
}

.newsletter-form {
  display: flex;
  gap: 10px;
  max-width: 440px;
  margin: 0 auto;
}

.newsletter-form input {
  flex: 1;
  padding: 13px 18px;
  border: none;
  border-radius: var(--radius-full);
  outline: none;
  font-size: 0.9rem;
  font-family: inherit;
}

.newsletter-form button {
  padding: 13px 22px;
  background: var(--primary);
  border: none;
  border-radius: var(--radius-full);
  color: white;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  transition: all var(--transition);
}

.newsletter-form button:hover {
  background: #3182ce;
  transform: translateY(-2px);
}

/* ==================== CTA ==================== */
.cta-section {
  padding: 48px 0 64px;
  background: white;
}

.cta-content {
  background: linear-gradient(135deg, var(--primary) 0%, #1a365d 100%);
  border-radius: 24px;
  padding: 2.5rem 2.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  box-shadow: var(--shadow-lg);
}

.cta-text h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.45rem;
  font-weight: 700;
  color: white;
  margin: 0 0 6px;
}

.cta-text p {
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  font-size: 0.95rem;
}

.btn-cta {
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

.btn-cta:hover {
  gap: 12px;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 992px) {
  .president-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .president-card {
    position: static;
  }

  .expertise-content {
    grid-template-columns: 1fr;
  }

  .expertise-stats {
    flex-direction: row;
    justify-content: space-around;
    min-width: auto;
  }
}
@keyframes slideUp {
  from {
    transform: translateX(-50%) translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
  }
}
@media (max-width: 768px) {
.hero-section {
  position: relative;
  height: 48vh;
  min-height: 340px;
  max-height: 460px;
  overflow: hidden;
}

.slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
  /* Pas de filtre sombre sur l'image elle-même */
  filter: none;
}

  .slide-content {
    bottom: 12%;
    left: 5%;
    right: 5%;
  }

  .slide-title {
    font-size: 1.25rem;
  }

  .slide-text {
    font-size: 0.9rem;
  }
.slide-content {
  bottom: 12%;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
}
  .nav-btn {
    width: 36px;
    height: 36px;
    font-size: 0.9rem;
  }

  .prev {
    left: 10px;
  }
  .next {
    right: 10px;
  }

  .president-section {
    padding: 40px 0 48px;
  }

  .message-card {
    padding: 1.5rem;
  }

  .message-header h2 {
    font-size: 1.25rem;
  }

  .expertise-features {
    grid-template-columns: 1fr;
  }

  .services-grid,
  .team-grid,
  .partenaires-grid {
    grid-template-columns: 1fr;
  }

  .partenaire-card {
    flex-direction: column;
    text-align: center;
  }

  .newsletter-form {
    flex-direction: column;
  }

  .cta-content {
    flex-direction: column;
    text-align: center;
    padding: 2rem 1.5rem;
  }
}

@media (min-width: 769px) and (max-width: 1100px) {
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .partenaires-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>