<template>
  <div class="management-page">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon"><i class="fas fa-leaf"></i></div>
          <div class="logo-text"><span class="logo-title">Herbier Admin</span><span class="logo-subtitle">Université de Man</span></div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item"><i class="fas fa-tachometer-alt"></i><span>Tableau de bord</span></router-link>
        <router-link to="/plantes" class="nav-item"><i class="fas fa-leaf"></i><span>Plantes</span></router-link>
        <router-link to="/equipe" class="nav-item"><i class="fas fa-users"></i><span>Équipe</span></router-link>
        <router-link to="/partenaires" class="nav-item"><i class="fas fa-handshake"></i><span>Partenaires</span></router-link>
        <router-link to="/slides" class="nav-item"><i class="fas fa-images"></i><span>Slides</span></router-link>
        <router-link to="/projets" class="nav-item"><i class="fas fa-project-diagram"></i><span>Projets</span></router-link>
        <router-link to="/activites" class="nav-item"><i class="fas fa-chart-line"></i><span>Activités</span></router-link>
        <router-link to="/temoignages" class="nav-item"><i class="fas fa-comment-dots"></i><span>Témoignages</span></router-link>
        <router-link to="/publications" class="nav-item"><i class="fas fa-book"></i><span>Publications</span></router-link>
        <router-link to="/statistiques" class="nav-item"><i class="fas fa-chart-bar"></i><span>Statistiques</span></router-link>
        <router-link to="/herbier-data" class="nav-item active"><i class="fas fa-database"></i><span>Données Herbier</span><span class="nav-badge">Sync</span></router-link>
        <router-link to="/settings" class="nav-item"><i class="fas fa-cog"></i><span>Paramètres</span></router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info-sidebar"><div class="user-avatar-sidebar">{{ userInitials }}</div><div class="user-details-sidebar"><span class="user-name-sidebar">{{ user?.nom || 'Admin' }}</span><span class="user-role">Super Admin</span></div></div>
        <button @click="confirmLogout" class="logout-btn"><i class="fas fa-sign-out-alt"></i><span>Déconnexion</span></button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-bar">
        <div class="page-title">
          <h1><i class="fas fa-database"></i> Données de l'Herbier</h1>
          <p>Visualisez et synchronisez toutes les données avec le site public</p>
        </div>
        <div class="top-actions">
          <button @click="refreshData" class="btn-secondary" :disabled="loading"><i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i> Rafraîchir</button>
          <button @click="syncWithPublicSite" class="btn-primary" :disabled="syncing"><i class="fas fa-cloud-upload-alt" :class="{ 'fa-spin': syncing }"></i> {{ syncing ? 'Synchronisation...' : 'Synchroniser' }}</button>
        </div>
      </header>

      <!-- Statistiques globales -->
      <div class="stats-overview">
        <div class="stat-box"><div class="stat-icon green"><i class="fas fa-leaf"></i></div><div class="stat-info"><h3>{{ stats.totalPlantes }}</h3><p>Plantes</p></div></div>
        <div class="stat-box"><div class="stat-icon orange"><i class="fas fa-users"></i></div><div class="stat-info"><h3>{{ stats.totalEquipe }}</h3><p>Équipe</p></div></div>
        <div class="stat-box"><div class="stat-icon blue"><i class="fas fa-handshake"></i></div><div class="stat-info"><h3>{{ stats.totalPartenaires }}</h3><p>Partenaires</p></div></div>
        <div class="stat-box"><div class="stat-icon purple"><i class="fas fa-project-diagram"></i></div><div class="stat-info"><h3>{{ stats.totalProjets }}</h3><p>Projets</p></div></div>
        <div class="stat-box"><div class="stat-icon teal"><i class="fas fa-images"></i></div><div class="stat-info"><h3>{{ stats.totalSlides }}</h3><p>Slides</p></div></div>
        <div class="stat-box"><div class="stat-icon pink"><i class="fas fa-comment-dots"></i></div><div class="stat-info"><h3>{{ stats.totalTemoignages }}</h3><p>Témoignages</p></div></div>
      </div>

      <!-- Sections de données -->
      <div class="data-sections">
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-leaf"></i> Plantes</h3><span class="badge">{{ data.plantes?.length || 0 }}</span></div><div class="data-preview"><div v-for="p in (data.plantes || []).slice(0, 5)" :key="p.id" class="preview-item"><span class="preview-name">{{ p.nom }}</span><span class="preview-famille">{{ p.famille }}</span></div><div v-if="(data.plantes || []).length > 5" class="preview-more">+ {{ (data.plantes || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-users"></i> Équipe</h3><span class="badge">{{ data.equipe?.length || 0 }}</span></div><div class="data-preview"><div v-for="m in (data.equipe || []).slice(0, 5)" :key="m.id" class="preview-item"><span class="preview-name">{{ m.nom }}</span><span class="preview-famille">{{ m.poste }}</span></div><div v-if="(data.equipe || []).length > 5" class="preview-more">+ {{ (data.equipe || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-handshake"></i> Partenaires</h3><span class="badge">{{ data.partenaires?.length || 0 }}</span></div><div class="data-preview"><div v-for="p in (data.partenaires || []).slice(0, 5)" :key="p.id" class="preview-item"><span class="preview-name">{{ p.nom }}</span><span class="preview-famille">{{ p.site_web ? 'Site web' : '-' }}</span></div><div v-if="(data.partenaires || []).length > 5" class="preview-more">+ {{ (data.partenaires || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-project-diagram"></i> Projets</h3><span class="badge">{{ data.projets?.length || 0 }}</span></div><div class="data-preview"><div v-for="p in (data.projets || []).slice(0, 5)" :key="p.id" class="preview-item"><span class="preview-name">{{ p.titre }}</span><span class="preview-famille">{{ p.categorie }}</span></div><div v-if="(data.projets || []).length > 5" class="preview-more">+ {{ (data.projets || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-images"></i> Slides</h3><span class="badge">{{ data.slides?.length || 0 }}</span></div><div class="data-preview"><div v-for="s in (data.slides || []).slice(0, 5)" :key="s.id" class="preview-item"><span class="preview-name">{{ s.titre }}</span><span class="preview-famille">{{ s.actif ? 'Actif' : 'Inactif' }}</span></div><div v-if="(data.slides || []).length > 5" class="preview-more">+ {{ (data.slides || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-chart-line"></i> Activités</h3><span class="badge">{{ data.activites?.length || 0 }}</span></div><div class="data-preview"><div v-for="a in (data.activites || []).slice(0, 5)" :key="a.id" class="preview-item"><span class="preview-name">{{ a.titre }}</span><span class="preview-famille">{{ a.actif ? 'Actif' : 'Inactif' }}</span></div><div v-if="(data.activites || []).length > 5" class="preview-more">+ {{ (data.activites || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-comment-dots"></i> Témoignages</h3><span class="badge">{{ data.temoignages?.length || 0 }}</span></div><div class="data-preview"><div v-for="t in (data.temoignages || []).slice(0, 5)" :key="t.id" class="preview-item"><span class="preview-name">{{ t.nom }}</span><span class="preview-famille">{{ t.organisation }}</span></div><div v-if="(data.temoignages || []).length > 5" class="preview-more">+ {{ (data.temoignages || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-book"></i> Publications</h3><span class="badge">{{ data.publications?.length || 0 }}</span></div><div class="data-preview"><div v-for="p in (data.publications || []).slice(0, 5)" :key="p.id" class="preview-item"><span class="preview-name">{{ p.titre }}</span><span class="preview-famille">{{ p.annee }}</span></div><div v-if="(data.publications || []).length > 5" class="preview-more">+ {{ (data.publications || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-chart-bar"></i> Statistiques</h3><span class="badge">{{ data.statistiques?.length || 0 }}</span></div><div class="data-preview"><div v-for="s in (data.statistiques || []).slice(0, 5)" :key="s.id" class="preview-item"><span class="preview-name">{{ s.titre }}</span><span class="preview-famille">{{ s.valeur }}{{ s.unite || '' }}</span></div><div v-if="(data.statistiques || []).length > 5" class="preview-more">+ {{ (data.statistiques || []).length - 5 }} autres</div></div></div>
        <div class="data-card"><div class="data-header"><h3><i class="fas fa-question-circle"></i> FAQs</h3><span class="badge">{{ data.faqs?.length || 0 }}</span></div><div class="data-preview"><div v-for="f in (data.faqs || []).slice(0, 5)" :key="f.id" class="preview-item"><span class="preview-name">{{ f.question }}</span><span class="preview-famille">{{ f.actif ? 'Actif' : 'Inactif' }}</span></div><div v-if="(data.faqs || []).length > 5" class="preview-more">+ {{ (data.faqs || []).length - 5 }} autres</div></div></div>
      </div>

      <!-- Historique synchronisation -->
      <div class="sync-history">
        <div class="sync-header"><h3><i class="fas fa-history"></i> Dernière synchronisation</h3><span class="sync-date">{{ lastSyncDate || 'Jamais synchronisé' }}</span></div>
        <div class="sync-progress" v-if="syncing"><div class="progress-bar"><div class="progress-fill" :style="{ width: syncProgress + '%' }"></div></div><span>{{ syncProgress }}%</span></div>
      </div>

      <!-- Message -->
      <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'HerbierData',
  data() {
    return {
      data: { plantes: [], equipe: [], partenaires: [], slides: [], projets: [], activites: [], temoignages: [], publications: [], faqs: [], statistiques: [], methodologie: [] },
      loading: false, syncing: false, syncProgress: 0, lastSyncDate: null, toastMessage: '', toastType: '', user: null
    }
  },
  computed: {
    userInitials() { return this.user?.nom ? this.user.nom.split(' ').map(n => n[0]).join('').toUpperCase() : 'AD' },
    stats() { return { totalPlantes: this.data.plantes?.length || 0, totalEquipe: this.data.equipe?.length || 0, totalPartenaires: this.data.partenaires?.length || 0, totalProjets: this.data.projets?.length || 0, totalSlides: this.data.slides?.length || 0, totalTemoignages: this.data.temoignages?.length || 0 } }
  },
  mounted() { const auth = useAuthStore(); this.user = auth.user; this.loadData(); this.loadLastSyncDate() },
  methods: {
    async loadData() { this.loading = true; try { const res = await axios.get('http://localhost:8001/api/herbier-data/'); this.data = res.data } catch(e) { console.error(e); this.showToast('Erreur chargement', 'error') } finally { this.loading = false } },
    async refreshData() { await this.loadData(); this.showToast('Données rafraîchies', 'success') },
    async syncWithPublicSite() {
      this.syncing = true; this.syncProgress = 0
      try {
        const syncData = { plantes: this.data.plantes, equipe: this.data.equipe, partenaires: this.data.partenaires, slides: this.data.slides, projets: this.data.projets, activites: this.data.activites, temoignages: this.data.temoignages, publications: this.data.publications, faqs: this.data.faqs, statistiques: this.data.statistiques, methodologie: this.data.methodologie, sync_date: new Date().toISOString() }
        
        for (let i = 0; i <= 100; i += 20) { this.syncProgress = i; await new Promise(r => setTimeout(r, 100)) }
        await axios.post('http://localhost:8000/api/sync-herbier-data/', syncData, { headers: { 'Content-Type': 'application/json' } })
        
        this.lastSyncDate = new Date().toLocaleString('fr-FR'); localStorage.setItem('last_sync_date', this.lastSyncDate)
        this.showToast('Synchronisation réussie', 'success')
      } catch(e) { console.error(e); this.showToast('Erreur synchronisation', 'error') }
      finally { this.syncing = false; this.syncProgress = 0 }
    },
    loadLastSyncDate() { const saved = localStorage.getItem('last_sync_date'); if (saved) this.lastSyncDate = saved },
    showToast(t, m) { this.toastType = t; this.toastMessage = m; setTimeout(() => { this.toastMessage = '' }, 3000) },
    confirmLogout() { if (confirm('Déconnexion ?')) { useAuthStore().logout(); this.$router.push('/login') } }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.management-page { display: flex; min-height: 100vh; background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e8 100%); font-family: 'Inter', sans-serif; }

/* Sidebar */
.sidebar { width: 280px; background: linear-gradient(180deg, #0d3b0f 0%, #1a472a 50%, #0a2412 100%); color: white; position: fixed; height: 100vh; left: 0; top: 0; box-shadow: 5px 0 30px rgba(0,0,0,0.1); z-index: 100; }
.sidebar-header { padding: 30px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
.logo { display: flex; align-items: center; gap: 15px; }
.logo-icon { width: 45px; height: 45px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 5px 15px rgba(255,215,0,0.3); }
.logo-icon i { font-size: 24px; color: #1a472a; }
.logo-text { display: flex; flex-direction: column; }
.logo-title { font-size: 18px; font-weight: 700; letter-spacing: 0.5px; }
.logo-subtitle { font-size: 10px; opacity: 0.7; margin-top: 2px; }
.sidebar-nav { flex: 1; padding: 0 16px; display: flex; flex-direction: column; gap: 6px; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; color: rgba(255,255,255,0.8); text-decoration: none; border-radius: 12px; transition: all 0.3s; position: relative; overflow: hidden; }
.nav-item::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: #FFD700; transform: scaleY(0); transition: transform 0.3s; }
.nav-item:hover::before, .nav-item.active::before { transform: scaleY(1); }
.nav-item:hover { background: rgba(255,255,255,0.1); color: white; transform: translateX(5px); }
.nav-item.active { background: rgba(255,215,0,0.15); color: #FFD700; }
.nav-item i { width: 22px; font-size: 18px; }
.nav-badge { margin-left: auto; font-size: 9px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; }
.sidebar-footer { padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: auto; }
.user-info-sidebar { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 12px; }
.user-avatar-sidebar { width: 45px; height: 45px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; color: #1a472a; }
.user-details-sidebar { display: flex; flex-direction: column; }
.user-name-sidebar { font-weight: 600; font-size: 14px; }
.user-role { font-size: 10px; opacity: 0.7; }
.logout-btn { width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; background: rgba(220,53,69,0.2); border: 1px solid rgba(220,53,69,0.5); border-radius: 12px; color: #ff6b6b; cursor: pointer; transition: all 0.3s; font-weight: 500; }
.logout-btn:hover { background: #dc3545; color: white; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(220,53,69,0.3); }

/* Main Content */
.main-content { flex: 1; margin-left: 280px; padding: 20px 30px; }
.top-bar { background: white; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); margin-bottom: 25px; flex-wrap: wrap; gap: 15px; }
.page-title h1 { font-size: 24px; font-weight: 700; color: #1a472a; margin-bottom: 4px; }
.page-title h1 i { color: #32CD32; margin-right: 10px; }
.page-title p { color: #666; font-size: 14px; }
.top-actions { display: flex; gap: 12px; }
.btn-primary, .btn-secondary { padding: 10px 20px; border: none; border-radius: 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 500; transition: all 0.3s; }
.btn-primary { background: linear-gradient(135deg, #32CD32, #228B22); color: white; }
.btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(50,205,50,0.3); }
.btn-secondary { background: #f5f5f5; color: #666; }
.btn-secondary:hover:not(:disabled) { background: #e0e0e0; }
.btn-primary:disabled, .btn-secondary:disabled { opacity: 0.6; cursor: not-allowed; }

/* Stats Overview */
.stats-overview { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 25px; }
.stat-box { background: white; border-radius: 16px; padding: 18px; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: transform 0.3s; }
.stat-box:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
.stat-icon { width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-icon i { font-size: 24px; color: white; }
.stat-icon.green { background: linear-gradient(135deg, #32CD32, #228B22); }
.stat-icon.orange { background: linear-gradient(135deg, #FFD700, #FFA500); }
.stat-icon.blue { background: linear-gradient(135deg, #17a2b8, #0d6efd); }
.stat-icon.purple { background: linear-gradient(135deg, #6f42c1, #5538a8); }
.stat-icon.teal { background: linear-gradient(135deg, #20c997, #159775); }
.stat-icon.pink { background: linear-gradient(135deg, #dc3545, #c82333); }
.stat-info h3 { font-size: 28px; font-weight: bold; color: #1a472a; margin-bottom: 4px; }
.stat-info p { color: #666; font-size: 13px; }

/* Data Sections */
.data-sections { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; margin-bottom: 25px; }
.data-card { background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: all 0.3s; }
.data-card:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
.data-header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: #f8f9fa; border-bottom: 1px solid #eee; }
.data-header h3 { font-size: 15px; color: #1a472a; display: flex; align-items: center; gap: 8px; margin: 0; }
.data-header h3 i { color: #32CD32; }
.badge { background: #e8f5e8; color: #32CD32; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.data-preview { padding: 15px; }
.preview-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.preview-item:last-child { border-bottom: none; }
.preview-name { font-weight: 500; color: #333; font-size: 13px; }
.preview-famille { color: #888; font-size: 11px; }
.preview-more { text-align: center; padding: 10px 0 5px; color: #32CD32; font-size: 12px; font-weight: 500; }

/* Sync History */
.sync-history { background: white; border-radius: 16px; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.sync-header h3 { font-size: 14px; color: #1a472a; display: flex; align-items: center; gap: 8px; margin: 0; }
.sync-date { color: #666; font-size: 13px; }
.sync-progress { display: flex; align-items: center; gap: 10px; min-width: 200px; }
.sync-progress .progress-bar { flex: 1; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden; }
.sync-progress .progress-fill { height: 100%; background: linear-gradient(90deg, #32CD32, #FFD700); border-radius: 3px; transition: width 0.3s; }
.sync-progress span { font-size: 12px; color: #32CD32; font-weight: 500; }

/* Toast */
.toast { position: fixed; bottom: 30px; right: 30px; padding: 14px 22px; border-radius: 12px; display: flex; align-items: center; gap: 12px; z-index: 1100; animation: slideInRight 0.3s; box-shadow: 0 10px 25px rgba(0,0,0,0.1); font-weight: 500; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.fa-spin { animation: fa-spin 2s infinite linear; }
@keyframes fa-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

@media (max-width: 768px) { .sidebar { width: 80px; } .sidebar-nav span, .sidebar-footer span, .logo-text, .user-info-sidebar, .nav-badge { display: none; } .nav-item { justify-content: center; } .main-content { margin-left: 80px; padding: 15px; } .stats-overview { grid-template-columns: repeat(2, 1fr); } .data-sections { grid-template-columns: 1fr; } .top-bar { flex-direction: column; align-items: flex-start; } .sync-history { flex-direction: column; text-align: center; } }
</style>
