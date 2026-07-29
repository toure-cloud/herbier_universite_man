<template>
    <div class="accueil">
        <!-- ============================================ -->
        <!-- HERO SECTION AVEC SLIDESHOW - HAUTEUR RÉDUITE -->
        <!-- ============================================ -->
        <section class="hero-section">
            <div class="slideshow-container">
                <div class="slide fade" v-for="(slide, index) in slides" :key="index" v-show="currentSlide === index">
                    <img :src="getImageUrl(slide.image)" :alt="slide.titre" @error="handleImageError">
                    <div class="slide-overlay"></div>
                    <div class="slide-content">
                        <div class="slide-badge">{{ slide.titre }}</div>
                        <h2 class="slide-title">{{ slide.titre }}</h2>
                        <p class="slide-text">{{ slide.texte_botanique }}</p>
                    </div>
                </div>
                <button class="prev" @click="changeSlide(-1)">❮</button>
                <button class="next" @click="changeSlide(1)">❯</button>
            </div>
            <div class="hero-scroll">
                <div class="scroll-mouse">
                    <div class="scroll-wheel"></div>
                </div>
                <span>Découvrir</span>
            </div>
        </section>

        <!-- ============================================ -->
        <!-- SECTION PRÉSIDENT ET MESSAGE DE BIENVENUE     -->
        <!-- ============================================ -->
        <section class="president-section">
            <div class="container">
                <div class="president-grid">
                    <div class="president-card" data-aos="fade-right">
                        <div class="president-image-wrapper">
                            <div class="president-image">
                                <img src="/images/president.png" alt="Président de l'Université de Man" @error="handleImageError">
                                <div class="president-social">
                                    <a href="#" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                                    <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                                    <a href="#" class="social-link"><i class="fab fa-google-scholar"></i></a>
                                </div>
                            </div>
                            <div class="president-name">
                                <h3>Prof. Coulibaly Lacina</h3>
                                <p>Président de l'Université de Man</p>
                                <div class="president-stats">
                                    <div class="president-stat">
                                        <span class="stat-num">15+</span>
                                        <span class="stat-label">Années d'expérience</span>
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
                    
                    <div class="message-card" data-aos="fade-left">
                        <div class="message-header">
                            <div class="quote-icon">
                                <i class="fas fa-quote-right"></i>
                            </div>
                            <span class="message-badge">Mot du Président</span>
                            <h2>Un engagement pour la préservation<br>de notre patrimoine botanique</h2>
                        </div>
                        <div class="message-body">
                            <p class="message-text">
                                C'est avec une grande fierté que je présente l'Herbier de l'Université de Man, 
                                un projet ambitieux qui incarne notre engagement pour la préservation de la biodiversité 
                                végétale en Côte d'Ivoire.
                            </p>
                            <p class="message-text">
                                Depuis sa création, notre herbier s'est imposé comme un centre d'excellence dédié 
                                à l'étude, la conservation et la valorisation de la flore de notre belle région montagneuse. 
                                Grâce au dévouement de nos chercheurs et à la qualité de nos partenariats scientifiques, 
                                nous avons pu développer des programmes de recherche innovants et former une nouvelle 
                                génération de botanistes passionnés.
                            </p>
                            <p class="message-text">
                                Cet outil numérique que nous vous proposons aujourd'hui témoigne de notre volonté 
                                de partager nos connaissances et de rendre accessible à tous ce patrimoine scientifique 
                                unique. Je vous invite à découvrir la richesse de notre collection et à nous rejoindre 
                                dans cette aventure passionnante au service de la nature.
                            </p>
                        </div>
                        <div class="message-footer">
                            <div class="signature">
                                <div class="signature-line"></div>
                                <p class="signature-text">Prof. Coulibaly Lacina</p>
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

        <!-- ============================================ -->
        <!-- SECTION EXPERTISE                            -->
        <!-- ============================================ -->
        <section class="expertise-section">
            <div class="container">
                <div class="expertise-content">
                    <div class="expertise-text" data-aos="fade-right">
                        <span class="section-badge">Notre Expertise</span>
                        <h2>Une équipe de<br>botanistes passionnés</h2>
                        <p>Fort d'une expérience de plus de 10 ans dans le domaine de la botanique tropicale, notre équipe met son savoir-faire au service de la connaissance et de la préservation de la flore.</p>
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
                            <div class="stat-number-count">10+</div>
                            <div class="stat-label">Années d'existence</div>
                        </div>
                        <div class="stat-big">
                            <div class="stat-number-count">5000+</div>
                            <div class="stat-label">Spécimens</div>
                        </div>
                        <div class="stat-big">
                            <div class="stat-number-count">150+</div>
                            <div class="stat-label">Espèces</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================ -->
        <!-- SECTION SERVICES                             -->
        <!-- ============================================ -->
        <section class="services-section">
            <div class="container">
                <div class="section-header" data-aos="fade-up">
                    <span class="section-badge">Nos Services</span>
                    <h2 class="section-title">Solutions sur mesure</h2>
                    <p class="section-subtitle">Des prestations adaptées à vos besoins spécifiques</p>
                </div>
                <div class="services-grid">
                    <div class="service-card" v-for="(service, index) in services" :key="index" data-aos="fade-up" :data-aos-delay="index * 100">
                        <div class="service-icon">
                            <i :class="service.icon"></i>
                        </div>
                        <h3>{{ service.titre }}</h3>
                        <p>{{ service.description }}</p>
                        <div class="service-hover">
                            <router-link to="/activites" class="service-link">
                                En savoir plus
                                <i class="fas fa-arrow-right"></i>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================ -->
        <!-- SECTION ÉQUIPE (DYNAMIQUE - BASE DE DONNÉES) -->
        <!-- ============================================ -->
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
                    <i class="fas fa-users" style="font-size: 40px; color: #ccc;"></i>
                    <p>Aucun membre de l'équipe disponible</p>
                </div>
                
                <div v-else class="team-grid">
                    <div class="team-card" v-for="(membre, index) in equipe" :key="membre.id" data-aos="fade-up" :data-aos-delay="index * 100">
                        <div class="team-image">
                            <img :src="getImageUrl(membre.photo || membre.image)" :alt="membre.nom" @error="handleImageError">
                            <div class="team-overlay">
                                <div class="team-social">
                                    <a v-if="membre.email" :href="'mailto:' + membre.email" class="team-social-link"><i class="fas fa-envelope"></i></a>
                                    <a href="#" class="team-social-link"><i class="fab fa-linkedin-in"></i></a>
                                    <a href="#" class="team-social-link"><i class="fab fa-twitter"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="team-info">
                            <h3>{{ membre.nom }}</h3>
                            <p class="team-poste">{{ membre.poste }}</p>
                            <p class="team-specialite">{{ membre.specialite || '-' }}</p>
                            <div class="team-contact" v-if="membre.email">
                                <i class="fas fa-envelope"></i>
                                <span>{{ membre.email }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================ -->
        <!-- SECTION PARTENAIRES (DYNAMIQUE - BD)         -->
        <!-- ============================================ -->
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
                    <i class="fas fa-handshake" style="font-size: 48px; color: #ccc;"></i>
                    <p style="margin-top: 1rem; color: #94a3b8;">Aucun partenaire disponible pour le moment</p>
                </div>
                
                <div v-else class="partenaires-grid">
                    <div class="partenaire-card" 
                         v-for="(partenaire, index) in partenaires" 
                         :key="partenaire.id" 
                         data-aos="fade-up" 
                         :data-aos-delay="index * 100">
                        
                        <div class="partenaire-logo">
                            <img 
                                :src="getPartenaireLogo(partenaire)" 
                                :alt="partenaire.nom" 
                                @error="handleImageError"
                            >
                        </div>
                        
                        <div class="partenaire-info">
                            <h4>{{ partenaire.nom }}</h4>
                            <p>{{ partenaire.description || 'Partenaire de l\'Université de Man' }}</p>
                            <span v-if="partenaire.type" class="partenaire-type">
                                <i class="fas fa-tag"></i>
                                {{ partenaire.type }}
                            </span>
                            <a v-if="partenaire.site_web" 
                               :href="partenaire.site_web" 
                               target="_blank" 
                               class="partenaire-link">
                                Visiter le site 
                                <i class="fas fa-external-link-alt"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================ -->
        <!-- SECTION NEWSLETTER                          -->
        <!-- ============================================ -->
        <section class="newsletter-section">
            <div class="container">
                <div class="newsletter-content" data-aos="zoom-in">
                    <div class="newsletter-icon">
                        <i class="fas fa-envelope-open-text"></i>
                    </div>
                    <h2>Restez connectés</h2>
                    <p>Recevez nos actualités et nos découvertes botaniques</p>
                    <form class="newsletter-form" @submit.prevent="subscribeNewsletter">
                        <input type="email" placeholder="Votre adresse email" required>
                        <button type="submit">
                            S'abonner
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </form>
                </div>
            </div>
        </section>

        <!-- ============================================ -->
        <!-- SECTION CTA                                 -->
        <!-- ============================================ -->
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
            // ✅ URL de l'API avec variable d'environnement
            apiUrl: import.meta.env.VITE_API_URL || 'https://herbier-backend.onrender.com/api',
            services: [
                {
                    titre: "Identification",
                    description: "Service expert d'identification botanique précis et fiable.",
                    icon: "fas fa-leaf"
                },
                {
                    titre: "Formation",
                    description: "Programmes de formation sur mesure adaptés à vos besoins.",
                    icon: "fas fa-graduation-cap"
                },
                {
                    titre: "Inventaire",
                    description: "Inventaires floristiques exhaustifs et cartographie.",
                    icon: "fas fa-chart-line"
                },
                {
                    titre: "Études d'impact",
                    description: "Évaluations environnementales rigoureuses.",
                    icon: "fas fa-file-alt"
                },
                {
                    titre: "Herbier",
                    description: "Création et maintenance de collections d'herbier.",
                    icon: "fas fa-box"
                },
                {
                    titre: "Conseil",
                    description: "Accompagnement personnalisé pour vos projets.",
                    icon: "fas fa-comments"
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
        // ============================================
        // CHARGEMENT DES DONNÉES DEPUIS LA BASE
        // ============================================
        
        async fetchSlides() {
            try {
                console.log('📡 Chargement des slides depuis:', `${this.apiUrl}/slides/`)
                const response = await axios.get(`${this.apiUrl}/slides/`, {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                console.log('📊 Slides reçus:', response.data)
                
                if (response.data && response.data.length > 0) {
                    this.slides = response.data
                } else {
                    this.setDefaultSlides()
                }
            } catch (error) {
                console.error('❌ Erreur chargement slides:', error)
                this.setDefaultSlides()
            }
        },
        
        setDefaultSlides() {
            this.slides = [
                { 
                    image: "/images/slide1.jpg", 
                    titre: "La Biodiversité des Montagnes", 
                    texte_botanique: "Les montagnes de Man abritent une flore unique et diversifiée avec des espèces endémiques remarquables." 
                },
                { 
                    image: "/images/slide2.jpg", 
                    titre: "Collection Botanique", 
                    texte_botanique: "Notre herbier conserve plus de 5000 spécimens de plantes de la région du Tonkpi." 
                },
                { 
                    image: "/images/slide3.jpg", 
                    titre: "Recherche et Conservation", 
                    texte_botanique: "Engagés dans la préservation de la flore pour les générations futures." 
                }
            ]
        },
        
        async fetchEquipe() {
            this.loading = true
            try {
                console.log('📡 Chargement de l\'équipe depuis:', `${this.apiUrl}/equipe/`)
                const response = await axios.get(`${this.apiUrl}/equipe/`, {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                console.log('📊 Équipe reçue:', response.data)
                
                if (response.data && response.data.length > 0) {
                    this.equipe = response.data
                } else {
                    this.equipe = []
                }
            } catch (error) {
                console.error('❌ Erreur chargement équipe:', error)
                this.equipe = []
            } finally {
                this.loading = false
            }
        },
        
        async fetchPartenaires() {
            this.partenairesLoading = true
            try {
                console.log('📡 Chargement des partenaires depuis:', `${this.apiUrl}/partenaires/`)
                const response = await axios.get(`${this.apiUrl}/partenaires/`, {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                console.log('📊 Partenaires reçus:', response.data)
                
                if (response.data) {
                    if (Array.isArray(response.data)) {
                        this.partenaires = response.data
                    } else if (response.data.results && Array.isArray(response.data.results)) {
                        this.partenaires = response.data.results
                    } else if (typeof response.data === 'object') {
                        this.partenaires = [response.data]
                    }
                } else {
                    this.partenaires = []
                }
            } catch (error) {
                console.error('❌ Erreur chargement partenaires:', error)
                this.partenaires = []
            } finally {
                this.partenairesLoading = false
            }
        },
        
        // ============================================
        // GESTION DES IMAGES
        // ============================================
        
        getImageUrl(imagePath) {
            if (!imagePath) return ''
            
            if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
                return imagePath
            }
            
            if (imagePath.startsWith('/media/')) {
                return `${this.apiUrl}${imagePath}`
            }
            
            if (imagePath.startsWith('/images/')) {
                return imagePath
            }
            
            if (imagePath.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
                return `/images/${imagePath}`
            }
            
            return imagePath
        },
        
        getPartenaireLogo(partenaire) {
            if (!partenaire) return ''
            
            const logoSource = partenaire.logo_url || partenaire.logo || partenaire.image || ''
            
            if (!logoSource) {
                return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f0f0f0" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="12" fill="%23999" text-anchor="middle" dy=".3em"%3E%3C/text%3E%3C/svg%3E'
            }
            
            return this.getImageUrl(logoSource)
        },
        
        handleImageError(event) {
            event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"%3E%3Crect fill="%23f0f0f0" width="200" height="200"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="14" fill="%23999" text-anchor="middle" dy=".3em"%3EPas d\'image%3C/text%3E%3C/svg%3E'
            event.target.style.objectFit = 'contain'
            event.target.style.padding = '20px'
        },
        
        // ============================================
        // SLIDESHOW
        // ============================================
        
        startSlideShow() {
            if (this.slides.length > 0) {
                this.slideInterval = setInterval(() => {
                    this.currentSlide = (this.currentSlide + 1) % this.slides.length
                }, 5000)
            }
        },
        
        stopSlideShow() {
            if (this.slideInterval) {
                clearInterval(this.slideInterval)
            }
        },
        
        changeSlide(direction) {
            if (this.slides.length === 0) return
            this.currentSlide = (this.currentSlide + direction + this.slides.length) % this.slides.length
            this.stopSlideShow()
            this.startSlideShow()
        },
        
        // ============================================
        // ANIMATIONS
        // ============================================
        
        initAnimations() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1'
                        entry.target.style.transform = 'translateY(0)'
                    }
                })
            }, { threshold: 0.1 })
            
            document.querySelectorAll('[data-aos]').forEach(el => {
                el.style.opacity = '0'
                el.style.transform = 'translateY(30px)'
                el.style.transition = 'all 0.6s ease-out'
                observer.observe(el)
            })
        },
        
        subscribeNewsletter() {
            alert("Merci pour votre abonnement ! Vous recevrez bientôt nos actualités.")
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ============================================ */
/* RESET & BASE                                 */
/* ============================================ */
.accueil {
    overflow-x: hidden;
}

.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}

/* ============================================ */
/* SECTION BADGE                                */
/* ============================================ */
.section-badge {
    display: inline-block;
    background: #eef2ff;
    color: #3498db;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 1px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    font-family: 'Inter', sans-serif;
    color: #64748b;
    font-size: 0.95rem;
}

.section-header {
    text-align: center;
    margin-bottom: 2.5rem;
}

/* ============================================ */
/* HERO SECTION - HAUTEUR RÉDUITE              */
/* ============================================ */
.hero-section {
    position: relative;
    height: 45vh;
    min-height: 350px;
    max-height: 450px;
    overflow: hidden;
}

.slideshow-container {
    position: relative;
    height: 100%;
}

.slide {
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 1s ease-in-out;
}

.slide.fade {
    opacity: 1;
}

.slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 30%;
}

.slide-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(26,42,58,0.6) 0%, rgba(44,62,80,0.4) 100%);
}

.slide-content {
    position: absolute;
    bottom: 10%;
    left: 8%;
    right: 8%;
    max-width: 550px;
    animation: slideUp 0.8s ease-out;
}

.slide-badge {
    display: inline-block;
    background: rgba(52,152,219,0.9);
    color: white;
    padding: 0.2rem 0.8rem;
    border-radius: 20px;
    font-size: 0.6rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
}

.slide-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.3rem;
    line-height: 1.2;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.slide-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.9);
    line-height: 1.4;
    max-width: 400px;
}

@keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.prev, .next {
    cursor: pointer;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    padding: 10px;
    color: white;
    font-weight: bold;
    font-size: 14px;
    background: rgba(0,0,0,0.4);
    border: none;
    border-radius: 50%;
    width: 35px;
    height: 35px;
    transition: all 0.3s ease;
    z-index: 10;
}

.prev:hover, .next:hover {
    background: #3498db;
    transform: translateY(-50%) scale(1.05);
}

.prev { left: 15px; }
.next { right: 15px; }

.hero-scroll {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    cursor: pointer;
    animation: bounce 2s infinite;
    z-index: 10;
}

.scroll-mouse {
    width: 18px;
    height: 26px;
    border: 2px solid white;
    border-radius: 20px;
    margin: 0 auto 3px;
    position: relative;
}

.scroll-wheel {
    width: 3px;
    height: 5px;
    background: white;
    border-radius: 2px;
    position: absolute;
    top: 4px;
    left: 50%;
    transform: translateX(-50%);
    animation: scroll 2s infinite;
}

@keyframes scroll {
    0% { top: 4px; opacity: 1; }
    100% { top: 16px; opacity: 0; }
}

@keyframes bounce {
    0%, 100% { transform: translateX(-50%) translateY(0); }
    50% { transform: translateX(-50%) translateY(4px); }
}

.hero-scroll span {
    font-size: 0.55rem;
    color: white;
    opacity: 0.8;
}

/* ============================================ */
/* PRESIDENT SECTION                            */
/* ============================================ */
.president-section {
    padding: 30px 0 60px 0;
    background: white;
    position: relative;
}

.president-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3498db, #2ecc71, #3498db);
    background-size: 200% 100%;
    animation: gradientMove 3s ease infinite;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.president-grid {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 2.5rem;
    align-items: start;
}

.president-card {
    position: sticky;
    top: 100px;
    transition: transform 0.3s ease;
}

.president-card:hover {
    transform: translateY(-5px);
}

.president-image-wrapper {
    background: #f8fafc;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.12);
    border: 1px solid rgba(52,152,219,0.1);
    transition: all 0.3s ease;
}

.president-image-wrapper:hover {
    box-shadow: 0 30px 80px rgba(52,152,219,0.15);
    border-color: rgba(52,152,219,0.3);
}

.president-image {
    position: relative;
    background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%);
}

.president-image img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.5s ease;
    min-height: 250px;
    object-fit: cover;
}

.president-card:hover .president-image img {
    transform: scale(1.02);
}

.president-image::after {
    content: '🎓 Honoraire';
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(255,215,0,0.9);
    color: #1a472a;
    padding: 0.2rem 0.8rem;
    border-radius: 30px;
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(255,215,0,0.3);
}

.president-social {
    position: absolute;
    bottom: 15px;
    left: 15px;
    display: flex;
    gap: 8px;
}

.social-link {
    width: 32px;
    height: 32px;
    background: rgba(255,255,255,0.95);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2c3e50;
    font-size: 0.8rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

.social-link:hover {
    background: #3498db;
    color: white;
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(52,152,219,0.3);
}

.president-name {
    padding: 1rem 1rem;
    text-align: center;
    background: white;
}

.president-name h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #1e293b;
    margin-bottom: 0.2rem;
}

.president-name h3::after {
    content: '';
    display: block;
    width: 35px;
    height: 2px;
    background: linear-gradient(90deg, #3498db, #2ecc71);
    margin: 0.4rem auto;
    border-radius: 2px;
}

.president-name > p {
    font-size: 0.75rem;
    color: #64748b;
    margin-bottom: 0.6rem;
    font-weight: 500;
}

.president-stats {
    display: flex;
    justify-content: center;
    gap: 1.2rem;
    padding-top: 0.6rem;
    border-top: 1px solid #e2e8f0;
}

.president-stat {
    text-align: center;
}

.stat-num {
    display: block;
    font-size: 1rem;
    font-weight: 700;
    color: #3498db;
    font-family: 'Playfair Display', serif;
}

.stat-label {
    font-size: 0.6rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.message-card {
    background: #f8fafc;
    border-radius: 20px;
    padding: 1.8rem;
    border: 1px solid #eef2f6;
    transition: all 0.3s ease;
}

.message-card:hover {
    border-color: rgba(52,152,219,0.2);
    box-shadow: 0 10px 40px rgba(0,0,0,0.05);
}

.message-header {
    margin-bottom: 1.5rem;
}

.quote-icon {
    font-size: 2.5rem;
    color: #3498db;
    opacity: 0.15;
    margin-bottom: 0.5rem;
}

.message-badge {
    display: inline-block;
    background: #eef2ff;
    color: #3498db;
    padding: 0.3rem 1.2rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 1px;
}

.message-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #1e293b;
    line-height: 1.3;
}

.message-text {
    font-family: 'Inter', sans-serif;
    color: #475569;
    line-height: 1.7;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
}

.message-text:last-child {
    margin-bottom: 0;
}

.message-text::first-letter {
    font-size: 1.2em;
    font-weight: 600;
    color: #3498db;
}

.message-footer {
    margin-top: 1.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 1rem;
}

.signature-line {
    width: 40px;
    height: 2px;
    background: linear-gradient(90deg, #3498db, #2ecc71);
    margin-bottom: 0.8rem;
    border-radius: 2px;
}

.signature-text {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.2rem;
}

.signature-title {
    font-size: 0.7rem;
    color: #64748b;
}

.signature-date {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #94a3b8;
    font-size: 0.75rem;
}

.signature-date i {
    color: #3498db;
}

/* ============================================ */
/* EXPERTISE SECTION                            */
/* ============================================ */
.expertise-section {
    padding: 60px 0;
    background: #f8fafc;
}

.expertise-content {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 3rem;
    align-items: center;
}

.expertise-text h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1e293b;
    margin-bottom: 1.2rem;
    line-height: 1.3;
}

.expertise-text p {
    font-family: 'Inter', sans-serif;
    color: #475569;
    line-height: 1.6;
    margin-bottom: 1.2rem;
}

.expertise-features {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}

.feature {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #334155;
    font-size: 0.85rem;
}

.feature i {
    color: #3498db;
    font-size: 0.9rem;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.5rem;
    background: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 40px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background: #2980b9;
    gap: 0.8rem;
    transform: translateY(-2px);
}

.expertise-stats {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    background: white;
    padding: 1.8rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.stat-big {
    text-align: center;
}

.stat-number-count {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: bold;
    color: #3498db;
}

.stat-label {
    font-size: 0.8rem;
    color: #64748b;
}

/* ============================================ */
/* SERVICES SECTION                             */
/* ============================================ */
.services-section {
    padding: 60px 0;
    background: white;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
}

.service-card {
    background: white;
    padding: 1.5rem;
    border-radius: 20px;
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid #e2e8f0;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 30px -12px rgba(0,0,0,0.1);
    border-color: #3498db;
}

.service-icon {
    width: 55px;
    height: 55px;
    background: #eef2ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
}

.service-icon i {
    font-size: 1.3rem;
    color: #3498db;
}

.service-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.service-card p {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.service-link {
    color: #3498db;
    text-decoration: none;
    font-size: 0.8rem;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}

.service-card:hover .service-link {
    gap: 0.5rem;
}

/* ============================================ */
/* TEAM SECTION                                 */
/* ============================================ */
.team-section {
    padding: 60px 0;
    background: #f8fafc;
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
}

.team-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.team-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 30px -12px rgba(0,0,0,0.1);
}

.team-image {
    position: relative;
    height: 260px;
    overflow: hidden;
}

.team-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.team-card:hover .team-image img {
    transform: scale(1.05);
}

.team-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(52,152,219,0.8);
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
    gap: 1rem;
}

.team-social-link {
    width: 36px;
    height: 36px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3498db;
    transition: all 0.3s ease;
}

.team-social-link:hover {
    background: #2c3e50;
    color: white;
    transform: translateY(-3px);
}

.team-info {
    padding: 1.2rem;
    text-align: center;
}

.team-info h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #1e293b;
    margin-bottom: 0.2rem;
}

.team-poste {
    font-size: 0.75rem;
    color: #3498db;
    font-weight: 500;
    margin-bottom: 0.3rem;
}

.team-specialite {
    font-size: 0.7rem;
    color: #64748b;
    margin-bottom: 0.8rem;
}

.team-contact {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.3rem;
    font-size: 0.7rem;
    color: #94a3b8;
}

.team-contact i {
    color: #3498db;
}

/* ============================================ */
/* PARTENAIRES SECTION                          */
/* ============================================ */
.partenaires-section {
    padding: 60px 0;
    background: #ffffff;
}

.partenaires-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
}

.partenaire-card {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: #f8fafc;
    padding: 1.2rem 1.5rem;
    border-radius: 16px;
    transition: all 0.3s ease;
    border: 1px solid #eef2f6;
}

.partenaire-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    border-color: #3498db;
    background: #ffffff;
}

.partenaire-logo {
    width: 70px;
    height: 70px;
    flex-shrink: 0;
    background: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.6rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    overflow: hidden;
}

.partenaire-logo img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transition: transform 0.3s ease;
}

.partenaire-card:hover .partenaire-logo img {
    transform: scale(1.05);
}

.partenaire-info {
    flex: 1;
    min-width: 0;
}

.partenaire-info h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: #1e293b;
    margin-bottom: 0.2rem;
    font-weight: 700;
}

.partenaire-info p {
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 0.3rem;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.partenaire-type {
    display: inline-block;
    font-size: 0.65rem;
    color: #3498db;
    background: #eef2ff;
    padding: 0.15rem 0.7rem;
    border-radius: 12px;
    margin-bottom: 0.3rem;
}

.partenaire-type i {
    font-size: 0.5rem;
    margin-right: 0.2rem;
}

.partenaire-link {
    font-size: 0.7rem;
    color: #3498db;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.partenaire-link:hover {
    color: #2980b9;
    gap: 0.5rem;
    text-decoration: underline;
}

/* ============================================ */
/* LOADING & EMPTY STATE                       */
/* ============================================ */
.loading-container {
    text-align: center;
    padding: 3rem 1rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    background: #f8fafc;
    border-radius: 16px;
}

.empty-state i {
    display: block;
    margin-bottom: 0.5rem;
}

.empty-state p {
    color: #94a3b8;
    font-size: 0.95rem;
}

.spinner {
    width: 35px;
    height: 35px;
    border: 3px solid #e2e8f0;
    border-top-color: #3498db;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ============================================ */
/* NEWSLETTER SECTION                           */
/* ============================================ */
.newsletter-section {
    padding: 60px 0;
    background: linear-gradient(135deg, #1e293b 0%, #2c3e50 100%);
    color: white;
}

.newsletter-content {
    text-align: center;
    max-width: 550px;
    margin: 0 auto;
}

.newsletter-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #3498db;
}

.newsletter-content h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}

.newsletter-content p {
    margin-bottom: 1.5rem;
    opacity: 0.8;
}

.newsletter-form {
    display: flex;
    gap: 1rem;
    max-width: 450px;
    margin: 0 auto;
}

.newsletter-form input {
    flex: 1;
    padding: 0.8rem 1rem;
    border: none;
    border-radius: 50px;
    outline: none;
    font-size: 0.9rem;
}

.newsletter-form button {
    padding: 0.8rem 1.5rem;
    background: #3498db;
    border: none;
    border-radius: 50px;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
}

.newsletter-form button:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

/* ============================================ */
/* CTA SECTION                                  */
/* ============================================ */
.cta-section {
    padding: 50px 0;
    background: white;
}

.cta-content {
    background: linear-gradient(135deg, #3498db, #2c3e50);
    border-radius: 24px;
    padding: 2.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.5rem;
}

.cta-text h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: white;
    margin-bottom: 0.3rem;
}

.cta-text p {
    color: rgba(255,255,255,0.8);
}

.btn-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.5rem;
    background: white;
    color: #3498db;
    text-decoration: none;
    border-radius: 40px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-cta:hover {
    gap: 0.8rem;
    transform: translateY(-2px);
}

/* ============================================ */
/* RESPONSIVE                                   */
/* ============================================ */
@media (max-width: 992px) {
    .president-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .president-card {
        position: static;
    }
    
    .president-image img {
        min-height: 220px;
    }
}

@media (max-width: 768px) {
    .hero-section {
        height: 35vh;
        min-height: 280px;
        max-height: 350px;
    }
    
    .slide-title {
        font-size: 1.2rem;
    }
    
    .slide-text {
        font-size: 0.7rem;
    }
    
    .slide-content {
        bottom: 8%;
        left: 5%;
        right: 5%;
    }
    
    .prev, .next {
        width: 28px;
        height: 28px;
        font-size: 10px;
        padding: 6px;
    }
    
    .president-section {
        padding: 20px 0 40px 0;
    }
    
    .president-image img {
        min-height: 180px;
    }
    
    .president-name h3 {
        font-size: 1rem;
    }
    
    .message-card {
        padding: 1.2rem;
    }
    
    .message-header h2 {
        font-size: 1.2rem;
    }
    
    .expertise-content {
        grid-template-columns: 1fr;
    }
    
    .expertise-stats {
        flex-direction: row;
        justify-content: center;
    }
    
    .services-grid {
        grid-template-columns: 1fr;
    }
    
    .team-grid {
        grid-template-columns: 1fr;
    }
    
    .partenaires-grid {
        grid-template-columns: 1fr;
    }
    
    .partenaire-card {
        flex-direction: column;
        text-align: center;
    }
    
    .partenaire-logo {
        width: 80px;
        height: 80px;
    }
    
    .newsletter-form {
        flex-direction: column;
    }
    
    .cta-content {
        flex-direction: column;
        text-align: center;
    }
    
    .expertise-features {
        grid-template-columns: 1fr;
    }
}

@media (min-width: 769px) and (max-width: 1024px) {
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