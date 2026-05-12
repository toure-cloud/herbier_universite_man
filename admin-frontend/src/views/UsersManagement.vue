<template>
  <div class="management-page">
    <aside class="sidebar"><div class="sidebar-header"><div class="logo"><div class="logo-icon"><i class="fas fa-leaf"></i></div><div class="logo-text"><span class="logo-title">Herbier Admin</span><span class="logo-subtitle">Université de Man</span></div></div></div>
      <nav class="sidebar-nav"><router-link to="/dashboard" class="nav-item"><i class="fas fa-tachometer-alt"></i><span>Dashboard</span></router-link><router-link to="/plantes" class="nav-item"><i class="fas fa-leaf"></i><span>Plantes</span></router-link><router-link to="/projets" class="nav-item"><i class="fas fa-project-diagram"></i><span>Projets</span></router-link><router-link to="/activites" class="nav-item"><i class="fas fa-chart-line"></i><span>Activités</span></router-link><router-link to="/users" class="nav-item active"><i class="fas fa-users"></i><span>Utilisateurs</span><span class="nav-badge">Admin</span></router-link><router-link to="/settings" class="nav-item"><i class="fas fa-cog"></i><span>Paramètres</span></router-link></nav>
      <div class="sidebar-footer"><div class="user-info-sidebar"><div class="user-avatar-sidebar">{{ userInitials }}</div><div class="user-details-sidebar"><span class="user-name-sidebar">{{ user?.nom || 'Admin' }}</span><span class="user-role">Super Admin</span></div></div><button @click="confirmLogout" class="logout-btn"><i class="fas fa-sign-out-alt"></i><span>Déconnexion</span></button></div>
    </aside>
    <main class="main-content">
      <header class="top-bar"><div class="page-title"><h1><i class="fas fa-users"></i> Gestion des utilisateurs</h1><p>Créez, modifiez ou supprimez des utilisateurs</p></div><button @click="openAddUserModal" class="btn-primary"><i class="fas fa-plus"></i> Nouvel utilisateur</button></header>
      <div class="stats-grid"><div class="stat-card"><div class="stat-icon blue"><i class="fas fa-users"></i></div><div class="stat-info"><h3>{{ users.length }}</h3><p>Utilisateurs</p></div></div><div class="stat-card"><div class="stat-icon green"><i class="fas fa-user-check"></i></div><div class="stat-info"><h3>{{ activeUsers }}</h3><p>Actifs</p></div></div><div class="stat-card"><div class="stat-icon orange"><i class="fas fa-user-shield"></i></div><div class="stat-info"><h3>{{ adminUsers }}</h3><p>Administrateurs</p></div></div></div>
      <div class="users-table">\n        <div v-for="u in users" :key="u.id" class="user-card"><div class="user-avatar-large">{{ u.nom?.charAt(0) || 'U' }}</div><div class="user-details"><h3>{{ u.nom }}</h3><p>{{ u.email }}</p><p class="user-phone">{{ u.telephone }}</p><div class="user-meta"><span class="role-badge" :class="{ admin: u.is_superuser }">{{ u.is_superuser ? 'Super Admin' : 'Utilisateur' }}</span><span class="status-badge" :class="{ active: u.is_active }">{{ u.is_active ? 'Actif' : 'Inactif' }}</span><span class="date-badge"><i class="fas fa-calendar"></i> Créé le {{ formatDate(u.date_joined) }}</span></div></div><div class="user-actions"><button @click="editUser(u)" class="btn-edit"><i class="fas fa-edit"></i> Modifier</button><button @click="toggleUserStatus(u)" class="btn-status" :class="{ active: u.is_active }"><i :class="u.is_active ? 'fas fa-ban' : 'fas fa-check'"></i> {{ u.is_active ? 'Désactiver' : 'Activer' }}</button><button @click="deleteUser(u)" class="btn-delete" :disabled="u.id === currentUserId"><i class="fas fa-trash"></i> Supprimer</button></div></div><div v-if="users.length===0" class="empty">Aucun utilisateur</div></div>
      <div class="modal" :class="{ active: showModal }" @click.self="closeModal"><div class="modal-content"><div class="modal-header"><h2>{{ editingUser ? 'Modifier' : 'Ajouter' }} un utilisateur</h2><button class="close" @click="closeModal"><i class="fas fa-times"></i></button></div><form @submit.prevent="saveUser" class="modal-form"><div class="form-row"><div class="form-group"><label>Nom complet *</label><input type="text" v-model="userForm.nom" required></div><div class="form-group"><label>Email *</label><input type="email" v-model="userForm.email" required></div></div><div class="form-row"><div class="form-group"><label>Téléphone *</label><input type="text" v-model="userForm.telephone" required></div><div class="form-group"><label>Rôle</label><select v-model="userForm.is_superuser"><option :value="false">Utilisateur standard</option><option :value="true">Super Administrateur</option></select></div></div><div class="form-row" v-if="!editingUser"><div class="form-group"><label>Mot de passe</label><input type="password" v-model="userForm.password"></div><div class="form-group"><label>Confirmer</label><input type="password" v-model="userForm.password2"></div></div><div class="modal-footer"><button type="button" class="btn-secondary" @click="closeModal">Annuler</button><button type="submit" class="btn-primary">Enregistrer</button></div></form></div></div>
      <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType==='success'?'fas fa-check-circle':'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
    </main>
  </div>
</template>
<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'
export default {
  name: 'UsersManagement',
  data() { return { users: [], showModal: false, editingUser: null, userForm: { nom: '', email: '', telephone: '', is_superuser: false, password: '', password2: '' }, toastMessage: '', toastType: '', user: null, currentUserId: null } },
  computed: { userInitials() { return this.user?.nom ? this.user.nom.split(' ').map(n=>n[0]).join('').toUpperCase() : 'AD' }, activeUsers() { return this.users.filter(u=>u.is_active).length }, adminUsers() { return this.users.filter(u=>u.is_superuser).length } },
  mounted() { const auth=useAuthStore(); this.user=auth.user; this.currentUserId=auth.user?.id; this.loadUsers() },
  methods: {
    async loadUsers() { try { const res = await axios.get('http://localhost:8001/api/users/'); this.users = res.data } catch(e){ console.error(e) } },
    openAddUserModal() { this.editingUser=null; this.userForm={nom:'',email:'',telephone:'',is_superuser:false,password:'',password2:''}; this.showModal=true },
    editUser(u) { this.editingUser=u; this.userForm={...u,password:'',password2:''}; this.showModal=true },
    async saveUser() { try { if(this.editingUser){ await axios.put(`http://localhost:8001/api/users/${this.editingUser.id}/`, this.userForm); this.showToast('Utilisateur modifié','success') } else { await axios.post('http://localhost:8001/api/users/', this.userForm); this.showToast('Utilisateur créé','success') } this.loadUsers(); this.closeModal() } catch(e){ this.showToast('Erreur','error') } },
    async toggleUserStatus(u) { if(u.id===this.currentUserId){ this.showToast('Vous ne pouvez pas modifier votre propre statut','error'); return } try { await axios.patch(`http://localhost:8001/api/users/${u.id}/`, { is_active: !u.is_active }); this.loadUsers(); this.showToast(u.is_active?'Utilisateur désactivé':'Utilisateur activé','success') } catch(e){ this.showToast('Erreur','error') } },
    async deleteUser(u) { if(u.id===this.currentUserId){ this.showToast('Vous ne pouvez pas vous supprimer','error'); return } if(confirm('Supprimer cet utilisateur ?')){ await axios.delete(`http://localhost:8001/api/users/${u.id}/`); this.loadUsers(); this.showToast('Utilisateur supprimé','success') } },
    closeModal(){ this.showModal=false }, formatDate(d){ return new Date(d).toLocaleDateString('fr-FR') }, showToast(t,m){ this.toastType=t; this.toastMessage=m; setTimeout(()=>{this.toastMessage=''},3000) },
    confirmLogout(){ if(confirm('Déconnexion ?')){ useAuthStore().logout(); this.$router.push('/login') } }
  }
}
</script>
<style scoped>
.management-page { display: flex; min-height: 100vh; background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e8 100%); }
.sidebar { width: 280px; background: linear-gradient(180deg, #0d3b0f 0%, #1a472a 50%, #0a2412 100%); color: white; position: fixed; height: 100vh; }
.sidebar-header { padding: 30px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.logo { display: flex; align-items: center; gap: 15px; }
.logo-icon { width: 45px; height: 45px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.logo-icon i { font-size: 24px; color: #1a472a; }
.logo-text { display: flex; flex-direction: column; }
.logo-title { font-size: 18px; font-weight: 700; }
.logo-subtitle { font-size: 10px; opacity: 0.7; }
.sidebar-nav { flex: 1; padding: 0 16px; display: flex; flex-direction: column; gap: 6px; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; color: rgba(255,255,255,0.8); text-decoration: none; border-radius: 12px; transition: all 0.3s; position: relative; }
.nav-item::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: #FFD700; transform: scaleY(0); transition: transform 0.3s; }
.nav-item:hover::before, .nav-item.active::before { transform: scaleY(1); }
.nav-item:hover { background: rgba(255,255,255,0.1); color: white; transform: translateX(5px); }
.nav-item.active { background: rgba(255,215,0,0.15); color: #FFD700; }
.nav-badge { margin-left: auto; font-size: 9px; background: #ff9800; padding: 2px 6px; border-radius: 20px; }
.sidebar-footer { padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: auto; }
.user-info-sidebar { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 12px; }
.user-avatar-sidebar { width: 45px; height: 45px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; color: #1a472a; }
.user-details-sidebar { display: flex; flex-direction: column; }
.user-name-sidebar { font-weight: 600; font-size: 14px; }
.user-role { font-size: 10px; opacity: 0.7; }
.logout-btn { width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; background: rgba(220,53,69,0.2); border: 1px solid rgba(220,53,69,0.5); border-radius: 12px; color: #ff6b6b; cursor: pointer; transition: all 0.3s; }
.logout-btn:hover { background: #dc3545; color: white; }
.main-content { flex: 1; margin-left: 280px; padding: 20px 30px; }
.top-bar { background: white; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; border-radius: 20px; margin-bottom: 25px; }
.page-title h1 { font-size: 24px; color: #1a472a; }
.page-title h1 i { color: #32CD32; margin-right: 10px; }
.btn-primary { padding: 10px 20px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 12px; cursor: pointer; }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px; }
.stat-card { background: white; border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 15px; }
.stat-icon { width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-icon.blue { background: #17a2b8; }
.stat-icon.green { background: #28a745; }
.stat-icon.orange { background: #ff9800; }
.stat-icon i { font-size: 24px; color: white; }
.stat-info h3 { font-size: 28px; font-weight: bold; color: #1a472a; }
.users-table { display: flex; flex-direction: column; gap: 15px; }
.user-card { background: white; border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 20px; transition: transform 0.3s; }
.user-card:hover { transform: translateX(5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.user-avatar-large { width: 70px; height: 70px; background: linear-gradient(135deg, #32CD32, #228B22); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: white; }
.user-details { flex: 1; }
.user-details h3 { color: #1a472a; margin-bottom: 4px; }
.user-details p { color: #666; font-size: 14px; margin-bottom: 4px; }
.user-phone { font-size: 12px; color: #999; }
.user-meta { display: flex; gap: 10px; margin-top: 8px; flex-wrap: wrap; }
.role-badge { padding: 4px 12px; border-radius: 20px; font-size: 11px; background: #e8f5e8; color: #32CD32; }
.role-badge.admin { background: #fff3e0; color: #ff9800; }
.status-badge { padding: 4px 12px; border-radius: 20px; font-size: 11px; background: #f8d7da; color: #dc3545; }
.status-badge.active { background: #d4edda; color: #28a745; }
.date-badge { padding: 4px 12px; border-radius: 20px; font-size: 11px; background: #e8f5e8; color: #32CD32; }
.user-actions { display: flex; gap: 10px; }
.btn-edit, .btn-status, .btn-delete { padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-size: 13px; display: flex; align-items: center; gap: 5px; transition: all 0.3s; }
.btn-edit { background: #ffc107; color: #1a472a; }
.btn-status { background: #dc3545; color: white; }
.btn-status.active { background: #28a745; }
.btn-delete { background: #dc3545; color: white; }
.btn-delete:disabled { opacity: 0.5; cursor: not-allowed; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal.active { visibility: visible; opacity: 1; }
.modal-content { background: white; border-radius: 24px; width: 90%; max-width: 600px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid #eee; }
.modal-header h2 { color: #1a472a; }
.close { background: none; border: none; font-size: 24px; cursor: pointer; }
.modal-form { padding: 20px; }
.form-row { display: flex; gap: 20px; margin-bottom: 15px; }
.form-group { flex: 1; display: flex; flex-direction: column; gap: 5px; }
.form-group label { font-weight: 500; font-size: 13px; }
.form-group input, .form-group select { padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 15px; padding: 20px; border-top: 1px solid #eee; }
.btn-secondary { padding: 10px 20px; background: #f5f5f5; border: none; border-radius: 8px; cursor: pointer; }
.toast { position: fixed; bottom: 30px; right: 30px; padding: 14px 22px; border-radius: 12px; display: flex; align-items: center; gap: 12px; z-index: 1100; animation: slideInRight 0.3s; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
.empty { text-align: center; padding: 60px; color: #999; }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@media (max-width: 768px) { .sidebar { width: 80px; } .sidebar-nav span, .sidebar-footer span, .logo-text, .user-info-sidebar { display: none; } .nav-item { justify-content: center; } .main-content { margin-left: 80px; padding: 15px; } .user-card { flex-direction: column; text-align: center; } .user-actions { justify-content: center; } .user-meta { justify-content: center; } .stats-grid { grid-template-columns: 1fr; } }
</style>
