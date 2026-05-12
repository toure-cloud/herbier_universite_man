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
        <router-link to="/projets" class="nav-item"><i class="fas fa-project-diagram"></i><span>Projets</span></router-link>
        <router-link to="/activites" class="nav-item"><i class="fas fa-chart-line"></i><span>Activités</span></router-link>
        <router-link to="/temoignages" class="nav-item"><i class="fas fa-comment-dots"></i><span>Témoignages</span></router-link>
        <router-link to="/publications" class="nav-item active"><i class="fas fa-book"></i><span>Publications</span></router-link>
        <router-link to="/statistiques" class="nav-item"><i class="fas fa-chart-bar"></i><span>Statistiques</span></router-link>
        <router-link to="/settings" class="nav-item"><i class="fas fa-cog"></i><span>Paramètres</span></router-link>
      </nav>
      <div class="sidebar-footer"><button @click="logout" class="logout-btn"><i class="fas fa-sign-out-alt"></i><span>Déconnexion</span></button></div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="page-title"><h1>Gestion des Publications</h1><p>Ajoutez, modifiez ou supprimez des publications scientifiques</p></div>
        <button @click="openModal" class="btn-primary"><i class="fas fa-plus"></i> Nouvelle publication</button>
      </header>

      <div class="filters-bar">
        <div class="search-box"><i class="fas fa-search"></i><input type="text" v-model="searchQuery" placeholder="Rechercher une publication..."></div>
        <div class="filter-group"><label>Année :</label><select v-model="filters.annee" class="filter-select"><option value="">Toutes</option><option v-for="a in anneesDisponibles" :key="a" :value="a">{{ a }}</option></select></div>
      </div>

      <div class="publications-list">
        <div v-for="pub in filteredPublications" :key="pub.id" class="publication-card">
          <div class="pub-icon"><i class="fas fa-file-alt"></i></div>
          <div class="pub-content">
            <h3>{{ pub.titre }}</h3>
            <p class="pub-auteurs"><i class="fas fa-user-edit"></i> {{ pub.auteurs }}</p>
            <p class="pub-meta"><span><i class="fas fa-book"></i> {{ pub.journal }}</span><span><i class="fas fa-calendar"></i> {{ pub.annee }}</span><span v-if="pub.doi"><i class="fas fa-doi"></i> DOI: {{ pub.doi }}</span></p>
            <p class="pub-resume" v-if="pub.resume">{{ pub.resume }}</p>
            <div class="pub-links"><a v-if="pub.lien" :href="pub.lien" target="_blank" class="pub-link"><i class="fas fa-external-link-alt"></i> Voir l'article</a></div>
          </div>
          <div class="pub-actions"><button @click="editItem(pub)" class="btn-edit"><i class="fas fa-edit"></i></button><button @click="deleteItem(pub)" class="btn-delete"><i class="fas fa-trash"></i></button></div>
        </div>
        <div v-if="filteredPublications.length === 0" class="empty">Aucune publication trouvée</div>
      </div>

      <!-- Modal Formulaire -->
      <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
        <div class="modal-content modal-large">
          <div class="modal-header"><h2>{{ editingId ? 'Modifier' : 'Ajouter' }} une publication</h2><button class="close" @click="closeModal"><i class="fas fa-times"></i></button></div>
          <form @submit.prevent="saveItem" class="modal-form">
            <div class="form-group"><label>Titre *</label><input type="text" v-model="form.titre" required></div>
            <div class="form-group"><label>Auteurs *</label><input type="text" v-model="form.auteurs" required placeholder="Kouassi J., Konan M., Yao P."></div>
            <div class="form-row"><div class="form-group"><label>Journal / Revue *</label><input type="text" v-model="form.journal" required></div><div class="form-group"><label>Année *</label><input type="number" v-model="form.annee" required min="1900" :max="new Date().getFullYear()"></div></div>
            <div class="form-row"><div class="form-group"><label>DOI</label><input type="text" v-model="form.doi" placeholder="10.xxxx/xxxxx"></div><div class="form-group"><label>Lien URL</label><input type="url" v-model="form.lien" placeholder="https://..."></div></div>
            <div class="form-group"><label>Résumé</label><textarea v-model="form.resume" rows="5"></textarea></div>
            <div class="form-group"><label>Ordre d'affichage</label><input type="number" v-model="form.ordre"></div>
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
  name: 'PublicationsManagement',
  data() {
    return {
      publications: [],
      searchQuery: '',
      filters: { annee: '' },
      showModal: false,
      editingId: null,
      form: { titre: '', auteurs: '', journal: '', annee: new Date().getFullYear(), doi: '', lien: '', resume: '', ordre: 0 },
      toastMessage: '', toastType: ''
    }
  },
  computed: {
    anneesDisponibles() { return [...new Set(this.publications.map(p => p.annee).filter(Boolean))].sort((a,b) => b - a) },
    filteredPublications() {
      let filtered = this.publications
      if (this.searchQuery) { const q = this.searchQuery.toLowerCase(); filtered = filtered.filter(p => p.titre?.toLowerCase().includes(q) || p.auteurs?.toLowerCase().includes(q) || p.journal?.toLowerCase().includes(q)) }
      if (this.filters.annee) filtered = filtered.filter(p => p.annee == this.filters.annee)
      return filtered.sort((a,b) => (b.annee || 0) - (a.annee || 0))
    }
  },
  mounted() { this.loadData() },
  methods: {
    async loadData() { try { const res = await axios.get('http://localhost:8001/api/herbier-data/'); this.publications = res.data.publications || [] } catch(e) { console.error(e) } },
    openModal() { this.editingId = null; this.form = { titre: '', auteurs: '', journal: '', annee: new Date().getFullYear(), doi: '', lien: '', resume: '', ordre: 0 }; this.showModal = true },
    editItem(item) { this.editingId = item.id; this.form = { ...item }; this.showModal = true },
    async saveItem() {
      try {
        let publications = [...this.publications]
        if (this.editingId) { const i = publications.findIndex(p => p.id === this.editingId); publications[i] = { ...this.form, id: this.editingId } }
        else { publications.push({ ...this.form, id: Date.now() }) }
        await axios.put('http://localhost:8001/api/herbier-data/', { ...(await axios.get('http://localhost:8001/api/herbier-data/')).data, publications })
        this.publications = publications; this.showToast(this.editingId ? 'Publication modifiée' : 'Publication ajoutée', 'success'); this.closeModal()
      } catch(e) { this.showToast('Erreur lors de la sauvegarde', 'error') }
    },
    async deleteItem(item) { if(confirm('Supprimer cette publication ?')) { const publications = this.publications.filter(p => p.id !== item.id); await axios.put('http://localhost:8001/api/herbier-data/', { ...(await axios.get('http://localhost:8001/api/herbier-data/')).data, publications }); this.publications = publications; this.showToast('Publication supprimée', 'success') } },
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
.filters-bar { display: flex; justify-content: space-between; align-items: center; padding: 20px 30px; background: white; margin: 20px; border-radius: 15px; flex-wrap: wrap; gap: 15px; }
.search-box { flex: 1; position: relative; max-width: 400px; }
.search-box i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #999; }
.search-box input { width: 100%; padding: 10px 15px 10px 40px; border: 1px solid #ddd; border-radius: 10px; }
.filter-group { display: flex; align-items: center; gap: 10px; }
.filter-select { padding: 10px 15px; border: 1px solid #ddd; border-radius: 10px; background: white; }
.publications-list { display: flex; flex-direction: column; gap: 15px; padding: 20px; }
.publication-card { display: flex; gap: 20px; background: white; border-radius: 15px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: all 0.3s; }
.publication-card:hover { transform: translateX(5px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
.pub-icon { flex-shrink: 0; width: 60px; height: 60px; background: #e8f5e8; border-radius: 15px; display: flex; align-items: center; justify-content: center; }
.pub-icon i { font-size: 30px; color: #32CD32; }
.pub-content { flex: 1; }
.pub-content h3 { color: #1a472a; margin-bottom: 8px; font-size: 16px; }
.pub-auteurs { color: #666; font-size: 13px; margin-bottom: 8px; }
.pub-auteurs i { color: #32CD32; margin-right: 5px; }
.pub-meta { display: flex; flex-wrap: wrap; gap: 15px; font-size: 12px; color: #888; margin-bottom: 10px; }
.pub-meta i { color: #32CD32; margin-right: 4px; }
.pub-resume { color: #555; font-size: 13px; line-height: 1.5; margin-top: 10px; }
.pub-links { margin-top: 12px; }
.pub-link { color: #32CD32; text-decoration: none; font-size: 13px; display: inline-flex; align-items: center; gap: 5px; }
.pub-link:hover { text-decoration: underline; }
.pub-actions { display: flex; gap: 8px; align-items: flex-start; }
.btn-edit, .btn-delete { padding: 8px 12px; border: none; border-radius: 8px; cursor: pointer; }
.btn-edit { background: #ffc107; color: #1a472a; }
.btn-delete { background: #dc3545; color: white; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal.active { visibility: visible; opacity: 1; }
.modal-content { background: white; border-radius: 20px; width: 90%; max-width: 700px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 25px; border-bottom: 1px solid #eee; }
.modal-header h2 { color: #1a472a; }
.close { background: none; border: none; font-size: 20px; cursor: pointer; }
.modal-form { padding: 25px; }
.form-row { display: flex; gap: 20px; margin-bottom: 15px; flex-wrap: wrap; }
.form-group { flex: 1; display: flex; flex-direction: column; gap: 5px; margin-bottom: 15px; }
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
@media (max-width: 768px) { .sidebar { width: 80px; } .sidebar-nav span, .sidebar-footer span, .logo span { display: none; } .main-content { margin-left: 80px; } .publication-card { flex-direction: column; } .pub-actions { align-self: flex-end; } .form-row { flex-direction: column; } }
</style>
