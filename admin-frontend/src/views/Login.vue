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
          <label for="email">Email</label>
          <div class="input-group">
            <i class="fas fa-envelope"></i>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="exemple@domaine.com"
              required
              autocomplete="email"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <div class="input-group">
            <i class="fas fa-lock"></i>
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              placeholder="Votre mot de passe"
              required
              autocomplete="current-password"
            />
            <button 
              type="button" 
              class="toggle-password"
              @click="showPassword = !showPassword"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
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

        <div class="login-footer">
          <router-link to="/forgot-password" class="forgot-link">
            Mot de passe oublié ?
          </router-link>
        </div>

        <div class="register-section">
          <div class="divider">
            <span>ou</span>
          </div>
          <p class="register-text">
            Vous n'avez pas de compte ?
            <router-link to="/register" class="register-link">
              Créer un compte <i class="fas fa-arrow-right"></i>
            </router-link>
          </p>
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
      if (!this.email || !this.password) {
        this.setMessage('Veuillez remplir tous les champs', 'error')
        return
      }

      this.loading = true
      this.message = ''
      
      const authStore = useAuthStore()
      
      try {
        console.log('🔐 Tentative de connexion pour:', this.email)
        
        const result = await authStore.login({
          email: this.email,
          password: this.password
        })
        
        console.log('📥 Réponse du login:', result)
        
        if (result.success) {
          if (result.requires2FA) {
            console.log('✅ 2FA requis - Redirection vers /verify-2fa')
            this.setMessage('📧 Un code de vérification a été envoyé à votre email', 'success')
            
            setTimeout(() => {
              this.$router.push('/verify-2fa')
            }, 1500)
          } else {
            console.log('✅ Connexion réussie sans 2FA')
            this.setMessage('Connexion réussie !', 'success')
            
            setTimeout(() => {
              this.$router.push('/dashboard')
            }, 1000)
          }
        } else {
          console.log('❌ Erreur de connexion:', result.message)
          this.setMessage(result.message || 'Email ou mot de passe incorrect', 'error')
        }
      } catch (error) {
        console.error('❌ Erreur lors de la connexion:', error)
        
        // ✅ Gestion améliorée des erreurs
        let errorMessage = 'Erreur de connexion au serveur'
        if (error.response) {
          // Le serveur a répondu avec un code d'erreur
          if (error.response.status === 500) {
            errorMessage = 'Erreur interne du serveur. Veuillez réessayer plus tard.'
          } else if (error.response.status === 401) {
            errorMessage = 'Email ou mot de passe incorrect'
          } else if (error.response.data?.message) {
            errorMessage = error.response.data.message
          } else if (error.response.data?.error) {
            errorMessage = error.response.data.error
          }
        } else if (error.request) {
          // La requête a été faite mais pas de réponse
          errorMessage = 'Impossible de contacter le serveur. Vérifiez votre connexion.'
        }
        
        this.setMessage(errorMessage, 'error')
      } finally {
        this.loading = false
      }
    },
    setMessage(text, type) {
      this.message = text
      this.messageType = type
    }
  },
  mounted() {
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
      this.$router.push('/dashboard')
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
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 30px;
  padding: 40px;
  max-width: 420px;
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
  margin: 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group i {
  position: absolute;
  left: 15px;
  color: #999;
}

.input-group input {
  width: 100%;
  padding: 12px 15px 12px 45px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #32CD32;
  box-shadow: 0 0 0 3px rgba(50,205,50,0.1);
}

.toggle-password {
  position: absolute;
  right: 15px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 0;
}

.btn-login {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #32CD32, #228B22);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(50,205,50,0.3);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
}

.forgot-link {
  color: #32CD32;
  text-decoration: none;
  font-size: 14px;
}

.forgot-link:hover {
  text-decoration: underline;
}

.register-section {
  margin-top: 24px;
  text-align: center;
}

.divider {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #e0e0e0;
}

.divider span {
  padding: 0 16px;
  color: #999;
  font-size: 13px;
  font-weight: 500;
}

.register-text {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.register-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #1a472a;
  font-weight: 600;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: #f0f7f0;
}

.register-link:hover {
  background: #e0f0e0;
  gap: 10px;
  transform: translateX(2px);
}

.register-link i {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.register-link:hover i {
  transform: translateX(4px);
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

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
}
</style>