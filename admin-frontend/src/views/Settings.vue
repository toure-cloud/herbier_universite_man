<template>
  <div class="management-page" v-if="isAuthenticated">
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
        <router-link to="/herbier-data" class="nav-item"><i class="fas fa-database"></i><span>Données Herbier</span></router-link>
        <router-link to="/settings" class="nav-item active"><i class="fas fa-cog"></i><span>Paramètres</span><span class="nav-badge">Admin</span></router-link>
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
          <h1><i class="fas fa-cog"></i> Paramètres & Administration</h1>
          <p>Gérez les utilisateurs, les permissions et les activités du système</p>
        </div>
        <div class="user-badge">
          <i class="fas fa-shield-alt"></i>
          <span>Super Administrateur</span>
        </div>
      </header>

      <!-- Message si accès non autorisé (utilisateur non super admin) -->
      <div v-if="!isSuperAdmin" class="access-denied">
        <i class="fas fa-lock"></i>
        <h2>Accès restreint</h2>
        <p>Cette page est réservée aux Super Administrateurs.</p>
        <router-link to="/dashboard" class="btn-primary">Retour au tableau de bord</router-link>
      </div>

      <template v-else>
        <!-- Statistiques rapides -->
        <div class="stats-grid">
          <div class="stat-card"><div class="stat-icon blue"><i class="fas fa-users"></i></div><div class="stat-info"><h3>{{ totalUsers }}</h3><p>Utilisateurs</p></div></div>
          <div class="stat-card"><div class="stat-icon green"><i class="fas fa-history"></i></div><div class="stat-info"><h3>{{ totalActions }}</h3><p>Actions récentes</p></div></div>
          <div class="stat-card"><div class="stat-icon orange"><i class="fas fa-database"></i></div><div class="stat-info"><h3>{{ totalModifications }}</h3><p>Modifications</p></div></div>
        </div>

        <!-- Tabs de navigation -->
        <div class="settings-tabs">
          <button :class="['tab-btn', { active: activeTab === 'users' }]" @click="activeTab = 'users'"><i class="fas fa-users"></i> Utilisateurs</button>
          <button :class="['tab-btn', { active: activeTab === 'activities' }]" @click="activeTab = 'activities'"><i class="fas fa-history"></i> Activités</button>
          <button :class="['tab-btn', { active: activeTab === 'moderation' }]" @click="activeTab = 'moderation'"><i class="fas fa-gavel"></i> Modération</button>
          <button :class="['tab-btn', { active: activeTab === 'backup' }]" @click="activeTab = 'backup'"><i class="fas fa-database"></i> Sauvegarde</button>
          <button :class="['tab-btn', { active: activeTab === 'security' }]" @click="activeTab = 'security'"><i class="fas fa-shield-alt"></i> Sécurité</button>
        </div>

        <!-- Onglet Utilisateurs -->
        <div v-show="activeTab === 'users'" class="tab-content">
          <div class="section-header"><h3><i class="fas fa-users"></i> Gestion des utilisateurs</h3><button @click="openAddUserModal" class="btn-primary"><i class="fas fa-plus"></i> Ajouter un utilisateur</button></div>
          
          <div class="users-table">
            <table>
              <thead><tr><th>Avatar</th><th>Nom</th><th>Email</th><th>Téléphone</th><th>Rôle</th><th>Statut</th><th>Dernière connexion</th><th>Actions</th></tr></thead>
              <tbody>
                <tr v-for="userItem in users" :key="userItem.id">
                  <td><div class="user-avatar-small">{{ userItem.nom?.charAt(0) || 'U' }}</div></td>
                  <td><strong>{{ userItem.nom }}</strong></td>
                  <td>{{ userItem.email }}</td>
                  <td>{{ userItem.telephone }}</td>
                  <td><span class="role-badge" :class="{ admin: userItem.is_superuser }">{{ userItem.is_superuser ? 'Super Admin' : 'Utilisateur' }}</span></td>
                  <td><span class="status-badge" :class="{ active: userItem.is_active }">{{ userItem.is_active ? 'Actif' : 'Inactif' }}</span></td>
                  <td>{{ formatDate(userItem.last_login) }}</td>
                  <td class="actions"><button @click="editUser(userItem)" class="btn-edit"><i class="fas fa-edit"></i></button><button @click="deleteUser(userItem)" class="btn-delete" :disabled="userItem.is_superuser && userItem.id === currentUserId"><i class="fas fa-trash"></i></button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Onglet Activités -->
        <div v-show="activeTab === 'activities'" class="tab-content">
          <div class="section-header"><h3><i class="fas fa-history"></i> Historique des activités</h3><button @click="clearActivities" class="btn-secondary"><i class="fas fa-trash-alt"></i> Vider l'historique</button></div>
          <div class="activities-list">
            <div v-for="activity in activities" :key="activity.id" class="activity-log">
              <div class="log-icon" :class="activity.type"><i :class="activity.icon"></i></div>
              <div class="log-details"><p class="log-message">{{ activity.message }}</p><span class="log-date">{{ formatDate(activity.created_at) }}</span></div>
              <div class="log-user"><i class="fas fa-user"></i> {{ activity.user_name }}</div>
              <button @click="deleteActivity(activity)" class="log-delete"><i class="fas fa-times"></i></button>
            </div>
            <div v-if="activities.length === 0" class="empty"><i class="fas fa-inbox"></i> Aucune activité enregistrée</div>
          </div>
        </div>

        <!-- Onglet Modération -->
        <div v-show="activeTab === 'moderation'" class="tab-content">
          <div class="section-header"><h3><i class="fas fa-gavel"></i> Modération du contenu</h3></div>
          
          <div class="moderation-section">
            <h4><i class="fas fa-leaf"></i> Plantes en attente de validation</h4>
            <div class="moderation-list">
              <div v-for="plant in pendingPlants" :key="plant.id" class="moderation-item">
                <img :src="plant.image || '/src/images/placeholder.jpg'" class="moderation-image" @error="e=>e.target.src='/src/images/placeholder.jpg'">
                <div class="moderation-info"><strong>{{ plant.nom }}</strong> - {{ plant.famille }}<br><small>Ajouté par: {{ plant.created_by || 'Inconnu' }}</small></div>
                <div class="moderation-actions"><button @click="approvePlant(plant)" class="btn-approve"><i class="fas fa-check"></i> Approuver</button><button @click="rejectPlant(plant)" class="btn-reject"><i class="fas fa-times"></i> Rejeter</button></div>
              </div>
              <div v-if="pendingPlants.length === 0" class="empty">Aucune plante en attente</div>
            </div>
          </div>

          <div class="moderation-section">
            <h4><i class="fas fa-comment-dots"></i> Témoignages en attente</h4>
            <div class="moderation-list">
              <div v-for="testimonial in pendingTestimonials" :key="testimonial.id" class="moderation-item">
                <div class="moderation-info"><strong>{{ testimonial.nom }}</strong> - {{ testimonial.organisation }}<br><small>{{ testimonial.texte }}</small></div>
                <div class="moderation-actions"><button @click="approveTestimonial(testimonial)" class="btn-approve"><i class="fas fa-check"></i> Publier</button><button @click="rejectTestimonial(testimonial)" class="btn-reject"><i class="fas fa-times"></i> Refuser</button></div>
              </div>
              <div v-if="pendingTestimonials.length === 0" class="empty">Aucun témoignage en attente</div>
            </div>
          </div>
        </div>

        <!-- Onglet Sauvegarde -->
        <div v-show="activeTab === 'backup'" class="tab-content">
          <div class="section-header"><h3><i class="fas fa-database"></i> Sauvegarde & Restauration</h3></div>
          <div class="backup-cards">
            <div class="backup-card"><i class="fas fa-download"></i><h4>Exporter les données</h4><p>Exportez toutes les données de l'herbier au format JSON</p><button @click="exportData" class="btn-primary"><i class="fas fa-download"></i> Exporter</button></div>
            <div class="backup-card"><i class="fas fa-upload"></i><h4>Importer des données</h4><p>Importez des données depuis un fichier JSON</p><input type="file" ref="importFile" accept=".json" @change="importData" style="display:none"><button @click="$refs.importFile.click()" class="btn-secondary"><i class="fas fa-upload"></i> Importer</button></div>
            <div class="backup-card"><i class="fas fa-history"></i><h4>Restaurer une sauvegarde</h4><p>Restaurez une version précédente des données</p><select v-model="selectedBackup" class="backup-select"><option value="">Sélectionner une sauvegarde</option><option v-for="b in backups" :key="b.id" :value="b.id">{{ b.name }} - {{ b.date }}</option></select><button @click="restoreBackup" class="btn-warning"><i class="fas fa-undo-alt"></i> Restaurer</button></div>
          </div>
        </div>

        <!-- Onglet Sécurité -->
        <div v-show="activeTab === 'security'" class="tab-content">
          <div class="section-header"><h3><i class="fas fa-shield-alt"></i> Sécurité & Permissions</h3></div>
          <div class="security-settings">
            <div class="security-card"><div class="security-icon"><i class="fas fa-user-lock"></i></div><div class="security-info"><h4>Changer mon mot de passe</h4><p>Mettez à jour votre mot de passe régulièrement</p><button @click="openChangePasswordModal" class="btn-primary">Changer le mot de passe</button></div></div>
            <div class="security-card"><div class="security-icon"><i class="fas fa-history"></i></div><div class="security-info"><h4>Historique des connexions</h4><p>Consultez toutes les connexions à votre compte</p><button @click="viewLoginHistory" class="btn-secondary">Voir l'historique</button></div></div>
            <div class="security-card"><div class="security-icon"><i class="fas fa-sign-out-alt"></i></div><div class="security-info"><h4>Sessions actives</h4><p>Gérez vos sessions actives sur tous les appareils</p><button @click="terminateAllSessions" class="btn-warning">Terminer toutes les sessions</button></div></div>
          </div>
        </div>
      </template>

      <!-- Modals -->
      <div class="modal" :class="{ active: showUserModal }" @click.self="closeUserModal">
        <div class="modal-content"><div class="modal-header"><h2>{{ editingUser ? 'Modifier' : 'Ajouter' }} un utilisateur</h2><button class="close" @click="closeUserModal"><i class="fas fa-times"></i></button></div>
        <form @submit.prevent="saveUser" class="modal-form"><div class="form-row"><div class="form-group"><label>Nom complet</label><input type="text" v-model="userForm.nom" required></div><div class="form-group"><label>Email</label><input type="email" v-model="userForm.email" required></div></div>
        <div class="form-row"><div class="form-group"><label>Téléphone</label><input type="text" v-model="userForm.telephone"></div><div class="form-group"><label>Rôle</label><select v-model="userForm.is_superuser"><option :value="false">Utilisateur</option><option :value="true">Super Administrateur</option></select></div></div>
        <div class="form-row" v-if="!editingUser"><div class="form-group"><label>Mot de passe</label><input type="password" v-model="userForm.password"></div><div class="form-group"><label>Confirmer</label><input type="password" v-model="userForm.password2"></div></div>
        <div class="modal-footer"><button type="button" class="btn-secondary" @click="closeUserModal">Annuler</button><button type="submit" class="btn-primary">Enregistrer</button></div></form></div>
      </div>

      <div class="modal" :class="{ active: showPasswordModal }" @click.self="closePasswordModal">
        <div class="modal-content"><div class="modal-header"><h2>Changer le mot de passe</h2><button class="close" @click="closePasswordModal"><i class="fas fa-times"></i></button></div>
        <form @submit.prevent="changePassword" class="modal-form"><div class="form-group"><label>Ancien mot de passe</label><input type="password" v-model="passwordForm.old" required></div><div class="form-group"><label>Nouveau mot de passe</label><input type="password" v-model="passwordForm.new" required></div><div class="form-group"><label>Confirmer</label><input type="password" v-model="passwordForm.confirm" required></div>
        <div class="modal-footer"><button type="button" class="btn-secondary" @click="closePasswordModal">Annuler</button><button type="submit" class="btn-primary">Changer</button></div></form></div>
      </div>

      <div class="modal-confirm" :class="{ active: showConfirmModal }"><div class="modal-overlay" @click="closeConfirmModal"></div><div class="modal-content"><div class="modal-icon warning"><i class="fas fa-exclamation-triangle"></i></div><h3>Confirmation</h3><p>{{ confirmMessage }}</p><div class="modal-buttons"><button class="btn-cancel" @click="closeConfirmModal">Annuler</button><button class="btn-confirm" @click="executeConfirmAction">Confirmer</button></div></div></div>

      <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
    </main>
  </div>

  <!-- Page de chargement pendant la vérification -->
  <div v-else class="loading-screen">
    <div class="spinner"></div>
    <p>Vérification de l'authentification...</p>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'Settings',
  data() {
    return {
      activeTab: 'users',
      users: [],
      activities: [],
      pendingPlants: [],
      pendingTestimonials: [],
      backups: [],
      totalUsers: 0,
      totalActions: 0,
      totalModifications: 0,
      currentUserId: null,
      showUserModal: false,
      showPasswordModal: false,
      showConfirmModal: false,
      editingUser: null,
      confirmAction: null,
      confirmMessage: '',
      selectedBackup: '',
      userForm: { nom: '', email: '', telephone: '', is_superuser: false, password: '', password2: '' },
      passwordForm: { old: '', new: '', confirm: '' },
      toastMessage: '', toastType: '', user: null,
      isAuthenticated: false,
      isSuperAdmin: false,
      authChecked: false
    }
  },
  computed: {
    userInitials() { return this.user?.nom ? this.user.nom.split(' ').map(n => n[0]).join('').toUpperCase() : 'AD' }
  },
  async mounted() {
    const authStore = useAuthStore()
    
    // Vérifier l'authentification
    if (!authStore.isAuthenticated) {
      this.$router.push('/login')
      return
    }
    
    this.isAuthenticated = true
    this.user = authStore.user
    this.currentUserId = authStore.user?.id
    
    // Vérifier si l'utilisateur est Super Admin
    this.isSuperAdmin = authStore.user?.is_superuser === true
    
    if (this.isSuperAdmin) {
      await this.loadData()
    }
  },
  methods: {
    async loadData() { await Promise.all([this.loadUsers(), this.loadActivities(), this.loadPendingContent(), this.loadBackups()]) },
    async loadUsers() { try { const res = await axios.get('http://localhost:8001/api/users/'); this.users = res.data; this.totalUsers = this.users.length } catch(e) { console.error(e) } },
    async loadActivities() { try { const res = await axios.get('http://localhost:8001/api/activities/'); this.activities = res.data; this.totalActions = this.activities.length } catch(e) { console.error(e) } },
    async loadPendingContent() { try { const data = await axios.get('http://localhost:8001/api/herbier-data/'); this.pendingPlants = (data.data.plantes || []).filter(p => !p.publie).slice(0, 10); this.pendingTestimonials = (data.data.temoignages || []).filter(t => !t.publie).slice(0, 10) } catch(e) { console.error(e) } },
    async loadBackups() { try { const res = await axios.get('http://localhost:8001/api/backups/'); this.backups = res.data } catch(e) { console.error(e) } },
    formatDate(d) { if (!d) return 'Jamais'; return new Date(d).toLocaleString('fr-FR') },
    openAddUserModal() { this.editingUser = null; this.userForm = { nom: '', email: '', telephone: '', is_superuser: false, password: '', password2: '' }; this.showUserModal = true },
    editUser(u) { this.editingUser = u; this.userForm = { ...u, password: '', password2: '' }; this.showUserModal = true },
    async saveUser() { try { if (this.editingUser) { await axios.put(`http://localhost:8001/api/users/${this.editingUser.id}/`, this.userForm); this.showToast('Utilisateur modifié', 'success') } else { await axios.post('http://localhost:8001/api/users/', this.userForm); this.showToast('Utilisateur créé', 'success') } this.loadUsers(); this.closeUserModal() } catch(e) { this.showToast('Erreur', 'error') } },
    async deleteUser(u) { if (u.id === this.currentUserId) { this.showToast('Vous ne pouvez pas vous supprimer vous-même', 'error'); return } this.confirm('Supprimer cet utilisateur ?', async () => { await axios.delete(`http://localhost:8001/api/users/${u.id}/`); this.loadUsers(); this.showToast('Utilisateur supprimé', 'success') }) },
    async deleteActivity(a) { this.confirm('Supprimer cette activité ?', async () => { await axios.delete(`http://localhost:8001/api/activities/${a.id}/`); this.loadActivities(); this.showToast('Activité supprimée', 'success') }) },
    async clearActivities() { this.confirm('Vider tout l\'historique ?', async () => { await axios.delete('http://localhost:8001/api/activities/clear/'); this.loadActivities(); this.showToast('Historique vidé', 'success') }) },
    async approvePlant(p) { this.confirm('Approuver cette plante ?', async () => { p.publie = true; await this.updatePlant(p); this.loadPendingContent(); this.showToast('Plante approuvée', 'success') }) },
    async rejectPlant(p) { this.confirm('Rejeter cette plante ?', async () => { await axios.delete(`http://localhost:8001/api/plantes/${p.id}/`); this.loadPendingContent(); this.showToast('Plante rejetée', 'success') }) },
    async approveTestimonial(t) { this.confirm('Publier ce témoignage ?', async () => { t.publie = true; await this.updateTestimonial(t); this.loadPendingContent(); this.showToast('Témoignage publié', 'success') }) },
    async rejectTestimonial(t) { this.confirm('Refuser ce témoignage ?', async () => { await axios.delete(`http://localhost:8001/api/temoignages/${t.id}/`); this.loadPendingContent(); this.showToast('Témoignage refusé', 'success') }) },
    async exportData() { try { const data = await axios.get('http://localhost:8001/api/herbier-data/'); const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `herbier_backup_${new Date().toISOString()}.json`; a.click(); URL.revokeObjectURL(url); this.showToast('Export réussi', 'success') } catch(e) { this.showToast('Erreur export', 'error') } },
    async importData(e) { const file = e.target.files[0]; if (!file) return; const reader = new FileReader(); reader.onload = async (ev) => { try { const data = JSON.parse(ev.target.result); await axios.put('http://localhost:8001/api/herbier-data/', data); this.showToast('Import réussi', 'success'); this.loadData() } catch(err) { this.showToast('Erreur import', 'error') } }; reader.readAsText(file) },
    async restoreBackup() { if (!this.selectedBackup) { this.showToast('Sélectionnez une sauvegarde', 'error'); return } this.confirm('Restaurer cette sauvegarde ?', async () => { await axios.post('http://localhost:8001/api/restore-backup/', { backup_id: this.selectedBackup }); this.showToast('Restauration réussie', 'success'); this.loadData() }) },
    async changePassword() { if (this.passwordForm.new !== this.passwordForm.confirm) { this.showToast('Les mots de passe ne correspondent pas', 'error'); return } try { await axios.post('http://localhost:8001/api/change-password/', { old_password: this.passwordForm.old, new_password: this.passwordForm.new }); this.showToast('Mot de passe changé', 'success'); this.closePasswordModal() } catch(e) { this.showToast('Erreur', 'error') } },
    async viewLoginHistory() { try { const res = await axios.get('http://localhost:8001/api/login-history/'); this.activities = res.data; this.activeTab = 'activities'; this.showToast('Historique chargé', 'success') } catch(e) { console.error(e) } },
    async terminateAllSessions() { this.confirm('Terminer toutes les sessions ? Vous devrez vous reconnecter.', async () => { await axios.post('http://localhost:8001/api/terminate-sessions/'); localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); window.location.href = '/login' }) },
    openChangePasswordModal() { this.passwordForm = { old: '', new: '', confirm: '' }; this.showPasswordModal = true },
    closePasswordModal() { this.showPasswordModal = false },
    closeUserModal() { this.showUserModal = false },
    confirm(msg, action) { this.confirmMessage = msg; this.confirmAction = action; this.showConfirmModal = true },
    closeConfirmModal() { this.showConfirmModal = false; this.confirmAction = null },
    executeConfirmAction() { if (this.confirmAction) this.confirmAction(); this.closeConfirmModal() },
    showToast(t, m) { this.toastType = t; this.toastMessage = m; setTimeout(() => { this.toastMessage = '' }, 3000) },
    async updatePlant(p) { const data = await axios.get('http://localhost:8001/api/herbier-data/'); const plantes = data.data.plantes.map(pl => pl.id === p.id ? p : pl); await axios.put('http://localhost:8001/api/herbier-data/', { ...data.data, plantes }) },
    async updateTestimonial(t) { const data = await axios.get('http://localhost:8001/api/herbier-data/'); const temoignages = data.data.temoignages.map(tm => tm.id === t.id ? t : tm); await axios.put('http://localhost:8001/api/herbier-data/', { ...data.data, temoignages }) },
    confirmLogout() { if (confirm('Déconnexion ?')) { useAuthStore().logout(); this.$router.push('/login') } }
  }
}
</script>

<style scoped>
/* Styles identiques à la version précédente... */
/* (Conserver tous les styles du fichier précédent) */
.loading-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%); color: white; }
.spinner { width: 50px; height: 50px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #FFD700; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }
@keyframes spin { to { transform: rotate(360deg); } }
.access-denied { text-align: center; padding: 60px; background: white; border-radius: 20px; margin: 40px; }
.access-denied i { font-size: 60px; color: #dc3545; margin-bottom: 20px; }
.access-denied h2 { color: #1a472a; margin-bottom: 10px; }
.access-denied p { color: #666; margin-bottom: 20px; }
</style>
