<template>
  <div class="auth-page admin-theme">
    <div class="auth-bg">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
    </div>

    <div class="auth-card">
      <div class="auth-brand">
        <div class="brand-icon admin-icon"><i class="fas fa-user-tie"></i></div>
        <div class="brand-text">
          <h1>Administrateur</h1>
          <span>Accès gestion de contenu</span>
        </div>
      </div>

      <div class="admin-badge">
        <i class="fas fa-user-shield"></i> Accès administrateur
      </div>

      <div class="auth-header">
        <h2>Connexion Admin</h2>
        <p>Gérez le contenu de l'herbier</p>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label>Email</label>
          <div class="input-wrap" :class="{ error: errors.email }">
            <i class="fas fa-envelope"></i>
            <input v-model.trim="form.email" type="email" required autocomplete="email" />
          </div>
          <p v-if="errors.email" class="field-error">{{ errors.email }}</p>
        </div>

        <div class="form-group">
          <label>Mot de passe</label>
          <div class="input-wrap" :class="{ error: errors.password }">
            <i class="fas fa-lock"></i>
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="current-password"
            />
            <button type="button" class="input-toggle" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <p v-if="errors.password" class="field-error">{{ errors.password }}</p>
        </div>

        <button type="submit" class="btn-primary admin-btn" :disabled="loading">
          <i v-if="loading" class="fas fa-spinner fa-spin"></i>
          <i v-else class="fas fa-sign-in-alt"></i>
          {{ loading ? 'Connexion…' : 'Se connecter' }}
        </button>
      </form>

      <div class="auth-footer">
        <router-link to="/it-login" class="link-muted">
          <i class="fas fa-shield-alt"></i> Accès SuperIT
        </router-link>
      </div>
    </div>

    <Toast />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Toast from '../components/Toast.vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

const form = ref({ email: '', password: '' })
const errors = ref({})
const showPassword = ref(false)
const loading = ref(false)

const handleSubmit = async () => {
  errors.value = {}

  if (!form.value.email) {
    errors.value.email = 'Email requis'
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = "Format d'email invalide"
    return
  }
  if (!form.value.password) {
    errors.value.password = 'Mot de passe requis'
    return
  }

  loading.value = true
  try {
    const res = await auth.loginAdmin({
      email: form.value.email,
      password: form.value.password,
    })

    if (res.success && res.requires2FA) {
      toast.success('Code envoyé à votre email')
      setTimeout(() => {
        router.push({
          path: '/verify-2fa',
          query: {
            email: form.value.email,                          // ✅ AJOUT
            redirect: route.query.redirect || undefined,
          },
        })
      }, 600)
    } else {
      toast.error(res.message || 'Accès refusé')
    }
  } catch {
    toast.error('Erreur de connexion')
  } finally {
    loading.value = false
  }
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
.admin-theme { background: #0f172a; }

.auth-bg { position: absolute; inset: 0; pointer-events: none; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.25; }
.orb-1 { width: 500px; height: 500px; background: #10b981; top: -200px; left: -150px; }
.orb-2 { width: 400px; height: 400px; background: #059669; bottom: -150px; right: -100px; }

.auth-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px 36px 28px;
  box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.4);
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
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

.admin-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: #ecfdf5;
  color: #059669;
  font-size: 11px;
  font-weight: 600;
  border-radius: 20px;
  margin: 0 auto 20px;
}

.auth-header { text-align: center; margin-bottom: 24px; }
.auth-header h2 { font-size: 20px; color: #0f172a; margin: 0 0 6px; font-weight: 700; }
.auth-header p { font-size: 13px; color: #64748b; margin: 0; }

.auth-form { display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 13px; font-weight: 600; color: #334155; }

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  background: #fff;
  transition: all 0.15s;
}
.input-wrap:focus-within {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
.input-wrap.error { border-color: #ef4444; }
.input-wrap > i:first-child {
  padding-left: 14px;
  color: #94a3b8;
  font-size: 14px;
}
.input-wrap input {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 14px;
  font-size: 14px;
  background: transparent;
  font-family: inherit;
  color: #0f172a;
}
.input-toggle {
  background: none;
  border: none;
  padding: 0 14px;
  color: #94a3b8;
  cursor: pointer;
  font-size: 14px;
}
.input-toggle:hover { color: #10b981; }

.field-error { color: #dc2626; font-size: 12px; margin: 0; }

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 13px 24px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  box-shadow: 0 4px 14px -4px rgba(16, 185, 129, 0.5);
  transition: all 0.15s;
}
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.7; cursor: not-allowed; }

.auth-footer {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px solid #f1f5f9;
  text-align: center;
}
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
  .auth-card { padding: 32px 24px 24px; border-radius: 16px; }
}
</style>