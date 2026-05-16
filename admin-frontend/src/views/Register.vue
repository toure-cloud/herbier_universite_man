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
        <div class="form-group">
          <label>Nom complet *</label>
          <input type="text" v-model="form.nom" placeholder="Jean Kouassi" required>
        </div>

        <div class="form-group">
          <label>Email *</label>
          <input type="email" v-model="form.email" placeholder="admin@herbier-man.ci" required>
        </div>

        <div class="form-group">
          <label>Téléphone *</label>
          <input type="tel" v-model="form.telephone" placeholder="+225 07 00 00 00" required>
        </div>

        <div class="form-group">
          <label>Mot de passe *</label>
          <input :type="showPassword ? 'text' : 'password'" v-model="form.password" required>
          <button type="button" class="toggle-password" @click="showPassword = !showPassword">
            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>

        <div class="form-group">
          <label>Confirmer *</label>
          <input :type="showPassword2 ? 'text' : 'password'" v-model="form.password2" required>
          <button type="button" class="toggle-password" @click="showPassword2 = !showPassword2">
            <i :class="showPassword2 ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </button>
        </div>

        <button type="submit" class="btn-register" :disabled="loading">
          <span v-if="!loading">Créer mon compte</span>
          <span v-else><i class="fas fa-spinner fa-pulse"></i> Création...</span>
        </button>
      </form>

      <div class="login-link">
        Déjà un compte ? 
        <router-link to="/login">Se connecter</router-link>
      </div>

      <div v-if="successMessage" class="success-message">
        <i class="fas fa-check-circle"></i>
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="error-message">
        <i class="fas fa-exclamation-circle"></i>
        {{ errorMessage }}
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
        password2: ''
      },
      showPassword: false,
      showPassword2: false,
      loading: false,
      successMessage: '',
      errorMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.successMessage = ''
      this.errorMessage = ''
      
      if (this.form.password !== this.form.password2) {
        this.errorMessage = 'Les mots de passe ne correspondent pas'
        this.loading = false
        return
      }
      
      const authStore = useAuthStore()
      const result = await authStore.register(this.form)
      
      if (result.success) {
        this.successMessage = result.message
        setTimeout(() => {
          this.$router.push('/verify-2fa')
        }, 3000)
      } else {
        this.errorMessage = result.message
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
  background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%);
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
}

.logo i {
  font-size: 40px;
  color: #32CD32;
}

.logo h1 {
  color: #1a472a;
  margin: 0;
}

.register-header p {
  color: #666;
  font-size: 14px;
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

.success-message {
  margin-top: 15px;
  padding: 10px;
  background: #d4edda;
  color: #155724;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background: #f8d7da;
  color: #721c24;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
</style>
