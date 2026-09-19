<template>
  <div id="app">
    <nav class="navbar" :class="{ scrolled: isScrolled }">
      <div class="nav-container">
        <!-- Logo -->
        <router-link to="/" class="logo-link" @click="closeMobileMenu">
          <img
            v-if="logoImage"
            :src="logoImage"
            alt="Logo Université de Man"
            class="logo-img"
            @error="handleLogoError"
          />
          <div class="logo-text">
            <span class="site-title">Herbier de l'Université de Man</span>
            <span class="logo-subtitle">Conservation et valorisation de la flore</span>
          </div>
        </router-link>

        <!-- Menu desktop -->
        <ul class="nav-menu" :class="{ open: mobileMenuOpen }">
          <li>
            <router-link to="/" class="nav-link" exact @click="closeMobileMenu">Accueil</router-link>
          </li>
          <li>
            <router-link to="/herbier" class="nav-link" @click="closeMobileMenu">Herbier</router-link>
          </li>
          <li>
            <router-link to="/activites" class="nav-link" @click="closeMobileMenu">Activités</router-link>
          </li>
          <li>
            <router-link to="/projets" class="nav-link" @click="closeMobileMenu">Projets</router-link>
          </li>
          <li>
            <router-link to="/contact" class="nav-link" @click="closeMobileMenu">Contact</router-link>
          </li>
        </ul>

        <!-- Recherche -->
        <div class="search-bar">
          <input
            type="text"
            v-model="searchQuery"
            @keyup.enter="searchPlants"
            placeholder="Rechercher une plante..."
            aria-label="Rechercher une plante"
          />
          <button type="button" @click="searchPlants" aria-label="Rechercher">
            <i class="fas fa-search"></i>
          </button>
        </div>

        <!-- Burger mobile -->
        <button
          class="mobile-toggle"
          type="button"
          @click="mobileMenuOpen = !mobileMenuOpen"
          :aria-expanded="mobileMenuOpen"
          aria-label="Menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <main class="main-content">
      <router-view :searchQuery="searchQuery" @search="handleSearch" />
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section brand">
          <div class="footer-logo">
            <img
              v-if="footerLogoImage"
              :src="footerLogoImage"
              alt="Logo"
              class="footer-logo-img"
              @error="handleFooterLogoError"
            />
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
          <p>Email : herbier@univ-man.ci</p>
          <p>Tél : +225 00 00 00 00</p>
        </div>

        <div class="footer-section">
          <h4><i class="fas fa-share-alt"></i> Suivez-nous</h4>
          <div class="social-links">
            <a href="#" class="social-link" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social-link" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" class="social-link" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="#" class="social-link" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Herbier de l'Université de Man — Tous droits réservés</p>
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
      logoImage: '/images/uman.png',
      footerLogoImage: '/images/uman.png',
      mobileMenuOpen: false,
      isScrolled: false
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll, { passive: true })
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 16
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    async searchPlants() {
      if (!this.searchQuery.trim()) return
      try {
        const response = await axios.get(
          `http://localhost:8000/api/rechercher/?q=${encodeURIComponent(this.searchQuery)}`
        )
        this.searchResults = response.data
        this.$emit('search', this.searchResults)
        if (this.$route.path !== '/herbier') {
          this.$router.push('/herbier')
        }
        this.closeMobileMenu()
      } catch (error) {
        console.error('Erreur de recherche:', error)
      }
    },
    handleSearch(results) {
      this.searchResults = results
    },
    handleLogoError() {
      this.logoImage = ''
    },
    handleFooterLogoError() {
      this.footerLogoImage = ''
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #2b6cb0;
  --primary-dark: #1a4f8a;
  --primary-light: #ebf4ff;
  --nav-bg: #0f2744;
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --text-muted: #718096;
  --bg-page: #f7fafc;
  --border: #e2e8f0;
  --radius-full: 9999px;
  --transition: 0.22s ease;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg-page);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

/* ========== NAVBAR ========== */
.navbar {
  background: var(--nav-bg);
  color: #fff;
  padding: 0.65rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: box-shadow 0.25s ease, background 0.25s ease;
}

.navbar.scrolled {
  background: rgba(15, 39, 68, 0.97);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
}

/* Logo — pas de fond, pas d'effet "sélectionné" */
.logo-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0;
}

.logo-link:hover,
.logo-link:focus,
.logo-link.router-link-active {
  background: transparent !important;
  opacity: 0.95;
}

.logo-img {
  width: 42px;
  height: 42px;
  object-fit: contain;
  display: block;
  /* Pas de filter si le logo a déjà les bonnes couleurs */
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.site-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
}

.logo-subtitle {
  font-size: 0.68rem;
  color: rgba(255, 255, 255, 0.65);
  font-style: italic;
  margin-top: 2px;
}

/* Liens nav */
.nav-menu {
  display: flex;
  list-style: none;
  gap: 2px;
  margin: 0;
  padding: 0;
}

.nav-link {
  display: block;
  color: rgba(255, 255, 255, 0.88);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  transition: background var(--transition), color var(--transition);
  background: transparent;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Actif uniquement sur les liens du menu, pas le logo */
.nav-menu .router-link-active {
  background: var(--primary) !important;
  color: #fff !important;
}

/* Recherche */
.search-bar {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--radius-full);
  padding: 3px 4px 3px 14px;
  transition: border-color var(--transition), background var(--transition);
}

.search-bar:focus-within {
  background: rgba(255, 255, 255, 0.14);
  border-color: rgba(99, 179, 237, 0.45);
}

.search-bar input {
  border: none;
  outline: none;
  background: transparent;
  color: #fff;
  font-size: 0.875rem;
  font-family: inherit;
  width: 190px;
  padding: 6px 0;
}

.search-bar input::placeholder {
  color: rgba(255, 255, 255, 0.45);
}

.search-bar button {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition), transform var(--transition);
}

.search-bar button:hover {
  background: #3182ce;
  transform: scale(1.04);
}

/* Burger */
.mobile-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  cursor: pointer;
  padding: 9px;
}

.mobile-toggle span {
  display: block;
  height: 2px;
  background: #fff;
  border-radius: 1px;
}

/* ========== FOOTER ========== */
.footer {
  background: var(--nav-bg);
  color: #fff;
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2.75rem 1.5rem 2.25rem;
  display: grid;
  grid-template-columns: 1.35fr repeat(3, 1fr);
  gap: 2.25rem;
}

.footer-logo {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.footer-logo-img {
  width: 44px;
  height: 44px;
  object-fit: contain;
  flex-shrink: 0;
}

.footer-section h3 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  margin: 0 0 4px;
}

.footer-section h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #90cdf4;
  margin: 0 0 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-section p {
  margin: 0 0 5px;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
}

.footer-section.brand p {
  margin-top: 4px;
  max-width: 250px;
}

.social-links {
  display: flex;
  gap: 8px;
}

.social-link {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  color: #fff;
  text-decoration: none;
  font-size: 0.85rem;
  transition: background var(--transition), transform var(--transition);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.social-link:hover {
  background: var(--primary);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.footer-bottom {
  text-align: center;
  padding: 1.1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 900px) {
  .mobile-toggle {
    display: flex;
  }

  .nav-menu {
    position: fixed;
    top: 0;
    right: 0;
    width: min(280px, 85vw);
    height: 100vh;
    background: var(--nav-bg);
    flex-direction: column;
    padding: 72px 20px 24px;
    gap: 4px;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    box-shadow: -6px 0 24px rgba(0, 0, 0, 0.2);
    z-index: 999;
  }

  .nav-menu.open {
    transform: translateX(0);
  }

  .nav-link {
    padding: 12px 16px;
    font-size: 1rem;
  }

  .search-bar {
    display: none;
  }

  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 1.75rem;
  }
}

@media (max-width: 600px) {
  .logo-subtitle {
    display: none;
  }

  .site-title {
    font-size: 0.95rem;
  }

  .logo-img {
    width: 36px;
    height: 36px;
  }

  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .footer-logo {
    justify-content: center;
    flex-direction: column;
    align-items: center;
  }

  .footer-section h4 {
    justify-content: center;
  }

  .social-links {
    justify-content: center;
  }

  .footer-section.brand p {
    max-width: none;
  }
}
</style>