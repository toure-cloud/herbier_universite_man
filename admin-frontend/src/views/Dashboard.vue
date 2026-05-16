<template>
  <div class="dashboard">
    <nav class="sidebar">
      <div class="logo">
        <i class="fas fa-leaf"></i>
        <span>Herbier Admin</span>
      </div>
      <div class="nav-menu">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i> Tableau de bord
        </router-link>
        <router-link to="/herbier-data" class="nav-item">
          <i class="fas fa-database"></i> Données
        </router-link>
        <router-link to="/settings" class="nav-item">
          <i class="fas fa-cog"></i> Paramètres
        </router-link>
        <button @click="logout" class="nav-item logout">
          <i class="fas fa-sign-out-alt"></i> Déconnexion
        </button>
      </div>
    </nav>

    <div class="main-content">
      <div class="top-bar">
        <h1>Tableau de bord</h1>
        <div class="user-info">
          <span>{{ user?.nom || 'Administrateur' }}</span>
          <div class="avatar">
            {{ (user?.nom || 'A').charAt(0) }}
          </div>
        </div>
      </div>

      <div class="content">
        <div class="stats-grid">
          <div class="stat-card">
            <i class="fas fa-leaf"></i>
            <div>
              <h3>{{ stats.total_plantes || 0 }}</h3>
              <p>Plantes</p>
            </div>
          </div>
          <div class="stat-card">
            <i class="fas fa-users"></i>
            <div>
              <h3>{{ stats.total_equipe || 0 }}</h3>
              <p>Équipe</p>
            </div>
          </div>
          <div class="stat-card">
            <i class="fas fa-project-diagram"></i>
            <div>
              <h3>{{ stats.total_projets || 0 }}</h3>
              <p>Projets</p>
            </div>
          </div>
          <div class="stat-card">
            <i class="fas fa-images"></i>
            <div>
              <h3>{{ stats.total_slides || 0 }}</h3>
              <p>Slides</p>
            </div>
          </div>
        </div>

        <div class="welcome-card">
          <h2>Bienvenue dans l'administration</h2>
          <p>Gérez votre herbier depuis cette interface.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { publicAPI } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {},
      user: null
    }
  },
  async mounted() {
    const authStore = useAuthStore()
    this.user = authStore.user
    await this.loadStats()
  },
  methods: {
    async loadStats() {
      try {
        const res = await publicAPI.getDashboard()
        this.stats = res.data
      } catch (error) {
        console.error('Erreur chargement stats:', error)
      }
    },
    async logout() {
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
  width: 260px;
  background: linear-gradient(180deg, #1a472a 0%, #0d3b0f 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
}

.logo {
  padding: 30px 20px;
  font-size: 20px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo i {
  font-size: 28px;
  color: #FFD700;
}

.nav-menu {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.3s ease;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.nav-item.router-link-active {
  background: #FFD700;
  color: #1a472a;
}

.logout {
  margin-top: auto;
  color: #ff6b6b;
}

.logout:hover {
  background: rgba(220,53,69,0.2);
  color: #ff6b6b;
}

.main-content {
  flex: 1;
  margin-left: 260px;
}

.top-bar {
  background: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.top-bar h1 {
  font-size: 24px;
  color: #1a472a;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
}

.content {
  padding: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.stat-card i {
  font-size: 40px;
  color: #32CD32;
}

.stat-card h3 {
  font-size: 28px;
  margin: 0;
  color: #1a472a;
}

.stat-card p {
  margin: 0;
  color: #666;
}

.welcome-card {
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 15px;
  padding: 40px;
  color: white;
}

.welcome-card h2 {
  margin: 0 0 10px 0;
}

.welcome-card p {
  margin: 0;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .sidebar {
    width: 70px;
  }
  .logo span, .nav-item span {
    display: none;
  }
  .main-content {
    margin-left: 70px;
  }
}
</style>
