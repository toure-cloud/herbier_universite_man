<template>
  <div class="login-container">
    <!-- Background avec effet de feuilles -->
    <div class="login-bg">
      <div class="bg-leaf leaf-1"></div>
      <div class="bg-leaf leaf-2"></div>
      <div class="bg-leaf leaf-3"></div>
      <div class="bg-leaf leaf-4"></div>
      <div class="bg-leaf leaf-5"></div>
    </div>

    <div class="login-wrapper">
      <div class="login-card">
        <!-- Logo et titre -->
        <div class="login-header">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <i class="fas fa-leaf"></i>
            </div>
            <div class="logo-text">
              <h1>Herbier</h1>
              <span>Université de Man</span>
            </div>
          </div>
          <h2>Connexion administrateur</h2>
          <p>Accédez à votre espace de gestion</p>
        </div>

        <!-- Formulaire de connexion -->
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Champ Email -->
          <div class="form-group" :class="{ 'error': errors.email, 'focused': focusedField === 'email' }">
            <label>
              <i class="fas fa-envelope"></i>
              <span>Adresse email</span>
            </label>
            <div class="input-wrapper">
              <input 
                type="email" 
                v-model="form.email" 
                @focus="focusedField = 'email'"
                @blur="focusedField = null"
                placeholder="admin@herbier-man.ci"
                :class="{ 'has-error': errors.email }"
                autocomplete="email"
              >
              <i class="fas fa-check-circle input-icon-check" v-if="form.email && !errors.email"></i>
            </div>
            <div class="error-message" v-if="errors.email">
              <i class="fas fa-exclamation-circle"></i>
              {{ errors.email }}
            </div>
          </div>

          <!-- Champ Mot de passe -->
          <div class="form-group" :class="{ 'error': errors.password, 'focused': focusedField === 'password' }">
            <label>
              <i class="fas fa-lock"></i>
              <span>Mot de passe</span>
            </label>
            <div class="input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                v-model="form.password" 
                @focus="focusedField = 'password'"
                @blur="focusedField = null"
                placeholder="••••••••"
                :class="{ 'has-error': errors.password }"
                autocomplete="current-password"
              >
              <button 
                type="button" 
                class="toggle-password" 
                @click="togglePassword"
                :title="showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
              <i class="fas fa-check-circle input-icon-check" v-if="form.password && !errors.password"></i>
            </div>
            <div class="error-message" v-if="errors.password">
              <i class="fas fa-exclamation-circle"></i>
              {{ errors.password }}
            </div>
          </div>

          <!-- Options supplémentaires -->
          <div class="form-options">
            <label class="checkbox">
              <input type="checkbox" v-model="rememberMe">
              <span class="checkmark"></span>
              <span class="checkbox-text">Se souvenir de moi</span>
            </label>
            <a href="#" class="forgot-link" @click.prevent="forgotPassword">Mot de passe oublié ?</a>
          </div>

          <!-- Bouton de connexion -->
          <button type="submit" class="btn-login" :disabled="isLoading">
            <span v-if="!isLoading">
              <i class="fas fa-sign-in-alt"></i>
              Se connecter
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-pulse"></i>
              Connexion en cours...
            </span>
          </button>
        </form>

        <!-- Séparateur -->
        <div class="login-divider">
          <span>ou</span>
        </div>

        <!-- Lien d'inscription -->
        <div class="login-footer">
          <p>Pas encore de compte ?</p>
          <router-link to="/register" class="register-link">
            Créer un compte administrateur
            <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>

        <!-- Message d'alerte global -->
        <div v-if="alertMessage" class="alert-message" :class="alertType">
          <i :class="alertType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle'"></i>
          <span>{{ alertMessage }}</span>
          <button class="alert-close" @click="clearAlert">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>

      <!-- Footer informations -->
      <div class="login-footer-info">
        <p>
          <i class="fas fa-shield-alt"></i>
          Connexion sécurisée à 2 facteurs
        </p>
        <p>© 2024 Herbier Université de Man - Tous droits réservés</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      showPassword: false,
      rememberMe: false,
      isLoading: false,
      focusedField: null,
      alertMessage: '',
      alertType: '',
      errors: {
        email: '',
        password: ''
      }
    }
  },
  mounted() {
    // Vérifier si l'email est sauvegardé
    const savedEmail = localStorage.getItem('saved_email')
    if (savedEmail) {
      this.form.email = savedEmail
      this.rememberMe = true
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    
    validateForm() {
      let isValid = true
      this.errors = { email: '', password: '' }
      
      // Validation email
      if (!this.form.email) {
        this.errors.email = 'L\'adresse email est requise'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = 'Veuillez entrer une adresse email valide'
        isValid = false
      }
      
      // Validation mot de passe
      if (!this.form.password) {
        this.errors.password = 'Le mot de passe est requis'
        isValid = false
      } else if (this.form.password.length < 6) {
        this.errors.password = 'Le mot de passe doit contenir au moins 6 caractères'
        isValid = false
      }
      
      return isValid
    },
    
    showAlert(message, type = 'error') {
      this.alertMessage = message
      this.alertType = type
      setTimeout(() => {
        this.clearAlert()
      }, 5000)
    },
    
    clearAlert() {
      this.alertMessage = ''
      this.alertType = ''
    },
    
    async handleLogin() {
      if (!this.validateForm()) {
        return
      }
      
      this.isLoading = true
      this.clearAlert()
      
      // Sauvegarder l'email si "Se souvenir de moi" est coché
      if (this.rememberMe) {
        localStorage.setItem('saved_email', this.form.email)
      } else {
        localStorage.removeItem('saved_email')
      }
      
      const authStore = useAuthStore()
      const result = await authStore.login({ 
        email: this.form.email, 
        password: this.form.password 
      })
      
      if (result.success && result.requires2FA) {
        this.showAlert('Code de vérification envoyé à votre adresse email', 'success')
        setTimeout(() => {
          this.$router.push('/verify-2fa')
        }, 1500)
      } else if (!result.success) {
        this.showAlert(result.message || 'Email ou mot de passe incorrect')
        // Animation d'erreur sur les champs
        this.errors.email = result.message || 'Identifiants incorrects'
        this.errors.password = result.message || 'Identifiants incorrects'
      }
      
      this.isLoading = false
    },
    
    forgotPassword() {
      this.$router.push('/forgot-password')
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%);
}

/* Background avec feuilles animées */
.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.bg-leaf {
  position: absolute;
  opacity: 0.1;
  animation: float 20s infinite ease-in-out;
}

.bg-leaf::before {
  content: "🌿";
  font-size: 100px;
  position: absolute;
}

.leaf-1 { top: 10%; left: -50px; animation-delay: 0s; }
.leaf-2 { bottom: 20%; right: -50px; animation-delay: 5s; }
.leaf-3 { top: 50%; left: 20%; animation-delay: 10s; transform: scale(0.8); }
.leaf-4 { bottom: 10%; left: 30%; animation-delay: 15s; transform: scale(1.2); }
.leaf-5 { top: 30%; right: 10%; animation-delay: 2s; transform: scale(0.9); }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(10deg); }
}

.login-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 480px;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 32px;
  padding: 48px 40px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.3);
}

/* Header */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.logo-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px -5px rgba(50, 205, 50, 0.3);
}

.logo-icon i {
  font-size: 28px;
  color: white;
}

.logo-text h1 {
  font-size: 28px;
  font-weight: 800;
  color: #1a472a;
  margin: 0;
  line-height: 1;
}

.logo-text span {
  font-size: 12px;
  color: #666;
  letter-spacing: 1px;
}

.login-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a472a;
  margin-bottom: 8px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

/* Form Group */
.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.form-group label i {
  color: #32CD32;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 42px 14px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 14px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: white;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 4px rgba(50, 205, 50, 0.1);
}

.input-wrapper input.has-error {
  border-color: #dc3545;
}

.input-wrapper input.has-error:focus {
  box-shadow: 0 0 0 4px rgba(220, 53, 69, 0.1);
}

.input-icon-check {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #28a745;
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
  color: #999;
  padding: 0;
  font-size: 16px;
  transition: color 0.3s ease;
}

.toggle-password:hover {
  color: #32CD32;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #dc3545;
  margin-top: 6px;
}

.error-message i {
  font-size: 12px;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  padding-left: 28px;
  user-select: none;
}

.checkbox input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: white;
  border: 2px solid #ddd;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.checkbox:hover input ~ .checkmark {
  border-color: #32CD32;
}

.checkbox input:checked ~ .checkmark {
  background-color: #32CD32;
  border-color: #32CD32;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox input:checked ~ .checkmark:after {
  display: block;
}

.checkbox .checkmark:after {
  left: 5px;
  top: 1px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-text {
  font-size: 13px;
  color: #555;
}

.forgot-link {
  font-size: 13px;
  color: #32CD32;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #228B22;
  text-decoration: underline;
}

/* Button Login */
.btn-login {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  border-radius: 14px;
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
  box-shadow: 0 10px 25px -5px rgba(50, 205, 50, 0.4);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Divider */
.login-divider {
  text-align: center;
  margin: 28px 0;
  position: relative;
}

.login-divider::before,
.login-divider::after {
  content: "";
  position: absolute;
  top: 50%;
  width: calc(50% - 30px);
  height: 1px;
  background: #e0e0e0;
}

.login-divider::before {
  left: 0;
}

.login-divider::after {
  right: 0;
}

.login-divider span {
  background: white;
  padding: 0 16px;
  color: #999;
  font-size: 13px;
}

/* Footer */
.login-footer {
  text-align: center;
}

.login-footer p {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
}

.register-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #f5f5f5;
  color: #1a472a;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.register-link:hover {
  background: #e8f5e8;
  gap: 12px;
}

.login-footer-info {
  text-align: center;
  margin-top: 24px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.login-footer-info p:first-child {
  margin-bottom: 8px;
}

.login-footer-info i {
  margin-right: 6px;
}

/* Alert Message */
.alert-message {
  position: fixed;
  top: 20px;
  right: 20px;
  left: auto;
  max-width: 400px;
  padding: 14px 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1000;
  animation: slideInRight 0.3s ease;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
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

.alert-message.success {
  background: #d4edda;
  border-left: 4px solid #28a745;
  color: #155724;
}

.alert-message.error {
  background: #f8d7da;
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.alert-message.info {
  background: #d1ecf1;
  border-left: 4px solid #17a2b8;
  color: #0c5460;
}

.alert-message i {
  font-size: 20px;
}

.alert-message span {
  flex: 1;
  font-size: 14px;
}

.alert-close {
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.alert-close:hover {
  opacity: 1;
}

/* Responsive */
@media (max-width: 520px) {
  .login-card {
    padding: 32px 24px;
  }
  
  .login-header h2 {
    font-size: 20px;
  }
  
  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .alert-message {
    left: 20px;
    right: 20px;
    max-width: none;
  }
}
</style>
