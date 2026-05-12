<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="icon">
          <i class="fas fa-leaf"></i>
        </div>
        <h1>Administration Herbier</h1>
        <p>Connectez-vous à votre espace d'administration</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>
            <i class="fas fa-envelope"></i>
            Email
          </label>
          <input 
            type="email" 
            v-model="email" 
            required
            placeholder="admin@herbier-man.ci"
          >
        </div>

        <div class="form-group">
          <label>
            <i class="fas fa-lock"></i>
            Mot de passe
          </label>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password" 
            required
            placeholder="••••••••"
          >
          <button type="button" class="toggle-password" @click="showPassword = !showPassword">
            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>

        <button type="submit" class="btn-login" :disabled="loading">
          <span v-if="!loading">
            <i class="fas fa-sign-in-alt"></i>
            Se connecter
          </span>
          <span v-else>
            <i class="fas fa-spinner fa-pulse"></i>
            Connexion...
          </span>
        </button>
      </form>

      <div class="register-link">
        Pas encore de compte ? 
        <router-link to="/register">Créer un compte</router-link>
      </div>

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
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      loading: false,
      message: '',
      messageType: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.message = ''
      
      const authStore = useAuthStore()
      const result = await authStore.login({ email: this.email, password: this.password })
      
      if (result.success && result.requires2FA) {
        this.$router.push('/verify-2fa')
      } else if (!result.success) {
        this.messageType = 'error'
        this.message = result.message
      }
      
      this.loading = false
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
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 30px;
  padding: 40px;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header .icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.login-header .icon i {
  font-size: 30px;
  color: white;
}

.login-header h1 {
  font-size: 24px;
  color: #1a472a;
  margin-bottom: 10px;
}

.login-header p {
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

.form-group input {
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

.btn-login {
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

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(50,205,50,0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.register-link a {
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
