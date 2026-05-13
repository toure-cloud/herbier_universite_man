<template>
  <div class="management-page">
    <!-- Sidebar identique à avant -->
    <aside class="sidebar">...</aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="page-title">
          <h1><i class="fas fa-leaf"></i> Gestion des Plantes</h1>
          <p>{{ isSuperAdmin ? 'Gérez toutes les plantes' : 'Gérez vos plantes' }}</p>
        </div>
        <button @click="openModal" class="btn-primary"><i class="fas fa-plus"></i> Nouvelle plante</button>
      </header>

      <div class="filters-card">
        <div class="search-box"><i class="fas fa-search"></i><input type="text" v-model="searchQuery" placeholder="Rechercher..."></div>
        <div class="stats-badge"><i class="fas fa-chart-simple"></i> {{ filteredPlantes.length }} plante(s)</div>
      </div>

      <div class="plants-grid">
        <div v-for="plante in filteredPlantes" :key="plante.id" class="plant-card">
          <div class="plant-image"><img :src="plante.image || '/images/placeholder.jpg'" @error="handleImageError"><div class="plant-badge" v-if="plante.created_by !== currentUserId && isSuperAdmin">Créé par un autre</div></div>
          <div class="plant-info"><h3>{{ plante.nom }}</h3><p class="plant-famille">{{ plante.famille }}</p><p>{{ plante.description | truncate(80) }}</p><div class="plant-footer"><span class="plant-date"><i class="fas fa-calendar"></i> {{ formatDate(plante.date_creation) }}</span><div class="plant-actions"><button @click="editItem(plante)" class="btn-edit"><i class="fas fa-edit"></i></button><button @click="deleteItem(plante)" class="btn-delete" :disabled="plante.created_by !== currentUserId && !isSuperAdmin"><i class="fas fa-trash"></i></button></div></div></div>
        </div>
        <div v-if="filteredPlantes.length === 0" class="empty"><i class="fas fa-seedling"></i> Aucune plante</div>
      </div>

      <!-- Modal formulaire identique -->
      <div class="modal" :class="{ active: showModal }" @click.self="closeModal">...</div>
      <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType==='success'?'fas fa-check-circle':'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'PlantesManagement',
  filters: { truncate: (v, l) => v?.length > l ? v.substring(0,l)+'...' : v || '' },
  data() {
    return {
      plantes: [], searchQuery: '', showModal: false, editingId: null, form: { nom: '', famille: '', nom_scientifique: '', description: '', habitat: '', image: '', publie: true, created_by: null },
      toastMessage: '', toastType: '', user: null, currentUserId: null, isSuperAdmin: false
    }
  },
  computed: {
    filteredPlantes() { let f = this.plantes; if(this.searchQuery){ const q=this.searchQuery.toLowerCase(); f=f.filter(p=>p.nom?.toLowerCase().includes(q)||p.famille?.toLowerCase().includes(q)) } return f }
  },
  mounted() { const auth=useAuthStore(); this.user=auth.user; this.currentUserId=auth.user?.id; this.isSuperAdmin=auth.user?.is_superuser; this.loadData() },
  methods: {
    async loadData() { try { const res = await axios.get('http://localhost:8001/api/herbier-data/'); this.plantes = res.data.plantes || [] } catch(e) { console.error(e) } },
    openModal() { this.editingId=null; this.form={nom:'',famille:'',nom_scientifique:'',description:'',habitat:'',image:'',publie:true}; this.showModal=true },
    editItem(i) { this.editingId=i.id; this.form={...i}; this.showModal=true },
    async saveItem() {
      try {
        let plantes = [...this.plantes]
        if(this.editingId){ const idx=plantes.findIndex(p=>p.id===this.editingId); plantes[idx]={...this.form,id:this.editingId,created_by:plantes[idx].created_by||this.currentUserId} }
        else{ plantes.push({...this.form,id:Date.now(),created_by:this.currentUserId,date_creation:new Date().toISOString()}) }
        const data = await axios.get('http://localhost:8001/api/herbier-data/')
        await axios.put('http://localhost:8001/api/herbier-data/', {...data.data, plantes})
        this.plantes = plantes; this.showToast(this.editingId?'Plante modifiée':'Plante ajoutée','success'); this.closeModal()
        this.loadData()
      } catch(e){ this.showToast('Erreur','error') }
    },
    async deleteItem(i){ if(!this.isSuperAdmin && i.created_by!==this.currentUserId){ this.showToast('Vous ne pouvez pas supprimer cette plante','error'); return } if(confirm('Supprimer ?')){ const plantes=this.plantes.filter(p=>p.id!==i.id); const data=await axios.get('http://localhost:8001/api/herbier-data/'); await axios.put('http://localhost:8001/api/herbier-data/',{...data.data,plantes}); this.plantes=plantes; this.showToast('Plante supprimée','success') } },
    closeModal(){ this.showModal=false },
    showToast(t,m){ this.toastType=t; this.toastMessage=m; setTimeout(()=>{this.toastMessage=''},3000) },
    handleImageError(e){ e.target.src='/images/placeholder.jpg' },
    formatDate(d){ if(!d) return ''; return new Date(d).toLocaleDateString('fr-FR') }
  }
}
</script>
<style scoped>
/* Styles identiques aux versions précédentes */
.management-page { display: flex; min-height: 100vh; background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e8 100%); }
.sidebar { width: 280px; background: linear-gradient(180deg, #0d3b0f 0%, #1a472a 50%, #0a2412 100%); color: white; position: fixed; height: 100vh; }
.main-content { flex: 1; margin-left: 280px; padding: 20px 30px; }
.top-bar { background: white; padding: 15px 25px; display: flex; justify-content: space-between; align-items: center; border-radius: 20px; margin-bottom: 25px; }
.btn-primary { padding: 10px 20px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 12px; cursor: pointer; }
.filters-card { background: white; border-radius: 16px; padding: 15px 20px; display: flex; gap: 15px; margin-bottom: 25px; align-items: center; }
.search-box { flex: 1; position: relative; }
.search-box i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #999; }
.search-box input { width: 100%; padding: 10px 15px 10px 45px; border: 1px solid #ddd; border-radius: 12px; }
.stats-badge { background: #e8f5e8; padding: 8px 18px; border-radius: 30px; color: #32CD32; }
.plants-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
.plant-card { background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: transform 0.3s; }
.plant-card:hover { transform: translateY(-5px); }
.plant-image { position: relative; height: 180px; overflow: hidden; }
.plant-image img { width: 100%; height: 100%; object-fit: cover; }
.plant-badge { position: absolute; top: 10px; right: 10px; background: #ff9800; color: white; padding: 4px 10px; border-radius: 20px; font-size: 10px; }
.plant-info { padding: 15px; }
.plant-info h3 { color: #1a472a; margin-bottom: 5px; }
.plant-famille { color: #32CD32; font-size: 12px; margin-bottom: 10px; }
.plant-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; }
.plant-date { font-size: 11px; color: #999; }
.plant-actions { display: flex; gap: 8px; }
.btn-edit, .btn-delete { padding: 6px 10px; border: none; border-radius: 6px; cursor: pointer; }
.btn-edit { background: #ffc107; }
.btn-delete { background: #dc3545; color: white; }
.btn-delete:disabled { opacity: 0.5; cursor: not-allowed; }
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal.active { visibility: visible; opacity: 1; }
.modal-content { background: white; border-radius: 24px; width: 90%; max-width: 600px; }
.modal-header { display: flex; justify-content: space-between; padding: 20px; border-bottom: 1px solid #eee; }
.modal-form { padding: 20px; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; gap: 5px; }
.form-group input, .form-group textarea { padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 15px; padding: 20px; border-top: 1px solid #eee; }
.btn-secondary { padding: 10px 20px; background: #f5f5f5; border: none; border-radius: 8px; cursor: pointer; }
.toast { position: fixed; bottom: 30px; right: 30px; padding: 14px 22px; border-radius: 12px; display: flex; align-items: center; gap: 12px; z-index: 1100; animation: slideInRight 0.3s; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
.empty { text-align: center; padding: 60px; color: #999; }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
</style>
