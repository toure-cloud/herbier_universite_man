<template>
  <div class="herbier-data">
    <nav class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <i class="fas fa-leaf"></i>
          <span>Herbier Admin</span>
        </div>
      </div>
      
      <div class="sidebar-menu">
        <router-link to="/dashboard" class="menu-item">
          <i class="fas fa-tachometer-alt"></i>
          <span>Tableau de bord</span>
        </router-link>
        <router-link to="/herbier-data" class="menu-item active">
          <i class="fas fa-database"></i>
          <span>Gestion des données</span>
        </router-link>
        <router-link to="/settings" class="menu-item">
          <i class="fas fa-cog"></i>
          <span>Paramètres</span>
        </router-link>
      </div>
      
      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          <span>Déconnexion</span>
        </button>
      </div>
    </nav>
    
    <div class="main-content">
      <div class="top-bar">
        <h1>Gestion des données de l'herbier</h1>
        <button @click="saveData" class="btn-save" :disabled="saving">
          <i class="fas fa-save"></i>
          {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
        </button>
      </div>
      
      <div class="content">
        <div class="tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['tab', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id">
            <i :class="tab.icon"></i>
            {{ tab.name }}
          </button>
        </div>
        
        <div class="tab-content">
          <!-- Plantes -->
          <div v-show="activeTab === 'plantes'" class="data-section">
            <div class="section-header">
              <h2>Plantes</h2>
              <button @click="addItem('plantes')" class="btn-add">
                <i class="fas fa-plus"></i>
                Ajouter une plante
              </button>
            </div>
            
            <div class="data-table">
              <table>
                <thead>
                  <tr>
                    <th>Nom</th>
                    <th>Famille</th>
                    <th>Nom scientifique</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(plante, index) in formData.plantes" :key="index">
                    <td><input v-model="plante.nom" class="table-input"></td>
                    <td><input v-model="plante.famille" class="table-input"></td>
                    <td><input v-model="plante.nom_scientifique" class="table-input"></td>
                    <td>
                      <button @click="editItem('plantes', index)" class="btn-edit">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button @click="deleteItem('plantes', index)" class="btn-delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Équipe -->
          <div v-show="activeTab === 'equipe'" class="data-section">
            <div class="section-header">
              <h2>Équipe</h2>
              <button @click="addItem('equipe')" class="btn-add">
                <i class="fas fa-plus"></i>
                Ajouter un membre
              </button>
            </div>
            
            <div class="data-table">
              <table>
                <thead>
                  <tr>
                    <th>Nom</th>
                    <th>Poste</th>
                    <th>Email</th>
                    <th>Photo URL</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(membre, index) in formData.equipe" :key="index">
                    <td><input v-model="membre.nom" class="table-input"></td>
                    <td><input v-model="membre.poste" class="table-input"></td>
                    <td><input v-model="membre.email" class="table-input"></td>
                    <td><input v-model="membre.photo" class="table-input" placeholder="/src/images/..."></td>
                    <td>
                      <button @click="editItem('equipe', index)" class="btn-edit">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button @click="deleteItem('equipe', index)" class="btn-delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Projets -->
          <div v-show="activeTab === 'projets'" class="data-section">
            <div class="section-header">
              <h2>Projets</h2>
              <button @click="addItem('projets')" class="btn-add">
                <i class="fas fa-plus"></i>
                Ajouter un projet
              </button>
            </div>
            
            <div class="data-table">
              <table>
                <thead>
                  <tr>
                    <th>Titre</th>
                    <th>Catégorie</th>
                    <th>Statut</th>
                    <th>Lieu</th>
                    <th>Année</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(projet, index) in formData.projets" :key="index">
                    <td><input v-model="projet.titre" class="table-input"></td>
                    <td>
                      <select v-model="projet.categorie" class="table-input">
                        <option value="recherche">Recherche</option>
                        <option value="conservation">Conservation</option>
                        <option value="formation">Formation</option>
                        <option value="developpement">Développement</option>
                      </select>
                    </td>
                    <td>
                      <select v-model="projet.statut" class="table-input">
                        <option value="termine">Terminé</option>
                        <option value="encours">En cours</option>
                        <option value="planifie">Planifié</option>
                      </select>
                    </td>
                    <td><input v-model="projet.lieu" class="table-input"></td>
                    <td><input v-model="projet.annee" class="table-input"></td>
                    <td>
                      <button @click="editItem('projets', index)" class="btn-edit">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button @click="deleteItem('projets', index)" class="btn-delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Autres sections similaires... -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

export default {
  name: 'HerbierData',
  data() {
    return {
      activeTab: 'plantes',
      formData: {
        plantes: [],
        equipe: [],
        partenaires: [],
        slides: [],
        projets: [],
        activites: [],
        temoignages: [],
        publications: [],
        faqs: [],
        statistiques: [],
        methodologie: []
      },
      saving: false,
      tabs: [
        { id: 'plantes', name: '🌿 Plantes', icon: 'fas fa-leaf' },
        { id: 'equipe', name: '👥 Équipe', icon: 'fas fa-users' },
        { id: 'partenaires', name: '🤝 Partenaires', icon: 'fas fa-handshake' },
        { id: 'slides', name: '📸 Slides', icon: 'fas fa-images' },
        { id: 'projets', name: '📊 Projets', icon: 'fas fa-project-diagram' },
        { id: 'activites', name: '⚡ Activités', icon: 'fas fa-chart-line' },
        { id: 'temoignages', name: '💬 Témoignages', icon: 'fas fa-comment' },
        { id: 'publications', name: '📚 Publications', icon: 'fas fa-book' },
        { id: 'faqs', name: '❓ FAQs', icon: 'fas fa-question-circle' },
        { id: 'statistiques', name: '📈 Statistiques', icon: 'fas fa-chart-bar' }
      ]
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get('http://localhost:8001/api/herbier-data/')
        const data = response.data
        for (const key in this.formData) {
          if (data[key]) {
            this.formData[key] = data[key]
          }
        }
      } catch (error) {
        console.error('Erreur chargement données', error)
      }
    },
    async saveData() {
      this.saving = true
      try {
        await axios.put('http://localhost:8001/api/herbier-data/', this.formData)
        alert('Données sauvegardées avec succès !')
      } catch (error) {
        console.error('Erreur sauvegarde', error)
        alert('Erreur lors de la sauvegarde')
      }
      this.saving = false
    },
    addItem(section) {
      let newItem = {}
      switch(section) {
        case 'plantes':
          newItem = { id: Date.now(), nom: '', famille: '', description: '', nom_scientifique: '', habitat: '', statut_conservation: '' }
          break
        case 'equipe':
          newItem = { id: Date.now(), nom: '', poste: '', email: '', specialite: '', photo: '', telephone: '' }
          break
        case 'projets':
          newItem = { id: Date.now(), titre: '', categorie: 'recherche', statut: 'encours', featured: false, annee: '', lieu: '', partenaires: 0, beneficiaires: '', budget: '', duree: '', impact: '', progression: 0, description: '', tags: '', image: '', caption: '' }
          break
        default:
          newItem = { id: Date.now() }
      }
      this.formData[section].push(newItem)
    },
    deleteItem(section, index) {
      if (confirm('Supprimer cet élément ?')) {
        this.formData[section].splice(index, 1)
      }
    },
    editItem(section, index) {
      // Ouvrir modal d'édition détaillée - à implémenter
      console.log(`Éditer ${section}[${index}]`)
    },
    async handleLogout() {
      const authStore = useAuthStore()
      await authStore.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.herbier-data {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #1a472a 0%, #0d3b0f 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: bold;
}

.logo i {
  font-size: 28px;
  color: #FFD700;
}

.sidebar-menu {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.menu-item.active {
  background: #FFD700;
  color: #1a472a;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255,255,255,0.1);
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
}

.main-content {
  flex: 1;
  margin-left: 280px;
}

.top-bar {
  background: white;
  padding: 20px 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-bar h1 {
  font-size: 24px;
  color: #1a472a;
}

.btn-save {
  padding: 10px 20px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.content {
  padding: 30px;
}

.tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.tab {
  padding: 10px 20px;
  background: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.tab:hover {
  background: #e8f5e8;
}

.tab.active {
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
}

.data-section {
  background: white;
  border-radius: 20px;
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-add {
  padding: 8px 16px;
  background: #32CD32;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.data-table {
  overflow-x: auto;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.btn-edit, .btn-delete {
  padding: 5px 10px;
  margin: 0 3px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-edit {
  background: #ffc107;
  color: #1a472a;
}

.btn-delete {
  background: #dc3545;
  color: white;
}
</style>
