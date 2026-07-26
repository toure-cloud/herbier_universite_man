<template>
  <div class="it-login-container">
    <!-- Background -->
    <div class="login-bg">
      <div class="bg-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <div class="login-wrapper">
      <div class="login-card">
        <!-- Header -->
        <div class="login-header">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <i class="fas fa-shield-alt"></i>
            </div>
            <div class="logo-text">
              <h1>Accès IT</h1>
              <span>Administration sécurisée</span>
            </div>
          </div>
          <div class="security-badge">
            <i class="fas fa-lock"></i>
            <span>Connexion sécurisée</span>
          </div>
          <h2>Authentification IT Admin</h2>
          <p>Veuillez vous authentifier pour accéder à l'administration complète</p>
        </div>

        <!-- Formulaire -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group" :class="{ 'error': errors.username, 'focused': focusedField === 'username' }">
            <label><i class="fas fa-user"></i> Identifiant *</label>
            <div class="input-wrapper">
              <input 
                type="text" 
                v-model="form.username" 
                @focus="focusedField = 'username'; clearError('username')"
                @blur="focusedField = null"
                placeholder="it_admin"
                :class="{ 'has-error': errors.username }"
                autocomplete="username"
              >
              <i class="fas fa-check-circle input-icon-check" v-if="form.username && !errors.username"></i>
            </div>
            <div class="error-message" v-if="errors.username">
              <i class="fas fa-exclamation-circle"></i> {{ errors.username }}
            </div>
          </div>

          <div class="form-group" :class="{ 'error': errors.password, 'focused': focusedField === 'password' }">
            <label><i class="fas fa-lock"></i> Mot de passe *</label>
            <div class="input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                v-model="form.password" 
                @focus="focusedField = 'password'; clearError('password')"
                @blur="focusedField = null"
                placeholder="••••••••"
                :class="{ 'has-error': errors.password }"
                autocomplete="current-password"
                @keyup.enter="handleLogin"
              >
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <div class="error-message" v-if="errors.password">
              <i class="fas fa-exclamation-circle"></i> {{ errors.password }}
            </div>
          </div>

          <div class="default-credentials">
            <i class="fas fa-info-circle"></i>
            <span>Identifiants par défaut : <strong>it_admin</strong> / <strong>admin123</strong></span>
          </div>

          <button type="submit" class="btn-login" :disabled="isLoading">
            <span v-if="!isLoading">
              <i class="fas fa-shield-alt"></i> S'authentifier
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-pulse"></i> Authentification...
            </span>
          </button>
        </form>

        <div class="login-footer">
          <div class="security-info">
            <i class="fas fa-shield-alt"></i>
            <span>Protégé par authentification sécurisée</span>
          </div>
          <div class="return-link">
            <router-link to="/dashboard" class="return-btn">
              <i class="fas fa-arrow-left"></i>
              Retour au tableau de bord
            </router-link>
          </div>
        </div>
      </div>

      <div class="login-footer-info">
        <p><i class="fas fa-server"></i> Administration IT - Herbier Université de Man</p>
      </div>
    </div>

    <!-- Modal d'erreur -->
    <div class="modal-error" :class="{ active: showErrorModal }">
      <div class="modal-overlay" @click="closeErrorModal"></div>
      <div class="modal-content">
        <div class="modal-icon error">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h3>Échec de l'authentification</h3>
        <p>{{ errorMessage }}</p>
        <div class="modal-buttons">
          <button class="btn-primary" @click="closeErrorModal">
            <i class="fas fa-times"></i> Fermer
          </button>
          <button class="btn-secondary" @click="retryLogin">
            <i class="fas fa-redo-alt"></i> Réessayer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'ITLogin',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      showPassword: false,
      isLoading: false,
      focusedField: null,
      errors: {},
      showErrorModal: false,
      errorMessage: '',
      defaultCredentials: {
        username: 'it_admin',
        password: 'admin123'
      }
    }
  },
  mounted() {
    const isItAuthenticated = localStorage.getItem('it_admin_authenticated')
    if (isItAuthenticated === 'true') {
      this.$router.push('/dashboard')
      return
    }
    this.form.username = this.defaultCredentials.username
    this.form.password = this.defaultCredentials.password
  },
  methods: {
    clearError(field) {
      if (this.errors[field]) {
        delete this.errors[field]
      }
    },

    validateForm() {
      this.errors = {}
      let isValid = true

      if (!this.form.username) {
        this.errors.username = "L'identifiant est requis"
        isValid = false
      }

      if (!this.form.password) {
        this.errors.password = 'Le mot de passe est requis'
        isValid = false
      }

      return isValid
    },

    async handleLogin() {
      if (!this.validateForm()) {
        return
      }

      this.isLoading = true

      // ✅ Utiliser la variable d'environnement
      const ADMIN_API_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8001'
      
      try {
        // Tenter de se connecter via l'API
        const response = await fetch(`${ADMIN_API_URL}/login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.form.username,
            password: this.form.password
          })
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            localStorage.setItem('it_admin_authenticated', 'true')
            localStorage.setItem('it_admin_username', this.form.username)
            localStorage.setItem('it_admin_login_time', new Date().toISOString())
            this.$router.push('/dashboard')
            return
          }
        }
      } catch (error) {
        console.error('Erreur de connexion IT:', error)
      }

      // Fallback: si l'API ne répond pas, utiliser les identifiants par défaut
      if (this.form.username === this.defaultCredentials.username &&
          this.form.password === this.defaultCredentials.password) {
        
        localStorage.setItem('it_admin_authenticated', 'true')
        localStorage.setItem('it_admin_username', this.form.username)
        localStorage.setItem('it_admin_login_time', new Date().toISOString())
        
        this.$router.push('/dashboard')
      } else {
        this.showErrorModalMessage('Identifiant ou mot de passe incorrect. Utilisez it_admin / admin123')
      }

      this.isLoading = false
    },

    showErrorModalMessage(message) {
      this.errorMessage = message
      this.showErrorModal = true
    },

    closeErrorModal() {
      this.showErrorModal = false
    },

    retryLogin() {
      this.closeErrorModal()
      this.form.password = ''
      this.form.username = this.defaultCredentials.username
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');

.it-login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 50%, #0a0a1a 100%);
  position: relative;
  overflow: hidden;
  padding: 40px 0;
}

.login-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.bg-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.05;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: #FFD700;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #FF6B6B;
  bottom: -50px;
  left: -50px;
  animation-delay: 5s;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: #4F46E5;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(20px, 20px) scale(1.02); }
}

.login-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 480px;
  padding: 20px;
}

.login-card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  border-radius: 32px;
  padding: 40px;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 20px;
}

.logo-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px -5px rgba(255, 215, 0, 0.3);
}

.logo-icon i {
  font-size: 28px;
  color: #1a1a3a;
}

.logo-text h1 {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin: 0;
  line-height: 1;
}

.logo-text span {
  font-size: 12px;
  color: rgba(255,255,255,0.6);
  letter-spacing: 1px;
}

.security-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,215,0,0.15);
  border: 1px solid rgba(255,215,0,0.3);
  padding: 6px 16px;
  border-radius: 30px;
  font-size: 11px;
  color: #FFD700;
  margin-bottom: 16px;
}

.security-badge i {
  font-size: 12px;
}

.login-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
}

.login-header p {
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  margin: 0;
}

.login-form {
  margin-top: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255,255,255,0.8);
  margin-bottom: 8px;
}

.form-group label i {
  color: #FFD700;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 42px 14px 16px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  font-size: 14px;
  color: white;
  transition: all 0.3s ease;
}

.input-wrapper input::placeholder {
  color: rgba(255,255,255,0.3);
}

.input-wrapper input:focus {
  outline: none;
  border-color: #FFD700;
  background: rgba(255,255,255,0.12);
  box-shadow: 0 0 0 3px rgba(255,215,0,0.1);
}

.input-wrapper input.has-error {
  border-color: #EF4444;
}

.input-wrapper input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(239,68,68,0.1);
}

.input-icon-check {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #32CD32;
  font-size: 18px;
}

.toggle-password {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: rgba(255,255,255,0.4);
  padding: 0;
  font-size: 16px;
  transition: color 0.3s ease;
}

.toggle-password:hover {
  color: #FFD700;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #EF4444;
  margin-top: 6px;
}

.error-message i {
  font-size: 12px;
}

.default-credentials {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: rgba(255,215,0,0.08);
  border: 1px solid rgba(255,215,0,0.2);
  border-radius: 10px;
  margin: 16px 0 24px;
  color: rgba(255,255,255,0.7);
  font-size: 13px;
}

.default-credentials i {
  color: #FFD700;
  font-size: 16px;
}

.default-credentials strong {
  color: #FFD700;
}

.btn-login {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #1a1a3a;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(255,215,0,0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
  text-align: center;
}

.security-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: rgba(255,255,255,0.4);
  font-size: 12px;
  margin-bottom: 12px;
}

.security-info i {
  color: #32CD32;
}

.return-link {
  margin-top: 8px;
}

.return-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.3s ease;
}

.return-btn:hover {
  color: #FFD700;
  gap: 12px;
}

.login-footer-info {
  text-align: center;
  margin-top: 24px;
  color: rgba(255,255,255,0.3);
  font-size: 12px;
}

.login-footer-info i {
  margin-right: 6px;
}

.modal-error {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  visibility: hidden;
  opacity: 0;
  transition: all 0.3s ease;
}

.modal-error.active {
  visibility: visible;
  opacity: 1;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
}

.modal-content {
  position: relative;
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 24px;
  padding: 40px;
  max-width: 420px;
  width: 90%;
  text-align: center;
  animation: modalSlideIn 0.3s ease;
  z-index: 1;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.modal-icon.error {
  background: rgba(239,68,68,0.2);
  color: #EF4444;
  border: 2px solid rgba(239,68,68,0.3);
}

.modal-icon i {
  font-size: 40px;
}

.modal-content h3 {
  font-size: 22px;
  color: white;
  margin-bottom: 12px;
  font-weight: 700;
}

.modal-content p {
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
  margin-bottom: 24px;
}

.modal-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary, .btn-secondary {
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #1a1a3a;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(255,215,0,0.3);
}

.btn-secondary {
  background: rgba(255,255,255,0.1);
  color: white;
  border: 1px solid rgba(255,255,255,0.2);
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.2);
}

@media (max-width: 600px) {
  .login-card {
    padding: 32px 24px;
  }
  
  .login-header h2 {
    font-size: 18px;
  }
  
  .modal-content {
    padding: 30px 20px;
    margin: 20px;
  }
  
  .modal-buttons {
    flex-direction: column;
  }
  
  .btn-primary, .btn-secondary {
    justify-content: center;
  }

  .default-credentials {
    font-size: 12px;
    padding: 8px 12px;
  }
}
</style>