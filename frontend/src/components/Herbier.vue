<template>
    <div class="herbier">
        <!-- Hero Section -->
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
                <h1 class="hero-title" data-aos="fade-up">
                    L'Herbier Numérique
                </h1>
                <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="200">
                    Explorez notre collection de <span class="highlight">{{ totalPlants }}+ spécimens</span> <br>
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
                        <div class="stat-label">Espèces protégées</div>
                    </div>
                </div>
            </div>
            <div class="hero-wave">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
                    <path fill="#ffffff" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
                </svg>
            </div>
        </section>

        <!-- Barre de Recherche Avancée -->
        <section class="search-section">
            <div class="container">
                <div class="search-card" data-aos="fade-up">
                    <div class="search-header">
                        <i class="fas fa-search"></i>
                        <h3>Recherche avancée</h3>
                        <button class="toggle-filters" @click="showAdvancedFilters = !showAdvancedFilters">
                            <i :class="showAdvancedFilters ? 'fas fa-chevron-up' : 'fas fa-sliders-h'"></i>
                            {{ showAdvancedFilters ? 'Masquer' : 'Filtres avancés' }}
                        </button>
                    </div>
                    
                    <div class="search-main">
                        <div class="search-input-wrapper">
                            <i class="fas fa-search"></i>
                            <input 
                                type="text" 
                                v-model="searchQuery" 
                                @input="debouncedSearch"
                                placeholder="Rechercher par nom, famille, genre, description, habitat..."
                                class="search-input"
                            >
                            <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        
                        <div class="search-filters">
                            <div class="filter-group">
                                <label>
                                    <i class="fas fa-tag"></i>
                                    Famille
                                </label>
                                <select v-model="selectedFamily" @change="filterPlants" class="filter-select">
                                    <option value="">Toutes les familles</option>
                                    <option v-for="family in familiesList" :key="family" :value="family">
                                        {{ family }}
                                    </option>
                                </select>
                            </div>
                            
                            <div class="filter-group">
                                <label>
                                    <i class="fas fa-leaf"></i>
                                    Statut de conservation
                                </label>
                                <select v-model="selectedConservation" @change="filterPlants" class="filter-select">
                                    <option value="">Tous</option>
                                    <option value="En danger critique">En danger critique</option>
                                    <option value="En danger">En danger</option>
                                    <option value="Vulnérable">Vulnérable</option>
                                    <option value="Quasi menacée">Quasi menacée</option>
                                    <option value="Préoccupation mineure">Préoccupation mineure</option>
                                </select>
                            </div>
                            
                            <div class="filter-group">
                                <label>
                                    <i class="fas fa-sort-amount-down"></i>
                                    Trier par
                                </label>
                                <select v-model="sortBy" @change="sortPlants" class="filter-select">
                                    <option value="nom">Nom (A-Z)</option>
                                    <option value="-nom">Nom (Z-A)</option>
                                    <option value="famille">Famille (A-Z)</option>
                                    <option value="-famille">Famille (Z-A)</option>
                                    <option value="date_creation">Plus récent</option>
                                    <option value="-date_creation">Plus ancien</option>
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
                                <button 
                                    :class="['view-btn', { active: viewMode === 'compact' }]"
                                    @click="viewMode = 'compact'"
                                    title="Vue compacte">
                                    <i class="fas fa-table"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Filtres avancés -->
                        <div v-show="showAdvancedFilters" class="advanced-filters">
                            <div class="filter-row">
                                <div class="filter-group">
                                    <label><i class="fas fa-microscope"></i> Nom scientifique</label>
                                    <input type="text" v-model="filters.scientificName" @input="filterPlants" placeholder="Rechercher par nom scientifique">
                                </div>
                                <div class="filter-group">
                                    <label><i class="fas fa-map-marker-alt"></i> Habitat</label>
                                    <input type="text" v-model="filters.habitat" @input="filterPlants" placeholder="Forêt, savane, montagne...">
                                </div>
                            </div>
                            <div class="filter-row">
                                <div class="filter-group">
                                    <label><i class="fas fa-calendar"></i> Date d'ajout</label>
                                    <select v-model="filters.dateRange" @change="filterPlants">
                                        <option value="">Toutes les dates</option>
                                        <option value="today">Aujourd'hui</option>
                                        <option value="week">Cette semaine</option>
                                        <option value="month">Ce mois</option>
                                        <option value="year">Cette année</option>
                                    </select>
                                </div>
                                <div class="filter-group">
                                    <label><i class="fas fa-image"></i> Avec image</label>
                                    <select v-model="filters.hasImage" @change="filterPlants">
                                        <option value="">Tous</option>
                                        <option value="true">Avec image uniquement</option>
                                        <option value="false">Sans image uniquement</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="search-results-info">
                        <div class="results-count">
                            <i class="fas fa-leaf"></i>
                            <span>{{ filteredPlants.length }} résultat(s) trouvé(s)</span>
                            <span v-if="filteredPlants.length !== plants.length" class="filter-badge">
                                Filtres actifs
                            </span>
                        </div>
                        <div class="results-actions">
                            <button v-if="hasActiveFilters" @click="resetFilters" class="reset-btn">
                                <i class="fas fa-redo-alt"></i>
                                Réinitialiser
                            </button>
                            <button class="export-btn" @click="exportData">
                                <i class="fas fa-download"></i>
                                Exporter
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Chargement de l'herbier...</p>
            </div>
        </div>

        <!-- Vue Grille -->
        <template v-else-if="filteredPlants.length > 0">
            <section class="plants-section" v-if="viewMode === 'grid'">
                <div class="container">
                    <div class="plants-grid">
                        <div 
                            v-for="(plant, index) in paginatedPlants" 
                            :key="plant.id"
                            class="plant-card"
                            data-aos="fade-up"
                            :data-aos-delay="(index % 6) * 50"
                            @click="openPlantModal(plant)">
                            <div class="plant-image">
                                <img :src="getImageUrl(plant.image)" :alt="plant.nom" @error="handleImageError">
                                <div class="plant-badge" :class="getConservationClass(plant.statut_conservation)" v-if="plant.statut_conservation">
                                    {{ plant.statut_conservation }}
                                </div>
                                <div class="plant-overlay">
                                    <button class="quick-view">
                                        <i class="fas fa-eye"></i>
                                        <span>Détails complets</span>
                                    </button>
                                </div>
                            </div>
                            <div class="plant-details">
                                <h3 class="plant-name">{{ plant.nom }}</h3>
                                <div class="plant-family">
                                    <i class="fas fa-tag"></i>
                                    <span>{{ plant.famille }}</span>
                                </div>
                                <div class="plant-scientific" v-if="plant.nom_scientifique">
                                    <i class="fas fa-microscope"></i>
                                    <span>{{ plant.nom_scientifique }}</span>
                                </div>
                                <p class="plant-description">{{ truncateText(plant.description, 100) }}</p>
                                <div class="plant-footer">
                                    <div class="plant-habitat" v-if="plant.habitat">
                                        <i class="fas fa-map-marker-alt"></i>
                                        <span>{{ truncateText(plant.habitat, 30) }}</span>
                                    </div>
                                    <div class="plant-date" v-if="plant.date_creation">
                                        <i class="fas fa-calendar-alt"></i>
                                        <span>{{ formatDateShort(plant.date_creation) }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Vue Liste -->
            <section class="plants-section" v-if="viewMode === 'list'">
                <div class="container">
                    <div class="plants-list">
                        <div 
                            v-for="(plant, index) in paginatedPlants" 
                            :key="plant.id"
                            class="plant-list-item"
                            data-aos="fade-up"
                            :data-aos-delay="index * 20"
                            @click="openPlantModal(plant)">
                            <div class="list-image">
                                <img :src="getImageUrl(plant.image)" :alt="plant.nom" @error="handleImageError">
                                <div class="list-badge" :class="getConservationClass(plant.statut_conservation)" v-if="plant.statut_conservation">
                                    {{ plant.statut_conservation }}
                                </div>
                            </div>
                            <div class="list-content">
                                <div class="list-header">
                                    <div>
                                        <h3 class="list-name">{{ plant.nom }}</h3>
                                        <div class="list-family">
                                            <i class="fas fa-tag"></i>
                                            <span>{{ plant.famille }}</span>
                                        </div>
                                    </div>
                                </div>
                                <p class="list-description">{{ truncateText(plant.description, 200) }}</p>
                                <div class="list-meta">
                                    <div v-if="plant.nom_scientifique" class="meta-item">
                                        <i class="fas fa-microscope"></i>
                                        <strong>Nom scientifique:</strong> {{ plant.nom_scientifique }}
                                    </div>
                                    <div v-if="plant.habitat" class="meta-item">
                                        <i class="fas fa-map-marker-alt"></i>
                                        <strong>Habitat:</strong> {{ plant.habitat }}
                                    </div>
                                    <div v-if="plant.statut_conservation" class="meta-item">
                                        <i class="fas fa-shield-alt"></i>
                                        <strong>Statut:</strong> {{ plant.statut_conservation }}
                                    </div>
                                    <div v-if="plant.date_creation" class="meta-item">
                                        <i class="fas fa-calendar-alt"></i>
                                        <strong>Ajouté le:</strong> {{ formatDate(plant.date_creation) }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Vue Compacte (Tableau) -->
            <section class="plants-section" v-if="viewMode === 'compact'">
                <div class="container">
                    <div class="compact-table-wrapper">
                        <table class="compact-table">
                            <thead>
                                <tr>
                                    <th>Image</th>
                                    <th @click="sortByField('nom')">Nom <i class="fas fa-sort"></i></th>
                                    <th @click="sortByField('famille')">Famille <i class="fas fa-sort"></i></th>
                                    <th>Nom scientifique</th>
                                    <th>Habitat</th>
                                    <th>Statut</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="plant in paginatedPlants" :key="plant.id" @click="openPlantModal(plant)">
                                    <td class="compact-image">
                                        <img :src="getImageUrl(plant.image)" :alt="plant.nom" @error="handleImageError">
                                    </td>
                                    <td class="compact-name">{{ plant.nom }}</td>
                                    <td>{{ plant.famille }}</td>
                                    <td class="compact-scientific">{{ truncateText(plant.nom_scientifique, 30) }}</td>
                                    <td class="compact-habitat">{{ truncateText(plant.habitat, 25) }}</td>
                                    <td>
                                        <span class="status-badge" :class="getConservationClass(plant.statut_conservation)" v-if="plant.statut_conservation">
                                            {{ plant.statut_conservation }}
                                        </span>
                                    </td>
                                    <td>
                                        <button class="view-details-btn" @click.stop="openPlantModal(plant)">
                                            <i class="fas fa-eye"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
                        @click="currentPage = page">
                        {{ page }}
                    </button>
                    <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </template>

        <!-- Aucun Résultat -->
        <section v-else class="no-results-section">
            <div class="container">
                <div class="no-results-card" data-aos="fade-up">
                    <div class="no-results-icon">
                        <i class="fas fa-seedling"></i>
                    </div>
                    <h3>Aucune plante trouvée</h3>
                    <p>Nous n'avons pas trouvé de spécimens correspondant à vos critères.</p>
                    <button @click="resetFilters" class="btn-primary">
                        <i class="fas fa-redo-alt"></i>
                        Réinitialiser la recherche
                    </button>
                </div>
            </div>
        </section>

        <!-- Modal Détails Complets Plante -->
        <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
            <div class="modal-container modal-large">
                <button class="modal-close" @click="closeModal">
                    <i class="fas fa-times"></i>
                </button>
                <div class="modal-content" v-if="selectedPlant">
                    <div class="modal-image-section">
                        <img :src="getImageUrl(selectedPlant.image)" :alt="selectedPlant.nom" class="modal-main-image">
                        <div class="modal-badge" :class="getConservationClass(selectedPlant.statut_conservation)" v-if="selectedPlant.statut_conservation">
                            {{ selectedPlant.statut_conservation }}
                        </div>
                    </div>
                    <div class="modal-info-section">
                        <h2 class="modal-title">{{ selectedPlant.nom }}</h2>
                        <div class="modal-family">
                            <i class="fas fa-tag"></i>
                            <span>{{ selectedPlant.famille }}</span>
                        </div>
                        
                        <div class="modal-details-grid">
                            <div class="detail-card" v-if="selectedPlant.nom_scientifique">
                                <div class="detail-icon"><i class="fas fa-microscope"></i></div>
                                <div class="detail-content">
                                    <h4>Nom scientifique</h4>
                                    <p><em>{{ selectedPlant.nom_scientifique }}</em></p>
                                </div>
                            </div>
                            
                            <div class="detail-card" v-if="selectedPlant.habitat">
                                <div class="detail-icon"><i class="fas fa-map-marker-alt"></i></div>
                                <div class="detail-content">
                                    <h4>Habitat</h4>
                                    <p>{{ selectedPlant.habitat }}</p>
                                </div>
                            </div>
                            
                            <div class="detail-card" v-if="selectedPlant.statut_conservation">
                                <div class="detail-icon"><i class="fas fa-shield-alt"></i></div>
                                <div class="detail-content">
                                    <h4>Statut de conservation</h4>
                                    <p>{{ selectedPlant.statut_conservation }}</p>
                                </div>
                            </div>
                            
                            <div class="detail-card" v-if="selectedPlant.date_creation">
                                <div class="detail-icon"><i class="fas fa-calendar-alt"></i></div>
                                <div class="detail-content">
                                    <h4>Date d'ajout</h4>
                                    <p>{{ formatDate(selectedPlant.date_creation) }}</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="modal-section full-width" v-if="selectedPlant.description">
                            <h4><i class="fas fa-align-left"></i> Description complète</h4>
                            <p class="full-description">{{ selectedPlant.description }}</p>
                        </div>
                        
                        <div class="modal-actions">
                            <button class="btn-primary" @click="sharePlant">
                                <i class="fas fa-share-alt"></i>
                                Partager
                            </button>
                            <button class="btn-outline" @click="closeModal">
                                <i class="fas fa-times"></i>
                                Fermer
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

export default {
    name: 'Herbier',
    data() {
        return {
            plants: [],
            filteredPlants: [],
            searchQuery: '',
            selectedFamily: '',
            selectedConservation: '',
            sortBy: 'nom',
            viewMode: 'grid',
            currentPage: 1,
            itemsPerPage: 12,
            loading: true,
            showModal: false,
            selectedPlant: null,
            searchTimeout: null,
            showAdvancedFilters: false,
            filters: {
                scientificName: '',
                habitat: '',
                dateRange: '',
                hasImage: ''
            }
        }
    },
    computed: {
        totalPlants() {
            return this.plants.length
        },
        uniqueFamilies() {
            const families = new Set(this.plants.map(p => p.famille).filter(Boolean))
            return families.size
        },
        plantsWithImagesCount() {
            return this.plants.filter(p => p.image).length
        },
        endangeredSpecies() {
            return this.plants.filter(p => 
                p.statut_conservation && 
                (p.statut_conservation.toLowerCase().includes('danger') || 
                 p.statut_conservation.toLowerCase().includes('vulnérable'))
            ).length
        },
        familiesList() {
            const families = [...new Set(this.plants.map(p => p.famille).filter(Boolean))]
            return families.sort()
        },
        hasActiveFilters() {
            return this.searchQuery !== '' || 
                   this.selectedFamily !== '' || 
                   this.selectedConservation !== '' ||
                   this.filters.scientificName !== '' ||
                   this.filters.habitat !== '' ||
                   this.filters.dateRange !== '' ||
                   this.filters.hasImage !== ''
        },
        paginatedPlants() {
            const start = (this.currentPage - 1) * this.itemsPerPage
            const end = start + this.itemsPerPage
            return this.filteredPlants.slice(start, end)
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
            
            for (let i = start; i <= end; i++) {
                pages.push(i)
            }
            return pages
        }
    },
    mounted() {
        this.fetchPlants()
        this.initAnimations()
    },
    methods: {
        async fetchPlants() {
            this.loading = true
            try {
                const response = await axios.get('http://localhost:8000/api/plantes/')
                this.plants = response.data
                this.filteredPlants = [...this.plants]
                this.sortPlants()
                this.loading = false
            } catch (error) {
                console.error('Erreur lors du chargement:', error)
                this.loading = false
            }
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
        
        getImageUrl(imagePath) {
            if (!imagePath) return '/images/placeholder-plant.jpg'
            if (imagePath.startsWith('http')) return imagePath
            if (imagePath.startsWith('/media')) return `http://localhost:8000${imagePath}`
            return imagePath
        },
        
        handleImageError(event) {
            event.target.src = '/images/placeholder-plant.jpg'
        },
        
        getConservationClass(statut) {
            if (!statut) return ''
            const s = statut.toLowerCase()
            if (s.includes('danger critique')) return 'critical'
            if (s.includes('danger')) return 'endangered'
            if (s.includes('vulnérable')) return 'vulnerable'
            if (s.includes('quasi')) return 'near-threatened'
            return 'least-concern'
        },
        
        debouncedSearch() {
            clearTimeout(this.searchTimeout)
            this.searchTimeout = setTimeout(() => {
                this.filterPlants()
            }, 300)
        },
        
        filterPlants() {
            let filtered = [...this.plants]
            
            // Recherche textuelle
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase()
                filtered = filtered.filter(p => 
                    p.nom?.toLowerCase().includes(query) ||
                    p.famille?.toLowerCase().includes(query) ||
                    p.nom_scientifique?.toLowerCase().includes(query) ||
                    p.description?.toLowerCase().includes(query) ||
                    p.habitat?.toLowerCase().includes(query)
                )
            }
            
            // Filtre par famille
            if (this.selectedFamily) {
                filtered = filtered.filter(p => p.famille === this.selectedFamily)
            }
            
            // Filtre par statut de conservation
            if (this.selectedConservation) {
                filtered = filtered.filter(p => p.statut_conservation === this.selectedConservation)
            }
            
            // Filtre par nom scientifique
            if (this.filters.scientificName) {
                const query = this.filters.scientificName.toLowerCase()
                filtered = filtered.filter(p => 
                    p.nom_scientifique?.toLowerCase().includes(query)
                )
            }
            
            // Filtre par habitat
            if (this.filters.habitat) {
                const query = this.filters.habitat.toLowerCase()
                filtered = filtered.filter(p => 
                    p.habitat?.toLowerCase().includes(query)
                )
            }
            
            // Filtre par présence d'image
            if (this.filters.hasImage === 'true') {
                filtered = filtered.filter(p => p.image)
            } else if (this.filters.hasImage === 'false') {
                filtered = filtered.filter(p => !p.image)
            }
            
            // Filtre par date
            if (this.filters.dateRange) {
                const now = new Date()
                filtered = filtered.filter(p => {
                    if (!p.date_creation) return false
                    const date = new Date(p.date_creation)
                    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
                    switch (this.filters.dateRange) {
                        case 'today': return diffDays === 0
                        case 'week': return diffDays <= 7
                        case 'month': return diffDays <= 30
                        case 'year': return diffDays <= 365
                        default: return true
                    }
                })
            }
            
            this.filteredPlants = filtered
            this.sortPlants()
            this.currentPage = 1
        },
        
        sortPlants() {
            const [field, order] = this.sortBy.startsWith('-') 
                ? [this.sortBy.substring(1), 'desc'] 
                : [this.sortBy, 'asc']
            
            this.filteredPlants.sort((a, b) => {
                let valA = a[field] || ''
                let valB = b[field] || ''
                
                if (typeof valA === 'string') valA = valA.toLowerCase()
                if (typeof valB === 'string') valB = valB.toLowerCase()
                
                if (order === 'asc') {
                    return valA > valB ? 1 : -1
                } else {
                    return valA < valB ? 1 : -1
                }
            })
        },
        
        sortByField(field) {
            if (this.sortBy === field) {
                this.sortBy = '-' + field
            } else {
                this.sortBy = field
            }
            this.sortPlants()
        },
        
        clearSearch() {
            this.searchQuery = ''
            this.filterPlants()
        },
        
        resetFilters() {
            this.searchQuery = ''
            this.selectedFamily = ''
            this.selectedConservation = ''
            this.sortBy = 'nom'
            this.filters = {
                scientificName: '',
                habitat: '',
                dateRange: '',
                hasImage: ''
            }
            this.filterPlants()
        },
        
        truncateText(text, length) {
            if (!text) return ''
            if (text.length <= length) return text
            return text.substring(0, length) + '...'
        },
        
        formatDate(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString('fr-FR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
        },
        
        formatDateShort(dateString) {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString('fr-FR', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            })
        },
        
        openPlantModal(plant) {
            this.selectedPlant = plant
            this.showModal = true
            document.body.style.overflow = 'hidden'
        },
        
        closeModal() {
            this.showModal = false
            this.selectedPlant = null
            document.body.style.overflow = 'auto'
        },
        
        sharePlant() {
            if (navigator.share) {
                navigator.share({
                    title: this.selectedPlant.nom,
                    text: this.selectedPlant.description,
                    url: window.location.href
                })
            } else {
                navigator.clipboard.writeText(`${this.selectedPlant.nom} - ${this.selectedPlant.nom_scientifique || ''}`)
                alert('Informations copiées dans le presse-papier')
            }
        },
        
        exportData() {
            const dataStr = JSON.stringify(this.filteredPlants, null, 2)
            const dataBlob = new Blob([dataStr], { type: 'application/json' })
            const url = URL.createObjectURL(dataBlob)
            const link = document.createElement('a')
            link.href = url
            link.download = `herbier_export_${new Date().toISOString().split('T')[0]}.json`
            link.click()
            URL.revokeObjectURL(url)
        }
    },
    watch: {
        sortBy() {
            this.sortPlants()
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&family=Playfair+Display:wght@400;500;600;700&display=swap');

.herbier {
    overflow-x: hidden;
}

/* Hero Section */
.hero-herbier {
    position: relative;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    overflow: hidden;
    background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 50%, #1a2a3a 100%);
}

.hero-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 50%, rgba(52,152,219,0.1), transparent);
}

.hero-pattern {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.03"><path fill="white" d="M10,10 L20,10 L15,20 Z M30,30 L40,30 L35,40 Z M50,50 L60,50 L55,60 Z M70,70 L80,70 L75,80 Z"/></svg>');
    background-size: 60px 60px;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 900px;
    margin: 0 auto;
    padding: 100px 20px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.5rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 1.5rem;
}

.hero-badge i {
    font-size: 1rem;
    color: #3498db;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 3rem;
    line-height: 1.6;
}

.highlight {
    color: #3498db;
    font-weight: 600;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}

.stat-card {
    text-align: center;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.15);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.12);
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: bold;
    color: #3498db;
}

.stat-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
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

/* Search Section */
.search-section {
    padding: 48px 0;
    background: #f5f7fa;
}

.search-card {
    background: white;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    overflow: hidden;
    border: 1px solid #e8ecf0;
}

.search-header {
    background: #ffffff;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid #e8ecf0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.search-header i {
    font-size: 1.25rem;
    color: #3498db;
}

.search-header h3 {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
    flex: 1;
}

.toggle-filters {
    background: none;
    border: 1px solid #e2e8f0;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.8rem;
    color: #64748b;
    transition: all 0.2s ease;
}

.toggle-filters:hover {
    background: #f1f5f9;
    border-color: #3498db;
    color: #3498db;
}

.search-main {
    padding: 1.5rem;
}

.search-input-wrapper {
    position: relative;
    margin-bottom: 1.5rem;
}

.search-input-wrapper i {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    font-size: 1rem;
}

.search-input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 2.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    background: white;
    transition: all 0.2s ease;
}

.search-input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
}

.clear-btn {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    color: #94a3b8;
    transition: color 0.2s ease;
}

.clear-btn:hover {
    color: #e74c3c;
}

.search-filters {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.filter-group label {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    color: #475569;
    font-size: 0.9rem;
}

.filter-group label i {
    color: #3498db;
    margin-right: 0.5rem;
}

.filter-select {
    padding: 0.5rem 2rem 0.5rem 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    background: white;
    cursor: pointer;
    color: #334155;
    font-size: 0.9rem;
}

.filter-group input {
    padding: 0.5rem 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    width: 200px;
}

.view-toggle {
    display: flex;
    gap: 0.5rem;
    background: #f1f5f9;
    padding: 0.25rem;
    border-radius: 10px;
}

.view-btn {
    padding: 0.5rem 1rem;
    background: transparent;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #64748b;
}

.view-btn.active {
    background: #3498db;
    color: white;
}

/* Advanced Filters */
.advanced-filters {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e2e8f0;
}

.filter-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1rem;
}

.filter-row .filter-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
}

.filter-row .filter-group input,
.filter-row .filter-group select {
    width: 100%;
}

.search-results-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: #f8fafc;
    border-top: 1px solid #e8ecf0;
    flex-wrap: wrap;
    gap: 1rem;
}

.results-count {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Inter', sans-serif;
    color: #475569;
    font-size: 0.9rem;
}

.results-count i {
    color: #3498db;
}

.filter-badge {
    background: #eef2ff;
    color: #3498db;
    padding: 0.2rem 0.5rem;
    border-radius: 20px;
    font-size: 0.7rem;
}

.results-actions {
    display: flex;
    gap: 0.5rem;
}

.reset-btn, .export-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 1rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #64748b;
    transition: all 0.2s ease;
}

.reset-btn:hover, .export-btn:hover {
    background: #f1f5f9;
}

.reset-btn:hover {
    color: #e74c3c;
}

.export-btn:hover {
    color: #3498db;
}

/* Loading */
.loading-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    background: #f5f7fa;
}

.loading-spinner {
    text-align: center;
}

.spinner {
    width: 48px;
    height: 48px;
    border: 3px solid #e2e8f0;
    border-top-color: #3498db;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.loading-spinner p {
    font-family: 'Inter', sans-serif;
    color: #64748b;
}

/* Plants Grid */
.plants-section {
    padding: 60px 0;
    background: #f5f7fa;
}

.plants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.75rem;
}

.plant-card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
    cursor: pointer;
}

.plant-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 30px -12px rgba(0,0,0,0.12);
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

.plant-card:hover .plant-image img {
    transform: scale(1.05);
}

.plant-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    z-index: 2;
    color: white;
}

.plant-badge.critical { background: #e74c3c; }
.plant-badge.endangered { background: #e67e22; }
.plant-badge.vulnerable { background: #f39c12; }
.plant-badge.near-threatened { background: #3498db; }
.plant-badge.least-concern { background: #27ae60; }

.plant-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.plant-card:hover .plant-overlay {
    opacity: 1;
}

.quick-view {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.25rem;
    background: white;
    border: none;
    border-radius: 40px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.quick-view:hover {
    background: #2c3e50;
    color: white;
}

.plant-details {
    padding: 1.25rem;
}

.plant-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.35rem;
}

.plant-family {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #3498db;
    margin-bottom: 0.5rem;
}

.plant-scientific {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #94a3b8;
    margin-bottom: 0.75rem;
    font-style: italic;
}

.plant-description {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.plant-footer {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    font-size: 0.7rem;
    color: #94a3b8;
}

.plant-footer i {
    color: #3498db;
    width: 14px;
}

/* Plants List */
.plants-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.plant-list-item {
    display: flex;
    gap: 1.5rem;
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
    cursor: pointer;
}

.plant-list-item:hover {
    transform: translateX(4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}

.list-image {
    position: relative;
    width: 160px;
    height: 160px;
    flex-shrink: 0;
    overflow: hidden;
    background: #f1f5f9;
}

.list-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.plant-list-item:hover .list-image img {
    transform: scale(1.05);
}

.list-badge {
    position: absolute;
    bottom: 0.5rem;
    right: 0.5rem;
    padding: 0.2rem 0.5rem;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 500;
    color: white;
}

.list-badge.critical { background: #e74c3c; }
.list-badge.endangered { background: #e67e22; }
.list-badge.vulnerable { background: #f39c12; }

.list-content {
    flex: 1;
    padding: 1.25rem 1.25rem 1.25rem 0;
}

.list-header {
    margin-bottom: 0.75rem;
}

.list-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.25rem;
}

.list-family {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #3498db;
}

.list-description {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.list-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.75rem;
    color: #94a3b8;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.meta-item i {
    color: #3498db;
    width: 14px;
}

/* Compact Table */
.compact-table-wrapper {
    overflow-x: auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.compact-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Inter', sans-serif;
}

.compact-table th,
.compact-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
}

.compact-table th {
    background: #f8fafc;
    font-weight: 600;
    color: #1e293b;
    cursor: pointer;
    transition: background 0.2s ease;
}

.compact-table th:hover {
    background: #f1f5f9;
}

.compact-table th i {
    margin-left: 0.5rem;
    font-size: 0.7rem;
    color: #94a3b8;
}

.compact-table tbody tr {
    cursor: pointer;
    transition: background 0.2s ease;
}

.compact-table tbody tr:hover {
    background: #f8fafc;
}

.compact-image {
    width: 50px;
}

.compact-image img {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    object-fit: cover;
}

.compact-name {
    font-weight: 600;
    color: #1e293b;
}

.compact-scientific {
    font-style: italic;
    color: #64748b;
    font-size: 0.85rem;
}

.compact-habitat {
    color: #64748b;
    font-size: 0.85rem;
}

.status-badge {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    color: white;
}

.status-badge.critical { background: #e74c3c; }
.status-badge.endangered { background: #e67e22; }
.status-badge.vulnerable { background: #f39c12; }

.view-details-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #3498db;
    font-size: 1rem;
    transition: color 0.2s ease;
}

.view-details-btn:hover {
    color: #2980b9;
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
    border: 1px solid #e2e8f0;
    background: white;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
    color: #475569;
}

.page-btn:hover:not(:disabled) {
    background: #f1f5f9;
    border-color: #cbd5e1;
}

.page-btn.active {
    background: #3498db;
    color: white;
    border-color: #3498db;
}

.page-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* No Results */
.no-results-section {
    padding: 80px 0;
    background: #f5f7fa;
}

.no-results-card {
    text-align: center;
    background: white;
    border-radius: 24px;
    padding: 4rem;
    max-width: 480px;
    margin: 0 auto;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.no-results-icon {
    font-size: 4rem;
    color: #cbd5e1;
    margin-bottom: 1rem;
}

.no-results-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.no-results-card p {
    font-family: 'Inter', sans-serif;
    color: #64748b;
    margin-bottom: 1.5rem;
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
    border-radius: 28px;
    max-width: 1000px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
}

.modal-container.modal-large {
    max-width: 1100px;
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
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
}

.modal-close:hover {
    transform: scale(1.1);
    background: #e74c3c;
    color: white;
}

.modal-content {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 2rem;
    padding: 2rem;
}

.modal-image-section {
    position: relative;
}

.modal-main-image {
    width: 100%;
    border-radius: 20px;
    object-fit: cover;
}

.modal-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    color: white;
}

.modal-badge.critical { background: #e74c3c; }
.modal-badge.endangered { background: #e67e22; }
.modal-badge.vulnerable { background: #f39c12; }

.modal-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.modal-family {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #eef2ff;
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    color: #3498db;
    margin-bottom: 1.5rem;
}

.modal-details-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.detail-card {
    display: flex;
    gap: 1rem;
    padding: 0.75rem;
    background: #f8fafc;
    border-radius: 12px;
}

.detail-icon {
    width: 40px;
    height: 40px;
    background: #eef2ff;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3498db;
}

.detail-content h4 {
    font-size: 0.7rem;
    font-weight: 600;
    color: #94a3b8;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
}

.detail-content p {
    font-size: 0.85rem;
    color: #1e293b;
}

.modal-section.full-width {
    margin-top: 1rem;
}

.modal-section h4 {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 0.5rem;
}

.modal-section h4 i {
    color: #3498db;
    margin-right: 0.5rem;
}

.full-description {
    font-family: 'Inter', sans-serif;
    color: #475569;
    line-height: 1.7;
    font-size: 0.9rem;
}

.modal-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

.btn-primary, .btn-outline {
    padding: 0.7rem 1.5rem;
    border-radius: 40px;
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    font-size: 0.9rem;
}

.btn-primary {
    background: #3498db;
    color: white;
    border: none;
}

.btn-primary:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.btn-outline {
    background: transparent;
    color: #475569;
    border: 1px solid #cbd5e1;
}

.btn-outline:hover {
    background: #f8fafc;
    border-color: #94a3b8;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-subtitle {
        font-size: 1rem;
    }
    
    .hero-stats {
        gap: 1rem;
    }
    
    .stat-card {
        padding: 0.75rem 1rem;
    }
    
    .search-filters {
        flex-direction: column;
        align-items: stretch;
    }
    
    .filter-group {
        justify-content: space-between;
    }
    
    .filter-row {
        grid-template-columns: 1fr;
    }
    
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
        padding: 1rem;
    }
    
    .modal-content {
        grid-template-columns: 1fr;
    }
    
    .modal-details-grid {
        grid-template-columns: 1fr;
    }
    
    .modal-actions {
        flex-direction: column;
    }
    
    .search-results-info {
        flex-direction: column;
        align-items: flex-start;
    }
}

@media (min-width: 769px) and (max-width: 1024px) {
    .plants-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
