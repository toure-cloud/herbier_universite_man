<template>
  <div class="auth-page">
    <div class="auth-bg">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
    </div>

    <div class="auth-card">
      <div class="auth-brand">
        <div class="brand-icon"><i class="fas fa-shield-alt"></i></div>
        <div class="brand-text">
          <h1>Vérification 2FA</h1>
          <span>Sécurité renforcée</span>
        </div>
      </div>

      <div class="auth-header">
        <h2>Vérification en deux étapes</h2>
        <p>
          Un code à 6 chiffres a été envoyé à
          <strong>{{ displayEmail }}</strong>
        </p>
      </div>

      <form @submit.prevent="handleVerify" class="auth-form">
        <div class="code-inputs">
          <input
            v-for="(digit, index) in 6"
            :key="index"
            :ref="(el) => (inputs[index] = el)"
            v-model="code[index]"
            type="text"
            inputmode="numeric"
            maxlength="1"
            pattern="[0-9]"
            class="code-digit"
            :class="{ filled: code[index] }"
            @input="handleInput(index, $event)"
            @keydown="handleKeydown(index, $event)"
            @paste="handlePaste"
          />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading || fullCode.length !== 6">
          <i v-if="loading" class="fas fa-spinner fa-spin"></i>
          <i v-else class="fas fa-check-circle"></i>
          {{ loading ? 'Vérification…' : 'Vérifier' }}
        </button>

        <button
          type="button"
          class="btn-secondary"
          @click="handleResend"
          :disabled="resendLoading || resendTimer > 0"
        >
          <i v-if="resendLoading" class="fas fa-spinner fa-spin"></i>
          <i v-else class="fas fa-redo-alt"></i>
          <span v-if="resendTimer > 0">Renvoyer dans {{ resendTimer }}s</span>
          <span v-else>Renvoyer le code</span>
        </button>
      </form>

      <div class="auth-footer">
        <router-link to="/it-login" class="link-muted">
          <i class="fas fa-arrow-left"></i> Retour à la connexion
        </router-link>
      </div>
    </div>

    <Toast />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Toast from '../components/Toast.vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { authAPI } from '../utils/api'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

const code = ref(['', '', '', '', '', ''])
const inputs = ref([])
const loading = ref(false)
const resendLoading = ref(false)
const resendTimer = ref(0)
let timerInterval = null

const fullCode = computed(() => code.value.join(''))

const displayEmail = computed(() => {
  return auth.email || localStorage.getItem('auth_email') || route.query.email || 'votre email'
})

onMounted(() => {
  const email = route.query.email || auth.email || localStorage.getItem('auth_email')
  if (!email) {
    toast.error('Aucune session en cours')
    router.push('/it-login')
    return
  }
  if (!auth.email || auth.email !== email) {
    auth.setEmail(email)
  }
  nextTick(() => inputs.value[0]?.focus())
})

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval)
})

const handleInput = (index, event) => {
  const value = event.target.value.replace(/\D/g, '')
  if (!value) {
    code.value[index] = ''
    return
  }
  code.value[index] = value[0]
  if (index < 5 && value) inputs.value[index + 1]?.focus()
  if (fullCode.value.length === 6 && !loading.value) {
    setTimeout(() => handleVerify(), 150)
  }
}

const handleKeydown = (index, event) => {
  if (event.key === 'Backspace' && !code.value[index] && index > 0) {
    inputs.value[index - 1]?.focus()
  } else if (event.key === 'ArrowLeft' && index > 0) {
    inputs.value[index - 1]?.focus()
  } else if (event.key === 'ArrowRight' && index < 5) {
    inputs.value[index + 1]?.focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const pasted = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)
  if (!pasted) return
  code.value = pasted.split('').concat(Array(6 - pasted.length).fill(''))
  nextTick(() => {
    const nextEmpty = code.value.findIndex((c) => !c)
    inputs.value[nextEmpty === -1 ? 5 : nextEmpty]?.focus()
    if (fullCode.value.length === 6) handleVerify()
  })
}

const handleVerify = async () => {
  if (fullCode.value.length !== 6) {
    toast.error('Veuillez entrer les 6 chiffres')
    return
  }
  if (loading.value) return
  loading.value = true

  try {
    const result = await auth.verify2FA(fullCode.value)
    if (result.success) {
      toast.success('Authentification réussie')
      setTimeout(() => {
        router.push(route.query.redirect || '/dashboard')
      }, 600)
    } else {
      toast.error(result.message || 'Code invalide')
      code.value = ['', '', '', '', '', '']
      nextTick(() => inputs.value[0]?.focus())
    }
  } catch {
    toast.error('Erreur de connexion')
  } finally {
    loading.value = false
  }
}

const handleResend = async () => {
  if (resendTimer.value > 0 || resendLoading.value) return

  const email = auth.email || localStorage.getItem('auth_email')
  if (!email) {
    toast.error('Session expirée')
    router.push('/it-login')
    return
  }

  resendLoading.value = true
  try {
    await authAPI.resendCode({ email })
    toast.success('Nouveau code envoyé')
    startTimer(60)
  } catch {
    toast.error("Impossible d'envoyer le code")
  } finally {
    resendLoading.value = false
  }
}

const startTimer = (seconds) => {
  resendTimer.value = seconds
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = setInterval(() => {
    resendTimer.value--
    if (resendTimer.value <= 0) {
      clearInterval(timerInterval)
      timerInterval = null
    }
  }, 1000)
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
  padding: 24px;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', system-ui, sans-serif;
}
.auth-bg { position: absolute; inset: 0; pointer-events: none; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.3; }
.orb-1 { width: 500px; height: 500px; background: #10b981; top: -200px; left: -150px; }
.orb-2 { width: 400px; height: 400px; background: #3b82f6; bottom: -150px; right: -100px; }

.auth-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 460px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px 36px 28px;
  box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.4);
  text-align: center;
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  justify-content: center;
}
.brand-icon {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  font-size: 20px;
  box-shadow: 0 8px 20px -4px rgba(16, 185, 129, 0.5);
}
.brand-text { display: flex; flex-direction: column; text-align: left; }
.brand-text h1 { font-size: 15px; font-weight: 700; color: #0f172a; margin: 0; }
.brand-text span { font-size: 11px; color: #64748b; }

.auth-header { margin-bottom: 28px; }
.auth-header h2 { font-size: 22px; font-weight: 700; color: #0f172a; margin: 0 0 8px; }
.auth-header p { font-size: 13.5px; color: #64748b; margin: 0; line-height: 1.5; }
.auth-header strong { color: #0f172a; font-weight: 600; }

.auth-form { display: flex; flex-direction: column; gap: 18px; }

.code-inputs {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin: 8px 0 4px;
}
.code-digit {
  width: 52px;
  height: 62px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  text-align: center;
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  transition: all 0.15s;
  font-family: 'Inter', monospace;
  outline: none;
}
.code-digit:focus {
  border-color: #10b981;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
  transform: scale(1.04);
}
.code-digit.filled {
  border-color: #10b981;
  background: #ecfdf5;
}

.btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 13px 24px;
  border-radius: 10px;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
  border: none;
}
.btn-primary {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5);
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px -4px rgba(16, 185, 129, 0.6);
}
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-secondary {
  background: #f8fafc;
  color: #475569;
  border: 1.5px solid #e2e8f0;
}
.btn-secondary:hover:not(:disabled) {
  background: #f1f5f9;
  border-color: #10b981;
  color: #10b981;
}
.btn-secondary:disabled { opacity: 0.6; cursor: not-allowed; }

.auth-footer { margin-top: 24px; padding-top: 18px; border-top: 1px solid #f1f5f9; }
.link-muted {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
  text-decoration: none;
}
.link-muted:hover { color: #10b981; }

@media (max-width: 480px) {
  .auth-card { padding: 30px 22px 22px; border-radius: 16px; }
  .code-digit { width: 42px; height: 52px; font-size: 20px; }
  .code-inputs { gap: 6px; }
}
</style>
