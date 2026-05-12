<template>
  <div class="forgot-container">
    <div class="login-bg">
      <div class="bg-leaf leaf-1"></div>
      <div class="bg-leaf leaf-2"></div>
      <div class="bg-leaf leaf-3"></div>
    </div>

    <div class="forgot-wrapper">
      <div class="forgot-card">
        <div class="forgot-header">
          <div class="logo-wrapper">
            <div class="logo-icon"><i class="fas fa-lock"></i></div>
            <div class="logo-text"><h1>Mot de passe oublié</h1><span>Réinitialisation</span></div>
          </div>
          <h2>{{ step === 1 ? 'Réinitialiser votre mot de passe' : step === 2 ? 'Vérification' : 'Nouveau mot de passe' }}</h2>
          <p>{{ stepMessage }}</p>
        </div>

        <!-- Étape 1: Demande d'email -->
        <form v-if="step === 1" @submit.prevent="sendResetCode" class="forgot-form">
          <div class="form-group" :class="{ 'error': errors.email }">
            <label><i class="fas fa-envelope"></i> Adresse email</label>
            <div class="input-wrapper">
              <input type="email" v-model="form.email" placeholder="admin@herbier-man.ci" required>
              <i class="fas fa-check-circle input-icon-check" v-if="form.email && !errors.email"></i>
            </div>
            <div class="error-message" v-if="errors.email">{{ errors.email }}</div>
          </div>
          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading"><i class="fas fa-paper-plane"></i> Envoyer le code</span>
            <span v-else><i class="fas fa-spinner fa-pulse"></i> Envoi en cours...</span>
          </button>
        </form>

        <!-- Étape 2: Vérification du code -->
        <form v-if="step === 2" @submit.prevent="verifyCode" class="forgot-form">
          <div class="form-group" :class="{ 'error': errors.code }">
            <label><i class="fas fa-key"></i> Code de vérification</label>
            <div class="code-inputs">
              <input v-for="(digit, index) in 6" :key="index" type="text" maxlength="1" v-model="codeDigits[index]" @input="handleCodeInput(index, $event)" @keydown="handleCodeKeydown(index, $event)" ref="codeInputs" class="code-digit" :class="{ 'has-error': errors.code }">
            </div>
            <div class="error-message" v-if="errors.code">{{ errors.code }}</div>
          </div>
          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading"><i class="fas fa-check-circle"></i> Vérifier</span>
            <span v-else><i class="fas fa-spinner fa-pulse"></i> Vérification...</span>
          </button>
          <button type="button" class="btn-resend" @click="sendResetCode" :disabled="resendLoading">
            <span v-if="!resendLoading"><i class="fas fa-redo-alt"></i> Renvoyer le code</span>
            <span v-else><i class="fas fa-spinner fa-pulse"></i> Envoi...</span>
          </button>
        </form>

        <!-- Étape 3: Nouveau mot de passe -->
        <form v-if="step === 3" @submit.prevent="resetPassword" class="forgot-form">
          <div class="form-group" :class="{ 'error': errors.new_password }">
            <label><i class="fas fa-lock"></i> Nouveau mot de passe</label>
            <div class="input-wrapper">
              <input :type="showPassword ? 'text' : 'password'" v-model="form.new_password" placeholder="••••••••" required>
              <button type="button" class="toggle-password" @click="showPassword = !showPassword"><i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i></button>
            </div>
            <div class="error-message" v-if="errors.new_password">{{ errors.new_password }}</div>
          </div>
          <div class="form-group" :class="{ 'error': errors.confirm_password }">
            <label><i class="fas fa-lock"></i> Confirmer le mot de passe</label>
            <div class="input-wrapper">
              <input :type="showConfirmPassword ? 'text' : 'password'" v-model="form.confirm_password" placeholder="••••••••" required>
              <button type="button" class="toggle-password" @click="showConfirmPassword = !showConfirmPassword"><i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i></button>
            </div>
            <div class="error-message" v-if="errors.confirm_password">{{ errors.confirm_password }}</div>
          </div>
          <div class="password-strength" v-if="form.new_password">
            <div class="strength-bar" :class="passwordStrength.class"></div>
            <span class="strength-text">{{ passwordStrength.text }}</span>
          </div>
          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading"><i class="fas fa-save"></i> Réinitialiser</span>
            <span v-else><i class="fas fa-spinner fa-pulse"></i> Réinitialisation...</span>
          </button>
        </form>

        <div class="login-footer">
          <router-link to="/login" class="back-link"><i class="fas fa-arrow-left"></i> Retour à la connexion</router-link>
        </div>
      </div>
    </div>

    <!-- Modal de succès -->
    <div class="modal-success" :class="{ active: showSuccessModal }">
      <div class="modal-overlay" @click="closeSuccessModal"></div>
      <div class="modal-content">
        <div class="modal-icon success"><i class="fas fa-check-circle"></i></div>
        <h3>Succès !</h3>
        <p>{{ successMessage }}</p>
        <div class="modal-buttons"><button class="btn-primary" @click="goToLogin">Aller à la connexion</button></div>
      </div>
    </div>

    <div v-if="toastMessage" class="toast" :class="toastType"><i :class="toastType === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i><span>{{ toastMessage }}</span></div>
  </div>
</template>

<script>
import axios from 'axios'

const API_URL = 'http://localhost:8001/api'

export default {
  name: 'ForgotPassword',
  data() {
    return {
      step: 1,
      form: { email: '', new_password: '', confirm_password: '' },
      codeDigits: ['', '', '', '', '', ''],
      showPassword: false,
      showConfirmPassword: false,
      loading: false,
      resendLoading: false,
      resetToken: null,
      errors: {},
      toastMessage: '',
      toastType: '',
      showSuccessModal: false,
      successMessage: ''
    }
  },
  computed: {
    stepMessage() {
      if (this.step === 1) return 'Entrez votre adresse email pour recevoir un code de réinitialisation'
      if (this.step === 2) return 'Entrez le code à 6 chiffres reçu par email'
      return 'Créez un nouveau mot de passe sécurisé'
    },
    fullCode() { return this.codeDigits.join('') },
    passwordStrength() {
      const pwd = this.form.new_password
      if (!pwd) return { class: '', text: '' }
      let strength = 0
      if (pwd.length >= 8) strength++
      if (pwd.match(/[a-z]/)) strength++
      if (pwd.match(/[A-Z]/)) strength++
      if (pwd.match(/[0-9]/)) strength++
      if (pwd.match(/[^a-zA-Z0-9]/)) strength++
      if (strength <= 2) return { class: 'weak', text: 'Faible' }
      if (strength <= 4) return { class: 'medium', text: 'Moyen' }
      return { class: 'strong', text: 'Fort' }
    }
  },
  methods: {
    showToast(message, type) { this.toastMessage = message; this.toastType = type; setTimeout(() => { this.toastMessage = '' }, 5000) },
    
    async sendResetCode() {
      if (!this.form.email) { this.errors.email = 'Email requis'; return }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) { this.errors.email = 'Email invalide'; return }
      
      this.loading = true
      this.errors = {}
      
      try {
        const response = await axios.post(`${API_URL}/forgot-password/`, { email: this.form.email })
        if (response.data.success) {
          this.step = 2
          this.$nextTick(() => { if (this.$refs.codeInputs) this.$refs.codeInputs[0]?.focus() })
          this.showToast('Code envoyé à votre adresse email', 'success')
        }
      } catch (error) {
        this.showToast(error.response?.data?.error || 'Erreur', 'error')
      }
      this.loading = false
    },
    
    handleCodeInput(index, event) {
      const value = event.target.value
      if (value && /^\d$/.test(value)) {
        this.codeDigits[index] = value
        if (index < 5) this.$refs.codeInputs[index + 1].focus()
        else this.verifyCode()
      } else if (value === '') this.codeDigits[index] = ''
    },
    
    handleCodeKeydown(index, event) {
      if (event.key === 'Backspace' && !this.codeDigits[index] && index > 0) this.$refs.codeInputs[index - 1].focus()
    },
    
    async verifyCode() {
      if (this.fullCode.length !== 6) { this.errors.code = 'Code à 6 chiffres requis'; return }
      
      this.loading = true
      this.errors = {}
      
      try {
        const response = await axios.post(`${API_URL}/verify-reset-code/`, { email: this.form.email, code: this.fullCode })
        if (response.data.success) {
          this.resetToken = response.data.reset_token
          this.step = 3
        }
      } catch (error) {
        this.errors.code = error.response?.data?.error || 'Code invalide'
      }
      this.loading = false
    },
    
    async resetPassword() {
      this.errors = {}
      let isValid = true
      
      if (!this.form.new_password) { this.errors.new_password = 'Mot de passe requis'; isValid = false }
      else if (this.form.new_password.length < 6) { this.errors.new_password = 'Minimum 6 caractères'; isValid = false }
      
      if (this.form.new_password !== this.form.confirm_password) { this.errors.confirm_password = 'Les mots de passe ne correspondent pas'; isValid = false }
      
      if (!isValid) return
      
      this.loading = true
      
      try {
        const response = await axios.post(`${API_URL}/reset-password/`, {
          email: this.form.email,
          new_password: this.form.new_password,
          confirm_password: this.form.confirm_password
        })
        if (response.data.success) {
          this.successMessage = response.data.message
          this.showSuccessModal = true
        }
      } catch (error) {
        this.showToast(error.response?.data?.error || 'Erreur', 'error')
      }
      this.loading = false
    },
    
    closeSuccessModal() { this.showSuccessModal = false },
    goToLogin() { this.closeSuccessModal(); this.$router.push('/login') }
  }
}
</script>

<style scoped>
.forgot-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a472a 0%, #0d3b0f 100%); position: relative; }
.login-bg { position: fixed; top: 0; left: 0; right: 0; bottom: 0; overflow: hidden; z-index: 0; }
.bg-leaf { position: absolute; opacity: 0.1; animation: float 20s infinite; }
.bg-leaf::before { content: "🌿"; font-size: 100px; }
.leaf-1 { top: 10%; left: -50px; }
.leaf-2 { bottom: 20%; right: -50px; animation-delay: 5s; }
.leaf-3 { top: 40%; left: 30%; animation-delay: 10s; }
@keyframes float { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-30px) rotate(10deg); } }
.forgot-wrapper { position: relative; z-index: 1; width: 100%; max-width: 500px; padding: 20px; }
.forgot-card { background: white; border-radius: 32px; padding: 48px 40px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); }
.forgot-header { text-align: center; margin-bottom: 32px; }
.logo-wrapper { display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 24px; }
.logo-icon { width: 50px; height: 50px; background: linear-gradient(135deg, #32CD32, #228B22); border-radius: 16px; display: flex; align-items: center; justify-content: center; }
.logo-icon i { font-size: 28px; color: white; }
.logo-text h1 { font-size: 24px; font-weight: 800; color: #1a472a; margin: 0; }
.logo-text span { font-size: 12px; color: #666; }
.forgot-header h2 { font-size: 24px; color: #1a472a; margin-bottom: 8px; }
.forgot-header p { color: #666; font-size: 14px; }
.form-group { margin-bottom: 24px; }
.form-group label { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: #333; margin-bottom: 8px; }
.form-group label i { color: #32CD32; }
.input-wrapper { position: relative; }
.input-wrapper input { width: 100%; padding: 14px 42px 14px 16px; border: 2px solid #e0e0e0; border-radius: 14px; font-size: 15px; transition: all 0.3s; }
.input-wrapper input:focus { outline: none; border-color: #32CD32; box-shadow: 0 0 0 4px rgba(50,205,50,0.1); }
.input-wrapper input.has-error { border-color: #dc3545; }
.input-icon-check { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); color: #28a745; font-size: 18px; }
.toggle-password { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #999; }
.code-inputs { display: flex; gap: 12px; justify-content: center; margin: 20px 0; }
.code-digit { width: 50px; height: 60px; text-align: center; font-size: 24px; font-weight: bold; border: 2px solid #ddd; border-radius: 12px; }
.code-digit:focus { outline: none; border-color: #32CD32; box-shadow: 0 0 0 3px rgba(50,205,50,0.1); }
.code-digit.has-error { border-color: #dc3545; }
.error-message { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #dc3545; margin-top: 6px; }
.btn-submit { width: 100%; padding: 14px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 14px; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 12px; }
.btn-submit:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(50,205,50,0.4); }
.btn-resend { width: 100%; padding: 14px; background: #f5f5f5; border: none; border-radius: 14px; font-size: 16px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; color: #666; }
.btn-resend:hover:not(:disabled) { background: #e8e8e8; }
.password-strength { margin-top: 8px; }
.strength-bar { height: 4px; border-radius: 2px; margin-bottom: 4px; }
.strength-bar.weak { width: 33%; background: #dc3545; }
.strength-bar.medium { width: 66%; background: #ffc107; }
.strength-bar.strong { width: 100%; background: #28a745; }
.strength-text { font-size: 11px; color: #666; }
.login-footer { text-align: center; margin-top: 24px; }
.back-link { color: #32CD32; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; }
.back-link:hover { text-decoration: underline; }
.modal-success { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 2000; visibility: hidden; opacity: 0; transition: all 0.3s; }
.modal-success.active { visibility: visible; opacity: 1; }
.modal-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; }
.modal-content { position: relative; background: white; border-radius: 24px; padding: 40px; max-width: 400px; width: 90%; text-align: center; }
.modal-icon { width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; background: #d4edda; color: #28a745; }
.modal-icon i { font-size: 40px; }
.modal-content h3 { font-size: 24px; color: #1a472a; margin-bottom: 12px; }
.btn-primary { padding: 12px 24px; background: linear-gradient(135deg, #32CD32, #228B22); color: white; border: none; border-radius: 12px; cursor: pointer; }
.toast { position: fixed; bottom: 20px; right: 20px; padding: 12px 20px; border-radius: 10px; display: flex; align-items: center; gap: 10px; z-index: 1100; animation: slideIn 0.3s; }
.toast.success { background: #28a745; color: white; }
.toast.error { background: #dc3545; color: white; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
@media (max-width: 550px) { .forgot-card { padding: 32px 24px; } .code-digit { width: 40px; height: 50px; font-size: 20px; } }
</style>
