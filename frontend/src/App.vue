<template>
    <div id="app">
        <nav class="navbar">
            <div class="nav-container">
                <div class="logo">
                    <router-link to="/" class="logo-link">
                        <img 
                            :src="logoImage" 
                            alt="Logo Université de Man" 
                            class="logo-img"
                            @error="handleLogoError"
                        >
                        <div class="logo-text">
                            <h1 class="site-title">Herbier de l'Université de Man</h1>
                            <p class="logo-subtitle">Conservation et valorisation de la flore</p>
                        </div>
                    </router-link>
                </div>
                <ul class="nav-menu">
                    <li><router-link to="/" class="nav-link">Accueil</router-link></li>
                    <li><router-link to="/herbier" class="nav-link">Herbier</router-link></li>
                    <li><router-link to="/activites" class="nav-link">Activités</router-link></li>
                    <li><router-link to="/projets" class="nav-link">Projets</router-link></li>
                    <li><router-link to="/contact" class="nav-link">Contact</router-link></li>
                </ul>
                <div class="search-bar">
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        @keyup.enter="searchPlants"
                        placeholder="Rechercher une plante..."
                    >
                    <button @click="searchPlants">
                        <i class="fas fa-search"></i>
                    </button>
                </div>
            </div>
        </nav>
        
        <router-view 
            :searchQuery="searchQuery"
            @search="handleSearch"
        ></router-view>
        
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-logo">
                        <img 
                            :src="footerLogoImage" 
                            alt="Logo" 
                            class="footer-logo-img"
                            @error="handleFooterLogoError"
                        >
                        <div>
                            <h3>Herbier Université de Man</h3>
                            <p>Préservation et étude de la biodiversité végétale</p>
                        </div>
                    </div>
                </div>
                <div class="footer-section">
                    <h4><i class="fas fa-map-marker-alt"></i> Adresse</h4>
                    <p>Université de Man</p>
                    <p>BP 20, Man</p>
                    <p>Côte d'Ivoire</p>
                </div>
                <div class="footer-section">
                    <h4><i class="fas fa-envelope"></i> Contact</h4>
                    <p>Email: herbier@univ-man.ci</p>
                    <p>Tél: +225 00 00 00 00</p>
                </div>
                <div class="footer-section">
                    <h4><i class="fas fa-share-alt"></i> Suivez-nous</h4>
                    <div class="social-links">
                        <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Herbier de l'Université de Man - Tous droits réservés</p>
            </div>
        </footer>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'App',
    data() {
        return {
            searchQuery: '',
            searchResults: [],
            logoImage: '/src/images/uman.png',
            footerLogoImage: '/src/images/uman.png'
        }
    },
    methods: {
        async searchPlants() {
            if (this.searchQuery.trim()) {
                try {
                    const response = await axios.get(`http://localhost:8000/api/rechercher/?q=${this.searchQuery}`)
                    this.searchResults = response.data
                    this.$emit('search', this.searchResults)
                    
                    if (this.$route.path !== '/herbier') {
                        this.$router.push('/herbier')
                    }
                } catch (error) {
                    console.error('Erreur de recherche:', error)
                }
            }
        },
        handleSearch(results) {
            this.searchResults = results
        },
        handleLogoError() {
            console.warn('Logo non trouvé, utilisation du texte uniquement')
            this.logoImage = ''
        },
        handleFooterLogoError() {
            this.footerLogoImage = ''
        }
    }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f5f7fa;
}

#app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Navbar styles */
.navbar {
    background: linear-gradient(135deg, #028e3a 0%, #36a104 100%);
    color: white;
    padding: 0.75rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.nav-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

/* Logo styles */
.logo {
    display: flex;
    align-items: center;
}

.logo-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    transition: transform 0.3s ease;
}

.logo-link:hover {
    transform: translateY(-2px);
}

.logo-img {
    width: 46px;
    height: 48px;
    object-fit: contain;
    /* Pour logo blanc sur fond vert */
    filter: brightness(0) invert(1);
}

/* Si vous avez un logo coloré, enlever le filter */
/* .logo-img {
    filter: none;
} */

.logo-text {
    display: flex;
    flex-direction: column;
}

.site-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: white;
    margin: 0;
    font-family: 'Playfair Display', 'Georgia', serif;
    letter-spacing: 0.5px;
    line-height: 1.2;
}

.logo-subtitle {
    font-size: 0.7rem;
    opacity: 0.8;
    margin-top: 2px;
    font-style: italic;
    color: rgba(255,255,255,0.9);
}

/* Navigation links */
.nav-menu {
    display: flex;
    list-style: none;
    gap: 0.5rem;
}

.nav-link {
    color: rgba(255,255,255,0.9);
    text-decoration: none;
    font-weight: 500;
    padding: 0.6rem 1.2rem;
    border-radius: 40px;
    transition: all 0.3s ease;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
}

.nav-link:hover {
    background: rgba(255,255,255,0.12);
    color: white;
    transform: translateY(-2px);
}

.router-link-active {
    background: rgba(52,152,219,0.3);
    color: white;
    border: none;
}

.router-link-active:hover {
    background: rgba(52,152,219,0.4);
    transform: translateY(-2px);
}

/* Search bar styles */
.search-bar {
    display: flex;
    gap: 0.5rem;
    background: rgba(255,255,255,0.12);
    border-radius: 40px;
    padding: 0.2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

.search-bar input {
    padding: 0.6rem 1rem;
    border: none;
    border-radius: 40px;
    width: 240px;
    outline: none;
    font-size: 0.85rem;
    background: transparent;
    color: white;
}

.search-bar input::placeholder {
    color: rgba(255,255,255,0.6);
}

.search-bar button {
    padding: 0.5rem 1rem;
    background: #3498db;
    border: none;
    border-radius: 40px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: white;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.search-bar button:hover {
    background: #2980b9;
    transform: scale(1.02);
}

/* Footer styles */
.footer {
    background: linear-gradient(135deg, #1a2a3a 0%, #1e2f3e 100%);
    color: white;
    margin-top: auto;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.footer-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 3rem 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.footer-logo {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.footer-logo-img {
    width: 50px;
    height: 50px;
    object-fit: contain;
    filter: brightness(0) invert(1);
    opacity: 0.9;
}

.footer-section h3, .footer-section h4 {
    margin-bottom: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #3498db;
}

.footer-section h4 i {
    margin-right: 0.5rem;
    font-size: 0.9rem;
}

.footer-section p {
    margin: 0.5rem 0;
    opacity: 0.8;
    font-size: 0.85rem;
    line-height: 1.5;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    color: white;
    transition: all 0.3s ease;
}

.social-link:hover {
    background: #3498db;
    color: white;
    transform: translateY(-3px);
}

.footer-bottom {
    text-align: center;
    padding: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-size: 0.8rem;
    opacity: 0.7;
}

/* Responsive design */
@media (max-width: 1024px) {
    .nav-container {
        flex-direction: column;
        text-align: center;
    }
    
    .logo-link {
        justify-content: center;
    }
    
    .nav-menu {
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .search-bar {
        width: 100%;
        max-width: 400px;
    }
    
    .search-bar input {
        width: 100%;
    }
}

@media (max-width: 768px) {
    .navbar {
        padding: 1rem;
    }
    
    .site-title {
        font-size: 1rem;
    }
    
    .logo-subtitle {
        font-size: 0.6rem;
    }
    
    .logo-img {
        width: 36px;
        height: 36px;
    }
    
    .nav-link {
        padding: 0.4rem 0.8rem;
        font-size: 0.8rem;
    }
    
    .nav-menu {
        gap: 0.3rem;
    }
    
    .footer-content {
        grid-template-columns: 1fr;
        text-align: center;
    }
    
    .footer-logo {
        justify-content: center;
    }
    
    .social-links {
        justify-content: center;
    }
}

/* Animation d'entrée */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

main, .router-view {
    animation: fadeIn 0.4s ease-out;
}
</style>
