<template>
  <div class="verify-container">
    <div class="verify-card">
      <div class="verify-header">
        <div class="icon">
          <i class="fas fa-shield-alt"></i>
        </div>
        <h1>Vérification en deux étapes</h1>
        <p>Un code de vérification a été envoyé à votre numéro de téléphone</p>
      </div>

      <form @submit.prevent="handleVerify" class="verify-form">
        <!-- Affichage du numéro de téléphone (non modifiable) -->
        <div class="form-group">
          <label>
            <i class="fas fa-phone-alt"></i>
            Numéro de téléphone
          </label>
          <div class="phone-display">
            <div class="phone-info">
              <span class="phone-number">{{ formattedPhone }}</span>
              <span class="phone-badge" v-if="phoneExists">✓ Numéro enregistré</span>
            </div>
            <p class="helper-text">Le code a été envoyé à ce numéro</p>
          </div>
        </div>

        <!-- Code de vérification à 6 chiffres -->
        <div class="form-group">
          <label>
            <i class="fas fa-key"></i>
            Code de vérification
          </label>
          <div class="code-inputs">
            <input 
              v-for="(digit, index) in 6" 
              :key="index"
              type="text"
              maxlength="1"
              v-model="codeDigits[index]"
              @input="handleCodeInput(index, $event)"
              @keydown="handleCodeKeydown(index, $event)"
              ref="codeInputs"
              class="code-digit"
              :disabled="loading"
            >
          </div>
          <span class="helper-text">Entrez le code à 6 chiffres reçu par SMS</span>
        </div>

        <div class="info-message">
          <i class="fas fa-info-circle"></i>
          <span>Un SMS contenant le code de vérification a été envoyé à votre numéro</span>
        </div>

        <button type="submit" class="btn-verify" :disabled="loading">
          <span v-if="!loading">
            <i class="fas fa-check-circle"></i>
            Vérifier
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i>
            Vérification en cours...
          </span>
        </button>

        <button type="button" class="btn-resend" @click="resendCode" :disabled="resendLoading">
          <span v-if="!resendLoading">
            <i class="fas fa-redo-alt"></i>
            Renvoyer le code
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i>
            Envoi en cours...
          </span>
        </button>
      </form>

      <div class="login-link">
        <router-link to="/login">
          <i class="fas fa-arrow-left"></i>
          Retour à la connexion
        </router-link>
      </div>

      <div v-if="successMessage" class="alert alert-success">
        <i class="fas fa-check-circle"></i>
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="alert alert-error">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../services/api'

export default {
  name: 'Verify2FA',
  data() {
    return {
      telephone: '',
      codeDigits: ['', '', '', '', '', ''],
      loading: false,
      resendLoading: false,
      successMessage: '',
      errorMessage: ''
    }
  },
  computed: {
    fullCode() {
      return this.codeDigits.join('')
    },
    phoneExists() {
      return !!this.telephone
    },
    formattedPhone() {
      if (!this.telephone) return 'Aucun numéro enregistré'
      // Formater l'affichage du téléphone
      let formatted = this.telephone
      let spaced = ''
      for (let i = 0; i < this.telephone.length; i++) {
        if (i > 0 && i % 2 === 0) {
          spaced += ' '
        }
        spaced += this.telephone[i]
      }
      return spaced || this.telephone
    }
  },
  mounted() {
    // Récupérer le numéro depuis localStorage (stocké lors de l'inscription)
    const storedPhone = localStorage.getItem('auth_telephone')
    const storedEmail = localStorage.getItem('auth_email')
    
    console.log('📞 Téléphone stocké:', storedPhone)
    console.log('📧 Email stocké:', storedEmail)
    
    if (storedPhone) {
      this.telephone = storedPhone
    } else {
      this.errorMessage = 'Aucun numéro de téléphone trouvé. Veuillez vous réinscrire.'
    }
    
    // Focus sur le premier champ du code
    this.$nextTick(() => {
      if (this.$refs.codeInputs && this.$refs.codeInputs[0]) {
        this.$refs.codeInputs[0].focus()
      }
    })
  },
  methods: {
    handleCodeInput(index, event) {
      const value = event.target.value
      if (value && /^\d$/.test(value)) {
        this.codeDigits[index] = value
        if (index < 5) {
          this.$refs.codeInputs[index + 1].focus()
        } else {
          this.handleVerify()
        }
      } else if (value === '') {
        this.codeDigits[index] = ''
      }
    },
    
    handleCodeKeydown(index, event) {
      if (event.key === 'Backspace' && !this.codeDigits[index] && index > 0) {
        this.$refs.codeInputs[index - 1].focus()
      }
    },
    
    async handleVerify() {
      if (!this.telephone) {
        this.errorMessage = 'Numéro de téléphone non trouvé. Veuillez vous réinscrire.'
        return
      }
      
      if (this.fullCode.length !== 6) {
        this.errorMessage = 'Veuillez entrer le code à 6 chiffres'
        return
      }
      
      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''
      
      try {
        const response = await authAPI.verify2FA({
          telephone: this.telephone,  // Envoyer le numéro sans espaces
          code: this.fullCode
        })
        
        if (response.data.success) {
          this.successMessage = 'Authentification réussie ! Redirection...'
          localStorage.setItem('access_token', response.data.access)
          localStorage.setItem('refresh_token', response.data.refresh)
          localStorage.removeItem('auth_telephone')
          localStorage.removeItem('auth_email')
          
          setTimeout(() => {
            this.$router.push('/dashboard')
          }, 1500)
        } else {
          this.errorMessage = response.data.message || 'Code invalide'
          this.resetCode()
        }
      } catch (error) {
        console.error('Erreur:', error)
        this.errorMessage = error.response?.data?.error || 'Erreur lors de la vérification'
        this.resetCode()
      } finally {
        this.loading = false
      }
    },
    
    async resendCode() {
      if (!this.telephone) {
        this.errorMessage = 'Numéro de téléphone non trouvé. Veuillez vous réinscrire.'
        return
      }
      
      this.resendLoading = true
      this.errorMessage = ''
      this.successMessage = ''
      
      try {
        const response = await authAPI.resendCode({ telephone: this.telephone })
        
        if (response.data.success) {
          this.successMessage = 'Un nouveau code a été envoyé par SMS'
          setTimeout(() => { this.successMessage = '' }, 3000)
        } else {
          this.errorMessage = response.data.message || 'Erreur lors de l\'envoi'
        }
      } catch (error) {
        console.error('Erreur:', error)
        this.errorMessage = error.response?.data?.error || 'Erreur lors de l\'envoi'
      } finally {
        this.resendLoading = false
      }
    },
    
    resetCode() {
      this.codeDigits = ['', '', '', '', '', '']
      if (this.$refs.codeInputs && this.$refs.codeInputs[0]) {
        this.$refs.codeInputs[0].focus()
      }
    }
  }
}
</script>

<style scoped>
.verify-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%);
  padding: 20px;
}

.verify-card {
  background: white;
  border-radius: 24px;
  padding: 40px;
  max-width: 550px;
  width: 100%;
  box-shadow: 0 25px 50px rgba(0,0,0,0.25);
}

.verify-header {
  text-align: center;
  margin-bottom: 30px;
}

.icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.icon i {
  font-size: 32px;
  color: white;
}

.verify-header h1 {
  font-size: 24px;
  color: #1a472a;
  margin-bottom: 10px;
}

.verify-header p {
  color: #666;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.form-group label i {
  color: #32CD32;
  margin-right: 8px;
}

.phone-display {
  background: #f5f5f5;
  border-radius: 10px;
  padding: 15px;
}

.phone-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.phone-number {
  font-size: 18px;
  font-weight: bold;
  color: #1a472a;
  font-family: monospace;
}

.phone-badge {
  background: #d4edda;
  color: #155724;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.helper-text {
  display: block;
  color: #888;
  font-size: 11px;
  margin-top: 8px;
}

.code-inputs {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 10px 0;
}

.code-digit {
  width: 55px;
  height: 65px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  border: 2px solid #ddd;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.code-digit:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
}

.info-message {
  background: #e8f5e9;
  padding: 12px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2e7d32;
  font-size: 13px;
}

.info-message i {
  font-size: 16px;
}

.btn-verify {
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
  margin-bottom: 12px;
}

.btn-verify:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(50,205,50,0.3);
}

.btn-resend {
  width: 100%;
  padding: 12px;
  background: none;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
}

.btn-resend:hover:not(:disabled) {
  border-color: #32CD32;
  color: #32CD32;
}

.btn-verify:disabled, .btn-resend:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link a {
  color: #666;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.login-link a:hover {
  color: #32CD32;
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

@media (max-width: 600px) {
  .verify-card {
    padding: 25px;
  }
  
  .code-digit {
    width: 45px;
    height: 55px;
    font-size: 20px;
  }
  
  .phone-info {
    flex-direction: column;
    text-align: center;
  }
}
</style>
