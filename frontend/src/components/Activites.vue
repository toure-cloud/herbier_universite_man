<template>
    <div class="activites">
        <!-- Hero Section avec animation -->
        <section class="hero-activites">
            <div class="hero-background">
                <div class="hero-particles"></div>
            </div>
            <div class="hero-overlay"></div>
            <div class="hero-content" data-aos="fade-up">
                <div class="hero-badge">
                    <i class="fas fa-seedling"></i>
                    <span>Notre Engagement</span>
                </div>
                <h1 class="hero-title">Des actions concrètes<br>pour <span class="highlight">la biodiversité</span></h1>
                <p class="hero-subtitle">Découvrez comment nous agissons quotidiennement pour la recherche, <br>la conservation et la formation en botanique</p>
                <div class="hero-stats">
                    <div class="hero-stat" v-for="stat in heroStats" :key="stat.label">
                        <div class="stat-number">{{ stat.value }}</div>
                        <div class="stat-label">{{ stat.label }}</div>
                    </div>
                </div>
            </div>
            <div class="hero-wave">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
                    <path fill="#ffffff" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
                </svg>
            </div>
        </section>

        <!-- Section Services/Expertise -->
        <section class="expertise-section">
            <div class="container">
                <div class="section-header" data-aos="fade-up">
                    <span class="section-badge">Nos Services</span>
                    <h2 class="section-title">Domaines d'Expertise</h2>
                    <p class="section-subtitle">Des compétences scientifiques de haut niveau au service de la botanique</p>
                </div>

                <div class="services-grid">
                    <div 
                        v-for="(service, index) in services" 
                        :key="index"
                        class="service-card"
                        data-aos="fade-up"
                        :data-aos-delay="index * 100">
                        <div class="service-icon">
                            <i :class="service.icon"></i>
                        </div>
                        <h3>{{ service.title }}</h3>
                        <p>{{ service.description }}</p>
                        <ul class="service-features">
                            <li v-for="(feature, idx) in service.features" :key="idx">
                                <i class="fas fa-check-circle"></i>
                                <span>{{ feature }}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section Méthodologie -->
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
                        :data-aos-delay="index * 100">
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

        <!-- Section Impact -->
        <section class="impact-section">
            <div class="container">
                <div class="impact-content">
                    <div class="impact-text" data-aos="fade-right">
                        <span class="section-badge light">Notre Impact</span>
                        <h2>Des résultats <span class="highlight">concrets</span> et mesurables</h2>
                        <p>Depuis notre création, nous mesurons l'impact de nos actions à travers des indicateurs précis et des réalisations tangibles.</p>
                    </div>
                    <div class="impact-stats" data-aos="fade-left">
                        <div 
                            v-for="(stat, index) in impactStats" 
                            :key="index"
                            class="impact-card">
                            <div class="impact-number">
                                <span class="counter" :data-target="stat.value">{{ stat.displayValue || stat.value }}</span>
                                <span class="impact-unit">{{ stat.unit }}</span>
                            </div>
                            <div class="impact-label">{{ stat.label }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section Publications -->
        <section class="publications-section">
            <div class="container">
                <div class="section-header" data-aos="fade-up">
                    <span class="section-badge">Recherche</span>
                    <h2 class="section-title">Publications scientifiques</h2>
                    <p class="section-subtitle">Nos contributions à la science botanique</p>
                </div>

                <div class="publications-grid">
                    <div 
                        v-for="(pub, index) in publications" 
                        :key="index"
                        class="publication-card"
                        data-aos="fade-up"
                        :data-aos-delay="index * 100">
                        <div class="publication-icon">
                            <i class="fas fa-file-alt"></i>
                        </div>
                        <div class="publication-details">
                            <h3>{{ pub.title }}</h3>
                            <p class="publication-authors">{{ pub.authors }}</p>
                            <p class="publication-journal">{{ pub.journal }} • {{ pub.year }}</p>
                            <a :href="pub.link" class="publication-link" v-if="pub.link">
                                Lire l'article <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section Témoignages -->
        <section class="testimonials-section">
            <div class="container">
                <div class="section-header" data-aos="fade-up">
                    <span class="section-badge">Témoignages</span>
                    <h2 class="section-title">Ils nous font confiance</h2>
                    <p class="section-subtitle">Ce que nos partenaires disent de notre travail</p>
                </div>

                <div class="testimonials-grid">
                    <div 
                        v-for="(testimonial, index) in testimonials" 
                        :key="index"
                        class="testimonial-card"
                        data-aos="fade-up"
                        :data-aos-delay="index * 100">
                        <div class="testimonial-quote">
                            <i class="fas fa-quote-left"></i>
                            <p>{{ testimonial.text }}</p>
                        </div>
                        <div class="testimonial-author">
                            <div class="author-avatar">
                                <img :src="testimonial.avatar" :alt="testimonial.name">
                            </div>
                            <div class="author-info">
                                <h4>{{ testimonial.name }}</h4>
                                <p>{{ testimonial.position }}</p>
                                <span>{{ testimonial.organization }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section CTA -->
        <section class="cta-section">
            <div class="container">
                <div class="cta-content" data-aos="zoom-in">
                    <h2>Vous avez un projet ?</h2>
                    <p>Collaborons ensemble pour un avenir durable et la préservation de notre patrimoine végétal</p>
                    <div class="cta-buttons">
                        <router-link to="/contact" class="btn-primary">
                            Proposer un projet
                            <i class="fas fa-arrow-right"></i>
                        </router-link>
                        <a href="#" class="btn-secondary">
                            Télécharger notre brochure
                            <i class="fas fa-download"></i>
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'Activites',
    data() {
        return {
            heroStats: [
                { value: '10+', label: "Années d'expertise" },
                { value: '5000+', label: 'Spécimens étudiés' },
                { value: '150+', label: 'Espèces identifiées' },
                { value: '25+', label: 'Chercheurs' }
            ],
            services: [
                {
                    icon: "fas fa-leaf",
                    title: "Identification des plantes",
                    description: "Service expert d'identification botanique utilisant des techniques de pointe.",
                    features: [
                        "Identification morphologique et moléculaire",
                        "Base de données de référence",
                        "Expertise reconnue internationalement"
                    ]
                },
                {
                    icon: "fas fa-graduation-cap",
                    title: "Formations aux inventaires",
                    description: "Programmes de formation complets pour maîtriser l'inventaire botanique.",
                    features: [
                        "Formations pratiques sur le terrain",
                        "Modules certifiants",
                        "Suivi post-formation personnalisé"
                    ]
                },
                {
                    icon: "fas fa-chart-line",
                    title: "Inventaire floristique",
                    description: "Inventaires exhaustifs suivant les protocoles scientifiques.",
                    features: [
                        "Protocoles scientifiques validés",
                        "Équipe expérimentée",
                        "Rapports détaillés et cartographie"
                    ]
                },
                {
                    icon: "fas fa-industry",
                    title: "Études d'impact",
                    description: "Évaluations environnementales conformes aux normes.",
                    features: [
                        "Conformité aux normes internationales",
                        "Expertise pluridisciplinaire",
                        "Mesures d'atténuation proposées"
                    ]
                },
                {
                    icon: "fas fa-box",
                    title: "Réalisation d'herbier",
                    description: "Création et maintenance de collections d'herbier scientifiques.",
                    features: [
                        "Techniques de collecte et séchage",
                        "Étiquetage et classement",
                        "Conservation optimale"
                    ]
                },
                {
                    icon: "fas fa-globe-africa",
                    title: "Gestion durable",
                    description: "Stratégies pour une gestion durable des écosystèmes.",
                    features: [
                        "Conservation in situ et ex situ",
                        "Plan de gestion adapté",
                        "Suivi et évaluation"
                    ]
                }
            ],
            methodologie: [
                {
                    icon: "fas fa-clipboard-list",
                    title: "Phase préparatoire",
                    description: "Analyse des besoins, revue de littérature, définition des protocoles et préparation du travail de terrain."
                },
                {
                    icon: "fas fa-hiking",
                    title: "Travail de terrain",
                    description: "Collecte des données, échantillonnage, photographies, et relevés botaniques systématiques."
                },
                {
                    icon: "fas fa-microscope",
                    title: "Analyse en laboratoire",
                    description: "Identification des spécimens, analyses statistiques, interprétation des données collectées."
                },
                {
                    icon: "fas fa-chart-bar",
                    title: "Rapport et valorisation",
                    description: "Rédaction des rapports, cartographie, recommandations et présentation des résultats."
                }
            ],
            impactStats: [
                { value: "150", unit: "+", label: "Projets réalisés", displayValue: "150" },
                { value: "25", unit: "", label: "Chercheurs permanents", displayValue: "25" },
                { value: "50", unit: "+", label: "Publications", displayValue: "50" },
                { value: "1000", unit: "+", label: "Étudiants formés", displayValue: "1000" }
            ],
            publications: [
                {
                    title: "Diversité floristique des Montagnes de Man",
                    authors: "Kouassi J., Konan M., Yao P.",
                    journal: "Journal of Tropical Botany",
                    year: 2023,
                    link: "#"
                },
                {
                    title: "Conservation des espèces endémiques en Côte d'Ivoire",
                    authors: "Konan M., Kouassi J., Traoré A.",
                    journal: "African Biodiversity Review",
                    year: 2023,
                    link: "#"
                },
                {
                    title: "Impact du changement climatique sur la flore",
                    authors: "Yao P., Kouassi J., Konan M.",
                    journal: "Climate and Biodiversity",
                    year: 2024,
                    link: "#"
                }
            ],
            testimonials: [
                {
                    text: "Une équipe exceptionnelle qui a réalisé un inventaire botanique remarquable dans notre réserve naturelle. Leur expertise est inestimable.",
                    name: "Dr. Bernard Amani",
                    position: "Directeur",
                    organization: "Parc National de Taï",
                    avatar: "/src/images/avatar1.jpg"
                },
                {
                    text: "Collaboration exceptionnelle pour nos projets de recherche. Leur professionnalisme et leur rigueur scientifique sont remarquables.",
                    name: "Prof. Sylvie Koffi",
                    position: "Chercheuse",
                    organization: "Université Félix Houphouët-Boigny",
                    avatar: "/src/images/avatar2.jpg"
                }
            ]
        }
    },
    mounted() {
        this.initAnimations()
        this.initCounters()
    },
    methods: {
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
        initCounters() {
            const counters = document.querySelectorAll('.counter')
            counters.forEach(counter => {
                const target = parseInt(counter.dataset.target)
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

.activites {
    overflow-x: hidden;
}

/* Hero Section - Palette bleu nuit */
.hero-activites {
    position: relative;
    min-height: 600px;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    display: flex;
    align-items: center;
    text-align: center;
    color: white;
    overflow: hidden;
}

.hero-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
}

.hero-particles {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: radial-gradient(circle at 25% 40%, rgba(139, 92, 246, 0.1) 1px, transparent 1px);
    background-size: 40px 40px;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 50%, rgba(139, 92, 246, 0.08), transparent);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 900px;
    margin: 0 auto;
    padding: 120px 20px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(139, 92, 246, 0.15);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.2rem;
    border-radius: 40px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid rgba(139, 92, 246, 0.3);
    margin-bottom: 1.5rem;
}

.hero-badge i {
    color: #A78BFA;
    font-size: 0.9rem;
}

.highlight {
    color: #A78BFA;
    position: relative;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    line-height: 1.2;
    margin-bottom: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
}

.hero-stat {
    text-align: center;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 1rem 1.8rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.hero-stat .stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: bold;
    color: #A78BFA;
}

.hero-stat .stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    opacity: 0.9;
}

.hero-wave {
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    line-height: 0;
}

/* Container */
.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Section Header */
.section-header {
    text-align: center;
    margin-bottom: 3rem;
}

.section-badge {
    display: inline-block;
    background: linear-gradient(135deg, #E0E7FF, #C7D2FE);
    color: #4338CA;
    padding: 0.3rem 1rem;
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}

.section-badge.light {
    background: rgba(139, 92, 246, 0.2);
    color: #A78BFA;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #1E293B;
    margin-bottom: 0.8rem;
    font-weight: 700;
}

.section-subtitle {
    font-family: 'Inter', sans-serif;
    color: #64748B;
    font-size: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

/* Services Section */
.expertise-section {
    padding: 80px 0;
    background: #ffffff;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 2rem;
}

.service-card {
    background: #ffffff;
    border-radius: 28px;
    padding: 2rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.05);
    transition: all 0.4s cubic-bezier(0.2, 0.9, 0.4, 1.1);
    border: 1px solid #E2E8F0;
}

.service-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(79, 70, 229, 0.12);
    border-color: #C7D2FE;
}

.service-icon {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #E0E7FF, #C7D2FE);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
}

.service-icon i {
    font-size: 1.8rem;
    color: #4338CA;
}

.service-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #1E293B;
    margin-bottom: 0.75rem;
}

.service-card > p {
    font-family: 'Inter', sans-serif;
    color: #64748B;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 1.2rem;
}

.service-features {
    list-style: none;
    padding: 0;
    margin: 0;
}

.service-features li {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.4rem 0;
    font-size: 0.85rem;
    color: #475569;
}

.service-features li i {
    color: #6366F1;
    font-size: 0.8rem;
}

/* Methodologie Section */
.methodologie-section {
    padding: 80px 0;
    background: linear-gradient(135deg, #F8FAFC, #EEF2FF);
}

.methodologie-timeline {
    max-width: 900px;
    margin: 0 auto;
}

.timeline-step {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.step-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.step-number {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    z-index: 2;
}

.step-line {
    width: 2px;
    flex: 1;
    background: linear-gradient(to bottom, #4F46E5, #C7D2FE);
    margin: 0.5rem 0;
}

.step-card {
    flex: 1;
    background: white;
    border-radius: 24px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    gap: 1.2rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}

.step-card:hover {
    transform: translateX(5px);
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.1);
}

.step-icon {
    width: 48px;
    height: 48px;
    background: #EEF2FF;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.step-icon i {
    font-size: 1.4rem;
    color: #4F46E5;
}

.step-content {
    flex: 1;
}

.step-content h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #1E293B;
    margin-bottom: 0.5rem;
}

.step-content p {
    font-family: 'Inter', sans-serif;
    color: #64748B;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Impact Section */
.impact-section {
    padding: 80px 0;
    background: linear-gradient(135deg, #1E1B4B, #312E81);
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
    font-size: 2.2rem;
    margin: 1rem 0;
    line-height: 1.2;
}

.impact-text h2 .highlight {
    color: #C4B5FD;
}

.impact-text p {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    opacity: 0.9;
    line-height: 1.6;
}

.impact-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
}

.impact-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 1.8rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.15);
    transition: transform 0.3s ease;
}

.impact-card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.12);
}

.impact-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.impact-number .impact-unit {
    font-size: 1.5rem;
    color: #C4B5FD;
}

.impact-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    opacity: 0.85;
}

/* Publications Section */
.publications-section {
    padding: 80px 0;
    background: #ffffff;
}

.publications-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 1.5rem;
}

.publication-card {
    display: flex;
    gap: 1.2rem;
    background: #F8FAFC;
    border-radius: 20px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    border: 1px solid #E2E8F0;
}

.publication-card:hover {
    transform: translateX(6px);
    background: #ffffff;
    border-color: #C7D2FE;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.08);
}

.publication-icon {
    width: 48px;
    height: 48px;
    background: #EEF2FF;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.publication-icon i {
    font-size: 1.4rem;
    color: #4F46E5;
}

.publication-details h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 0.3rem;
}

.publication-authors {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #64748B;
    margin-bottom: 0.2rem;
}

.publication-journal {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: #94A3B8;
    margin-bottom: 0.5rem;
}

.publication-link {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #4F46E5;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: gap 0.3s ease;
}

.publication-link:hover {
    gap: 0.6rem;
}

/* Testimonials Section */
.testimonials-section {
    padding: 80px 0;
    background: linear-gradient(135deg, #F8FAFC, #EEF2FF);
}

.testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 2rem;
}

.testimonial-card {
    background: white;
    border-radius: 28px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}

.testimonial-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(79, 70, 229, 0.1);
}

.testimonial-quote i {
    font-size: 2rem;
    color: #4F46E5;
    opacity: 0.3;
    margin-bottom: 1rem;
    display: block;
}

.testimonial-quote p {
    font-family: 'Inter', sans-serif;
    font-style: italic;
    color: #475569;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.testimonial-author {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.author-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    overflow: hidden;
    background: #EEF2FF;
    display: flex;
    align-items: center;
    justify-content: center;
}

.author-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.author-info h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #1E293B;
    margin-bottom: 0.2rem;
}

.author-info p {
    font-size: 0.75rem;
    color: #64748B;
}

.author-info span {
    font-size: 0.7rem;
    color: #94A3B8;
}

/* CTA Section */
.cta-section {
    padding: 60px 0;
    background: #ffffff;
}

.cta-content {
    text-align: center;
    max-width: 680px;
    margin: 0 auto;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    border-radius: 40px;
    color: white;
}

.cta-content h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    margin-bottom: 0.8rem;
}

.cta-content p {
    font-family: 'Inter', sans-serif;
    margin-bottom: 1.8rem;
    opacity: 0.9;
}

.cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.btn-primary, .btn-secondary {
    padding: 0.8rem 1.8rem;
    border-radius: 50px;
    text-decoration: none;
    transition: all 0.3s ease;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.btn-primary {
    background: white;
    color: #4F46E5;
    border: none;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    gap: 0.8rem;
}

.btn-secondary {
    background: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
}

.btn-secondary:hover {
    background: rgba(255,255,255,0.3);
    transform: translateY(-3px);
}

/* Responsive */
@media (max-width: 992px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .impact-content {
        grid-template-columns: 1fr;
        text-align: center;
    }
    
    .impact-text h2 {
        font-size: 1.8rem;
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-stats {
        gap: 1rem;
    }
    
    .hero-stat {
        padding: 0.6rem 1.2rem;
    }
    
    .hero-stat .stat-number {
        font-size: 1.3rem;
    }
    
    .section-title {
        font-size: 1.8rem;
    }
    
    .services-grid {
        grid-template-columns: 1fr;
    }
    
    .methodologie-timeline {
        padding-left: 1rem;
    }
    
    .step-card {
        flex-direction: column;
        text-align: center;
    }
    
    .step-icon {
        margin: 0 auto;
    }
    
    .impact-stats {
        grid-template-columns: 1fr;
    }
    
    .publications-grid {
        grid-template-columns: 1fr;
    }
    
    .testimonials-grid {
        grid-template-columns: 1fr;
    }
    
    .cta-content {
        margin: 0 1rem;
        padding: 2rem 1rem;
    }
    
    .cta-content h2 {
        font-size: 1.5rem;
    }
    
    .cta-buttons {
        flex-direction: column;
        align-items: center;
    }
}

@media (max-width: 480px) {
    .hero-title {
        font-size: 1.6rem;
    }
    
    .hero-subtitle {
        font-size: 0.9rem;
    }
    
    .hero-stats {
        flex-direction: column;
        align-items: center;
    }
    
    .hero-stat {
        width: 80%;
    }
}
</style>
