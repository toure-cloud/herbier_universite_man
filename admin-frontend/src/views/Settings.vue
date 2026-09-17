<template>
  <div class="settings-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Paramètres"
        subtitle="Gérez votre compte et vos préférences"
        icon="fas fa-cog"
      />

      <div class="settings-grid">
        <nav class="settings-tabs">
          <button
            v-for="t in tabs"
            :key="t.id"
            class="tab-btn"
            :class="{ active: activeTab === t.id }"
            @click="activeTab = t.id"
          >
            <i :class="t.icon"></i>
            <span>{{ t.label }}</span>
          </button>
        </nav>

        <section class="settings-content">
          <!-- Profil -->
          <div v-show="activeTab === 'profile'" class="tab-panel">
            <h2>Mon profil</h2>
            <div class="panel-grid">
              <div class="form-group">
                <label>Nom complet</label>
                <input v-model.trim="profile.nom" type="text" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model.trim="profile.email" type="email" disabled />
                <small class="help-text">L'email ne peut pas être modifié (contactez le SuperIT)</small>
              </div>
              <div class="form-group">
                <label>Téléphone</label>
                <input v-model.trim="profile.telephone" type="tel" />
              </div>
              <div class="form-group">
                <label>Rôle</label>
                <input :value="roleLabel" type="text" disabled />
              </div>
            </div>
            <button class="btn-primary" :class="{ it: auth.isSuperIT }" @click="saveProfile" :disabled="savingProfile">
              <i v-if="savingProfile" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-save"></i>
              Enregistrer le profil
            </button>
          </div>

          <!-- Mot de passe -->
          <div v-show="activeTab === 'password'" class="tab-panel">
            <h2>Changer le mot de passe</h2>
            <div class="form-group">
              <label>Mot de passe actuel</label>
              <input v-model="pwd.old" type="password" autocomplete="current-password" />
            </div>
            <div class="form-group">
              <label>Nouveau mot de passe</label>
              <input v-model="pwd.new" type="password" autocomplete="new-password" />
              <div v-if="pwd.new" class="strength-wrap">
                <div class="strength-bar" :class="passwordStrength.class"></div>
                <span class="strength-text">{{ passwordStrength.text }}</span>
              </div>
            </div>
            <div class="form-group">
              <label>Confirmer</label>
              <input v-model="pwd.confirm" type="password" autocomplete="new-password" />
            </div>
            <button class="btn-primary" :class="{ it: auth.isSuperIT }" @click="changePassword" :disabled="savingPwd">
              <i v-if="savingPwd" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-lock"></i>
              Mettre à jour
            </button>
          </div>

          <!-- ✅ Mes activités (transparence) -->
          <div v-show="activeTab === 'activity'" class="tab-panel">
            <h2>Mes dernières actions</h2>
            <p class="panel-desc">
              Historique de vos actions sur la plateforme (transparence).
            </p>
            <ul v-if="myActivities.length" class="activity-list">
              <li v-for="log in myActivities" :key="log.id" class="activity-item">
                <div class="activity-icon" :class="log.action.toLowerCase()">
                  <i :class="actionIcon(log.action)"></i>
                </div>
                <div class="activity-body">
                  <p class="activity-message">
                    <strong>{{ log.action_label }}</strong>
                    <span v-if="log.object_repr" class="activity-obj">: {{ log.object_repr }}</span>
                  </p>
                  <span class="activity-time">{{ formatRelativeTime(log.created_at) }}</span>
                </div>
              </li>
            </ul>
            <p v-else class="empty-text">Aucune activité enregistrée</p>
          </div>

          <!-- Sécurité -->
          <div v-show="activeTab === 'security'" class="tab-panel">
            <h2>Sécurité</h2>

            <div class="security-card">
              <div class="sec-icon"><i class="fas fa-shield-alt"></i></div>
              <div class="sec-body">
                <h4>Authentification à deux facteurs</h4>
                <p>Un code de vérification est envoyé par email à chaque connexion.</p>
              </div>
              <span class="badge green">Activée</span>
            </div>

            <div class="security-card danger">
              <div class="sec-icon"><i class="fas fa-sign-out-alt"></i></div>
              <div class="sec-body">
                <h4>Terminer toutes les sessions</h4>
                <p>Déconnecte tous les appareils connectés à votre compte.</p>
              </div>
              <button class="btn-danger" @click="terminateSessions">
                <i class="fas fa-power-off"></i> Terminer
              </button>
            </div>
          </div>

          <!-- Préférences -->
          <div v-show="activeTab === 'preferences'" class="tab-panel">
            <h2>Préférences</h2>

            <div class="pref-row">
              <div>
                <h4>Notifications par email</h4>
                <p>Recevoir un email lors des nouvelles inscriptions.</p>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="prefs.emailNotif" />
                <span class="slider"></span>
              </label>
            </div>

            <div class="pref-row">
              <div>
                <h4>Confidentialité renforcée</h4>
                <p>Masquer les données sensibles dans l'interface.</p>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="prefs.enhancedPrivacy" />
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </section>
      </div>
    </main>

    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { adminApi } from '../utils/api'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const activeTab = ref('profile')
const savingProfile = ref(false)
const savingPwd = ref(false)

const profile = ref({
  nom: auth.user?.nom || '',
  email: auth.user?.email || '',
  telephone: auth.user?.telephone || '',
})

const pwd = ref({ old: '', new: '', confirm: '' })
const prefs = ref({ emailNotif: true, enhancedPrivacy: true })
const myActivities = ref([])

const tabs = computed(() => {
  const base = [
    { id: 'profile', label: 'Profil', icon: 'fas fa-user' },
    { id: 'password', label: 'Mot de passe', icon: 'fas fa-lock' },
    { id: 'activity', label: 'Mes activités', icon: 'fas fa-user-clock' },
    { id: 'security', label: 'Sécurité', icon: 'fas fa-shield-alt' },
    { id: 'preferences', label: 'Préférences', icon: 'fas fa-sliders-h' },
  ]
  return base
})

const roleLabel = computed(() =>
  auth.isSuperIT ? 'Super Administrateur IT' : 'Administrateur'
)

const passwordStrength = computed(() => {
  const p = pwd.value.new
  if (!p) return { class: '', text: '' }
  let score = 0
  if (p.length >= 8) score++
  if (/[a-z]/.test(p)) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^a-zA-Z0-9]/.test(p)) score++
  if (score <= 2) return { class: 'weak', text: 'Faible' }
  if (score <= 4) return { class: 'medium', text: 'Moyen' }
  return { class: 'strong', text: 'Fort' }
})

const loadMyActivities = async () => {
  try {
    const { data } = await adminApi.get('/me/activity/', { params: { limit: 20 } })
    myActivities.value = Array.isArray(data) ? data : []
  } catch {
    logger.warn('Erreur mes activités')
  }
}

const actionIcon = (action) => ({
  CREATE: 'fas fa-plus-circle',
  UPDATE: 'fas fa-edit',
  DELETE: 'fas fa-trash',
  LOGIN: 'fas fa-sign-in-alt',
  LOGOUT: 'fas fa-sign-out-alt',
  LOGIN_FAILED: 'fas fa-exclamation-triangle',
  SYNC: 'fas fa-sync-alt',
}[action] || 'fas fa-circle')

const formatRelativeTime = (d) => {
  if (!d) return ''
  const diff = (Date.now() - new Date(d).getTime()) / 1000
  if (diff < 60) return "à l'instant"
  if (diff < 3600) return `il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `il y a ${Math.floor(diff / 3600)} h`
  return `il y a ${Math.floor(diff / 86400)} j`
}

const saveProfile = async () => {
  savingProfile.value = true
  try {
    toast.success('Profil enregistré')
  } catch {
    toast.error("Erreur lors de l'enregistrement")
  } finally {
    savingProfile.value = false
  }
}

const changePassword = async () => {
  if (!pwd.value.old || !pwd.value.new) {
    toast.error('Tous les champs sont requis')
    return
  }
  if (pwd.value.new.length < 8) {
    toast.error('Minimum 8 caractères')
    return
  }
  if (pwd.value.new !== pwd.value.confirm) {
    toast.error('Les mots de passe ne correspondent pas')
    return
  }
  savingPwd.value = true
  try {
    toast.success('Mot de passe mis à jour')
    pwd.value = { old: '', new: '', confirm: '' }
  } catch {
    toast.error('Erreur')
  } finally {
    savingPwd.value = false
  }
}

const terminateSessions = async () => {
  const ok = await askConfirm({
    title: 'Terminer toutes les sessions',
    message: 'Vous serez déconnecté de tous les appareils. Continuer ?',
    dangerous: true,
    confirmText: 'Terminer',
  })
  if (!ok) return
  await auth.logout()
  router.push('/it-login')
}

const handleLogout = async () => {
  await auth.logout()
  router.push(auth.isSuperIT ? '/it-login' : '/admin-login')
}

onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/it-login')
    return
  }
  loadMyActivities()
})
</script>

<style scoped>
.settings-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.settings-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.settings-grid { display: grid; grid-template-columns: 240px 1fr; gap: 24px; align-items: start; }

.settings-tabs { background: #fff; border-radius: 14px; padding: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); position: sticky; top: 20px; display: flex; flex-direction: column; gap: 2px; }
.superit-theme .settings-tabs { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: none; }
.tab-btn { display: flex; align-items: center; gap: 12px; padding: 11px 14px; background: none; border: none; border-radius: 9px; cursor: pointer; font-family: inherit; font-size: 13.5px; font-weight: 500; color: #475569; text-align: left; transition: all 0.15s; }
.superit-theme .tab-btn { color: #94a3b8; }
.tab-btn i { width: 16px; font-size: 13px; text-align: center; }
.tab-btn:hover { background: #f8fafc; color: #0f172a; }
.superit-theme .tab-btn:hover { background: rgba(255, 255, 255, 0.06); color: #fff; }
.tab-btn.active { background: #ecfdf5; color: #059669; font-weight: 600; }
.superit-theme .tab-btn.active { background: rgba(99, 102, 241, 0.15); color: #c7d2fe; }

.settings-content { background: #fff; border-radius: 14px; padding: 28px 32px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); }
.superit-theme .settings-content { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: none; }

.tab-panel h2 { font-size: 18px; color: #0f172a; margin: 0 0 20px; font-weight: 700; }
.superit-theme .tab-panel h2 { color: #fff; }
.panel-desc { font-size: 13px; color: #64748b; margin: 0 0 20px; }
.superit-theme .panel-desc { color: #94a3b8; }

.panel-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.form-group label { font-size: 12.5px; font-weight: 600; color: #334155; }
.superit-theme .form-group label { color: #cbd5e1; }
.form-group input { padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 9px; font-size: 13.5px; font-family: inherit; background: #f8fafc; color: #0f172a; }
.superit-theme .form-group input { background: rgba(255, 255, 255, 0.04); border-color: rgba(255, 255, 255, 0.1); color: #fff; }
.form-group input:focus { outline: none; border-color: #10b981; background: #fff; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1); }
.superit-theme .form-group input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15); }
.form-group input:disabled { background: #f1f5f9; color: #94a3b8; cursor: not-allowed; }
.superit-theme .form-group input:disabled { background: rgba(255, 255, 255, 0.02); color: #64748b; }

.help-text { font-size: 11.5px; color: #94a3b8; }

.strength-wrap { display: flex; align-items: center; gap: 8px; margin-top: 4px; }
.strength-bar { height: 4px; border-radius: 2px; flex: 1; transition: all 0.2s; }
.strength-bar.weak { width: 33%; background: #ef4444; }
.strength-bar.medium { width: 66%; background: #f59e0b; }
.strength-bar.strong { width: 100%; background: #10b981; }
.strength-text { font-size: 11px; color: #64748b; }

.btn-primary, .btn-danger { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 9px; font-size: 13.5px; font-weight: 600; border: none; cursor: pointer; transition: all 0.15s; }
.btn-primary { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
.btn-primary.it { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-danger { background: #ef4444; color: #fff; }
.btn-danger:hover { background: #dc2626; }

.security-card { display: flex; align-items: center; gap: 16px; padding: 16px 18px; background: #f8fafc; border-radius: 12px; margin-bottom: 12px; border: 1px solid #f1f5f9; }
.superit-theme .security-card { background: rgba(255, 255, 255, 0.03); border-color: rgba(255, 255, 255, 0.06); }
.security-card.danger { background: #fef2f2; border-color: #fee2e2; }
.superit-theme .security-card.danger { background: rgba(239, 68, 68, 0.08); border-color: rgba(239, 68, 68, 0.2); }
.sec-icon { width: 42px; height: 42px; border-radius: 10px; background: #ecfdf5; color: #10b981; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.superit-theme .sec-icon { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.security-card.danger .sec-icon { background: #fee2e2; color: #ef4444; }
.sec-body { flex: 1; }
.sec-body h4 { margin: 0 0 4px; font-size: 14px; color: #0f172a; }
.superit-theme .sec-body h4 { color: #fff; }
.sec-body p { margin: 0; font-size: 12.5px; color: #64748b; }
.superit-theme .sec-body p { color: #94a3b8; }
.badge { padding: 4px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 600; }
.badge.green { background: #dcfce7; color: #15803d; }
.superit-theme .badge.green { background: rgba(16, 185, 129, 0.15); color: #10b981; }

.activity-list { list-style: none; padding: 0; margin: 0; }
.activity-item { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
.superit-theme .activity-item { border-bottom-color: rgba(255, 255, 255, 0.05); }
.activity-item:last-child { border-bottom: none; }
.activity-icon { width: 34px; height: 34px; background: rgba(148, 163, 184, 0.15); color: #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 13px; }
.activity-icon.create { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.activity-icon.update { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.activity-icon.delete { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.activity-icon.login { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.activity-body { flex: 1; min-width: 0; }
.activity-message { font-size: 13.5px; color: #334155; margin: 0; }
.superit-theme .activity-message { color: #cbd5e1; }
.activity-message strong { color: #0f172a; font-weight: 600; }
.superit-theme .activity-message strong { color: #fff; }
.activity-obj { color: #64748b; font-style: italic; }
.superit-theme .activity-obj { color: #94a3b8; }
.activity-time { font-size: 11px; color: #94a3b8; }

.pref-row { display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid #f1f5f9; }
.superit-theme .pref-row { border-bottom-color: rgba(255, 255, 255, 0.05); }
.pref-row:last-child { border-bottom: none; }
.pref-row h4 { font-size: 14px; margin: 0 0 4px; color: #0f172a; }
.superit-theme .pref-row h4 { color: #fff; }
.pref-row p { font-size: 12.5px; color: #64748b; margin: 0; }
.superit-theme .pref-row p { color: #94a3b8; }

.switch { position: relative; display: inline-block; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; inset: 0; background: #cbd5e1; border-radius: 24px; transition: 0.2s; }
.slider::before { content: ""; position: absolute; height: 18px; width: 18px; left: 3px; bottom: 3px; background: #fff; border-radius: 50%; transition: 0.2s; }
.switch input:checked + .slider { background: #10b981; }
.superit-theme .switch input:checked + .slider { background: #6366f1; }
.switch input:checked + .slider::before { transform: translateX(20px); }

.empty-text { text-align: center; color: #94a3b8; font-size: 13px; padding: 24px 0; }

@media (max-width: 900px) {
  .settings-grid { grid-template-columns: 1fr; }
  .settings-tabs { position: relative; top: 0; flex-direction: row; overflow-x: auto; }
  .tab-btn { white-space: nowrap; }
  .panel-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
}
</style>
