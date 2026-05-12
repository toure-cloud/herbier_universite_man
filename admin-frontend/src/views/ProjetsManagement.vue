<template>
  <div class="management-page">
    <aside class="sidebar">
      <div class="sidebar-header"><div class="logo"><i class="fas fa-leaf"></i><span>Herbier Admin</span></div></div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item"><i class="fas fa-tachometer-alt"></i><span>Tableau de bord</span></router-link>
        <router-link to="/plantes" class="nav-item"><i class="fas fa-leaf"></i><span>Plantes</span></router-link>
        <router-link to="/equipe" class="nav-item"><i class="fas fa-users"></i><span>Équipe</span></router-link>
        <router-link to="/partenaires" class="nav-item"><i class="fas fa-handshake"></i><span>Partenaires</span></router-link>
        <router-link to="/slides" class="nav-item"><i class="fas fa-images"></i><span>Slides</span></router-link>
        <router-link to="/projets" class="nav-item active"><i class="fas fa-project-diagram"></i><span>Projets</span></router-link>
        <router-link to="/activites" class="nav-item"><i class="fas fa-chart-line"></i><span>Activités</span></router-link>
        <router-link to="/temoignages" class="nav-item"><i class="fas fa-comment-dots"></i><span>Témoignages</span></router-link>
        <router-link to="/publications" class="nav-item"><i class="fas fa-book"></i><span>Publications</span></router-link>
        <router-link to="/statistiques" class="nav-item"><i class="fas fa-chart-bar"></i><span>Statistiques</span></router-link>
        <router-link to="/settings" class="nav-item"><i class="fas fa-cog"></i><span>Paramètres</span></router-link>
      </nav>
      <div class="sidebar-footer"><button @click="logout" class="logout-btn"><i class="fas fa-sign-out-alt"></i><span>Déconnexion</span></button></div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="page-title"><h1>Gestion des Projets</h1><p>Ajoutez, modifiez ou supprimez des projets</p></div>
        <button @click="openModal" class="btn-primary"><i class="fas fa-plus"></i> Nouveau projet</button>
      </header>

      <!-- Filtres -->
      <div class="filters-bar">
        <div class="search-box"><i class="fas fa-search"></i><input type="text" v-model="searchQuery" placeholder="Rechercher un projet..."></div>
        <select v-model="filters.categorie" class="filter-select"><option value="">Toutes les catégories</option><option value="recherche">Recherche</option><option value="conservation">Conservation</option><option value="formation">Formation</option><option value="developpement">Développement</option></select>
        <select v-model="filters.statut" class="filter-select"><option value="">Tous les statuts</option><option value="termine">Terminé</option><option value="encours">En cours</option><option value="planifie">Planifié</option></select>
      </div>

      <!-- Liste des projets -->
      <div class="projects-grid">
        <div v-for="projet in filteredProjets" :key="projet.id" class="project-card">
          <div class="project-image"><img :src="getImageUrl(projet.image)" @error="handleImageError"><span class="project-category">{{ getCategorieLabel(projet.categorie) }}</span><span class="project-status" :class="projet.statut">{{ getStatutLabel(projet.statut) }}</span></div>
          <div class="project-info"><h3>{{ projet.titre }}</h3><p>{{ projet.description }}</p><div class="project-meta"><span><i class="fas fa-calendar"></i> {{ projet.annee }}</span><span><i class="fas fa-map-marker-alt"></i> {{ projet.lieu }}</span><span><i class="fas fa-users"></i> {{ projet.partenaires }} partenaires</span></div><div class="project-progress" v-if="projet.progression"><div class="progress-bar"><div class="progress-fill" :style="{ width: projet.progression + '%' }"></div></div><span>{{ projet.progression }}%</span></div><div class="project-actions"><button @click="editItem(projet)" class="btn-edit"><i class="fas fa-edit"></i> Modifier</button><button @click="deleteItem(projet)" class="btn-delete"><i class="fas fa-trash"></i> Supprimer</button></div></div>
        </div>
        <div v-if="filteredProjets.length === 0" class="empty">Aucun projet trouvé</div>
      </div>

      <!-- Modal Formulaire -->
      <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
        <div class="modal-content modal-large">
          <div class="modal-header"><h2>{{ editingId ? 'Modifier' : 'Ajouter' }} un projet</h2><button class="close" @click="closeModal"><i class="fas fa-times"></i></button></div>
          <form @submit.prevent="saveItem" class="modal-form">
            <div class="form-row"><div class="form-group"><label>Titre *</label><input type="text" v-model="form.titre" required></div><div class="form-group"><label>Catégorie *</label><select v-model="form.categorie" required><option value="recherche">Recherche</option><option value="conservation">Conservation</option><option value="formation">Formation</option><option value="developpement">Développement</option></select></div></div>
            <div class="form-row"><div class="form-group"><label>Statut *</label><select v-model="form.statut"><option value="termine">Terminé</option><option value="encours">En cours</option><option value="planifie">Planifié</option></select></div><div class="form-group"><label>Année/Période *</label><input type="text" v-model="form.annee" placeholder="2023-2024"></div></div>
            <div class="form-row"><div class="form-group"><label>Lieu *</label><input type="text" v-model="form.lieu"></div><div class="form-group"><label>Nombre de partenaires</label><input type="number" v-model="form.partenaires"></div></div>
            <div class="form-row"><div class="form-group"><label>Bénéficiaires</label><input type="text" v-model="form.beneficiaires"></div><div class="form-group"><label>Budget</label><input type="text" v-model="form.budget"></div></div>
            <div class="form-row"><div class="form-group"><label>Durée</label><input type="text" v-model="form.duree" placeholder="24 mois"></div><div class="form-group"><label>Impact</label><input type="text" v-model="form.impact"></div></div>
            <div class="form-group"><label>Progression (%)</label><input type="number" v-model="form.progression" min="0" max="100"></div>
            <div class="form-group"><label>Description courte *</label><textarea v-model="form.description" rows="3" required></textarea></div>
            <div class="form-group"><label>Description détaillée</label><textarea v-model="form.description_longue" rows="5"></textarea></div>
            <div class="form-group"><label>Objectifs</label><textarea v-model="form.objectifs" rows="3"></textarea></div>
            <div class="form-group"><label>Résultats obtenus</label><textarea v-model="form.resultats" rows="3"></textarea></div>
            <div class="form-group"><label>Tags (séparés par des virgules)</label><input type="text" v-model="form.tags" placeholder="biodiversité, conservation, recherche"></div>
            <div class="form-group"><label>Image principale (URL)</label><input type="text" v-model="form.image" placeholder="/src/images/..."></div>
            <div class="form-group"><label>Images galerie (URLs séparées par des virgules)</label><input type="text" v-model="imagesGalerieInput" placeholder="https://.../image1.jpg, https://.../image2.jpg"></div>
            <div class="form-group"><label><input type="checkbox" v-model="form.featured"> Projet à la une</label></div>
            <div class="modal-footer"><button type="button" class="btn-secondary" @click="closeModal">Annuler</button><button type="submit" class="btn-primary">Enregistrer</button></div>
          </form>
        </div>
      </div>

      <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'ProjetsManagement',
  data() {
    return {
      projets: [],
      searchQuery: '',
      filters: { categorie: '', statut: '' },
      showModal: false,
      editingId: null,
      imagesGalerieInput: '',
      form: { titre: '', categorie: 'recherche', statut: 'encours', annee: '', lieu: '', partenaires: 0, beneficiaires: '', budget: '', duree: '', impact: '', progression: 0, description: '', description_longue: '', objectifs: '', resultats: '', tags: '', image: '', images_galerie: [], featured: false },
      toastMessage: '', toastType: ''
    }
  },
  computed: {
    filteredProjets() {
      let filtered = this.projets
      if (this.searchQuery) { const q = this.searchQuery.toLowerCase(); filtered = filtered.filter(p => p.titre?.toLowerCase().includes(q) || p.description?.toLowerCase().includes(q)) }
      if (this.filters.categorie) filtered = filtered.filter(p => p.categorie === this.filters.categorie)
      if (this.filters.statut) filtered = filtered.filter(p => p.statut === this.filters.statut)
      return filtered
    }
  },
  mounted() { this.loadData() },
  methods: {
    async loadData() { try { const res = await axios.get('http://localhost:8001/api/herbier-data/'); this.projets = res.data.projets || [] } catch(e) { console.error(e) } },
    getImageUrl(url) { if (!url) return '/src/images/projet-placeholder.jpg'; if (url.startsWith('http')) return url; return url },
    handleImageError(e) { e.target.src = '/src/images/projet-placeholder.jpg' },
    getCategorieLabel(cat) { const labels = { recherche: '🔬 Recherche', conservation: '🌿 Conservation', formation: '📚 Formation', developpement: '💼 Développement' }; return labels[cat] || cat },
    getStatutLabel(statut) { const labels = { termine: '✅ Terminé', encours: '🔄 En cours', planifie: '📅 Planifié' }; return labels[statut] || statut },
    openModal() { this.editingId = null; this.form = { titre: '', categorie: 'recherche', statut: 'encours', annee: '', lieu: '', partenaires: 0, beneficiaires: '', budget: '', duree: '', impact: '', progression: 0, description: '', description_longue: '', objectifs: '', resultats: '', tags: '', image: '', images_galerie: [], featured: false }; this.imagesGalerieInput = ''; this.showModal = true },
    editItem(item) { this.editingId = item.id; this.form = { ...item }; this.imagesGalerieInput = (item.images_galerie || []).join(', '); this.showModal = true },
    async saveItem() {
      try {
        if (this.imagesGalerieInput) this.form.images_galerie = this.imagesGalerieInput.split(',').map(s => s.trim()).filter(s => s)
        else this.form.images_galerie = []
        let projets = [...this.projets]
        if (this.editingId) { const i = projets.findIndex(p => p.id === this.editingId); projets[i] = { ...this.form, id: this.editingId } }
        else { projets.push({ ...this.form, id: Date.now() }) }
        await axios.put('http://localhost:8001/api/herbier-data/', { ...(await axios.get('http://localhost:8001/api/herbier-data/')).data, projets })
        this.projets = projets; this.showToast(this.editingId ? 'Projet modifié' : 'Projet ajouté', 'success'); this.closeModal()
      } catch(e) { this.showToast('Erreur lors de la sauvegarde', 'error') }
    },
    async deleteItem(item) { if(confirm('Supprimer ce projet ?')) { const projets = this.projets.filter(p => p.id !== item.id); await axios.put('http://localhost:8001/api/herbier-data/', { ...(await axios.get('http://localhost:8001/api/herbier-data/')).data, projets }); this.projets = projets; this.showToast('Projet supprimé', 'success') } },
    closeModal() { this.showModal = false },
    showToast(type, msg) { this.toastType = type; this.toastMessage = msg; setTimeout(() => { this.toastMessage = '' }, 3000) },
    async logout() { await useAuthStore().logout(); this.$router.push('/login') }
  }
}
</script>

<style scoped>
.management-page { display: flex; min-height: 100vh; background: #f5f7fa; }
.sidebar { width: 280px; background: linear-gradient(180deg, #1a472a 0%, #0d3b0f 100%); color: white; position: fixed; height: 100vh; }
.sidebar-header { padding: 30px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.logo { display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: bold; }
.logo i { font-size: 28px; color: #FFD700; }
.sidebar-nav { flex: 1; padding: 20px 16px; display: flex; flex-direction: column; gap: 4px; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; color: rgba(255,255,255,0.8); text-decoration: none; border-radius: 12px; transition: all 0.3s; }
.nav-item:hover, .nav-item.active { background: #FFD700; color: #1a472a; }
.sidebar-footer { padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); }
.logout-btn { width: 100%; display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: rgba(255,255,255,0.1); border: none; border-radius: 12px; color: white; cursor: pointer; }
.main-content { flex: 1; margin-left: 280px; }
.top-bar { background: white; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.page-title h1 { font-size: 24px; color: #1a472a; }
.btn-primary { padding: 10px 20px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 10px; cursor: pointer; display: flex; align-items: center; gap: 8px; }
.filters-bar { display: flex; gap: 15px; padding: 20px 30px; background: white; margin: 20px; border-radius: 15px; flex-wrap: wrap; }
.search-box { flex: 1; position: relative; min-width: 200px; }
.search-box i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #999; }
.search-box input { width: 100%; padding: 10px 15px 10px 40px; border: 1px solid #ddd; border-radius: 10px; }
.filter-select { padding: 10px 15px; border: 1px solid #ddd; border-radius: 10px; background: white; }
.projects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; padding: 20px; }
.project-card { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: transform 0.3s; }
.project-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
.project-image { position: relative; height: 180px; overflow: hidden; }
.project-image img { width: 100%; height: 100%; object-fit: cover; }
.project-category { position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; }
.project-status { position: absolute; top: 10px; right: 10px; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
.project-status.termine { background: #28a745; color: white; }
.project-status.encours { background: #ffc107; color: #1a472a; }
.project-status.planifie { background: #17a2b8; color: white; }
.project-info { padding: 15px; }
.project-info h3 { font-size: 18px; color: #1a472a; margin-bottom: 8px; }
.project-info p { color: #666; font-size: 13px; line-height: 1.5; margin-bottom: 10px; }
.project-meta { display: flex; flex-wrap: wrap; gap: 10px; font-size: 12px; color: #888; margin-bottom: 10px; }
.project-meta i { margin-right: 3px; color: #32CD32; }
.project-progress { display: flex; align-items: center; gap: 10px; margin: 10px 0; }
.progress-bar { flex: 1; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #32CD32, #FFD700); border-radius: 3px; }
.project-progress span { font-size: 12px; color: #666; }
.project-actions { display: flex; gap: 10px; margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; }
.btn-edit, .btn-delete { padding: 6px 12px; border: none; border-radius: 5px; cursor: pointer; font-size: 12px; display: inline-flex; align-items: center; gap: 5px; }
.btn-edit { background: #ffc107; color: #1a472a; }
.btn-delete { background: #dc3545; color: white; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal.active { visibility: visible; opacity: 1; }
.modal-content { background: white; border-radius: 20px; width: 90%; max-width: 800px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 25px; border-bottom: 1px solid #eee; }
.modal-header h2 { color: #1a472a; }
.close { background: none; border: none; font-size: 20px; cursor: pointer; }
.modal-form { padding: 25px; }
.form-row { display: flex; gap: 20px; margin-bottom: 15px; flex-wrap: wrap; }
.form-group { flex: 1; display: flex; flex-direction: column; gap: 5px; min-width: 180px; }
.form-group label { font-weight: 500; color: #333; font-size: 13px; }
.form-group input, .form-group select, .form-group textarea { padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; width: 100%; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: #32CD32; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }
.btn-secondary { padding: 10px 20px; background: #f5f5f5; border: none; border-radius: 8px; cursor: pointer; }
.toast { position: fixed; bottom: 20px; right: 20px; padding: 12px 20px; border-radius: 10px; display: flex; align-items: center; gap: 10px; z-index: 1100; animation: slideIn 0.3s; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.empty { text-align: center; padding: 60px; color: #999; }
@media (max-width: 768px) { .sidebar { width: 80px; } .sidebar-nav span, .sidebar-footer span, .logo span { display: none; } .main-content { margin-left: 80px; } .projects-grid { grid-template-columns: 1fr; } .form-row { flex-direction: column; } }
</style>
