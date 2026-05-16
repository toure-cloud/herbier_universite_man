<template>
  <div class="dashboard">
    <h1>Tableau de bord</h1>
    <p>Bienvenue dans l'administration de l'Herbier</p>
    
    <div class="stats" v-if="stats">
      <div class="stat-card">
        <h3>Plantes</h3>
        <p>{{ stats.total_plantes || 0 }}</p>
      </div>
      <div class="stat-card">
        <h3>Équipe</h3>
        <p>{{ stats.total_equipe || 0 }}</p>
      </div>
      <div class="stat-card">
        <h3>Projets</h3>
        <p>{{ stats.total_projets || 0 }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { publicAPI, adminAPI } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: null,
      loading: false
    }
  },
  async mounted() {
    await this.loadStats()
  },
  methods: {
    async loadStats() {
      this.loading = true
      try {
        const res = await publicAPI.getDashboard()
        this.stats = res.data
      } catch (error) {
        console.error('Erreur chargement stats:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.stat-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.stat-card h3 {
  margin: 0 0 10px 0;
  color: #2d5016;
}
.stat-card p {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  color: #32CD32;
}
</style>
