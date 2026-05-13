<template>
  <div class="management-page">
    <aside class="sidebar"><div class="sidebar-header"><div class="logo"><div class="logo-icon"><i class="fas fa-leaf"></i></div><div class="logo-text"><span class="logo-title">Herbier Admin</span><span class="logo-subtitle">Université de Man</span></div></div></div>
      <nav class="sidebar-nav"><router-link to="/dashboard" class="nav-item"><i class="fas fa-tachometer-alt"></i><span>Tableau de bord</span></router-link><router-link to="/plantes" class="nav-item"><i class="fas fa-leaf"></i><span>Plantes</span></router-link><router-link to="/equipe" class="nav-item"><i class="fas fa-users"></i><span>Équipe</span></router-link><router-link to="/partenaires" class="nav-item active"><i class="fas fa-handshake"></i><span>Partenaires</span></router-link><router-link to="/slides" class="nav-item"><i class="fas fa-images"></i><span>Slides</span></router-link><router-link to="/projets" class="nav-item"><i class="fas fa-project-diagram"></i><span>Projets</span></router-link><router-link to="/activites" class="nav-item"><i class="fas fa-chart-line"></i><span>Activités</span></router-link><router-link to="/temoignages" class="nav-item"><i class="fas fa-comment-dots"></i><span>Témoignages</span></router-link><router-link to="/publications" class="nav-item"><i class="fas fa-book"></i><span>Publications</span></router-link><router-link to="/statistiques" class="nav-item"><i class="fas fa-chart-bar"></i><span>Statistiques</span></router-link><router-link to="/settings" class="nav-item"><i class="fas fa-cog"></i><span>Paramètres</span></router-link></nav>
      <div class="sidebar-footer"><div class="user-info-sidebar"><div class="user-avatar-sidebar">{{ userInitials }}</div><div class="user-details-sidebar"><span class="user-name-sidebar">{{ user?.nom || 'Admin' }}</span><span class="user-role">Super Admin</span></div></div><button @click="confirmLogout" class="logout-btn"><i class="fas fa-sign-out-alt"></i><span>Déconnexion</span></button></div>
    </aside>
    <main class="main-content">
      <header class="top-bar"><div class="page-title"><h1><i class="fas fa-handshake"></i> Gestion des partenaires</h1><p>Ajoutez, modifiez ou supprimez des partenaires</p></div><button @click="openModal" class="btn-primary"><i class="fas fa-plus"></i> Nouveau partenaire</button></header>
      <div class="filters-card"><div class="search-box"><i class="fas fa-search"></i><input type="text" v-model="searchQuery" placeholder="Rechercher un partenaire..."></div><div class="stats-badge"><i class="fas fa-chart-simple"></i> {{ filteredPartenaires.length }} partenaire(s)</div></div>
      <div class="partners-grid"><div v-for="p in filteredPartenaires" :key="p.id" class="partner-card"><div class="partner-logo"><img :src="p.logo || '/images/logo-placeholder.png'" @error="e=>e.target.src='/images/logo-placeholder.png'"></div><div class="partner-info"><h3>{{ p.nom }}</h3><p>{{ p.description || 'Aucune description' }}</p><a v-if="p.site_web" :href="p.site_web" target="_blank" class="partner-link"><i class="fas fa-external-link-alt"></i> Visiter le site</a></div><div class="partner-actions"><button @click="editItem(p)" class="btn-edit"><i class="fas fa-edit"></i></button><button @click="deleteItem(p)" class="btn-delete"><i class="fas fa-trash"></i></button></div></div><div v-if="filteredPartenaires.length===0" class="empty"><i class="fas fa-handshake-slash"></i> Aucun partenaire trouvé</div></div>
      <div class="modal" :class="{ active: showModal }" @click.self="closeModal"><div class="modal-content"><div class="modal-header"><h2>{{ editingId ? 'Modifier' : 'Ajouter' }} un partenaire</h2><button class="close" @click="closeModal"><i class="fas fa-times"></i></button></div><form @submit.prevent="saveItem" class="modal-form"><div class="form-group"><label>Nom *</label><input type="text" v-model="form.nom" required></div><div class="form-group"><label>Site web</label><input type="url" v-model="form.site_web" placeholder="https://..."></div><div class="form-group"><label>Description</label><textarea v-model="form.description" rows="3"></textarea></div><div class="form-group"><label>Logo URL</label><input type="text" v-model="form.logo" placeholder="/images/..."></div><div class="modal-footer"><button type="button" class="btn-secondary" @click="closeModal">Annuler</button><button type="submit" class="btn-primary">Enregistrer</button></div></form></div></div>
      <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType==='success'?'fas fa-check-circle':'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
    </main>
  </div>
</template>
<script>
import { useAuthStore } from '../stores/auth'; import axios from 'axios'
export default { name: 'PartenairesManagement', data() { return { partenaires: [], searchQuery: '', showModal: false, editingId: null, form: { nom: '', site_web: '', description: '', logo: '' }, toastMessage: '', toastType: '', user: null } }, computed: { userInitials() { return this.user?.nom ? this.user.nom.split(' ').map(n=>n[0]).join('').toUpperCase() : 'AD' }, filteredPartenaires() { let f = this.partenaires; if(this.searchQuery){ const q=this.searchQuery.toLowerCase(); f=f.filter(p=>p.nom?.toLowerCase().includes(q)||p.description?.toLowerCase().includes(q)) } return f } }, mounted() { const auth=useAuthStore(); this.user=auth.user; this.loadData() }, methods: { async loadData(){ try{ const res=await axios.get('http://localhost:8001/api/herbier-data/'); this.partenaires=res.data.partenaires||[] }catch(e){ console.error(e) } }, openModal(){ this.editingId=null; this.form={nom:'',site_web:'',description:'',logo:''}; this.showModal=true }, editItem(i){ this.editingId=i.id; this.form={...i}; this.showModal=true }, async saveItem(){ try{ let partenaires=[...this.partenaires]; if(this.editingId){ const idx=partenaires.findIndex(p=>p.id===this.editingId); partenaires[idx]={...this.form,id:this.editingId} }else{ partenaires.push({...this.form,id:Date.now()}) } await axios.put('http://localhost:8001/api/herbier-data/',{...(await axios.get('http://localhost:8001/api/herbier-data/')).data,partenaires}); this.partenaires=partenaires; this.showToast(this.editingId?'Partenaire modifié':'Partenaire ajouté','success'); this.closeModal() }catch(e){ this.showToast('Erreur','error') } }, async deleteItem(i){ if(confirm('Supprimer ce partenaire ?')){ const partenaires=this.partenaires.filter(p=>p.id!==i.id); await axios.put('http://localhost:8001/api/herbier-data/',{...(await axios.get('http://localhost:8001/api/herbier-data/')).data,partenaires}); this.partenaires=partenaires; this.showToast('Partenaire supprimé','success') } }, closeModal(){ this.showModal=false }, showToast(t,m){ this.toastType=t; this.toastMessage=m; setTimeout(()=>{this.toastMessage=''},3000) }, confirmLogout(){ if(confirm('Déconnexion ?')){ useAuthStore().logout(); this.$router.push('/login') } } } }
</script>
<style scoped>
.management-page { display: flex; min-height: 100vh; background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e8 100%); font-family: 'Inter', sans-serif; }
.sidebar { width: 280px; background: linear-gradient(180deg, #0d3b0f 0%, #1a472a 50%, #0a2412 100%); color: white; position: fixed; height: 100vh; left: 0; top: 0; box-shadow: 5px 0 30px rgba(0,0,0,0.1); z-index: 100; }
.sidebar-header { padding: 30px 24px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
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
.nav-item i { width: 22px; font-size: 18px; }
.sidebar-footer { padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: auto; }
.user-info-sidebar { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 12px; }
.user-avatar-sidebar { width: 45px; height: 45px; background: linear-gradient(135deg, #FFD700, #FFA500); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; color: #1a472a; }
.user-details-sidebar { display: flex; flex-direction: column; }
.user-name-sidebar { font-weight: 600; font-size: 14px; }
.user-role { font-size: 10px; opacity: 0.7; }
.logout-btn { width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; background: rgba(220,53,69,0.2); border: 1px solid rgba(220,53,69,0.5); border-radius: 12px; color: #ff6b6b; cursor: pointer; transition: all 0.3s; font-weight: 500; }
.logout-btn:hover { background: #dc3545; color: white; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(220,53,69,0.3); }
.main-content { flex: 1; margin-left: 280px; padding: 20px 30px; }
.top-bar { background: white; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); margin-bottom: 25px; }
.page-title h1 { font-size: 24px; font-weight: 700; color: #1a472a; }
.page-title h1 i { color: #32CD32; margin-right: 10px; }
.page-title p { color: #666; font-size: 14px; }
.btn-primary { padding: 10px 20px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 500; transition: all 0.3s; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(50,205,50,0.3); }
.filters-card { background: white; border-radius: 16px; padding: 15px 20px; display: flex; gap: 15px; margin-bottom: 25px; align-items: center; flex-wrap: wrap; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.search-box { flex: 1; position: relative; min-width: 200px; }
.search-box i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #999; }
.search-box input { width: 100%; padding: 10px 15px 10px 45px; border: 1px solid #e0e0e0; border-radius: 12px; font-size: 14px; }
.stats-badge { background: #e8f5e8; padding: 8px 18px; border-radius: 30px; color: #32CD32; font-weight: 500; }
.partners-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
.partner-card { background: white; border-radius: 20px; padding: 20px; display: flex; gap: 20px; align-items: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: all 0.3s; }
.partner-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
.partner-logo { width: 80px; height: 80px; flex-shrink: 0; background: #f5f5f5; border-radius: 15px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.partner-logo img { max-width: 80%; max-height: 80%; object-fit: contain; }
.partner-info { flex: 1; }
.partner-info h3 { color: #1a472a; margin-bottom: 8px; font-size: 18px; }
.partner-info p { color: #666; font-size: 13px; line-height: 1.5; margin-bottom: 10px; }
.partner-link { color: #32CD32; text-decoration: none; font-size: 12px; display: inline-flex; align-items: center; gap: 5px; transition: color 0.3s; }
.partner-link:hover { color: #228B22; text-decoration: underline; }
.partner-actions { display: flex; gap: 8px; }
.btn-edit, .btn-delete { padding: 8px 12px; border: none; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
.btn-edit { background: #ffc107; color: #1a472a; }
.btn-delete { background: #dc3545; color: white; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal.active { visibility: visible; opacity: 1; }
.modal-content { background: white; border-radius: 24px; width: 90%; max-width: 500px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 25px; border-bottom: 1px solid #eee; }
.modal-header h2 { color: #1a472a; }
.close { background: none; border: none; font-size: 24px; cursor: pointer; }
.modal-form { padding: 25px; }
.form-group { margin-bottom: 20px; display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-weight: 500; color: #333; font-size: 13px; }
.form-group input, .form-group textarea { padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; width: 100%; }
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: #32CD32; box-shadow: 0 0 0 3px rgba(50,205,50,0.1); }
.modal-footer { display: flex; justify-content: flex-end; gap: 15px; margin-top: 25px; padding-top: 20px; border-top: 1px solid #eee; }
.btn-secondary { padding: 10px 25px; background: #f5f5f5; border: none; border-radius: 10px; cursor: pointer; font-weight: 500; }
.toast { position: fixed; bottom: 30px; right: 30px; padding: 14px 22px; border-radius: 12px; display: flex; align-items: center; gap: 12px; z-index: 1100; animation: slideInRight 0.3s; box-shadow: 0 10px 25px rgba(0,0,0,0.1); font-weight: 500; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.empty { text-align: center; padding: 60px; color: #999; background: white; border-radius: 20px; }
.empty i { font-size: 50px; margin-bottom: 15px; display: block; }
@media (max-width: 768px) { .sidebar { width: 80px; } .sidebar-nav span, .sidebar-footer span, .logo-text, .user-info-sidebar { display: none; } .nav-item { justify-content: center; } .main-content { margin-left: 80px; padding: 15px; } .top-bar { flex-direction: column; gap: 15px; text-align: center; } .partner-card { flex-direction: column; text-align: center; } .partner-actions { justify-content: center; } }
</style>
