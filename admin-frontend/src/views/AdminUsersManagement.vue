<template>
  <div class="admin-management">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon"><i class="fas fa-shield-alt"></i></div>
          <div class="logo-text">
            <span class="logo-title">IT Administration</span>
            <span class="logo-subtitle">Gestion sécurisée</span>
          </div>
        </div>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-arrow-left"></i><span>Retour au tableau de bord</span>
        </router-link>
        <router-link to="/administrateurs" class="nav-item active">
          <i class="fas fa-user-shield"></i><span>Administrateurs</span>
          <span class="nav-badge">{{ admins.length }}</span>
        </router-link>
        <router-link to="/settings" class="nav-item">
          <i class="fas fa-cog"></i><span>Paramètres</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info-sidebar">
          <div class="user-avatar-sidebar">{{ userInitials }}</div>
          <div class="user-details-sidebar">
            <span class="user-name-sidebar">{{ user?.nom || 'IT Admin' }}</span>
            <span class="user-role">Super Admin</span>
          </div>
        </div>
        <button @click="confirmLogout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i><span>Déconnexion</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Bar -->
      <header class="top-bar">
        <div class="page-title">
          <div class="title-icon">
            <i class="fas fa-user-shield"></i>
          </div>
          <div class="title-text">
            <h1>Gestion des Administrateurs</h1>
            <p>Gérez les comptes administrateurs de la plateforme</p>
          </div>
        </div>
        <button @click="openAddAdminModal" class="btn-primary">
          <i class="fas fa-plus"></i> Nouvel administrateur
        </button>
      </header>

      <!-- Statistiques -->
      <div class="stats-grid">
        <div class="stat-card total">
          <div class="stat-icon"><i class="fas fa-users"></i></div>
          <div class="stat-info">
            <h3>{{ admins.length }}</h3>
            <p>Total</p>
          </div>
        </div>
        <div class="stat-card active">
          <div class="stat-icon"><i class="fas fa-user-check"></i></div>
          <div class="stat-info">
            <h3>{{ activeAdmins }}</h3>
            <p>Actifs</p>
          </div>
        </div>
        <div class="stat-card inactive">
          <div class="stat-icon"><i class="fas fa-user-slash"></i></div>
          <div class="stat-info">
            <h3>{{ inactiveAdmins }}</h3>
            <p>Inactifs</p>
          </div>
        </div>
        <div class="stat-card super">
          <div class="stat-icon"><i class="fas fa-crown"></i></div>
          <div class="stat-info">
            <h3>{{ superAdmins }}</h3>
            <p>Super Admins</p>
          </div>
        </div>
      </div>

      <!-- Filtres -->
      <div class="filters-section">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input type="text" v-model="searchQuery" placeholder="Rechercher un administrateur...">
        </div>
        <div class="filter-group">
          <select v-model="filterRole" class="filter-select">
            <option value="">Tous les rôles</option>
            <option value="it_admin">Super Admin</option>
            <option value="admin">Administrateur</option>
          </select>
          <select v-model="filterStatus" class="filter-select">
            <option value="">Tous les statuts</option>
            <option value="active">Actif</option>
            <option value="inactive">Inactif</option>
          </select>
        </div>
        <div class="results-count">
          <i class="fas fa-chart-simple"></i>
          <span>{{ filteredAdmins.length }} administrateur(s)</span>
        </div>
      </div>

      <!-- Liste des administrateurs -->
      <div class="admins-list">
        <div v-for="admin in filteredAdmins" :key="admin.id" class="admin-card">
          <div class="admin-avatar" :class="{ 'super-admin': admin.role === 'it_admin' || admin.is_superuser }">
            {{ getInitials(admin.nom) }}
            <div class="status-indicator" :class="{ active: admin.is_active }"></div>
          </div>
          
          <div class="admin-info">
            <div class="admin-header">
              <h3>{{ admin.nom }}</h3>
              <span class="role-badge" :class="admin.role === 'it_admin' || admin.is_superuser ? 'super' : 'admin'">
                <i :class="admin.role === 'it_admin' || admin.is_superuser ? 'fas fa-crown' : 'fas fa-user-shield'"></i>
                {{ admin.role === 'it_admin' || admin.is_superuser ? 'Super Admin' : 'Administrateur' }}
              </span>
              <span class="status-badge" :class="admin.is_active ? 'active' : 'inactive'">
                {{ admin.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </div>
            
            <div class="admin-details">
              <div class="detail-item">
                <i class="fas fa-envelope"></i>
                <span>{{ admin.email }}</span>
              </div>
              <div class="detail-item">
                <i class="fas fa-phone"></i>
                <span>{{ admin.telephone || 'Non renseigné' }}</span>
              </div>
              <div class="detail-item">
                <i class="fas fa-calendar-alt"></i>
                <span>Créé le {{ formatDate(admin.date_joined) }}</span>
              </div>
              <div class="detail-item" v-if="admin.last_login">
                <i class="fas fa-clock"></i>
                <span>Dernière connexion : {{ formatDate(admin.last_login) }}</span>
              </div>
            </div>
          </div>

          <div class="admin-actions">
            <button @click="editAdmin(admin)" class="action-btn edit">
              <i class="fas fa-edit"></i>
              <span>Modifier</span>
            </button>
            <button @click="toggleAdminStatus(admin)" class="action-btn status" :class="{ active: admin.is_active }">
              <i :class="admin.is_active ? 'fas fa-ban' : 'fas fa-check-circle'"></i>
              <span>{{ admin.is_active ? 'Désactiver' : 'Activer' }}</span>
            </button>
            <button @click="deleteAdmin(admin)" class="action-btn delete" :disabled="admin.id === currentUserId">
              <i class="fas fa-trash"></i>
              <span>Supprimer</span>
            </button>
          </div>
        </div>

        <div v-if="filteredAdmins.length === 0" class="empty-state">
          <i class="fas fa-user-shield"></i>
          <h3>Aucun administrateur trouvé</h3>
          <p>Essayez de modifier vos critères de recherche</p>
          <button @click="resetFilters" class="btn-primary">
            <i class="fas fa-redo-alt"></i> Réinitialiser
          </button>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <div class="modal" :class="{ active: showModal }" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-title">
            <i :class="editingAdmin ? 'fas fa-edit' : 'fas fa-user-plus'"></i>
            <h2>{{ editingAdmin ? 'Modifier' : 'Ajouter' }} un administrateur</h2>
          </div>
          <button class="close-btn" @click="closeModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="saveAdmin" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label><i class="fas fa-user"></i> Nom complet <span class="required">*</span></label>
              <input type="text" v-model="adminForm.nom" required placeholder="Jean Kouassi">
            </div>
            <div class="form-group">
              <label><i class="fas fa-envelope"></i> Email <span class="required">*</span></label>
              <input type="email" v-model="adminForm.email" required placeholder="admin@herbier-man.ci">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label><i class="fas fa-phone"></i> Téléphone <span class="required">*</span></label>
              <input type="tel" v-model="adminForm.telephone" required placeholder="+225 01 23 45 67">
            </div>
            <div class="form-group">
              <label><i class="fas fa-shield-alt"></i> Rôle</label>
              <select v-model="adminForm.role">
                <option value="admin">Administrateur</option>
                <option value="it_admin">Super Administrateur</option>
              </select>
            </div>
          </div>
          <div v-if="!editingAdmin" class="form-row">
            <div class="form-group">
              <label><i class="fas fa-lock"></i> Mot de passe <span class="required">*</span></label>
              <div class="password-wrapper">
                <input :type="showPassword ? 'text' : 'password'" v-model="adminForm.password" required minlength="8" placeholder="••••••••">
                <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                  <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label><i class="fas fa-lock"></i> Confirmer <span class="required">*</span></label>
              <div class="password-wrapper">
                <input :type="showPassword2 ? 'text' : 'password'" v-model="adminForm.password2" required minlength="8" placeholder="••••••••">
                <button type="button" class="toggle-password" @click="showPassword2 = !showPassword2">
                  <i :class="showPassword2 ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="form-group checkbox">
            <label>
              <input type="checkbox" v-model="adminForm.is_active">
              <span class="checkmark"></span>
              <span>Compte actif</span>
            </label>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="closeModal">Annuler</button>
            <button type="submit" class="btn-primary" :disabled="loading">
              <i v-if="loading" class="fas fa-spinner fa-spin"></i>
              {{ loading ? 'Enregistrement...' : editingAdmin ? 'Mettre à jour' : 'Créer' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toastMessage" class="toast" :class="toastType">
      <div class="toast-icon">
        <i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
      </div>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001'

export default {
  name: 'AdminUsersManagement',
  data() {
    return {
      admins: [],
      searchQuery: '',
      filterRole: '',
      filterStatus: '',
      showModal: false,
      editingAdmin: null,
      showPassword: false,
      showPassword2: false,
      loading: false,
      adminForm: {
        nom: '',
        email: '',
        telephone: '',
        role: 'admin',
        password: '',
        password2: '',
        is_active: true
      },
      toastMessage: '',
      toastType: '',
      user: null,
      currentUserId: null,
      isITAuthenticated: false
    }
  },
  computed: {
    userInitials() {
      return this.user?.nom ? this.user.nom.split(' ').map(n => n[0]).join('').toUpperCase() : 'AD'
    },
    activeAdmins() {
      return this.admins.filter(a => a.is_active).length
    },
    inactiveAdmins() {
      return this.admins.filter(a => !a.is_active).length
    },
    superAdmins() {
      return this.admins.filter(a => a.role === 'it_admin' || a.is_superuser).length
    },
    filteredAdmins() {
      let filtered = this.admins
      
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        filtered = filtered.filter(a => 
          a.nom?.toLowerCase().includes(q) || 
          a.email?.toLowerCase().includes(q)
        )
      }
      
      if (this.filterRole) {
        if (this.filterRole === 'it_admin') {
          filtered = filtered.filter(a => a.role === 'it_admin' || a.is_superuser)
        } else {
          filtered = filtered.filter(a => a.role === this.filterRole)
        }
      }
      
      if (this.filterStatus) {
        const isActive = this.filterStatus === 'active'
        filtered = filtered.filter(a => a.is_active === isActive)
      }
      
      return filtered
    }
  },
  mounted() {
    const isItAuthenticated = localStorage.getItem('it_admin_authenticated')
    if (!isItAuthenticated || isItAuthenticated !== 'true') {
      this.$router.push('/it-login')
      return
    }
    this.isITAuthenticated = true
    
    const auth = useAuthStore()
    this.user = auth.user
    this.currentUserId = auth.user?.id
    this.loadAdmins()
  },
  methods: {
    async loadAdmins() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/users/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        this.admins = response.data || []
      } catch (error) {
        console.error('Erreur chargement administrateurs:', error)
        if (error.response?.status === 401) {
          this.$router.push('/login')
        } else if (error.response?.status === 403) {
          this.showToast('error', 'Vous n\'avez pas les droits pour accéder à cette page')
          this.$router.push('/dashboard')
        } else {
          this.showToast('error', 'Erreur lors du chargement des administrateurs')
        }
      }
    },

    openAddAdminModal() {
      this.editingAdmin = null
      this.adminForm = {
        nom: '',
        email: '',
        telephone: '',
        role: 'admin',
        password: '',
        password2: '',
        is_active: true
      }
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    editAdmin(admin) {
      this.editingAdmin = admin
      this.adminForm = {
        nom: admin.nom || '',
        email: admin.email || '',
        telephone: admin.telephone || '',
        role: admin.role || 'admin',
        password: '',
        password2: '',
        is_active: admin.is_active !== undefined ? admin.is_active : true
      }
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    closeModal() {
      this.showModal = false
      this.editingAdmin = null
      this.showPassword = false
      this.showPassword2 = false
      document.body.style.overflow = 'auto'
    },

    async saveAdmin() {
      if (!this.adminForm.nom || !this.adminForm.email || !this.adminForm.telephone) {
        this.showToast('error', 'Tous les champs obligatoires doivent être remplis')
        return
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.adminForm.email)) {
        this.showToast('error', 'Veuillez entrer une adresse email valide')
        return
      }

      if (!this.editingAdmin) {
        if (!this.adminForm.password || this.adminForm.password.length < 8) {
          this.showToast('error', 'Le mot de passe doit contenir au moins 8 caractères')
          return
        }
        if (this.adminForm.password !== this.adminForm.password2) {
          this.showToast('error', 'Les mots de passe ne correspondent pas')
          return
        }
      }

      this.loading = true

      try {
        const data = { ...this.adminForm }
        
        if (this.editingAdmin) {
          delete data.password
          delete data.password2
        }

        if (this.editingAdmin) {
          await axios.put(
            `${API_BASE_URL}/api/users/${this.editingAdmin.id}/`,
            data,
            {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
              }
            }
          )
          this.showToast('success', 'Administrateur modifié avec succès')
        } else {
          await axios.post(
            `${API_BASE_URL}/api/users/create/`,
            data,
            {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
              }
            }
          )
          this.showToast('success', 'Administrateur créé avec succès')
        }

        this.closeModal()
        await this.loadAdmins()
      } catch (error) {
        console.error('Erreur sauvegarde administrateur:', error)
        const errorMsg = error.response?.data?.errors || 
                        error.response?.data?.error || 
                        'Erreur lors de l\'enregistrement'
        this.showToast('error', typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg))
      } finally {
        this.loading = false
      }
    },

    async toggleAdminStatus(admin) {
      if (admin.id === this.currentUserId) {
        this.showToast('error', 'Vous ne pouvez pas modifier votre propre statut')
        return
      }

      const action = admin.is_active ? 'désactiver' : 'activer'
      if (!confirm(`Voulez-vous vraiment ${action} l'administrateur ${admin.nom} ?`)) return

      try {
        await axios.put(
          `${API_BASE_URL}/api/users/${admin.id}/toggle-status/`,
          { is_active: !admin.is_active },
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        )
        this.showToast('success', `Administrateur ${admin.is_active ? 'désactivé' : 'activé'} avec succès`)
        await this.loadAdmins()
      } catch (error) {
        console.error('Erreur changement statut:', error)
        this.showToast('error', 'Erreur lors du changement de statut')
      }
    },

    async deleteAdmin(admin) {
      if (admin.id === this.currentUserId) {
        this.showToast('error', 'Vous ne pouvez pas vous supprimer vous-même')
        return
      }

      if (!confirm(`Voulez-vous vraiment supprimer définitivement l'administrateur ${admin.nom} ?`)) return

      try {
        await axios.delete(
          `${API_BASE_URL}/api/users/${admin.id}/delete/`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          }
        )
        this.showToast('success', 'Administrateur supprimé avec succès')
        await this.loadAdmins()
      } catch (error) {
        console.error('Erreur suppression:', error)
        this.showToast('error', 'Erreur lors de la suppression')
      }
    },

    getInitials(name) {
      if (!name) return 'A'
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    },

    formatDate(dateString) {
      if (!dateString) return 'Jamais'
      const date = new Date(dateString)
      return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    resetFilters() {
      this.searchQuery = ''
      this.filterRole = ''
      this.filterStatus = ''
    },

    showToast(type, message) {
      this.toastType = type
      this.toastMessage = message
      setTimeout(() => {
        this.toastMessage = ''
      }, 4000)
    },

    confirmLogout() {
      if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        localStorage.removeItem('it_admin_authenticated')
        localStorage.removeItem('it_admin_username')
        localStorage.removeItem('it_admin_login_time')
        localStorage.removeItem('is_super_admin')
        useAuthStore().logout()
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
/* ============================================
   STYLES PROFESSIONNELS - PALETTE NOIR & OR
   ============================================ */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.admin-management {
  display: flex;
  min-height: 100vh;
  background: #f0f2f5;
  font-family: 'Inter', sans-serif;
}

/* ============================================
   SIDEBAR - STYLE ÉLÉGANT
   ============================================ */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 50%, #0d0d0d 100%);
  color: #e0e0e0;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  box-shadow: 4px 0 30px rgba(0,0,0,0.3);
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 28px 24px;
  border-bottom: 1px solid rgba(255,215,0,0.1);
  margin-bottom: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(255,215,0,0.25);
}

.logo-icon i {
  font-size: 22px;
  color: #0a0a0a;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  color: #FFD700;
  letter-spacing: 0.5px;
}

.logo-subtitle {
  font-size: 10px;
  color: rgba(255,255,255,0.4);
  letter-spacing: 1px;
  text-transform: uppercase;
}

.sidebar-nav {
  flex: 1;
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.3s;
  position: relative;
  font-size: 14px;
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  background: #FFD700;
  border-radius: 0 3px 3px 0;
  transform: scaleY(0);
  transition: transform 0.3s;
}

.nav-item:hover::before,
.nav-item.active::before {
  transform: scaleY(1);
}

.nav-item:hover {
  background: rgba(255,215,0,0.08);
  color: #ffffff;
  transform: translateX(4px);
}

.nav-item.active {
  background: rgba(255,215,0,0.12);
  color: #FFD700;
}

.nav-item i {
  width: 20px;
  font-size: 16px;
}

.nav-badge {
  margin-left: auto;
  font-size: 10px;
  background: #FFD700;
  color: #0a0a0a;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 600;
}

.sidebar-footer {
  padding: 16px 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
  margin-top: auto;
}

.user-info-sidebar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding: 8px 10px;
  background: rgba(255,255,255,0.04);
  border-radius: 10px;
}

.user-avatar-sidebar {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: #0a0a0a;
}

.user-details-sidebar {
  display: flex;
  flex-direction: column;
}

.user-name-sidebar {
  font-weight: 600;
  font-size: 13px;
  color: #e0e0e0;
}

.user-role {
  font-size: 9px;
  color: rgba(255,255,255,0.35);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  background: rgba(220,53,69,0.12);
  border: 1px solid rgba(220,53,69,0.2);
  border-radius: 10px;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  font-size: 13px;
}

.logout-btn:hover {
  background: rgba(220,53,69,0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220,53,69,0.15);
}

/* ============================================
   MAIN CONTENT
   ============================================ */
.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 24px 32px 40px;
}

/* ============================================
   TOP BAR
   ============================================ */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(255,215,0,0.2);
}

.title-icon i {
  font-size: 22px;
  color: #0a0a0a;
}

.title-text h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 2px;
}

.title-text p {
  font-size: 14px;
  color: #6b7280;
}

.btn-primary {
  padding: 10px 22px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #0a0a0a;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  transition: all 0.3s;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255,215,0,0.35);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ============================================
   STATS GRID
   ============================================ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s;
  border-left: 4px solid transparent;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

.stat-card.total { border-left-color: #4F46E5; }
.stat-card.active { border-left-color: #22c55e; }
.stat-card.inactive { border-left-color: #ef4444; }
.stat-card.super { border-left-color: #FFD700; }

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-card.total .stat-icon { background: rgba(79,70,229,0.12); color: #4F46E5; }
.stat-card.active .stat-icon { background: rgba(34,197,94,0.12); color: #22c55e; }
.stat-card.inactive .stat-icon { background: rgba(239,68,68,0.12); color: #ef4444; }
.stat-card.super .stat-icon { background: rgba(255,215,0,0.15); color: #FFD700; }

.stat-icon i { font-size: 20px; }

.stat-info h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1.2;
}

.stat-info p {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

/* ============================================
   FILTERS
   ============================================ */
.filters-section {
  background: white;
  border-radius: 14px;
  padding: 16px 20px;
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  align-items: center;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.search-box {
  flex: 1;
  position: relative;
  min-width: 200px;
}

.search-box i {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-box input {
  width: 100%;
  padding: 10px 16px 10px 42px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s;
  background: #f9fafb;
  font-family: 'Inter', sans-serif;
}

.search-box input:focus {
  outline: none;
  border-color: #FFD700;
  box-shadow: 0 0 0 3px rgba(255,215,0,0.1);
  background: white;
}

.filter-group {
  display: flex;
  gap: 10px;
}

.filter-select {
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Inter', sans-serif;
  color: #374151;
}

.filter-select:focus {
  outline: none;
  border-color: #FFD700;
  box-shadow: 0 0 0 3px rgba(255,215,0,0.1);
}

.results-count {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #6b7280;
  padding: 6px 14px;
  background: #f3f4f6;
  border-radius: 20px;
  white-space: nowrap;
}

.results-count i {
  color: #FFD700;
}

/* ============================================
   ADMIN LIST
   ============================================ */
.admins-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.admin-card {
  background: white;
  border-radius: 14px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s;
}

.admin-card:hover {
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  transform: translateX(4px);
}

.admin-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: white;
  position: relative;
  flex-shrink: 0;
  background: linear-gradient(135deg, #6b7280, #4b5563);
}

.admin-avatar.super-admin {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #0a0a0a;
  box-shadow: 0 4px 15px rgba(255,215,0,0.25);
}

.status-indicator {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid white;
  background: #ef4444;
}

.status-indicator.active {
  background: #22c55e;
}

.admin-info {
  flex: 1;
  min-width: 0;
}

.admin-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 6px;
}

.admin-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.role-badge.super {
  background: rgba(255,215,0,0.15);
  color: #b8860b;
}

.role-badge.admin {
  background: rgba(79,70,229,0.1);
  color: #4F46E5;
}

.status-badge {
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.status-badge.active {
  background: rgba(34,197,94,0.12);
  color: #16a34a;
}

.status-badge.inactive {
  background: rgba(239,68,68,0.12);
  color: #dc2626;
}

.admin-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 4px 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #6b7280;
}

.detail-item i {
  color: #9ca3af;
  width: 14px;
  font-size: 12px;
}

.admin-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

.action-btn {
  padding: 7px 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s;
  font-family: 'Inter', sans-serif;
}

.action-btn.edit {
  background: rgba(255,193,7,0.12);
  color: #b8860b;
}

.action-btn.edit:hover {
  background: rgba(255,193,7,0.25);
  transform: translateY(-2px);
}

.action-btn.status {
  background: rgba(239,68,68,0.1);
  color: #dc2626;
}

.action-btn.status.active {
  background: rgba(34,197,94,0.1);
  color: #16a34a;
}

.action-btn.status:hover {
  transform: translateY(-2px);
}

.action-btn.delete {
  background: rgba(239,68,68,0.1);
  color: #dc2626;
}

.action-btn.delete:hover:not(:disabled) {
  background: rgba(239,68,68,0.25);
  transform: translateY(-2px);
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ============================================
   EMPTY STATE
   ============================================ */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 14px;
}

.empty-state i {
  font-size: 56px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  color: #1a1a2e;
  margin-bottom: 6px;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 20px;
}

/* ============================================
   MODAL
   ============================================ */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  visibility: hidden;
  opacity: 0;
  transition: all 0.3s;
  backdrop-filter: blur(4px);
  padding: 20px;
}

.modal.active {
  visibility: visible;
  opacity: 1;
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 620px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
  position: sticky;
  top: 0;
  background: white;
  border-radius: 20px 20px 0 0;
  z-index: 1;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-title i {
  font-size: 22px;
  color: #FFD700;
}

.modal-title h2 {
  font-size: 20px;
  color: #1a1a2e;
  margin: 0;
}

.close-btn {
  width: 36px;
  height: 36px;
  background: none;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #1a1a2e;
  transform: rotate(90deg);
}

.close-btn i {
  font-size: 18px;
}

.modal-form {
  padding: 24px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-group label .required {
  color: #ef4444;
}

.form-group input,
.form-group select {
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  width: 100%;
  transition: all 0.3s;
  background: #f9fafb;
  font-family: 'Inter', sans-serif;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #FFD700;
  box-shadow: 0 0 0 3px rgba(255,215,0,0.1);
  background: white;
}

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-right: 44px;
}

.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 4px;
  transition: color 0.3s;
}

.toggle-password:hover {
  color: #FFD700;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 10px;
  margin: 8px 0 4px;
}

.form-group.checkbox label {
  font-weight: 400;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group.checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #FFD700;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.btn-secondary {
  padding: 10px 24px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
  font-family: 'Inter', sans-serif;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* ============================================
   TOAST
   ============================================ */
.toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 14px 22px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1100;
  animation: slideInRight 0.4s ease;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  font-weight: 500;
  min-width: 280px;
}

.toast.success {
  background: #22c55e;
  color: white;
}

.toast.error {
  background: #ef4444;
  color: white;
}

.toast-icon i {
  font-size: 20px;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 72px;
  }

  .sidebar-nav span,
  .sidebar-footer span,
  .logo-text,
  .user-info-sidebar,
  .nav-badge {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 12px;
  }

  .nav-item i {
    font-size: 18px;
    width: auto;
  }

  .main-content {
    margin-left: 72px;
    padding: 16px;
  }

  .top-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .admin-card {
    flex-direction: column;
    text-align: center;
  }

  .admin-actions {
    justify-content: center;
    width: 100%;
  }

  .admin-header {
    justify-content: center;
  }

  .admin-details {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .detail-item {
    justify-content: center;
  }

  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    flex-direction: column;
  }

  .form-row {
    flex-direction: column;
  }

  .modal-content {
    max-width: 95%;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .admin-actions {
    flex-direction: column;
  }

  .action-btn {
    justify-content: center;
  }
}
</style>