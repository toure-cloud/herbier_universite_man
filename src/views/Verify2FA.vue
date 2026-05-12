<template>
  <div class="verify-container">
    <div class="verify-card">
      <div class="verify-header">
        <div class="icon">
          <i class="fas fa-shield-alt"></i>
        </div>
        <h1>Vérification en deux étapes</h1>
        <p>Un code de vérification a été envoyé à votre email et téléphone</p>
      </div>

      <form @submit.prevent="handleVerify" class="verify-form">
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
            >
          </div>
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

        <button type="button" class="btn-resend" @click="resendCode" :disabled="resendLoading">
          <span v-if="!resendLoading">
            <i class="fas fa-redo-alt"></i>
            Renvoyer le code
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

export default {
  name: 'Verify2FA',
  data() {
    return {
      codeDigits: ['', '', '', '', '', ''],
      loading: false,
      resendLoading: false,
      message: '',
      messageType: ''
    }
  },
  computed: {
    fullCode() {
      return this.codeDigits.join('')
    }
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
      if (this.fullCode.length !== 6) {
        this.message = 'Veuillez entrer un code à 6 chiffres'
        this.messageType = 'error'
        return
      }
      
      this.loading = true
      this.message = ''
      
      const authStore = useAuthStore()
      const result = await authStore.verify2FA(this.fullCode)
      
      if (result.success) {
        this.messageType = 'success'
        this.message = 'Authentification réussie !'
        setTimeout(() => {
          this.$router.push('/dashboard')
        }, 1500)
      } else {
        this.messageType = 'error'
        this.message = result.message || 'Code invalide'
        this.codeDigits = ['', '', '', '', '', '']
        this.$refs.codeInputs[0].focus()
      }
      
      this.loading = false
    },
    async resendCode() {
      this.resendLoading = true
      this.message = ''
      
      const authStore = useAuthStore()
      try {
        const response = await axios.post('http://localhost:8001/api/resend-otp/', {
          email: authStore.getEmail
        })
        if (response.data.success) {
          this.messageType = 'success'
          this.message = 'Un nouveau code a été envoyé'
        }
      } catch (error) {
        this.messageType = 'error'
        this.message = 'Erreur lors de l\'envoi du code'
      }
      
      this.resendLoading = false
    }
  },
  mounted() {
    this.$refs.codeInputs[0].focus()
  }
}
</script>

<style scoped>
.verify-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.verify-card {
  background: white;
  border-radius: 30px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.verify-header {
  text-align: center;
  margin-bottom: 30px;
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
}

.code-inputs {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 20px 0;
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
}

.code-digit:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
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
  margin-top: 20px;
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
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 12px;
  color: #666;
}

.btn-resend:hover:not(:disabled) {
  border-color: #32CD32;
  color: #32CD32;
}

.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.message.success {
  background: #d4edda;
  color: #155724;
}

.message.error {
  background: #f8d7da;
  color: #721c24;
}
</style>
