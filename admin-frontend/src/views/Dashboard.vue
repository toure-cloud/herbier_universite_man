<template>
  <div class="dashboard">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-leaf"></i></div>
        <div class="stat-info">
          <h3>{{ stats.total_plantes || 0 }}</h3>
          <p>Plantes</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-users"></i></div>
        <div class="stat-info">
          <h3>{{ stats.total_equipe || 0 }}</h3>
          <p>Équipe</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-project-diagram"></i></div>
        <div class="stat-info">
          <h3>{{ stats.total_projets || 0 }}</h3>
          <p>Projets</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-images"></i></div>
        <div class="stat-info">
          <h3>{{ stats.total_slides || 0 }}</h3>
          <p>Slides</p>
        </div>
      </div>
    </div>

    <div class="sync-section">
      <h2>Synchronisation avec l'API publique</h2>
      <div class="sync-buttons">
        <button @click="syncAll" class="btn-sync" :disabled="syncing">
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': syncing }"></i>
          Synchroniser tout
        </button>
        <button @click="syncEndpoint('plantes')" class="btn-sync-secondary">
          Sync Plantes
        </button>
        <button @click="syncEndpoint('equipe')" class="btn-sync-secondary">
          Sync Équipe
        </button>
        <button @click="syncEndpoint('projets')" class="btn-sync-secondary">
          Sync Projets
        </button>
      </div>
    </div>

    <div class="logs-section" v-if="logs.length">
      <h2>Logs de synchronisation</h2>
      <div class="logs-table">
        <div v-for="log in logs" :key="log.created_at" class="log-item" :class="log.status.toLowerCase()">
          <span class="log-action">{{ log.action }}</span>
          <span class="log-status">{{ log.status }}</span>
          <span class="log-message">{{ log.message }}</span>
          <span class="log-date">{{ formatDate(log.created_at) }}</span>
        </div>
      </div>
    </div>

    <div class="api-status">
      <h3>Statut des APIs</h3>
      <div class="api-status-item">
        <span>API Publique:</span>
        <span :class="apiStatus.public ? 'online' : 'offline'">
          {{ apiStatus.public ? 'En ligne ✅' : 'Hors ligne ❌' }}
        </span>
      </div>
      <div class="api-status-item">
        <span>API Admin:</span>
        <span :class="apiStatus.admin ? 'online' : 'offline'">
          {{ apiStatus.admin ? 'En ligne ✅' : 'Hors ligne ❌' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI, publicAPI } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {},
      logs: [],
      syncing: false,
      apiStatus: {
        public: false,
        admin: true
      }
    }
  },
  mounted() {
    this.loadData()
    this.checkAPIStatus()
  },
  methods: {
    async loadData() {
      try {
        // Stats depuis l'API admin
        const dashboardRes = await adminAPI.getDashboard()
        this.stats = dashboardRes.data
        
        // Logs
        const logsRes = await adminAPI.getSyncLogs()
        this.logs = logsRes.data
      } catch (error) {
        console.error('Erreur chargement données:', error)
      }
    },
    
    async syncAll() {
      this.syncing = true
      try {
        const res = await adminAPI.syncAll()
        alert(`Synchronisation terminée: ${JSON.stringify(res.data.synced)}`)
        await this.loadData()
      } catch (error) {
        alert('Erreur lors de la synchronisation')
      } finally {
        this.syncing = false
      }
    },
    
    async syncEndpoint(endpoint) {
      try {
        const res = await adminAPI.syncEndpoint(endpoint)
        alert(`Synchronisation de ${endpoint} terminée`)
        await this.loadData()
      } catch (error) {
        alert(`Erreur lors de la synchronisation de ${endpoint}`)
      }
    },
    
    async checkAPIStatus() {
      try {
        await publicAPI.getPlantes()
        this.apiStatus.public = true
      } catch {
        this.apiStatus.public = false
      }
    },
    
    formatDate(date) {
      return new Date(date).toLocaleString('fr-FR')
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
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
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.stat-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-info h3 {
  font-size: 24px;
  margin: 0;
  color: #1a472a;
}

.stat-info p {
  margin: 0;
  color: #666;
}

.sync-section {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 30px;
}

.sync-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 15px;
}

.btn-sync, .btn-sync-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-sync {
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
}

.btn-sync-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-sync:hover, .btn-sync-secondary:hover {
  transform: translateY(-2px);
}

.logs-section {
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 30px;
}

.log-item {
  display: flex;
  gap: 15px;
  padding: 10px;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

.log-item.success {
  border-left: 3px solid #28a745;
}

.log-item.error {
  border-left: 3px solid #dc3545;
}

.log-action {
  width: 150px;
  font-weight: 500;
}

.log-status {
  width: 80px;
}

.log-status:contains("SUCCESS") {
  color: #28a745;
}

.log-message {
  flex: 1;
}

.log-date {
  width: 180px;
  color: #999;
  font-size: 12px;
}

.api-status {
  background: white;
  border-radius: 15px;
  padding: 20px;
}

.api-status-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.online {
  color: #28a745;
  font-weight: 500;
}

.offline {
  color: #dc3545;
  font-weight: 500;
}
</style>
