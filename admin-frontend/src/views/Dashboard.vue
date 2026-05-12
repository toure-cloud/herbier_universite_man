<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <i class="fas fa-leaf"></i>
          </div>
          <div class="logo-text">
            <span class="logo-title">Herbier Admin</span>
            <span class="logo-subtitle">Université de Man</span>
          </div>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item active">
          <i class="fas fa-tachometer-alt"></i>
          <span>Tableau de bord</span>
          <span class="nav-badge">v2.0</span>
        </router-link>
        <router-link to="/plantes" class="nav-item">
          <i class="fas fa-leaf"></i>
          <span>Plantes</span>
        </router-link>
        <router-link to="/equipe" class="nav-item">
          <i class="fas fa-users"></i>
          <span>Équipe</span>
        </router-link>
        <router-link to="/partenaires" class="nav-item">
          <i class="fas fa-handshake"></i>
          <span>Partenaires</span>
        </router-link>
        <router-link to="/slides" class="nav-item">
          <i class="fas fa-images"></i>
          <span>Slides</span>
        </router-link>
        <router-link to="/projets" class="nav-item">
          <i class="fas fa-project-diagram"></i>
          <span>Projets</span>
        </router-link>
        <router-link to="/activites" class="nav-item">
          <i class="fas fa-chart-line"></i>
          <span>Activités</span>
        </router-link>
        <router-link to="/temoignages" class="nav-item">
          <i class="fas fa-comment-dots"></i>
          <span>Témoignages</span>
        </router-link>
        <router-link to="/publications" class="nav-item">
          <i class="fas fa-book"></i>
          <span>Publications</span>
        </router-link>
        <router-link to="/statistiques" class="nav-item">
          <i class="fas fa-chart-bar"></i>
          <span>Statistiques</span>
        </router-link>
        <router-link to="/herbier-data" class="nav-item">
          <i class="fas fa-database"></i>
          <span>Données Herbier</span>
        </router-link>
        <router-link to="/settings" class="nav-item">
          <i class="fas fa-cog"></i>
          <span>Paramètres</span>
        </router-link>
      </nav>
      
      <div class="sidebar-footer">
        <div class="user-info-sidebar">
          <div class="user-avatar-sidebar">{{ userInitials }}</div>
          <div class="user-details-sidebar">
            <span class="user-name-sidebar">{{ user?.nom || 'Administrateur' }}</span>
            <span class="user-role">Super Administrateur</span>
          </div>
        </div>
        <button @click="confirmLogout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          <span>Déconnexion</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-bar">
        <div class="page-title">
          <h1>Tableau de bord</h1>
          <p>Bienvenue, {{ user?.nom || 'Administrateur' }}</p>
        </div>
        <div class="user-menu">
          <div class="notification-bell">
            <i class="fas fa-bell"></i>
            <span class="notification-dot" v-if="hasNotifications"></span>
          </div>
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <div class="user-info">
            <span class="user-name">{{ user?.nom }}</span>
            <span class="user-email">{{ user?.email }}</span>
          </div>
        </div>
      </header>

      <!-- Welcome Banner -->
      <div class="welcome-banner">
        <div class="welcome-content">
          <i class="fas fa-leaf welcome-icon"></i>
          <div class="welcome-text">
            <h2>Bon retour, {{ user?.nom?.split(' ')[0] || 'Administrateur' }} !</h2>
            <p>Voici un résumé de votre espace d'administration. Vous pouvez gérer l'intégralité du contenu du site depuis cette interface.</p>
          </div>
          <div class="welcome-stats">
            <div class="welcome-stat">
              <span class="stat-number">{{ stats.reduce((acc, s) => acc + s.value, 0) }}</span>
              <span class="stat-label">Éléments</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card" v-for="stat in stats" :key="stat.label" :style="{ '--card-color': stat.color }">
          <div class="stat-icon">
            <i :class="stat.icon"></i>
          </div>
          <div class="stat-info">
            <h3>{{ stat.value }}</h3>
            <p>{{ stat.label }}</p>
          </div>
          <div class="stat-trend" v-if="stat.trend">
            <i :class="stat.trend > 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
            <span>{{ Math.abs(stat.trend) }}%</span>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-header">
            <h3><i class="fas fa-chart-pie"></i> Répartition par catégorie</h3>
            <div class="chart-actions">
              <button class="chart-btn" @click="chartType = 'doughnut'">🍩</button>
              <button class="chart-btn" @click="chartType = 'bar'">📊</button>
            </div>
          </div>
          <div class="chart-content">
            <canvas ref="categoryChart"></canvas>
          </div>
        </div>
        
        <div class="chart-card">
          <div class="chart-header">
            <h3><i class="fas fa-history"></i> Activités récentes</h3>
            <button class="refresh-btn" @click="loadRecentActivities" title="Rafraîchir">
              <i class="fas fa-sync-alt"></i>
            </button>
          </div>
          <div class="activities-list">
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon" :class="activity.type">
                <i :class="activity.icon"></i>
              </div>
              <div class="activity-details">
                <p>{{ activity.message }}</p>
                <span>{{ formatDate(activity.time) }}</span>
              </div>
            </div>
            <div v-if="recentActivities.length === 0" class="no-activities">
              <i class="fas fa-inbox"></i>
              <p>Aucune activité récente</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h3><i class="fas fa-bolt"></i> Actions rapides</h3>
        <div class="actions-grid">
          <router-link to="/plantes" class="action-card">
            <i class="fas fa-plus-circle"></i>
            <span>Ajouter une plante</span>
          </router-link>
          <router-link to="/equipe" class="action-card">
            <i class="fas fa-user-plus"></i>
            <span>Ajouter un membre</span>
          </router-link>
          <router-link to="/projets" class="action-card">
            <i class="fas fa-plus"></i>
            <span>Nouveau projet</span>
          </router-link>
          <router-link to="/slides" class="action-card">
            <i class="fas fa-image"></i>
            <span>Ajouter un slide</span>
          </router-link>
          <router-link to="/herbier-data" class="action-card">
            <i class="fas fa-cloud-upload-alt"></i>
            <span>Synchroniser</span>
          </router-link>
        </div>
      </div>

      <!-- System Status -->
      <div class="system-status">
        <div class="status-item">
          <i class="fas fa-circle" :class="{ 'status-online': isOnline, 'status-offline': !isOnline }"></i>
          <span>Système {{ isOnline ? 'en ligne' : 'hors ligne' }}</span>
        </div>
        <div class="status-item">
          <i class="fas fa-database"></i>
          <span>Base de données connectée</span>
        </div>
        <div class="status-item">
          <i class="fas fa-clock"></i>
          <span>Dernière connexion: {{ lastLoginDate }}</span>
        </div>
      </div>
    </main>

    <!-- Modal de confirmation de déconnexion -->
    <div class="modal-logout" :class="{ active: showLogoutModal }">
      <div class="modal-overlay" @click="closeLogoutModal"></div>
      <div class="modal-content">
        <div class="modal-icon">
          <i class="fas fa-question-circle"></i>
        </div>
        <h3>Déconnexion</h3>
        <p>Êtes-vous sûr de vouloir vous déconnecter ?</p>
        <div class="modal-buttons">
          <button class="btn-cancel" @click="closeLogoutModal">
            <i class="fas fa-times"></i> Annuler
          </button>
          <button class="btn-confirm" @click="handleLogout">
            <i class="fas fa-sign-out-alt"></i> Déconnexion
          </button>
        </div>
      </div>
    </div>

    <!-- Toast notification -->
    <div v-if="toastMessage" class="toast" :class="toastType">
      <i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'Dashboard',
  data() {
    return {
      user: null,
      showLogoutModal: false,
      chartType: 'doughnut',
      isOnline: navigator.onLine,
      lastLoginDate: '',
      hasNotifications: false,
      toastMessage: '',
      toastType: '',
      stats: [
        { label: 'Plantes', value: 0, icon: 'fas fa-leaf', color: '#32CD32', trend: 12 },
        { label: 'Équipe', value: 0, icon: 'fas fa-users', color: '#FFD700', trend: 5 },
        { label: 'Projets', value: 0, icon: 'fas fa-project-diagram', color: '#17a2b8', trend: 8 },
        { label: 'Partenaires', value: 0, icon: 'fas fa-handshake', color: '#dc3545', trend: -2 },
        { label: 'Slides', value: 0, icon: 'fas fa-images', color: '#6f42c1', trend: 0 },
        { label: 'Témoignages', value: 0, icon: 'fas fa-comment-dots', color: '#20c997', trend: 15 }
      ],
      recentActivities: [],
      categoryChart: null
    }
  },
  computed: {
    userInitials() {
      if (this.user?.nom) {
        return this.user.nom.split(' ').map(n => n[0]).join('').toUpperCase()
      }
      return 'AD'
    }
  },
  mounted() {
    const authStore = useAuthStore()
    this.user = authStore.user
    this.loadStats()
    this.loadRecentActivities()
    this.initChart()
    this.loadLastLoginDate()
    
    // Vérifier le statut de connexion
    window.addEventListener('online', () => { this.isOnline = true; this.showToast('Connexion rétablie', 'success') })
    window.addEventListener('offline', () => { this.isOnline = false; this.showToast('Connexion perdue', 'error') })
  },
  beforeUnmount() {
    if (this.categoryChart) {
      this.categoryChart.destroy()
    }
  },
  methods: {
    async loadStats() {
      try {
        const response = await axios.get('http://localhost:8001/api/herbier-data/')
        const data = response.data
        
        this.stats[0].value = data.plantes?.length || 0
        this.stats[1].value = data.equipe?.length || 0
        this.stats[2].value = data.projets?.length || 0
        this.stats[3].value = data.partenaires?.length || 0
        this.stats[4].value = data.slides?.length || 0
        this.stats[5].value = data.temoignages?.length || 0
        
        this.updateChart()
      } catch (error) {
        console.error('Erreur chargement stats:', error)
      }
    },
    
    async loadRecentActivities() {
      try {
        const response = await axios.get('http://localhost:8001/api/login-history/', {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        })
        this.recentActivities = response.data.slice(0, 5).map(activity => ({
          ...activity,
          message: activity.success ? 'Connexion réussie depuis ' + (activity.ip_address || 'IP inconnue') : 'Tentative de connexion échouée',
          type: activity.success ? 'success' : 'error',
          icon: activity.success ? 'fas fa-sign-in-alt' : 'fas fa-exclamation-triangle'
        }))
      } catch (error) {
        console.error('Erreur chargement activités:', error)
      }
    },
    
    loadLastLoginDate() {
      const lastLogin = localStorage.getItem('last_login_date')
      if (lastLogin) {
        this.lastLoginDate = new Date(lastLogin).toLocaleString('fr-FR')
      } else {
        this.lastLoginDate = new Date().toLocaleString('fr-FR')
      }
    },
    
    initChart() {
      const ctx = this.$refs.categoryChart?.getContext('2d')
      if (ctx) {
        this.categoryChart = new Chart(ctx, {
          type: this.chartType,
          data: {
            labels: ['Plantes', 'Projets', 'Équipe', 'Partenaires', 'Slides'],
            datasets: [{
              data: [0, 0, 0, 0, 0],
              backgroundColor: ['#32CD32', '#17a2b8', '#FFD700', '#dc3545', '#6f42c1'],
              borderWidth: 0,
              borderRadius: 10
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: { position: 'bottom', labels: { font: { size: 12, family: "'Inter', sans-serif" } } },
              tooltip: { backgroundColor: '#1a472a', titleColor: '#FFD700' }
            }
          }
        })
      }
    },
    
    updateChart() {
      if (this.categoryChart) {
        this.categoryChart.data.datasets[0].data = [
          this.stats[0].value,
          this.stats[2].value,
          this.stats[1].value,
          this.stats[3].value,
          this.stats[4].value
        ]
        this.categoryChart.update()
      }
    },
    
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },
    
    showToast(message, type) {
      this.toastMessage = message
      this.toastType = type
      setTimeout(() => {
        this.toastMessage = ''
      }, 3000)
    },
    
    confirmLogout() {
      this.showLogoutModal = true
    },
    
    closeLogoutModal() {
      this.showLogoutModal = false
    },
    
    async handleLogout() {
      this.closeLogoutModal()
      this.showToast('Déconnexion en cours...', 'success')
      
      setTimeout(async () => {
        const authStore = useAuthStore()
        await authStore.logout()
        this.$router.push('/login')
      }, 500)
    }
  },
  watch: {
    chartType() {
      if (this.categoryChart) {
        this.categoryChart.destroy()
        this.initChart()
        setTimeout(() => this.updateChart(), 100)
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.dashboard {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e8 100%);
  font-family: 'Inter', sans-serif;
}

/* Sidebar */
.sidebar {
  width: 300px;
  background: linear-gradient(180deg, #0d3b0f 0%, #1a472a 50%, #0a2412 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  box-shadow: 5px 0 30px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  z-index: 100;
}

.sidebar-header {
  padding: 30px 24px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-icon {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(255,215,0,0.3);
}

.logo-icon i {
  font-size: 24px;
  color: #1a472a;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.logo-subtitle {
  font-size: 10px;
  opacity: 0.7;
  margin-top: 2px;
}

.sidebar-nav {
  flex: 1;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #FFD700;
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.nav-item:hover::before, .nav-item.active::before {
  transform: scaleY(1);
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
  transform: translateX(5px);
}

.nav-item.active {
  background: rgba(255,215,0,0.15);
  color: #FFD700;
}

.nav-item i {
  width: 22px;
  font-size: 18px;
}

.nav-badge {
  margin-left: auto;
  font-size: 9px;
  background: rgba(255,255,255,0.2);
  padding: 2px 6px;
  border-radius: 20px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255,255,255,0.1);
  margin-top: auto;
}

.user-info-sidebar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
  padding: 10px;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
}

.user-avatar-sidebar {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  color: #1a472a;
}

.user-details-sidebar {
  display: flex;
  flex-direction: column;
}

.user-name-sidebar {
  font-weight: 600;
  font-size: 14px;
}

.user-role {
  font-size: 10px;
  opacity: 0.7;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(220,53,69,0.2);
  border: 1px solid rgba(220,53,69,0.5);
  border-radius: 12px;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.logout-btn:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(220,53,69,0.3);
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 300px;
  padding: 20px 30px;
}

.top-bar {
  background: white;
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 20px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.05);
  margin-bottom: 25px;
}

.page-title h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a472a;
  margin-bottom: 4px;
}

.page-title p {
  color: #666;
  font-size: 14px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notification-bell {
  position: relative;
  cursor: pointer;
  font-size: 20px;
  color: #666;
  transition: color 0.3s;
}

.notification-bell:hover {
  color: #32CD32;
}

.notification-dot {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 10px;
  height: 10px;
  background: #dc3545;
  border-radius: 50%;
  border: 2px solid white;
}

.user-avatar {
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #1a472a;
}

.user-email {
  font-size: 12px;
  color: #666;
}

/* Welcome Banner */
.welcome-banner {
  background: linear-gradient(135deg, #1a472a, #2d5016);
  border-radius: 20px;
  padding: 25px 30px;
  margin-bottom: 25px;
  color: white;
  position: relative;
  overflow: hidden;
}

.welcome-banner::before {
  content: '🌿';
  position: absolute;
  right: -20px;
  bottom: -20px;
  font-size: 150px;
  opacity: 0.1;
}

.welcome-content {
  display: flex;
  align-items: center;
  gap: 25px;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.welcome-icon {
  font-size: 50px;
  color: #FFD700;
}

.welcome-text {
  flex: 1;
}

.welcome-text h2 {
  font-size: 24px;
  margin-bottom: 5px;
}

.welcome-text p {
  opacity: 0.9;
  font-size: 14px;
}

.welcome-stats {
  background: rgba(255,255,255,0.15);
  padding: 15px 25px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.welcome-stat {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #FFD700;
  display: block;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--card-color, #32CD32);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, rgba(50,205,50,0.1), rgba(34,139,34,0.05));
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon i {
  font-size: 28px;
  color: var(--card-color, #32CD32);
}

.stat-info h3 {
  font-size: 28px;
  font-weight: bold;
  color: #1a472a;
  margin-bottom: 4px;
}

.stat-info p {
  color: #666;
  font-size: 14px;
}

.stat-trend {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 20px;
  background: #f5f5f5;
}

.stat-trend i {
  color: #28a745;
}

/* Charts */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

.chart-card {
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  transition: transform 0.3s;
}

.chart-card:hover {
  transform: translateY(-3px);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.chart-header h3 i {
  color: #32CD32;
  margin-right: 8px;
}

.chart-header h3 {
  font-size: 16px;
  color: #1a472a;
  margin: 0;
}

.chart-actions, .refresh-btn {
  background: #f5f5f5;
  border: none;
  padding: 5px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.chart-actions button:hover, .refresh-btn:hover {
  background: #e0e0e0;
  transform: scale(1.05);
}

.chart-content {
  height: 250px;
}

/* Activities List */
.activities-list {
  max-height: 250px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.3s;
}

.activity-item:hover {
  background: #f8f9fa;
  padding-left: 5px;
}

.activity-icon {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-icon.success {
  background: #d4edda;
  color: #28a745;
}

.activity-icon.error {
  background: #f8d7da;
  color: #dc3545;
}

.activity-details {
  flex: 1;
}

.activity-details p {
  font-size: 13px;
  color: #333;
  margin-bottom: 4px;
}

.activity-details span {
  font-size: 11px;
  color: #999;
}

.no-activities {
  text-align: center;
  padding: 30px;
  color: #999;
}

.no-activities i {
  font-size: 40px;
  margin-bottom: 10px;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 25px;
}

.quick-actions h3 {
  font-size: 18px;
  color: #1a472a;
  margin-bottom: 15px;
}

.quick-actions h3 i {
  color: #32CD32;
  margin-right: 8px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.action-card {
  background: white;
  padding: 18px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
}

.action-card i {
  font-size: 24px;
  color: #32CD32;
}

.action-card:hover i {
  color: white;
}

.action-card span {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.action-card:hover span {
  color: white;
}

/* System Status */
.system-status {
  background: white;
  border-radius: 15px;
  padding: 15px 20px;
  display: flex;
  gap: 25px;
  flex-wrap: wrap;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.status-online {
  color: #28a745;
  font-size: 10px;
}

.status-offline {
  color: #dc3545;
  font-size: 10px;
}

/* Modal Logout */
.modal-logout {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  visibility: hidden;
  opacity: 0;
  transition: all 0.3s ease;
}

.modal-logout.active {
  visibility: visible;
  opacity: 1;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.modal-content {
  position: relative;
  background: white;
  border-radius: 24px;
  padding: 35px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  animation: modalSlideIn 0.3s ease;
  z-index: 1;
}

@keyframes modalSlideIn {
  from { transform: translateY(-50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-icon {
  width: 70px;
  height: 70px;
  background: #FFF3e0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.modal-icon i {
  font-size: 35px;
  color: #FF9800;
}

.modal-content h3 {
  font-size: 22px;
  color: #1a472a;
  margin-bottom: 10px;
}

.modal-content p {
  color: #666;
  margin-bottom: 25px;
}

.modal-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-cancel, .btn-confirm {
  padding: 12px 25px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-confirm {
  background: #dc3545;
  color: white;
}

.btn-confirm:hover {
  background: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(220,53,69,0.3);
}

/* Toast */
.toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 14px 22px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1100;
  animation: slideInRight 0.3s ease;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  font-weight: 500;
}

.toast.success {
  background: #28a745;
  color: white;
}

.toast.error {
  background: #dc3545;
  color: white;
}

@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

/* Responsive */
@media (max-width: 1024px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }
  
  .sidebar-nav span,
  .sidebar-footer span,
  .logo-text,
  .user-info-sidebar,
  .nav-badge {
    display: none;
  }
  
  .nav-item {
    justify-content: center;
  }
  
  .main-content {
    margin-left: 80px;
    padding: 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .welcome-content {
    flex-direction: column;
    text-align: center;
  }
  
  .top-bar {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .user-menu {
    justify-content: center;
  }
}
</style>
