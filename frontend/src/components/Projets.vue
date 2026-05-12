<template>
    <div class="projets">
        <!-- Hero Section -->
        <section class="hero-projets">
            <div class="hero-bg"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="hero-badge" data-aos="fade-down">
                    <i class="fas fa-project-diagram"></i>
                    <span>Nos Projets</span>
                </div>
                <h1 class="hero-title" data-aos="fade-up">
                    Des initiatives qui<br>façonnent l'avenir
                </h1>
                <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="200">
                    Découvrez nos projets de recherche, conservation et développement<br>
                    engagés pour la préservation de la biodiversité
                </p>
                <div class="hero-stats" data-aos="fade-up" data-aos-delay="400">
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
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
                    <path fill="#ffffff" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
                </svg>
            </div>
        </section>

        <!-- Filtres -->
        <section class="filters-section">
            <div class="container">
                <div class="filters-wrapper" data-aos="fade-up">
                    <div class="filter-buttons">
                        <button 
                            v-for="filter in filters" 
                            :key="filter.value"
                            :class="['filter-btn', { active: activeFilter === filter.value }]"
                            @click="setFilter(filter.value)">
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
                            @input="filterProjects">
                    </div>
                </div>
            </div>
        </section>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Chargement des projets...</p>
            </div>
        </div>

        <!-- Projets Grid -->
        <section v-else-if="filteredProjects.length > 0" class="projets-grid-section">
            <div class="container">
                <div class="projets-grid">
                    <div 
                        v-for="(projet, index) in paginatedProjects" 
                        :key="projet.id"
                        class="projet-card"
                        :class="{ 'featured': projet.featured }"
                        data-aos="fade-up"
                        :data-aos-delay="(index % 3) * 100">
                        <div class="projet-image">
                            <img :src="getImageUrl(projet.image)" :alt="projet.titre">
                            <div class="projet-category">{{ getCategorieLabel(projet.categorie) }}</div>
                            <div class="projet-status" :class="getStatusClass(projet.statut)">
                                <i :class="getStatusIcon(projet.statut)"></i>
                                {{ getStatusLabel(projet.statut) }}
                            </div>
                            <div class="projet-overlay">
                                <div class="overlay-buttons">
                                    <button class="overlay-btn" @click="openGallery(projet)">
                                        <i class="fas fa-images"></i>
                                    </button>
                                    <button class="overlay-btn" @click="openDetails(projet)">
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
                                <div class="meta-item">
                                    <i class="fas fa-map-marker-alt"></i>
                                    <span>{{ projet.lieu }}</span>
                                </div>
                                <div class="meta-item">
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
                                    <div class="progress-fill" :style="{ width: projet.progression + '%' }"></div>
                                </div>
                            </div>
                            <div class="projet-actions">
                                <button class="btn-details" @click="openDetails(projet)">
                                    En savoir plus
                                    <i class="fas fa-arrow-right"></i>
                                </button>
                                <div class="projet-tags">
                                    <span v-for="tag in getTagList(projet.tags).slice(0, 2)" :key="tag" class="tag">{{ tag }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Pagination -->
                <div class="pagination" v-if="totalPages > 1">
                    <button class="page-btn" :disabled="currentPage === 1" @click="currentPage--">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button 
                        v-for="page in displayedPages" 
                        :key="page"
                        :class="['page-btn', { active: currentPage === page }]"
                        @click="currentPage = page">
                        {{ page }}
                    </button>
                    <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </section>

        <!-- Projet en vedette -->
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
                            <p class="featured-description">{{ featuredProject.description_longue || featuredProject.description }}</p>
                            <div class="featured-stats">
                                <div class="featured-stat" v-if="featuredProject.duree">
                                    <i class="fas fa-calendar-check"></i>
                                    <span>Durée: {{ featuredProject.duree }}</span>
                                </div>
                                <div class="featured-stat" v-if="featuredProject.budget">
                                    <i class="fas fa-hand-holding-heart"></i>
                                    <span>Budget: {{ featuredProject.budget }}</span>
                                </div>
                                <div class="featured-stat" v-if="featuredProject.impact">
                                    <i class="fas fa-globe-africa"></i>
                                    <span>Impact: {{ featuredProject.impact }}</span>
                                </div>
                            </div>
                            <button class="btn-featured" @click="openDetails(featuredProject)">
                                Découvrir le projet
                                <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                        <div class="featured-image">
                            <img :src="getImageUrl(featuredProject.image)" :alt="featuredProject.titre">
                            <div class="image-caption">{{ featuredProject.caption || 'Projet phare de l\'herbier' }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Timeline des projets -->
        <section class="timeline-section" v-if="timelineProjects.length > 0 && !loading">
            <div class="container">
                <div class="section-header" data-aos="fade-up">
                    <span class="section-badge">Notre Histoire</span>
                    <h2 class="section-title">Projets par année</h2>
                    <p class="section-subtitle">Découvrez l'évolution de nos actions</p>
                </div>
                <div class="timeline">
                    <div class="timeline-item" v-for="(item, index) in timelineProjects" :key="item.annee" data-aos="fade-up" :data-aos-delay="index * 100">
                        <div class="timeline-year">
                            <div class="year-circle">{{ item.annee }}</div>
                            <div class="year-line"></div>
                        </div>
                        <div class="timeline-projects">
                            <div class="timeline-project" v-for="projet in item.projets" :key="projet.titre">
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

        <!-- Aucun résultat -->
        <section v-else-if="!loading && filteredProjects.length === 0" class="no-results-section">
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

        <!-- Call to Action -->
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

        <!-- Modal Détails Projet -->
        <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
            <div class="modal-container">
                <button class="modal-close" @click="closeModal">
                    <i class="fas fa-times"></i>
                </button>
                <div class="modal-content" v-if="selectedProjet">
                    <div class="modal-image">
                        <img :src="getImageUrl(selectedProjet.image)" :alt="selectedProjet.titre">
                        <div class="modal-badge" :class="getStatusClass(selectedProjet.statut)">
                            {{ getStatusLabel(selectedProjet.statut) }}
                        </div>
                    </div>
                    <div class="modal-info">
                        <h2 class="modal-title">{{ selectedProjet.titre }}</h2>
                        <div class="modal-meta">
                            <span><i class="fas fa-calendar"></i> {{ selectedProjet.annee }}</span>
                            <span><i class="fas fa-map-marker-alt"></i> {{ selectedProjet.lieu }}</span>
                            <span><i class="fas fa-tag"></i> {{ getCategorieLabel(selectedProjet.categorie) }}</span>
                        </div>
                        
                        <div class="modal-section" v-if="selectedProjet.description_longue">
                            <h4><i class="fas fa-align-left"></i> Description</h4>
                            <p>{{ selectedProjet.description_longue }}</p>
                        </div>
                        <div class="modal-section" v-else-if="selectedProjet.description">
                            <h4><i class="fas fa-align-left"></i> Description</h4>
                            <p>{{ selectedProjet.description }}</p>
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
                            <button class="btn-primary" v-if="selectedProjet.lien_rapport">
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

const API_URL = 'http://localhost:8000/api'

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
                'termine': 'Terminé',
                'encours': 'En cours',
                'planifie': 'Planifié'
            },
            categorieLabels: {
                'recherche': 'Recherche',
                'conservation': 'Conservation',
                'formation': 'Formation',
                'developpement': 'Développement',
                'autre': 'Autre'
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
                filtered = filtered.filter(p => 
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
            const end = start + this.itemsPerPage
            return this.filteredProjects.slice(start, end)
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
            
            for (let i = start; i <= end; i++) {
                pages.push(i)
            }
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
                    timeline[annee] = {
                        annee: annee,
                        projets: []
                    }
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
                const benef = parseInt(p.beneficiaires) || 0
                return sum + benef
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
                const response = await axios.get(`${API_URL}/projets/`)
                this.projets = response.data
                this.loading = false
            } catch (error) {
                console.error('Erreur lors du chargement des projets:', error)
                this.loading = false
            }
        },
        
        getImageUrl(imagePath) {
            if (!imagePath) return '/src/images/placeholder-project.jpg'
            if (imagePath.startsWith('http')) return imagePath
            if (imagePath.startsWith('/media')) return `http://localhost:8000${imagePath}`
            return imagePath
        },
        
        getCategorieLabel(categorie) {
            return this.categorieLabels[categorie] || categorie
        },
        
        getStatusLabel(statut) {
            return this.statutLabels[statut] || statut
        },
        
        getStatusClass(statut) {
            const classes = {
                'termine': 'termine',
                'encours': 'encours',
                'planifie': 'planifie'
            }
            return classes[statut] || ''
        },
        
        getStatusIcon(statut) {
            const icons = {
                'termine': 'fas fa-check-circle',
                'encours': 'fas fa-spinner fa-pulse',
                'planifie': 'fas fa-clock'
            }
            return icons[statut] || 'fas fa-circle'
        },
        
        getTagList(tags) {
            if (!tags) return []
            return tags.split(',').map(tag => tag.trim())
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
            alert('Fonctionnalité de partage à venir')
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

.projets {
    overflow-x: hidden;
}

/* Hero Section */
.hero-projets {
    position: relative;
    min-height: 500px;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    display: flex;
    align-items: center;
    text-align: center;
    color: white;
    padding: 100px 0 150px;
    overflow: hidden;
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: radial-gradient(circle at 25% 40%, rgba(139, 92, 246, 0.08) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.5;
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
    padding: 0 20px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(139, 92, 246, 0.15);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid rgba(139, 92, 246, 0.3);
    margin-bottom: 1.5rem;
}

.hero-badge i {
    color: #A78BFA;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    line-height: 1.2;
    margin: 1.5rem 0;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 3rem;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 0.8rem 1.5rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: bold;
    color: #A78BFA;
}

.stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    opacity: 0.8;
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

/* Filters */
.filters-section {
    padding: 40px 0;
    background: white;
    border-bottom: 1px solid #E2E8F0;
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
    gap: 0.8rem;
    flex-wrap: wrap;
}

.filter-btn {
    padding: 0.6rem 1.2rem;
    background: #F1F5F9;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.filter-btn:hover {
    background: #E2E8F0;
    transform: translateY(-2px);
}

.filter-btn.active {
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    color: white;
}

.filter-count {
    background: rgba(0,0,0,0.1);
    padding: 0.2rem 0.5rem;
    border-radius: 20px;
    font-size: 0.7rem;
}

.filter-search {
    position: relative;
}

.filter-search i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #94A3B8;
}

.filter-search input {
    padding: 0.7rem 1rem 0.7rem 2.5rem;
    border: 1px solid #E2E8F0;
    border-radius: 50px;
    width: 260px;
    outline: none;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
}

.filter-search input:focus {
    border-color: #4F46E5;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

/* Loading */
.loading-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
}

.loading-spinner {
    text-align: center;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 3px solid #E2E8F0;
    border-top-color: #4F46E5;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Projets Grid */
.projets-grid-section {
    padding: 60px 0;
    background: #F8FAFC;
}

.projets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 2rem;
}

.projet-card {
    background: white;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    transition: all 0.4s cubic-bezier(0.2, 0.9, 0.4, 1.1);
    position: relative;
}

.projet-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(79, 70, 229, 0.12);
}

.projet-card.featured {
    border: 2px solid #A78BFA;
}

.projet-card.featured::before {
    content: '⭐ Projet phare';
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: linear-gradient(135deg, #A78BFA, #7C3AED);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: bold;
    z-index: 2;
}

.projet-image {
    position: relative;
    height: 220px;
    overflow: hidden;
    background: #F1F5F9;
}

.projet-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.projet-card:hover .projet-image img {
    transform: scale(1.05);
}

.projet-category {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(5px);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    z-index: 2;
}

.projet-status {
    position: absolute;
    bottom: 1rem;
    left: 1rem;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.projet-status.termine {
    background: #10B981;
    color: white;
}

.projet-status.encours {
    background: #F59E0B;
    color: white;
}

.projet-status.planifie {
    background: #3B82F6;
    color: white;
}

.projet-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(79, 70, 229, 0.85);
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
    gap: 1rem;
}

.overlay-btn {
    width: 45px;
    height: 45px;
    background: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1.1rem;
}

.overlay-btn:hover {
    background: #4F46E5;
    color: white;
    transform: scale(1.1);
}

.projet-info {
    padding: 1.5rem;
}

.projet-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 0.8rem;
}

.projet-header h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #1E293B;
    margin: 0;
}

.projet-annee {
    font-size: 0.75rem;
    color: #64748B;
}

.projet-info p {
    font-family: 'Inter', sans-serif;
    color: #475569;
    line-height: 1.5;
    margin-bottom: 1rem;
    font-size: 0.85rem;
}

.projet-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.75rem;
    color: #64748B;
}

.meta-item i {
    color: #4F46E5;
}

.projet-progress {
    margin-bottom: 1rem;
}

.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: #64748B;
    margin-bottom: 0.3rem;
}

.progress-bar {
    height: 6px;
    background: #E2E8F0;
    border-radius: 3px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4F46E5, #A78BFA);
    border-radius: 3px;
    transition: width 1s ease;
}

.projet-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

.btn-details {
    background: none;
    border: none;
    color: #4F46E5;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Inter', sans-serif;
    transition: gap 0.3s ease;
}

.btn-details:hover {
    gap: 0.8rem;
}

.projet-tags {
    display: flex;
    gap: 0.5rem;
}

.tag {
    font-size: 0.65rem;
    padding: 0.2rem 0.5rem;
    background: #F1F5F9;
    border-radius: 20px;
    color: #475569;
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 3rem;
}

.page-btn {
    width: 40px;
    height: 40px;
    border: 1px solid #E2E8F0;
    background: white;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
}

.page-btn:hover:not(:disabled) {
    background: #4F46E5;
    color: white;
    border-color: #4F46E5;
}

.page-btn.active {
    background: #4F46E5;
    color: white;
    border-color: #4F46E5;
}

.page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Featured Section */
.featured-section {
    padding: 60px 0;
    background: linear-gradient(135deg, #F8FAFC, #EEF2FF);
}

.featured-wrapper {
    background: white;
    border-radius: 32px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    position: relative;
}

.featured-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: linear-gradient(135deg, #A78BFA, #7C3AED);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-weight: 500;
    font-size: 0.8rem;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.featured-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: center;
}

.featured-text {
    padding: 3rem;
}

.featured-text h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1E293B;
    margin-bottom: 1rem;
}

.featured-description {
    font-family: 'Inter', sans-serif;
    color: #475569;
    line-height: 1.7;
    margin-bottom: 2rem;
}

.featured-stats {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    margin-bottom: 2rem;
}

.featured-stat {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    color: #475569;
    font-size: 0.9rem;
}

.featured-stat i {
    color: #4F46E5;
    width: 20px;
}

.btn-featured {
    padding: 0.8rem 1.8rem;
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    color: white;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-featured:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(79, 70, 229, 0.3);
    gap: 0.8rem;
}

.featured-image {
    position: relative;
    height: 400px;
}

.featured-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.image-caption {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    color: white;
    padding: 1rem;
    text-align: center;
    font-size: 0.8rem;
}

/* Timeline Section */
.timeline-section {
    padding: 60px 0;
    background: white;
}

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
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1E293B;
    margin-bottom: 0.8rem;
}

.section-subtitle {
    font-family: 'Inter', sans-serif;
    color: #64748B;
}

.timeline {
    max-width: 800px;
    margin: 0 auto;
}

.timeline-item {
    display: flex;
    gap: 2rem;
    margin-bottom: 2rem;
}

.timeline-year {
    text-align: center;
    min-width: 100px;
}

.year-circle {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    margin: 0 auto 0.5rem;
}

.year-line {
    width: 2px;
    height: 100%;
    background: linear-gradient(to bottom, #4F46E5, #C7D2FE);
    margin: 0 auto;
}

.timeline-projects {
    flex: 1;
    padding-bottom: 2rem;
}

.timeline-project {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    padding: 1rem;
    background: #F8FAFC;
    border-radius: 16px;
    transition: all 0.3s ease;
}

.timeline-project:hover {
    transform: translateX(5px);
    background: #EEF2FF;
}

.timeline-dot {
    width: 10px;
    height: 10px;
    background: #4F46E5;
    border-radius: 50%;
    margin-top: 0.5rem;
}

.timeline-content h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #1E293B;
    margin-bottom: 0.3rem;
}

.timeline-content p {
    font-family: 'Inter', sans-serif;
    color: #64748B;
    font-size: 0.8rem;
}

/* No Results */
.no-results-section {
    padding: 80px 0;
    background: #F8FAFC;
}

.no-results-card {
    text-align: center;
    background: white;
    border-radius: 32px;
    padding: 4rem;
    max-width: 500px;
    margin: 0 auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.no-results-icon {
    font-size: 4rem;
    color: #94A3B8;
    margin-bottom: 1rem;
}

.no-results-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #1E293B;
    margin-bottom: 0.5rem;
}

.no-results-card p {
    font-family: 'Inter', sans-serif;
    color: #64748B;
    margin-bottom: 1.5rem;
}

.btn-reset {
    padding: 0.8rem 1.5rem;
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    color: white;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
}

.btn-reset:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.3);
}

/* CTA Section */
.cta-projets {
    padding: 60px 0;
    background: linear-gradient(135deg, #1E1B4B, #312E81);
    color: white;
}

.cta-content {
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}

.cta-content h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.cta-content p {
    font-family: 'Inter', sans-serif;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.cta-buttons .btn-primary {
    background: white;
    color: #4F46E5;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
}

.cta-buttons .btn-primary:hover {
    transform: translateY(-3px);
    gap: 0.8rem;
}

.cta-buttons .btn-secondary {
    background: rgba(255,255,255,0.2);
    color: white;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
}

.cta-buttons .btn-secondary:hover {
    background: rgba(255,255,255,0.3);
    transform: translateY(-3px);
}

/* Modal */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.modal.active {
    opacity: 1;
    visibility: visible;
}

.modal-container {
    background: white;
    border-radius: 32px;
    max-width: 1000px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
}

.modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 40px;
    height: 40px;
    background: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    z-index: 10;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: #EF4444;
    color: white;
    transform: scale(1.1);
}

.modal-content {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 2rem;
    padding: 2rem;
}

.modal-image {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
}

.modal-image img {
    width: 100%;
    border-radius: 20px;
}

.modal-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
}

.modal-badge.termine {
    background: #10B981;
    color: white;
}

.modal-badge.encours {
    background: #F59E0B;
    color: white;
}

.modal-badge.planifie {
    background: #3B82F6;
    color: white;
}

.modal-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #1E293B;
    margin-bottom: 1rem;
}

.modal-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    color: #64748B;
    font-size: 0.85rem;
}

.modal-meta i {
    color: #4F46E5;
    margin-right: 0.3rem;
}

.modal-section {
    margin-bottom: 1.5rem;
}

.modal-section h4 {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #1E293B;
    margin-bottom: 0.5rem;
}

.modal-section h4 i {
    color: #4F46E5;
    margin-right: 0.5rem;
}

.modal-section p {
    font-family: 'Inter', sans-serif;
    color: #475569;
    line-height: 1.6;
}

.modal-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: #F8FAFC;
    border-radius: 20px;
}

.modal-stat {
    text-align: center;
}

.stat-title {
    font-size: 0.7rem;
    color: #64748B;
    margin-bottom: 0.3rem;
}

.stat-value {
    font-size: 1.2rem;
    font-weight: bold;
    color: #4F46E5;
}

.modal-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.modal-actions .btn-primary {
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

.modal-actions .btn-outline {
    background: transparent;
    color: #4F46E5;
    border: 1px solid #4F46E5;
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

/* Responsive */
@media (max-width: 992px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .featured-content {
        grid-template-columns: 1fr;
    }
    
    .featured-text {
        padding: 2rem;
        order: 2;
    }
    
    .featured-image {
        height: 300px;
        order: 1;
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-stats {
        gap: 1rem;
    }
    
    .stat-item {
        padding: 0.5rem 1rem;
    }
    
    .stat-number {
        font-size: 1.3rem;
    }
    
    .filters-wrapper {
        flex-direction: column;
    }
    
    .filter-buttons {
        justify-content: center;
    }
    
    .projets-grid {
        grid-template-columns: 1fr;
    }
    
    .timeline-item {
        flex-direction: column;
    }
    
    .timeline-year {
        margin-bottom: 1rem;
    }
    
    .year-line {
        display: none;
    }
    
    .modal-content {
        grid-template-columns: 1fr;
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
    
    .stat-item {
        width: 80%;
    }
}
</style>
