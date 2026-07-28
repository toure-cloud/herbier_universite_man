<template>
  <div class="verify-container">
    <div class="verify-card">
      <div class="verify-header">
        <div class="icon">
          <i class="fas fa-shield-alt"></i>
        </div>
        <h1>Vérification en deux étapes</h1>
        <p>Un code de vérification a été envoyé à votre adresse email</p>
      </div>

      <form @submit.prevent="handleVerify" class="verify-form">
        <div class="code-inputs">
          <input 
            v-for="(digit, index) in 6" 
            :key="index"
            type="text"
            maxlength="1"
            v-model="codeDigits[index]"
            @input="handleCodeInput(index, $event)"
            @keydown="handleCodeKeydown(index, $event)"
            @paste="handlePaste"
            ref="codeInputs"
            class="code-digit"
            :class="{ 'code-digit-filled': codeDigits[index] }"
            autocomplete="one-time-code"
            inputmode="numeric"
            pattern="[0-9]"
          >
        </div>

        <button type="submit" class="btn-verify" :disabled="loading">
          <span v-if="!loading">
            <i class="fas fa-check-circle"></i>
            Vérifier
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i>
            Vérification...
          </span>
        </button>

        <button type="button" class="btn-resend" @click="resendCode" :disabled="resendLoading || resendTimer > 0">
          <span v-if="!resendLoading">
            <i class="fas fa-redo-alt"></i>
            Renvoyer le code
            <span v-if="resendTimer > 0" class="timer-badge">({{ resendTimer }}s)</span>
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i>
            Envoi...
          </span>
        </button>
      </form>

      <div v-if="message" class="message" :class="messageType">
        <i :class="messageType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

// ✅ Utiliser la variable d'environnement
const ADMIN_API_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8001/api'

export default {
  name: 'Verify2FA',
  data() {
    return {
      codeDigits: ['', '', '', '', '', ''],
      loading: false,
      resendLoading: false,
      message: '',
      messageType: '',
      resendTimer: 0,
      timerInterval: null
    }
  },
  computed: {
    fullCode() {
      return this.codeDigits.join('')
    },
    userEmail() {
      const authStore = useAuthStore()
      return authStore.getEmail
    }
  },
  mounted() {
    const authStore = useAuthStore()
    
    // ✅ Vérifier l'email
    if (!authStore.getEmail) {
      this.setMessage('Aucune session trouvée, veuillez vous connecter', 'error')
      setTimeout(() => {
        this.$router.push('/login')
      }, 1500)
      return
    }
    
    // ✅ Focus sur le premier champ
    this.$nextTick(() => {
      this.$refs.codeInputs[0]?.focus()
    })
  },
  beforeUnmount() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval)
      this.timerInterval = null
    }
  },
  methods: {
    handleCodeInput(index, event) {
      const value = event.target.value
      const cleanedValue = value.replace(/\D/g, '')
      
      if (cleanedValue && /^\d$/.test(cleanedValue)) {
        this.codeDigits[index] = cleanedValue
        if (index < 5) {
          this.$refs.codeInputs[index + 1]?.focus()
        } else {
          setTimeout(() => {
            if (this.fullCode.length === 6 && !this.loading) {
              this.handleVerify()
            }
          }, 300)
        }
      } else if (value === '' || cleanedValue === '') {
        this.codeDigits[index] = ''
      } else {
        this.codeDigits[index] = ''
      }
    },
    handleCodeKeydown(index, event) {
      if (event.key === 'ArrowLeft' && index > 0) {
        event.preventDefault()
        this.$refs.codeInputs[index - 1]?.focus()
      } else if (event.key === 'ArrowRight' && index < 5) {
        event.preventDefault()
        this.$refs.codeInputs[index + 1]?.focus()
      } else if (event.key === 'Backspace' && !this.codeDigits[index] && index > 0) {
        this.$refs.codeInputs[index - 1]?.focus()
      } else if (event.key === 'Delete' && !this.codeDigits[index] && index < 5) {
        this.$refs.codeInputs[index + 1]?.focus()
      }
    },
    handlePaste(event) {
      event.preventDefault()
      const pasteData = event.clipboardData.getData('text').replace(/\D/g, '')
      if (pasteData.length >= 6) {
        const code = pasteData.slice(0, 6).split('')
        this.codeDigits = code
        this.$refs.codeInputs[5]?.focus()
        setTimeout(() => {
          if (this.fullCode.length === 6 && !this.loading) {
            this.handleVerify()
          }
        }, 300)
      }
    },
    async handleVerify() {
      if (this.fullCode.length !== 6) {
        this.setMessage('Veuillez entrer un code à 6 chiffres', 'error')
        return
      }
      
      if (this.loading) return
      
      this.loading = true
      this.message = ''
      
      const authStore = useAuthStore()
      
      try {
        console.log('🔐 Vérification du code:', this.fullCode)
        console.log('📧 Email:', authStore.getEmail)
        
        const result = await authStore.verify2FA(this.fullCode)
        
        console.log('📥 Résultat vérification:', result)
        
        if (result.success) {
          this.setMessage('✅ Authentification réussie ! Redirection...', 'success')
          
          setTimeout(() => {
            console.log('🚀 Redirection vers /dashboard')
            this.$router.push('/dashboard')
          }, 1500)
        } else {
          this.setMessage(result.message || '❌ Code invalide', 'error')
          this.codeDigits = ['', '', '', '', '', '']
          this.$nextTick(() => {
            this.$refs.codeInputs[0]?.focus()
          })
        }
      } catch (error) {
        console.error('❌ Erreur de vérification:', error)
        let errorMessage = '❌ Erreur de connexion au serveur'
        
        if (error.response) {
          if (error.response.status === 401) {
            errorMessage = '❌ Code invalide ou expiré'
          } else if (error.response.status === 404) {
            errorMessage = '❌ Utilisateur non trouvé'
          } else if (error.response.data?.error) {
            errorMessage = `❌ ${error.response.data.error}`
          } else if (error.response.data?.message) {
            errorMessage = `❌ ${error.response.data.message}`
          }
        } else if (error.request) {
          errorMessage = '❌ Impossible de contacter le serveur'
        }
        
        this.setMessage(errorMessage, 'error')
        this.codeDigits = ['', '', '', '', '', '']
      } finally {
        this.loading = false
      }
    },
    async resendCode() {
      if (this.resendTimer > 0) {
        this.setMessage(`⏱️ Veuillez attendre ${this.resendTimer}s avant de renvoyer`, 'error')
        return
      }
      
      if (this.resendLoading) return
      
      this.resendLoading = true
      this.message = ''
      
      const authStore = useAuthStore()
      
      try {
        console.log('📧 Renvoi du code pour:', authStore.getEmail)
        
        const response = await axios.post(`${ADMIN_API_URL}/resend-code/`, {
          email: authStore.getEmail
        })
        
        console.log('📥 Réponse resend:', response.data)
        
        if (response.data.success) {
          this.setMessage('✅ Un nouveau code a été envoyé à votre email', 'success')
          this.startResendTimer(60)
        } else {
          this.setMessage(response.data.error || '❌ Erreur lors de l\'envoi', 'error')
        }
      } catch (error) {
        console.error('❌ Erreur resend:', error)
        let errorMessage = '❌ Erreur lors de l\'envoi du code'
        
        if (error.response) {
          if (error.response.status === 404) {
            errorMessage = '❌ Utilisateur non trouvé'
          } else if (error.response.data?.error) {
            errorMessage = `❌ ${error.response.data.error}`
          } else if (error.response.data?.message) {
            errorMessage = `❌ ${error.response.data.message}`
          }
        } else if (error.request) {
          errorMessage = '❌ Impossible de contacter le serveur'
        }
        
        this.setMessage(errorMessage, 'error')
      } finally {
        this.resendLoading = false
      }
    },
    setMessage(text, type) {
      this.message = text
      this.messageType = type
      
      if (type === 'error') {
        setTimeout(() => {
          if (this.message === text) {
            this.message = ''
          }
        }, 5000)
      }
    },
    startResendTimer(seconds) {
      this.resendTimer = seconds
      
      if (this.timerInterval) {
        clearInterval(this.timerInterval)
        this.timerInterval = null
      }
      
      this.timerInterval = setInterval(() => {
        this.resendTimer--
        if (this.resendTimer <= 0) {
          clearInterval(this.timerInterval)
          this.timerInterval = null
          this.resendTimer = 0
        }
      }, 1000)
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
  border-radius: 30px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
  text-align: center;
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.verify-header .icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.verify-header .icon i {
  font-size: 30px;
  color: white;
}

.verify-header h1 {
  font-size: 24px;
  color: #1a472a;
  margin-bottom: 10px;
}

.verify-header p {
  color: #666;
  margin-bottom: 0;
}

.code-inputs {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 30px 0;
}

.code-digit {
  width: 50px;
  height: 60px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  border: 2px solid #ddd;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: #fafafa;
  color: #1a472a;
}

.code-digit:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
  background: white;
  transform: scale(1.05);
}

.code-digit-filled {
  border-color: #32CD32;
  background: #f0fff0;
}

.btn-verify, .btn-resend {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-verify {
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}

.btn-verify::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: rotate(45deg);
  transition: all 0.5s;
}

.btn-verify:hover:not(:disabled)::after {
  left: 100%;
}

.btn-verify:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(50,205,50,0.3);
}

.btn-verify:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-resend {
  background: none;
  border: 1px solid #ddd;
  color: #666;
}

.btn-resend:hover:not(:disabled) {
  border-color: #32CD32;
  color: #32CD32;
  background: #f0fff0;
}

.btn-resend:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.timer-badge {
  font-size: 12px;
  font-weight: normal;
  color: #999;
}

.message {
  margin-top: 20px;
  padding: 12px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: fadeInUp 0.3s ease-out;
}

.message.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message i {
  font-size: 18px;
}

/* ✅ Responsive */
@media (max-width: 520px) {
  .verify-card {
    padding: 30px 20px;
  }
  
  .code-digit {
    width: 40px;
    height: 50px;
    font-size: 20px;
  }
  
  .code-inputs {
    gap: 8px;
  }
  
  .verify-header h1 {
    font-size: 20px;
  }
}

@media (max-width: 400px) {
  .code-digit {
    width: 35px;
    height: 45px;
    font-size: 18px;
  }
  
  .code-inputs {
    gap: 6px;
  }
}

/* ✅ Dark mode support */
@media (prefers-color-scheme: dark) {
  .verify-card {
    background: #1a1a2e;
  }
  
  .verify-header h1 {
    color: #32CD32;
  }
  
  .verify-header p {
    color: #aaa;
  }
  
  .code-digit {
    background: #2a2a3e;
    border-color: #444;
    color: white;
  }
  
  .code-digit:focus {
    background: #3a3a4e;
  }
  
  .code-digit-filled {
    border-color: #32CD32;
    background: #1a3a1a;
  }
  
  .btn-resend {
    color: #aaa;
    border-color: #444;
  }
  
  .btn-resend:hover:not(:disabled) {
    border-color: #32CD32;
    color: #32CD32;
    background: #1a2a1a;
  }
  
  .message.success {
    background: #1a3a1a;
    color: #32CD32;
    border-color: #32CD32;
  }
  
  .message.error {
    background: #3a1a1a;
    color: #ff6b6b;
    border-color: #ff6b6b;
  }
}
</style>