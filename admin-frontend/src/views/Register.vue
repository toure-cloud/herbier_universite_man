<template>
  <div class="login-container">
    <!-- Background avec effet de feuilles -->
    <div class="login-bg">
      <div class="bg-leaf leaf-1"></div>
      <div class="bg-leaf leaf-2"></div>
      <div class="bg-leaf leaf-3"></div>
    </div>

    <div class="login-wrapper">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <i class="fas fa-user-plus"></i>
            </div>
            <div class="logo-text">
              <h1>Inscription</h1>
              <span>Administrateur</span>
            </div>
          </div>
          <h2>Créer un compte</h2>
          <p>Remplissez le formulaire pour créer votre compte administrateur</p>
        </div>

        <form @submit.prevent="handleRegister" class="login-form">
          <!-- Nom complet -->
          <div class="form-group" :class="{ 'error': errors.nom, 'focused': focusedField === 'nom' }">
            <label><i class="fas fa-user"></i> Nom complet *</label>
            <div class="input-wrapper">
              <input 
                type="text" 
                v-model="form.nom" 
                @focus="focusedField = 'nom'; clearFieldError('nom')"
                @blur="focusedField = null"
                placeholder="Jean Kouassi"
                :class="{ 'has-error': errors.nom }"
              >
              <i class="fas fa-check-circle input-icon-check" v-if="form.nom && !errors.nom"></i>
            </div>
            <div class="error-message" v-if="errors.nom">
              <i class="fas fa-exclamation-circle"></i> {{ errors.nom }}
            </div>
          </div>

          <!-- Email -->
          <div class="form-group" :class="{ 'error': errors.email, 'focused': focusedField === 'email' }">
            <label><i class="fas fa-envelope"></i> Email *</label>
            <div class="input-wrapper">
              <input 
                type="email" 
                v-model="form.email" 
                @focus="focusedField = 'email'; clearFieldError('email')"
                @blur="focusedField = null"
                placeholder="admin@herbier-man.ci"
                :class="{ 'has-error': errors.email }"
              >
              <i class="fas fa-check-circle input-icon-check" v-if="form.email && !errors.email"></i>
            </div>
            <div class="error-message" v-if="errors.email">
              <i class="fas fa-exclamation-circle"></i> {{ errors.email }}
            </div>
          </div>

          <!-- Pays et Téléphone -->
          <div class="form-row">
            <div class="form-group half" :class="{ 'error': errors.pays, 'focused': focusedField === 'pays' }">
              <label><i class="fas fa-globe-africa"></i> Pays *</label>
              <div class="input-wrapper">
                <select 
                  v-model="form.pays" 
                  @change="onCountryChange"
                  @focus="focusedField = 'pays'; clearFieldError('pays')"
                  @blur="focusedField = null"
                  :class="{ 'has-error': errors.pays }"
                  class="country-select"
                >
                  <option value="">Sélectionnez un pays</option>
                  <option v-for="country in countries" :key="country.code" :value="country.code">
                    {{ country.flag }} {{ country.name }} ({{ country.dialCode }})
                  </option>
                </select>
                <i class="fas fa-check-circle input-icon-check" v-if="form.pays && !errors.pays"></i>
              </div>
              <div class="error-message" v-if="errors.pays">
                <i class="fas fa-exclamation-circle"></i> {{ errors.pays }}
              </div>
            </div>

            <div class="form-group half" :class="{ 'error': errors.telephone, 'focused': focusedField === 'telephone' }">
              <label><i class="fas fa-phone"></i> Téléphone *</label>
              <div class="input-wrapper">
                <span class="phone-prefix" v-if="selectedCountry">{{ selectedCountry.dialCode }}</span>
                <input 
                  type="tel" 
                  v-model="form.telephone" 
                  @focus="focusedField = 'telephone'; clearFieldError('telephone')"
                  @blur="validatePhoneNumber"
                  :placeholder="phonePlaceholder"
                  :class="{ 'has-error': errors.telephone }"
                  :style="{ paddingLeft: selectedCountry ? '70px' : '16px' }"
                >
                <i class="fas fa-check-circle input-icon-check" v-if="form.telephone && !errors.telephone"></i>
              </div>
              <div class="error-message" v-if="errors.telephone">
                <i class="fas fa-exclamation-circle"></i> {{ errors.telephone }}
              </div>
              <div class="help-text" v-if="selectedCountry">
                <i class="fas fa-info-circle"></i> Format: {{ selectedCountry.format }}
              </div>
            </div>
          </div>

          <!-- Mot de passe -->
          <div class="form-group" :class="{ 'error': errors.password, 'focused': focusedField === 'password' }">
            <label><i class="fas fa-lock"></i> Mot de passe *</label>
            <div class="input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                v-model="form.password" 
                @focus="focusedField = 'password'; clearFieldError('password')"
                @blur="focusedField = null"
                placeholder="••••••••"
                :class="{ 'has-error': errors.password }"
              >
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <div class="error-message" v-if="errors.password">
              <i class="fas fa-exclamation-circle"></i> {{ errors.password }}
            </div>
            <div class="password-strength" v-if="form.password">
              <div class="strength-bar" :class="passwordStrength.class"></div>
              <span class="strength-text">{{ passwordStrength.text }}</span>
            </div>
          </div>

          <!-- Confirmation mot de passe -->
          <div class="form-group" :class="{ 'error': errors.password2, 'focused': focusedField === 'password2' }">
            <label><i class="fas fa-lock"></i> Confirmer le mot de passe *</label>
            <div class="input-wrapper">
              <input 
                :type="showPassword2 ? 'text' : 'password'" 
                v-model="form.password2" 
                @focus="focusedField = 'password2'; clearFieldError('password2')"
                @blur="focusedField = null"
                placeholder="••••••••"
                :class="{ 'has-error': errors.password2 }"
              >
              <button type="button" class="toggle-password" @click="showPassword2 = !showPassword2">
                <i :class="showPassword2 ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
              <i class="fas fa-check-circle input-icon-check" v-if="form.password2 && form.password === form.password2 && !errors.password2"></i>
            </div>
            <div class="error-message" v-if="errors.password2">
              <i class="fas fa-exclamation-circle"></i> {{ errors.password2 }}
            </div>
          </div>

          <!-- Conditions -->
          <div class="form-group">
            <label class="checkbox">
              <input type="checkbox" v-model="form.acceptTerms">
              <span class="checkmark"></span>
              <span class="checkbox-text">J'accepte les <a href="#" @click.prevent>conditions d'utilisation</a></span>
            </label>
          </div>

          <!-- Bouton -->
          <button type="submit" class="btn-login" :disabled="isLoading">
            <span v-if="!isLoading">
              <i class="fas fa-user-plus"></i> Créer le compte
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-pulse"></i> Création en cours...
            </span>
          </button>
        </form>

        <div class="login-divider"><span>ou</span></div>

        <div class="login-footer">
          <p>Déjà un compte ?</p>
          <router-link to="/login" class="register-link">
            Se connecter <i class="fas fa-arrow-right"></i>
          </router-link>
        </div>
      </div>

      <div class="login-footer-info">
        <p><i class="fas fa-shield-alt"></i> Compte sécurisé à 2 facteurs</p>
      </div>
    </div>

    <!-- Modal de succès -->
    <div class="modal-success" :class="{ active: showSuccessModal }">
      <div class="modal-overlay" @click="closeSuccessModal"></div>
      <div class="modal-content">
        <div class="modal-icon success">
          <i class="fas fa-check-circle"></i>
        </div>
        <h3>Compte créé avec succès !</h3>
        <p>{{ successMessage }}</p>
        <div class="modal-buttons">
          <button class="btn-primary" @click="goToLogin">
            <i class="fas fa-sign-in-alt"></i>
            Se connecter
          </button>
          <button class="btn-secondary" @click="closeSuccessModal">
            <i class="fas fa-times"></i>
            Fermer
          </button>
        </div>
      </div>
    </div>

    <!-- Modal d'erreur -->
    <div class="modal-error" :class="{ active: showErrorModal }">
      <div class="modal-overlay" @click="closeErrorModal"></div>
      <div class="modal-content">
        <div class="modal-icon error">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h3>Erreur</h3>
        <p>{{ errorMessage }}</p>
        <div class="modal-buttons">
          <button class="btn-primary" @click="closeErrorModal">
            <i class="fas fa-times"></i>
            Fermer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        nom: '',
        email: '',
        pays: '',
        telephone: '',
        password: '',
        password2: '',
        acceptTerms: false
      },
      showPassword: false,
      showPassword2: false,
      isLoading: false,
      focusedField: null,
      errors: {},
      
      // Modals
      showSuccessModal: false,
      successMessage: '',
      showErrorModal: false,
      errorMessage: '',
      
      // Liste des pays
      countries: [
        { code: 'CI', name: 'Côte d\'Ivoire', flag: '🇨🇮', dialCode: '+225', minLength: 10, maxLength: 10, format: 'XX XX XX XX XX' },
        { code: 'FR', name: 'France', flag: '🇫🇷', dialCode: '+33', minLength: 9, maxLength: 9, format: 'X XX XX XX XX' },
        { code: 'SN', name: 'Sénégal', flag: '🇸🇳', dialCode: '+221', minLength: 9, maxLength: 9, format: 'XX XXX XX XX' },
        { code: 'CM', name: 'Cameroun', flag: '🇨🇲', dialCode: '+237', minLength: 9, maxLength: 9, format: 'X XX XX XX XX' },
        { code: 'ML', name: 'Mali', flag: '🇲🇱', dialCode: '+223', minLength: 8, maxLength: 8, format: 'XX XX XX XX' },
        { code: 'BF', name: 'Burkina Faso', flag: '🇧🇫', dialCode: '+226', minLength: 8, maxLength: 8, format: 'XX XX XX XX' },
        { code: 'NE', name: 'Niger', flag: '🇳🇪', dialCode: '+227', minLength: 8, maxLength: 8, format: 'XX XX XX XX' },
        { code: 'TG', name: 'Togo', flag: '🇹🇬', dialCode: '+228', minLength: 8, maxLength: 8, format: 'XX XX XX XX' },
        { code: 'BJ', name: 'Bénin', flag: '🇧🇯', dialCode: '+229', minLength: 8, maxLength: 8, format: 'XX XX XX XX' },
        { code: 'GA', name: 'Gabon', flag: '🇬🇦', dialCode: '+241', minLength: 7, maxLength: 7, format: 'X XX XX XX' },
        { code: 'CD', name: 'République Démocratique du Congo', flag: '🇨🇩', dialCode: '+243', minLength: 9, maxLength: 9, format: 'XXX XXX XXX' },
        { code: 'MA', name: 'Maroc', flag: '🇲🇦', dialCode: '+212', minLength: 9, maxLength: 9, format: 'XX XX XX XX X' },
        { code: 'TN', name: 'Tunisie', flag: '🇹🇳', dialCode: '+216', minLength: 8, maxLength: 8, format: 'XX XXX XXX' },
        { code: 'DZ', name: 'Algérie', flag: '🇩🇿', dialCode: '+213', minLength: 9, maxLength: 9, format: 'XX XXX XXX X' },
        { code: 'BE', name: 'Belgique', flag: '🇧🇪', dialCode: '+32', minLength: 9, maxLength: 9, format: 'XXX XX XX XX' },
        { code: 'CH', name: 'Suisse', flag: '🇨🇭', dialCode: '+41', minLength: 9, maxLength: 9, format: 'XX XXX XX XX' },
        { code: 'CA', name: 'Canada', flag: '🇨🇦', dialCode: '+1', minLength: 10, maxLength: 10, format: 'XXX XXX XXXX' },
        { code: 'US', name: 'États-Unis', flag: '🇺🇸', dialCode: '+1', minLength: 10, maxLength: 10, format: '(XXX) XXX-XXXX' }
      ]
    }
  },
  computed: {
    selectedCountry() {
      return this.countries.find(c => c.code === this.form.pays)
    },
    phonePlaceholder() {
      return this.selectedCountry ? this.selectedCountry.format : 'Ex: XX XX XX XX XX'
    },
    passwordStrength() {
      const password = this.form.password
      if (!password) return { class: '', text: '' }
      
      let strength = 0
      if (password.length >= 8) strength++
      if (password.match(/[a-z]/)) strength++
      if (password.match(/[A-Z]/)) strength++
      if (password.match(/[0-9]/)) strength++
      if (password.match(/[^a-zA-Z0-9]/)) strength++
      
      if (strength <= 2) return { class: 'weak', text: 'Faible' }
      if (strength <= 4) return { class: 'medium', text: 'Moyen' }
      return { class: 'strong', text: 'Fort' }
    }
  },
  mounted() {
    const savedEmail = localStorage.getItem('saved_email')
    if (savedEmail) {
      this.form.email = savedEmail
    }
  },
  methods: {
    clearFieldError(field) {
      if (this.errors[field]) {
        delete this.errors[field]
      }
    },
    
    clearErrors() {
      this.errors = {}
    },
    
    onCountryChange() {
      this.form.telephone = ''
      if (this.errors.telephone) delete this.errors.telephone
      if (this.errors.pays) delete this.errors.pays
    },
    
    validatePhoneNumber() {
      if (!this.form.pays) {
        this.errors.pays = 'Veuillez sélectionner un pays'
        return false
      }
      
      if (!this.form.telephone) {
        this.errors.telephone = 'Le numéro de téléphone est requis'
        return false
      }
      
      const country = this.selectedCountry
      if (!country) return false
      
      let cleanNumber = this.form.telephone.replace(/\D/g, '')
      
      if (cleanNumber.length !== country.minLength) {
        this.errors.telephone = `Le numéro doit contenir exactement ${country.minLength} chiffres (${country.format})`
        return false
      }
      
      if (country.code === 'CI') {
        const prefix = cleanNumber.substring(0, 2)
        const validPrefixes = ['01', '05', '07', '08']
        if (!validPrefixes.includes(prefix)) {
          this.errors.telephone = 'Numéro invalide pour la Côte d\'Ivoire. Doit commencer par 01, 05, 07 ou 08'
          return false
        }
      }
      
      if (country.code === 'FR') {
        const firstDigit = cleanNumber.charAt(0)
        if (!['0', '1', '2', '3', '4', '5', '6', '7'].includes(firstDigit)) {
          this.errors.telephone = 'Numéro invalide pour la France'
          return false
        }
      }
      
      delete this.errors.telephone
      return true
    },
    
    formatPhoneNumberForAPI() {
      const country = this.selectedCountry
      if (!country || !this.form.telephone) return this.form.telephone
      
      let cleanNumber = this.form.telephone.replace(/\D/g, '')
      return `${country.dialCode}${cleanNumber}`
    },
    
    validateForm() {
      this.clearErrors()
      let isValid = true
      
      if (!this.form.nom || this.form.nom.trim().length < 2) {
        this.errors.nom = 'Nom complet requis (minimum 2 caractères)'
        isValid = false
      }
      
      if (!this.form.email) {
        this.errors.email = 'L\'adresse email est requise'
        isValid = false
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = 'Veuillez entrer une adresse email valide'
        isValid = false
      }
      
      if (!this.form.pays) {
        this.errors.pays = 'Veuillez sélectionner un pays'
        isValid = false
      }
      
      if (!this.validatePhoneNumber()) {
        isValid = false
      }
      
      if (!this.form.password) {
        this.errors.password = 'Le mot de passe est requis'
        isValid = false
      } else if (this.form.password.length < 6) {
        this.errors.password = 'Le mot de passe doit contenir au moins 6 caractères'
        isValid = false
      }
      
      if (this.form.password !== this.form.password2) {
        this.errors.password2 = 'Les mots de passe ne correspondent pas'
        isValid = false
      }
      
      if (!this.form.acceptTerms) {
        this.showErrorModalMessage('Vous devez accepter les conditions d\'utilisation')
        isValid = false
      }
      
      return isValid
    },
    
    showSuccessModalMessage(message) {
      this.successMessage = message
      this.showSuccessModal = true
    },
    
    closeSuccessModal() {
      this.showSuccessModal = false
    },
    
    goToLogin() {
      this.closeSuccessModal()
      this.$router.push('/login')
    },
    
    showErrorModalMessage(message) {
      this.errorMessage = message
      this.showErrorModal = true
    },
    
    closeErrorModal() {
      this.showErrorModal = false
      this.errorMessage = ''
    },
    
    async handleRegister() {
      if (!this.validateForm()) {
        const firstError = document.querySelector('.form-group.error')
        if (firstError) {
          firstError.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
        return
      }
      
      this.isLoading = true
      const authStore = useAuthStore()
      
      const registerData = {
        nom: this.form.nom,
        email: this.form.email,
        telephone: this.formatPhoneNumberForAPI(),
        password: this.form.password,
        password2: this.form.password2
      }
      
      try {
        // ✅ Utiliser le store qui utilise les variables d'environnement
        const result = await authStore.register(registerData)
        
        if (result.success) {
          this.showSuccessModalMessage(result.message || 'Votre compte a été créé avec succès. Un code de vérification a été envoyé à votre email et téléphone.')
        } else {
          const errorMsg = result.message || 'Une erreur est survenue'
          this.showErrorModalMessage(errorMsg)
          
          if (errorMsg.toLowerCase().includes('email')) {
            this.errors.email = errorMsg
          } else if (errorMsg.toLowerCase().includes('téléphone') || errorMsg.toLowerCase().includes('phone')) {
            this.errors.telephone = errorMsg
          } else {
            this.errors.general = errorMsg
          }
        }
      } catch (error) {
        console.error('Erreur:', error)
        const errorMsg = error.response?.data?.error || error.response?.data?.message || error.message || 'Une erreur est survenue'
        this.showErrorModalMessage(errorMsg)
      } finally {
        this.isLoading = false
      }
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
  background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%);
  position: relative;
  overflow-y: auto;
  padding: 40px 0;
}

/* Background animations */
.login-bg {
  position: fixed;
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
  animation: float 20s infinite;
}

.bg-leaf::before {
  content: "🌿";
  font-size: 100px;
  position: absolute;
}

.leaf-1 { top: 10%; left: -50px; animation-delay: 0s; }
.leaf-2 { bottom: 20%; right: -50px; animation-delay: 5s; }
.leaf-3 { top: 40%; left: 30%; animation-delay: 10s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(10deg); }
}

.login-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 580px;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 32px;
  padding: 40px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
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

/* Form row */
.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 0;
}

.form-group.half {
  flex: 1;
  margin-bottom: 20px;
}

/* Form styles */
.form-group {
  margin-bottom: 20px;
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

.input-wrapper input, .country-select {
  width: 100%;
  padding: 12px 42px 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.phone-prefix {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  font-size: 14px;
  font-weight: 500;
  z-index: 1;
}

.input-wrapper input:focus, .country-select:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50, 205, 50, 0.1);
}

.input-wrapper input.has-error, .country-select.has-error {
  border-color: #dc3545;
}

.input-wrapper input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
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

.help-text {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #888;
  margin-top: 6px;
}

.help-text i {
  font-size: 11px;
  color: #32CD32;
}

/* Password strength */
.password-strength {
  margin-top: 8px;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  transition: all 0.3s ease;
  margin-bottom: 4px;
}

.strength-bar.weak {
  width: 33%;
  background: #dc3545;
}

.strength-bar.medium {
  width: 66%;
  background: #ffc107;
}

.strength-bar.strong {
  width: 100%;
  background: #28a745;
}

.strength-text {
  font-size: 11px;
  color: #666;
}

/* Checkbox */
.checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-text {
  font-size: 13px;
  color: #555;
}

.checkbox-text a {
  color: #32CD32;
  text-decoration: none;
}

.checkbox-text a:hover {
  text-decoration: underline;
}

/* Button */
.btn-login {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
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
  margin-top: 10px;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(50, 205, 50, 0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Divider */
.login-divider {
  text-align: center;
  margin: 24px 0;
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

.login-footer-info i {
  margin-right: 6px;
}

/* Modal Styles */
.modal-success, .modal-error {
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

.modal-success.active, .modal-error.active {
  visibility: visible;
  opacity: 1;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  background: white;
  border-radius: 24px;
  padding: 40px;
  max-width: 450px;
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

.modal-icon.success {
  background: #d4edda;
  color: #28a745;
}

.modal-icon.error {
  background: #f8d7da;
  color: #dc3545;
}

.modal-icon i {
  font-size: 40px;
}

.modal-content h3 {
  font-size: 24px;
  color: #1a472a;
  margin-bottom: 12px;
  font-weight: 700;
}

.modal-content p {
  color: #555;
  line-height: 1.6;
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 20px;
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
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(50, 205, 50, 0.3);
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

/* Responsive */
@media (max-width: 600px) {
  .login-card {
    padding: 32px 24px;
  }
  
  .login-header h2 {
    font-size: 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .modal-content {
    padding: 30px 20px;
    margin: 20px;
  }
  
  .modal-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .btn-primary, .btn-secondary {
    justify-content: center;
  }
  
  .modal-content h3 {
    font-size: 20px;
  }
}
</style>