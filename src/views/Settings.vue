<template>
  <div class="settings">
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
        <router-link to="/herbier-data" class="menu-item">
          <i class="fas fa-database"></i>
          <span>Gestion des données</span>
        </router-link>
        <router-link to="/settings" class="menu-item active">
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
        <h1>Paramètres</h1>
      </div>
      
      <div class="content">
        <div class="settings-card">
          <h2>Informations du compte</h2>
          <form @submit.prevent="updateProfile">
            <div class="form-group">
              <label>Nom complet</label>
              <input type="text" v-model="profile.nom">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="profile.email">
            </div>
            <div class="form-group">
              <label>Téléphone</label>
              <input type="tel" v-model="profile.telephone">
            </div>
            <button type="submit" class="btn-save">Mettre à jour</button>
          </form>
        </div>
        
        <div class="settings-card">
          <h2>Changer le mot de passe</h2>
          <form @submit.prevent="changePassword">
            <div class="form-group">
              <label>Mot de passe actuel</label>
              <input type="password" v-model="passwordForm.current">
            </div>
            <div class="form-group">
              <label>Nouveau mot de passe</label>
              <input type="password" v-model="passwordForm.new">
            </div>
            <div class="form-group">
              <label>Confirmer le mot de passe</label>
              <input type="password" v-model="passwordForm.confirm">
            </div>
            <button type="submit" class="btn-save">Changer</button>
          </form>
        </div>
        
        <div class="settings-card">
          <h2>Synchronisation</h2>
          <button @click="syncWithPublicSite" class="btn-sync">
            <i class="fas fa-sync-alt"></i>
            Synchroniser avec le site public
          </button>
          <p class="help-text">Synchronise toutes les données avec le site public de l'herbier</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Settings',
  data() {
    return {
      profile: {
        nom: '',
        email: '',
        telephone: ''
      },
      passwordForm: {
        current: '',
        new: '',
        confirm: ''
      }
    }
  },
  mounted() {
    const authStore = useAuthStore()
    const user = authStore.user
    if (user) {
      this.profile = {
        nom: user.nom,
        email: user.email,
        telephone: user.telephone
      }
    }
  },
  methods: {
    async updateProfile() {
      alert('Fonctionnalité à implémenter')
    },
    async changePassword() {
      if (this.passwordForm.new !== this.passwordForm.confirm) {
        alert('Les mots de passe ne correspondent pas')
        return
      }
      alert('Fonctionnalité à implémenter')
    },
    async syncWithPublicSite() {
      alert('Synchronisation des données avec le site public...')
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
.settings {
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
}

.top-bar h1 {
  font-size: 24px;
  color: #1a472a;
}

.content {
  padding: 30px;
  max-width: 800px;
}

.settings-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.settings-card h2 {
  color: #1a472a;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
}

.btn-save {
  padding: 10px 20px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.btn-sync {
  padding: 12px 24px;
  background: #FFD700;
  color: #1a472a;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.help-text {
  margin-top: 10px;
  color: #666;
  font-size: 14px;
}
</style>
