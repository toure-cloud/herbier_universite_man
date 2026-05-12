<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <div class="icon">
          <i class="fas fa-leaf"></i>
        </div>
        <h1>Création du Super Administrateur</h1>
        <p>Configurez le compte administrateur principal</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label>
            <i class="fas fa-user"></i>
            Nom complet *
          </label>
          <input 
            type="text" 
            v-model="form.nom" 
            required
            placeholder="Jean Kouassi"
          >
        </div>

        <div class="form-group">
          <label>
            <i class="fas fa-envelope"></i>
            Email *
          </label>
          <input 
            type="email" 
            v-model="form.email" 
            required
            placeholder="admin@herbier-man.ci"
          >
        </div>

        <div class="form-group">
          <label>
            <i class="fas fa-phone"></i>
            Téléphone *
          </label>
          <input 
            type="tel" 
            v-model="form.telephone" 
            required
            placeholder="+225 07 00 00 00"
          >
        </div>

        <div class="form-group">
          <label>
            <i class="fas fa-lock"></i>
            Mot de passe *
          </label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="form.password" 
            required
            placeholder="••••••••"
          >
          <button type="button" class="toggle-password" @click="showPassword = !showPassword">
            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>

        <div class="form-group">
          <label>
            <i class="fas fa-lock"></i>
            Confirmer le mot de passe *
          </label>
          <input 
            :type="showPassword2 ? 'text' : 'password'" 
            v-model="form.password2" 
            required
            placeholder="••••••••"
          >
          <button type="button" class="toggle-password" @click="showPassword2 = !showPassword2">
            <i :class="showPassword2 ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>

        <div class="form-group">
          <label class="checkbox">
            <input type="checkbox" v-model="form.acceptTerms" required>
            <span>J'accepte les conditions d'utilisation</span>
          </label>
        </div>

        <button type="submit" class="btn-register" :disabled="loading">
          <span v-if="!loading">
            <i class="fas fa-user-plus"></i>
            Créer le compte
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i>
            Création en cours...
          </span>
        </button>

        <div class="login-link">
          Déjà un compte ? 
          <router-link to="/login">Se connecter</router-link>
        </div>
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
  name: 'Register',
  data() {
    return {
      form: {
        nom: '',
        email: '',
        telephone: '',
        password: '',
        password2: '',
        acceptTerms: false
      },
      showPassword: false,
      showPassword2: false,
      loading: false,
      message: '',
      messageType: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.message = ''
      
      const authStore = useAuthStore()
      const result = await authStore.register(this.form)
      
      if (result.success) {
        this.messageType = 'success'
        this.message = result.message
        setTimeout(() => {
          this.$router.push('/verify-2fa')
        }, 3000)
      } else {
        this.messageType = 'error'
        this.message = result.message
      }
      
      this.loading = false
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
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 30px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header .icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.register-header .icon i {
  font-size: 30px;
  color: white;
}

.register-header h1 {
  font-size: 24px;
  color: #1a472a;
  margin-bottom: 10px;
}

.register-header p {
  color: #666;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-group label i {
  color: #32CD32;
  margin-right: 8px;
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

.toggle-password {
  position: absolute;
  right: 15px;
  top: 38px;
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
}

.checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox input {
  width: auto;
  margin-right: 10px;
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
}

.login-link a {
  color: #32CD32;
  text-decoration: none;
  font-weight: 600;
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
