<template>
  <div class="dashboard">
    <nav class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <i class="fas fa-leaf"></i>
          <span>Herbier Admin</span>
        </div>
      </div>
      
      <div class="sidebar-menu">
        <router-link to="/dashboard" class="menu-item" exact-active-class="active">
          <i class="fas fa-tachometer-alt"></i>
          <span>Tableau de bord</span>
        </router-link>
        <router-link to="/herbier-data" class="menu-item" active-class="active">
          <i class="fas fa-database"></i>
          <span>Gestion des données</span>
        </router-link>
        <router-link to="/settings" class="menu-item" active-class="active">
          <i class="fas fa-cog"></i>
          <span>Paramètres</span>
        </router-link>
      </div>
      
      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          <span>Déconnexion</span>
        </button>
      </div>
    </nav>
    
    <div class="main-content">
      <div class="top-bar">
        <div class="user-info">
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <div class="user-details">
            <span class="user-name">{{ user?.nom }}</span>
            <span class="user-email">{{ user?.email }}</span>
          </div>
        </div>
      </div>
      
      <div class="content">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-leaf"></i>
            </div>
            <div class="stat-info">
              <h3>{{ stats.totalPlantes || 0 }}</h3>
              <p>Plantes</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-project-diagram"></i>
            </div>
            <div class="stat-info">
              <h3>{{ stats.totalProjets || 0 }}</h3>
              <p>Projets</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-info">
              <h3>{{ stats.totalEquipe || 0 }}</h3>
              <p>Membres</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-handshake"></i>
            </div>
            <div class="stat-info">
              <h3>{{ stats.totalPartenaires || 0 }}</h3>
              <p>Partenaires</p>
            </div>
          </div>
        </div>
        
        <div class="recent-activity">
          <h2>Activités récentes</h2>
          <div class="activity-list">
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon" :class="activity.type">
                <i :class="activity.icon"></i>
              </div>
              <div class="activity-content">
                <p>{{ activity.message }}</p>
                <span class="activity-time">{{ formatDate(activity.time) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'Dashboard',
  data() {
    return {
      user: null,
      stats: {},
      recentActivities: []
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
  async mounted() {
    const authStore = useAuthStore()
    this.user = authStore.user
    await this.loadStats()
    await this.loadActivities()
  },
  methods: {
    async loadStats() {
      try {
        const response = await axios.get('http://localhost:8001/api/herbier-data/')
        const data = response.data
        this.stats = {
          totalPlantes: data.plantes?.length || 0,
          totalProjets: data.projets?.length || 0,
          totalEquipe: data.equipe?.length || 0,
          totalPartenaires: data.partenaires?.length || 0
        }
      } catch (error) {
        console.error('Erreur chargement stats', error)
      }
    },
    async loadActivities() {
      try {
        const response = await axios.get('http://localhost:8001/api/login-history/')
        this.recentActivities = response.data.map(history => ({
          id: history.id,
          type: history.success ? 'success' : 'error',
          icon: history.success ? 'fas fa-sign-in-alt' : 'fas fa-exclamation-triangle',
          message: history.success ? 'Connexion réussie' : 'Tentative de connexion échouée',
          time: history.login_time
        }))
      } catch (error) {
        console.error('Erreur chargement activités', error)
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleString('fr-FR')
    },
    async handleLogout() {
      const authStore = useAuthStore()
      await authStore.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #1a472a 0%, #0d3b0f 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: bold;
}

.logo i {
  font-size: 28px;
  color: #FFD700;
}

.sidebar-menu {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.menu-item.active {
  background: #FFD700;
  color: #1a472a;
}

.menu-item i {
  width: 20px;
  font-size: 18px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255,255,255,0.1);
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(220,53,69,0.8);
}

.main-content {
  flex: 1;
  margin-left: 280px;
}

.top-bar {
  background: white;
  padding: 20px 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  display: flex;
  justify-content: flex-end;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.user-details {
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

.content {
  padding: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon i {
  font-size: 28px;
  color: white;
}

.stat-info h3 {
  font-size: 28px;
  color: #1a472a;
  margin-bottom: 5px;
}

.stat-info p {
  color: #666;
}

.recent-activity {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.recent-activity h2 {
  color: #1a472a;
  margin-bottom: 20px;
  font-size: 18px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 12px;
  background: #f8f9fa;
}

.activity-icon {
  width: 40px;
  height: 40px;
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

.activity-content {
  flex: 1;
}

.activity-content p {
  color: #333;
  margin-bottom: 5px;
}

.activity-time {
  font-size: 12px;
  color: #999;
}
</style>
