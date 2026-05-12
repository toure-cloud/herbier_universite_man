<template>
  <div class="management-page">
    <aside class="sidebar">
      <div class="sidebar-header"><div class="logo"><i class="fas fa-leaf"></i><span>Herbier Admin</span></div></div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item"><i class="fas fa-tachometer-alt"></i><span>Tableau de bord</span></router-link>
        <router-link to="/plantes" class="nav-item"><i class="fas fa-leaf"></i><span>Plantes</span></router-link>
        <router-link to="/equipe" class="nav-item active"><i class="fas fa-users"></i><span>Équipe</span></router-link>
        <router-link to="/partenaires" class="nav-item"><i class="fas fa-handshake"></i><span>Partenaires</span></router-link>
        <router-link to="/slides" class="nav-item"><i class="fas fa-images"></i><span>Slides</span></router-link>
        <router-link to="/projets" class="nav-item"><i class="fas fa-project-diagram"></i><span>Projets</span></router-link>
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
        <div class="page-title"><h1>Gestion de l'équipe</h1><p>Ajoutez, modifiez ou supprimez des membres de l'équipe</p></div>
        <button @click="openModal" class="btn-primary"><i class="fas fa-plus"></i> Nouveau membre</button>
      </header>

      <div class="data-table">
        <table>
          <thead><tr><th>Photo</th><th>Nom</th><th>Poste</th><th>Email</th><th>Spécialité</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="membre in equipe" :key="membre.id">
              <td><img :src="membre.photo || '/src/images/avatar.jpg'" class="table-image" @error="handleImageError"></td>
              <td><strong>{{ membre.nom }}</strong></td>
              <td>{{ membre.poste }}</td>
              <td>{{ membre.email || '-' }}</td>
              <td>{{ membre.specialite || '-' }}</td>
              <td class="actions"><button @click="editItem(membre)" class="btn-edit"><i class="fas fa-edit"></i></button><button @click="deleteItem(membre)" class="btn-delete"><i class="fas fa-trash"></i></button></td>
            </tr>
            <tr v-if="equipe.length === 0"><td colspan="6" class="empty">Aucun membre trouvé</td></tr>
          </tbody>
        </table>
      </div>

      <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header"><h2>{{ editingId ? 'Modifier' : 'Ajouter' }} un membre</h2><button class="close" @click="closeModal"><i class="fas fa-times"></i></button></div>
          <form @submit.prevent="saveItem">
            <div class="form-group"><label>Nom *</label><input type="text" v-model="form.nom" required></div>
            <div class="form-group"><label>Poste *</label><input type="text" v-model="form.poste" required></div>
            <div class="form-group"><label>Email</label><input type="email" v-model="form.email"></div>
            <div class="form-group"><label>Spécialité</label><input type="text" v-model="form.specialite"></div>
            <div class="form-group"><label>Téléphone</label><input type="text" v-model="form.telephone"></div>
            <div class="form-group"><label>Photo URL</label><input type="text" v-model="form.photo" placeholder="/src/images/..."></div>
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
  name: 'EquipeManagement',
  data() {
    return { equipe: [], showModal: false, editingId: null, form: { nom: '', poste: '', email: '', specialite: '', telephone: '', photo: '' }, toastMessage: '', toastType: '' }
  },
  mounted() { this.loadData() },
  methods: {
    async loadData() { try { const res = await axios.get('http://localhost:8001/api/herbier-data/'); this.equipe = res.data.equipe || [] } catch(e) { console.error(e) } },
    openModal() { this.editingId = null; this.form = { nom: '', poste: '', email: '', specialite: '', telephone: '', photo: '' }; this.showModal = true },
    editItem(item) { this.editingId = item.id; this.form = { ...item }; this.showModal = true },
    async saveItem() {
      try {
        let equipe = [...this.equipe]
        if (this.editingId) { const i = equipe.findIndex(e => e.id === this.editingId); equipe[i] = { ...this.form, id: this.editingId } }
        else { equipe.push({ ...this.form, id: Date.now() }) }
        await axios.put('http://localhost:8001/api/herbier-data/', { ...(await axios.get('http://localhost:8001/api/herbier-data/')).data, equipe })
        this.equipe = equipe; this.showToast('success', this.editingId ? 'Membre modifié' : 'Membre ajouté'); this.closeModal()
      } catch(e) { this.showToast('error', 'Erreur') }
    },
    async deleteItem(item) { if(confirm('Supprimer ce membre ?')) { const equipe = this.equipe.filter(e => e.id !== item.id); await axios.put('http://localhost:8001/api/herbier-data/', { ...(await axios.get('http://localhost:8001/api/herbier-data/')).data, equipe }); this.equipe = equipe; this.showToast('success', 'Membre supprimé') } },
    closeModal() { this.showModal = false },
    showToast(type, msg) { this.toastType = type; this.toastMessage = msg; setTimeout(() => { this.toastMessage = '' }, 3000) },
    handleImageError(e) { e.target.src = '/src/images/avatar.jpg' },
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
.btn-primary { padding: 10px 20px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 10px; cursor: pointer; }
.data-table { background: white; margin: 20px; border-radius: 15px; overflow: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f8f9fa; font-weight: 600; color: #1a472a; }
.table-image { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; }
.actions { display: flex; gap: 8px; }
.btn-edit, .btn-delete { padding: 6px 10px; border: none; border-radius: 5px; cursor: pointer; }
.btn-edit { background: #ffc107; }
.btn-delete { background: #dc3545; color: white; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal.active { visibility: visible; opacity: 1; }
.modal-content { background: white; border-radius: 20px; width: 90%; max-width: 500px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid #eee; }
.close { background: none; border: none; font-size: 20px; cursor: pointer; }
form { padding: 20px; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 5px; }
.form-group input { padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-secondary { padding: 10px 20px; background: #f5f5f5; border: none; border-radius: 8px; cursor: pointer; }
.toast { position: fixed; bottom: 20px; right: 20px; padding: 12px 20px; border-radius: 10px; display: flex; align-items: center; gap: 10px; z-index: 1100; animation: slideIn 0.3s; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.empty { text-align: center; padding: 40px; color: #999; }
@media (max-width: 768px) { .sidebar { width: 80px; } .sidebar-nav span, .sidebar-footer span, .logo span { display: none; } .main-content { margin-left: 80px; } }
</style>
