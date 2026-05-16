<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <div class="logo">
          <i class="fas fa-leaf"></i>
          <h1>Créer un compte</h1>
        </div>
        <p>Devenez administrateur de l'Herbier</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- Nom complet -->
        <div class="form-group" :class="{ 'has-error': errors.nom }">
          <label>Nom complet *</label>
          <input 
            type="text" 
            v-model="form.nom" 
            placeholder="Jean Kouassi"
            :class="{ 'error-input': errors.nom }"
          >
          <span class="error-text" v-if="errors.nom">{{ errors.nom }}</span>
        </div>

        <!-- Email -->
        <div class="form-group" :class="{ 'has-error': errors.email }">
          <label>Email *</label>
          <input 
            type="email" 
            v-model="form.email" 
            placeholder="admin@herbier-man.ci"
            :class="{ 'error-input': errors.email }"
          >
          <span class="error-text" v-if="errors.email">{{ errors.email }}</span>
        </div>

        <!-- Téléphone avec sélecteur de pays -->
        <div class="form-group" :class="{ 'has-error': errors.telephone }">
          <label>Téléphone *</label>
          <div class="phone-input-group">
            <select v-model="selectedCountry" @change="updatePhoneFormat" class="country-select">
              <optgroup label="🌍 Afrique">
                <option 
                  v-for="country in africanCountries" 
                  :key="country.code" 
                  :value="country"
                >
                  {{ country.flag }} {{ country.name }} ({{ country.dialCode }})
                </option>
              </optgroup>
              <optgroup label="🇪🇺 Europe">
                <option 
                  v-for="country in europeanCountries" 
                  :key="country.code" 
                  :value="country"
                >
                  {{ country.flag }} {{ country.name }} ({{ country.dialCode }})
                </option>
              </optgroup>
              <optgroup label="🌎 Amérique">
                <option 
                  v-for="country in americanCountries" 
                  :key="country.code" 
                  :value="country"
                >
                  {{ country.flag }} {{ country.name }} ({{ country.dialCode }})
                </option>
              </optgroup>
              <optgroup label="🌏 Asie & Océanie">
                <option 
                  v-for="country in asianCountries" 
                  :key="country.code" 
                  :value="country"
                >
                  {{ country.flag }} {{ country.name }} ({{ country.dialCode }})
                </option>
              </optgroup>
            </select>
            <input 
              type="tel" 
              v-model="form.telephone" 
              :placeholder="phonePlaceholder"
              :maxlength="phoneMaxLength"
              @input="validatePhoneInput"
              :class="{ 'error-input': errors.telephone }"
            >
          </div>
          <span class="helper-text">{{ phoneHelperText }}</span>
          <span class="error-text" v-if="errors.telephone">{{ errors.telephone }}</span>
        </div>

        <!-- Mot de passe -->
        <div class="form-group" :class="{ 'has-error': errors.password }">
          <label>Mot de passe *</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="form.password" 
              placeholder="Au moins 6 caractères"
              :class="{ 'error-input': errors.password }"
            >
            <button type="button" class="toggle-password" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span class="helper-text">Minimum 6 caractères</span>
          <span class="error-text" v-if="errors.password">{{ errors.password }}</span>
        </div>

        <!-- Confirmation mot de passe -->
        <div class="form-group" :class="{ 'has-error': errors.password2 }">
          <label>Confirmer le mot de passe *</label>
          <div class="password-input">
            <input 
              :type="showPassword2 ? 'text' : 'password'" 
              v-model="form.password2" 
              placeholder="Confirmez votre mot de passe"
              :class="{ 'error-input': errors.password2 }"
            >
            <button type="button" class="toggle-password" @click="showPassword2 = !showPassword2">
              <i :class="showPassword2 ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <span class="error-text" v-if="errors.password2">{{ errors.password2 }}</span>
        </div>

        <button type="submit" class="btn-register" :disabled="loading">
          <span v-if="!loading">
            <i class="fas fa-user-plus"></i> Créer mon compte
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i> Création en cours...
          </span>
        </button>
      </form>

      <div class="login-link">
        Déjà un compte ? 
        <router-link to="/login">Se connecter</router-link>
      </div>

      <!-- Messages de succès/erreur -->
      <div v-if="successMessage" class="alert alert-success">
        <i class="fas fa-check-circle"></i>
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="alert alert-error">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
      </div>

      <!-- Affichage des erreurs détaillées -->
      <div v-if="serverErrors.length" class="alert alert-error">
        <i class="fas fa-times-circle"></i>
        <div>
          <strong>Erreurs de validation :</strong>
          <ul>
            <li v-for="(err, idx) in serverErrors" :key="idx">{{ err }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        nom: '',
        email: '',
        telephone: '',
        password: '',
        password2: ''
      },
      selectedCountry: {
        code: 'CI',
        name: 'Côte d\'Ivoire',
        dialCode: '+225',
        flag: '🇨🇮',
        phoneLength: 10,
        phoneFormat: 'XX XX XX XX XX'
      },
      // Pays africains
      africanCountries: [
        { code: 'CI', name: 'Côte d\'Ivoire', dialCode: '+225', flag: '🇨🇮', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'SN', name: 'Sénégal', dialCode: '+221', flag: '🇸🇳', phoneLength: 9, phoneFormat: 'XX XXX XX XX' },
        { code: 'CM', name: 'Cameroun', dialCode: '+237', flag: '🇨🇲', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'ML', name: 'Mali', dialCode: '+223', flag: '🇲🇱', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'BF', name: 'Burkina Faso', dialCode: '+226', flag: '🇧🇫', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'GN', name: 'Guinée', dialCode: '+224', flag: '🇬🇳', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'TG', name: 'Togo', dialCode: '+228', flag: '🇹🇬', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'BJ', name: 'Bénin', dialCode: '+229', flag: '🇧🇯', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'NE', name: 'Niger', dialCode: '+227', flag: '🇳🇪', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'GA', name: 'Gabon', dialCode: '+241', flag: '🇬🇦', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'CD', name: 'RDC', dialCode: '+243', flag: '🇨🇩', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'MA', name: 'Maroc', dialCode: '+212', flag: '🇲🇦', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'TN', name: 'Tunisie', dialCode: '+216', flag: '🇹🇳', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'DZ', name: 'Algérie', dialCode: '+213', flag: '🇩🇿', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'GH', name: 'Ghana', dialCode: '+233', flag: '🇬🇭', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'NG', name: 'Nigeria', dialCode: '+234', flag: '🇳🇬', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'KE', name: 'Kenya', dialCode: '+254', flag: '🇰🇪', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'ZA', name: 'Afrique du Sud', dialCode: '+27', flag: '🇿🇦', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'EG', name: 'Égypte', dialCode: '+20', flag: '🇪🇬', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' }
      ],
      // Pays européens
      europeanCountries: [
        { code: 'FR', name: 'France', dialCode: '+33', flag: '🇫🇷', phoneLength: 9, phoneFormat: 'XX XX XX XX XX' },
        { code: 'BE', name: 'Belgique', dialCode: '+32', flag: '🇧🇪', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'CH', name: 'Suisse', dialCode: '+41', flag: '🇨🇭', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'LU', name: 'Luxembourg', dialCode: '+352', flag: '🇱🇺', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'MC', name: 'Monaco', dialCode: '+377', flag: '🇲🇨', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'DE', name: 'Allemagne', dialCode: '+49', flag: '🇩🇪', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'ES', name: 'Espagne', dialCode: '+34', flag: '🇪🇸', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'IT', name: 'Italie', dialCode: '+39', flag: '🇮🇹', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'PT', name: 'Portugal', dialCode: '+351', flag: '🇵🇹', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'GB', name: 'Royaume-Uni', dialCode: '+44', flag: '🇬🇧', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'IE', name: 'Irlande', dialCode: '+353', flag: '🇮🇪', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'NL', name: 'Pays-Bas', dialCode: '+31', flag: '🇳🇱', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'SE', name: 'Suède', dialCode: '+46', flag: '🇸🇪', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'NO', name: 'Norvège', dialCode: '+47', flag: '🇳🇴', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'DK', name: 'Danemark', dialCode: '+45', flag: '🇩🇰', phoneLength: 8, phoneFormat: 'XX XX XX XX' },
        { code: 'FI', name: 'Finlande', dialCode: '+358', flag: '🇫🇮', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'PL', name: 'Pologne', dialCode: '+48', flag: '🇵🇱', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'CZ', name: 'République Tchèque', dialCode: '+420', flag: '🇨🇿', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'AT', name: 'Autriche', dialCode: '+43', flag: '🇦🇹', phoneLength: 9, phoneFormat: 'XX XX XX XX' },
        { code: 'GR', name: 'Grèce', dialCode: '+30', flag: '🇬🇷', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'RU', name: 'Russie', dialCode: '+7', flag: '🇷🇺', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' }
      ],
      // Pays américains
      americanCountries: [
        { code: 'CA', name: 'Canada', dialCode: '+1', flag: '🇨🇦', phoneLength: 10, phoneFormat: 'XXX-XXX-XXXX' },
        { code: 'US', name: 'États-Unis', dialCode: '+1', flag: '🇺🇸', phoneLength: 10, phoneFormat: 'XXX-XXX-XXXX' },
        { code: 'MX', name: 'Mexique', dialCode: '+52', flag: '🇲🇽', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'BR', name: 'Brésil', dialCode: '+55', flag: '🇧🇷', phoneLength: 11, phoneFormat: 'XX XXXXX XXXX' },
        { code: 'AR', name: 'Argentine', dialCode: '+54', flag: '🇦🇷', phoneLength: 10, phoneFormat: 'XX XX XX XX XX' },
        { code: 'CL', name: 'Chili', dialCode: '+56', flag: '🇨🇱', phoneLength: 9, phoneFormat: 'X XXXX XXXX' },
        { code: 'CO', name: 'Colombie', dialCode: '+57', flag: '🇨🇴', phoneLength: 10, phoneFormat: 'XX XXX XXXX' }
      ],
      // Pays asiatiques et océanie
      asianCountries: [
        { code: 'CN', name: 'Chine', dialCode: '+86', flag: '🇨🇳', phoneLength: 11, phoneFormat: 'XXX XXXX XXXX' },
        { code: 'IN', name: 'Inde', dialCode: '+91', flag: '🇮🇳', phoneLength: 10, phoneFormat: 'XX XXX XXXX' },
        { code: 'JP', name: 'Japon', dialCode: '+81', flag: '🇯🇵', phoneLength: 10, phoneFormat: 'XX XXXX XXXX' },
        { code: 'KR', name: 'Corée du Sud', dialCode: '+82', flag: '🇰🇷', phoneLength: 10, phoneFormat: 'XX XXXX XXXX' },
        { code: 'AU', name: 'Australie', dialCode: '+61', flag: '🇦🇺', phoneLength: 9, phoneFormat: 'XX XXXX XXXX' }
      ],
      showPassword: false,
      showPassword2: false,
      loading: false,
      successMessage: '',
      errorMessage: '',
      serverErrors: [],
      errors: {
        nom: '',
        email: '',
        telephone: '',
        password: '',
        password2: ''
      }
    }
  },
  computed: {
    phonePlaceholder() {
      return `Ex: ${this.selectedCountry.phoneFormat}`
    },
    phoneMaxLength() {
      // Retourner la longueur maximale sans les séparateurs
      return this.selectedCountry.phoneLength
    },
    phoneHelperText() {
      return `Format attendu : ${this.selectedCountry.phoneLength} chiffres (sans le ${this.selectedCountry.dialCode})`
    }
  },
  methods: {
    validatePhoneInput() {
      // Supprimer les espaces et caractères non numériques
      let value = this.form.telephone.replace(/\D/g, '')
      
      // Limiter la longueur
      if (value.length > this.phoneMaxLength) {
        value = value.slice(0, this.phoneMaxLength)
      }
      
      // Formater l'affichage selon le pays
      let formatted = value
      
      // Formatage spécial pour certains pays
      if (this.selectedCountry.code === 'CA' || this.selectedCountry.code === 'US') {
        // Format US/Canada: XXX-XXX-XXXX
        if (value.length >= 3) formatted = value.slice(0, 3) + (value.length > 3 ? '-' + value.slice(3, 6) : '')
        if (value.length >= 6) formatted = formatted.slice(0, 7) + (value.length > 6 ? '-' + value.slice(6, 10) : '')
      } else if (this.selectedCountry.code === 'BR') {
        // Format Brésil: XX XXXXX XXXX
        if (value.length >= 2) formatted = value.slice(0, 2) + (value.length > 2 ? ' ' + value.slice(2, 7) : '')
        if (value.length >= 7) formatted = formatted.slice(0, 8) + (value.length > 7 ? ' ' + value.slice(7, 11) : '')
      } else {
        // Format standard: espaces tous les 2 chiffres
        let spaced = ''
        for (let i = 0; i < value.length; i++) {
          if (i > 0 && i % 2 === 0 && i < this.phoneMaxLength) {
            spaced += ' '
          }
          spaced += value[i]
        }
        formatted = spaced
      }
      
      this.form.telephone = formatted
      
      // Validation en temps réel
      const cleanNumber = value
      if (cleanNumber && cleanNumber.length !== this.phoneMaxLength) {
        this.errors.telephone = `Le numéro doit contenir ${this.phoneMaxLength} chiffres`
      } else if (cleanNumber) {
        this.errors.telephone = ''
      }
    },
    
    updatePhoneFormat() {
      this.form.telephone = ''
      this.errors.telephone = ''
    },
    
    validateForm() {
      let isValid = true
      this.errors = {
        nom: '',
        email: '',
        telephone: '',
        password: '',
        password2: ''
      }
      
      // Validation nom
      if (!this.form.nom || this.form.nom.trim().length < 2) {
        this.errors.nom = 'Le nom doit contenir au moins 2 caractères'
        isValid = false
      }
      
      // Validation email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.form.email || !emailRegex.test(this.form.email)) {
        this.errors.email = 'Veuillez entrer une adresse email valide'
        isValid = false
      }
      
      // Validation téléphone
      const cleanPhone = this.form.telephone.replace(/\D/g, '')
      if (!cleanPhone || cleanPhone.length !== this.phoneMaxLength) {
        this.errors.telephone = `Le numéro doit contenir ${this.phoneMaxLength} chiffres`
        isValid = false
      } else if (!/^\d+$/.test(cleanPhone)) {
        this.errors.telephone = 'Le numéro ne doit contenir que des chiffres'
        isValid = false
      }
      
      // Validation mot de passe
      if (!this.form.password || this.form.password.length < 6) {
        this.errors.password = 'Le mot de passe doit contenir au moins 6 caractères'
        isValid = false
      }
      
      // Validation confirmation
      if (this.form.password !== this.form.password2) {
        this.errors.password2 = 'Les mots de passe ne correspondent pas'
        isValid = false
      }
      
      return isValid
    },
    
    async handleRegister() {
      if (!this.validateForm()) {
        this.errorMessage = 'Veuillez corriger les erreurs dans le formulaire'
        setTimeout(() => { this.errorMessage = '' }, 5000)
        return
      }
      
      this.loading = true
      this.successMessage = ''
      this.errorMessage = ''
      this.serverErrors = []
      
      // Préparer les données
      const cleanPhone = this.form.telephone.replace(/\D/g, '')
      
      const userData = {
        nom: this.form.nom.trim(),
        email: this.form.email.trim(),
        telephone: cleanPhone,
        pays_code: this.selectedCountry.dialCode,
        password: this.form.password,
        password2: this.form.password2
      }
      
      try {
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'
        const response = await axios.post(`${API_URL}/create-superadmin/`, userData)
        
        if (response.data.success) {
          this.successMessage = response.data.message
          // Stocker l'email pour la vérification 2FA
          localStorage.setItem('auth_email', response.data.email)
          // Rediriger vers la vérification 2FA après 3 secondes
          setTimeout(() => {
            this.$router.push('/verify-2fa')
          }, 3000)
        } else {
          this.errorMessage = response.data.message || 'Erreur lors de la création du compte'
        }
      } catch (error) {
        console.error('Erreur:', error)
        if (error.response?.data?.errors) {
          const errors = error.response.data.errors
          for (const [field, messages] of Object.entries(errors)) {
            if (field === 'non_field_errors') {
              this.serverErrors.push(...messages)
            } else if (field === 'password') {
              this.errors.password = messages[0]
            } else if (this.errors[field] !== undefined) {
              this.errors[field] = messages[0]
            } else {
              this.serverErrors.push(`${field}: ${messages.join(', ')}`)
            }
          }
          this.errorMessage = 'Erreurs de validation'
        } else {
          this.errorMessage = error.response?.data?.error || 'Erreur de connexion au serveur'
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%);
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  max-width: 550px;
  width: 100%;
  box-shadow: 0 25px 50px rgba(0,0,0,0.25);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 10px;
}

.logo i {
  font-size: 42px;
  color: #32CD32;
}

.logo h1 {
  font-size: 24px;
  color: #1a472a;
  margin: 0;
}

.register-header p {
  color: #666;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.form-group input:not([type="checkbox"]) {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
}

.form-group.has-error input {
  border-color: #dc3545;
}

.error-input {
  border-color: #dc3545 !important;
}

.error-text {
  display: block;
  color: #dc3545;
  font-size: 12px;
  margin-top: 5px;
}

.helper-text {
  display: block;
  color: #888;
  font-size: 11px;
  margin-top: 5px;
}

.phone-input-group {
  display: flex;
  gap: 10px;
}

.country-select {
  width: 160px;
  padding: 12px 8px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 13px;
  cursor: pointer;
  background: white;
}

.country-select optgroup {
  font-weight: bold;
  color: #1a472a;
}

.country-select option {
  font-weight: normal;
  padding: 5px;
}

.phone-input-group input {
  flex: 1;
}

.password-input {
  position: relative;
}

.password-input input {
  width: 100%;
  padding-right: 45px;
}

.toggle-password {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  font-size: 16px;
}

.btn-register {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(50,205,50,0.3);
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.login-link a {
  color: #32CD32;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}

.alert {
  margin-top: 20px;
  padding: 12px 15px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert ul {
  margin: 5px 0 0 20px;
  padding: 0;
}

.alert li {
  margin: 3px 0;
}

@media (max-width: 600px) {
  .register-card {
    padding: 25px;
  }
  
  .phone-input-group {
    flex-direction: column;
  }
  
  .country-select {
    width: 100%;
  }
}
</style>
