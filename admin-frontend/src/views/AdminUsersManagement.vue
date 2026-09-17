<template>
  <div class="admin-users-layout superit-theme">
    <Sidebar
      :user="auth.user"
      :is-super-it="true"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Gestion des administrateurs"
        subtitle="Créez, modifiez et gérez les comptes"
        icon="fas fa-users-cog"
      >
        <template #actions>
          <button class="btn-create" @click="openCreate">
            <i class="fas fa-user-plus"></i> Nouvel administrateur
          </button>
        </template>
      </TopBar>

      <section class="stats-row">
        <div class="stat-pill">
          <i class="fas fa-users"></i>
          <div>
            <span class="stat-value">{{ admins.length }}</span>
            <span class="stat-label">Total</span>
          </div>
        </div>
        <div class="stat-pill green">
          <i class="fas fa-user-check"></i>
          <div>
            <span class="stat-value">{{ activeAdmins }}</span>
            <span class="stat-label">Actifs</span>
          </div>
        </div>
        <div class="stat-pill red">
          <i class="fas fa-user-slash"></i>
          <div>
            <span class="stat-value">{{ inactiveAdmins }}</span>
            <span class="stat-label">Inactifs</span>
          </div>
        </div>
        <div class="stat-pill gold">
          <i class="fas fa-crown"></i>
          <div>
            <span class="stat-value">{{ superITCount }}</span>
            <span class="stat-label">SuperIT</span>
          </div>
        </div>
      </section>

      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher par nom ou email…" />
        </div>
        <select v-model="filterRole" class="filter-select">
          <option value="">Tous les rôles</option>
          <option value="it_admin">SuperIT</option>
          <option value="admin">Administrateur</option>
        </select>
        <select v-model="filterStatus" class="filter-select">
          <option value="">Tous les statuts</option>
          <option value="active">Actif</option>
          <option value="inactive">Inactif</option>
        </select>
        <div class="result-count">
          <i class="fas fa-user-shield"></i> {{ filtered.length }} résultat(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-users-cog"></i>
        <h3>Aucun administrateur trouvé</h3>
        <p>Modifiez vos filtres ou créez un nouveau compte</p>
        <button class="btn-create" @click="openCreate">
          <i class="fas fa-user-plus"></i> Créer un administrateur
        </button>
      </section>

      <section v-else class="users-list">
        <article
          v-for="admin in filtered"
          :key="admin.id"
          class="user-card"
          :class="{ 'is-me': admin.id === currentUserId, online: isOnline(admin) }"
        >
          <div class="user-avatar" :class="{ super: admin.role === 'it_admin' }">
            {{ getInitials(admin.nom) }}
            <span v-if="isOnline(admin)" class="online-ring"></span>
            <span class="status-dot" :class="{ active: admin.is_active }"></span>
          </div>

          <div class="user-body">
            <div class="user-head">
              <h3>
                {{ admin.nom }}
                <span v-if="admin.id === currentUserId" class="you-tag">vous</span>
              </h3>
              <span class="role-badge" :class="admin.role === 'it_admin' ? 'super' : 'admin'">
                <i :class="admin.role === 'it_admin' ? 'fas fa-crown' : 'fas fa-user-shield'"></i>
                {{ admin.role === 'it_admin' ? 'SuperIT' : 'Admin' }}
              </span>
              <span class="status-badge" :class="admin.is_active ? 'active' : 'inactive'">
                {{ admin.is_active ? 'Actif' : 'Inactif' }}
              </span>
              <span v-if="isOnline(admin)" class="online-badge">
                <span class="dot"></span> En ligne
              </span>
            </div>

            <div class="user-meta">
              <span><i class="fas fa-envelope"></i> {{ admin.email }}</span>
              <span><i class="fas fa-phone"></i> {{ admin.telephone || '—' }}</span>
              <span><i class="fas fa-calendar"></i> Créé le {{ formatDate(admin.date_joined) }}</span>
              <span v-if="admin.last_login">
                <i class="fas fa-clock"></i> Dernière connexion : {{ formatRelativeTime(admin.last_login) }}
              </span>
            </div>
          </div>

          <div class="user-actions">
            <button class="btn-icon" @click="openEdit(admin)" title="Modifier">
              <i class="fas fa-edit"></i>
            </button>
            <button
              class="btn-icon"
              :class="admin.is_active ? 'danger' : 'success'"
              :disabled="admin.id === currentUserId"
              @click="toggleStatus(admin)"
            >
              <i :class="admin.is_active ? 'fas fa-ban' : 'fas fa-check'"></i>
            </button>
            <button
              class="btn-icon danger"
              :disabled="admin.id === currentUserId"
              @click="removeAdmin(admin)"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-user-edit' : 'fas fa-user-plus'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouvel' }} administrateur</h2>
            </div>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>

          <form @submit.prevent="saveAdmin" class="modal-form">
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom complet *</label>
                <input v-model.trim="form.nom" type="text" required placeholder="Jean Kouassi" />
              </div>
              <div class="form-group">
                <label>Email *</label>
                <input v-model.trim="form.email" type="email" required placeholder="admin@herbier-man.ci" />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Téléphone *</label>
                <input v-model.trim="form.telephone" type="tel" required placeholder="+225 07 00 00 00 00" />
              </div>
              <div class="form-group">
                <label>Rôle</label>
                <select v-model="form.role">
                  <option value="admin">Administrateur</option>
                  <option value="it_admin">SuperIT</option>
                </select>
              </div>
            </div>

            <template v-if="!editing">
              <div class="form-row-2">
                <div class="form-group">
                  <label>Mot de passe *</label>
                  <div class="input-password">
                    <input
                      v-model="form.password"
                      :type="showPassword ? 'text' : 'password'"
                      minlength="8"
                      required
                      placeholder="8 caractères minimum"
                    />
                    <button type="button" @click="showPassword = !showPassword">
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                </div>
                <div class="form-group">
                  <label>Confirmer *</label>
                  <div class="input-password">
                    <input
                      v-model="form.password2"
                      :type="showPassword2 ? 'text' : 'password'"
                      minlength="8"
                      required
                      placeholder="••••••••"
                    />
                    <button type="button" @click="showPassword2 = !showPassword2">
                      <i :class="showPassword2 ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                </div>
              </div>
            </template>

            <label class="checkbox-wrap">
              <input type="checkbox" v-model="form.is_active" />
              <span>Compte actif</span>
            </label>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                <i v-else class="fas fa-save"></i>
                {{ saving ? 'Enregistrement…' : 'Enregistrer' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

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
import { adminAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const admins = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const filterRole = ref('')
const filterStatus = ref('')
const showModal = ref(false)
const editing = ref(null)
const showPassword = ref(false)
const showPassword2 = ref(false)

const form = ref({
  nom: '', email: '', telephone: '', role: 'admin',
  is_active: true, password: '', password2: '',
})

const currentUserId = computed(() => auth.user?.id)
const activeAdmins = computed(() => admins.value.filter((a) => a.is_active).length)
const inactiveAdmins = computed(() => admins.value.filter((a) => !a.is_active).length)
const superITCount = computed(() => admins.value.filter((a) => a.role === 'it_admin').length)

const filtered = computed(() => {
  let list = admins.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(
      (a) => a.nom?.toLowerCase().includes(q) || a.email?.toLowerCase().includes(q)
    )
  }
  if (filterRole.value) list = list.filter((a) => a.role === filterRole.value)
  if (filterStatus.value) {
    const active = filterStatus.value === 'active'
    list = list.filter((a) => a.is_active === active)
  }
  return list
})

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2)
}

const isOnline = (admin) => {
  if (!admin.last_login) return false
  return new Date(admin.last_login).getTime() > Date.now() - 30 * 60 * 1000
}

const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

const formatRelativeTime = (d) => {
  if (!d) return ''
  const diff = (Date.now() - new Date(d).getTime()) / 1000
  if (diff < 60) return "à l'instant"
  if (diff < 3600) return `il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `il y a ${Math.floor(diff / 3600)} h`
  return `il y a ${Math.floor(diff / 86400)} j`
}

const load = async () => {
  loading.value = true
  try {
    const { data } = await adminAPI.getUsers()
    admins.value = Array.isArray(data) ? data : []
  } catch {
    toast.error('Impossible de charger les administrateurs')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editing.value = null
  form.value = {
    nom: '', email: '', telephone: '', role: 'admin',
    is_active: true, password: '', password2: '',
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (admin) => {
  editing.value = admin
  form.value = {
    nom: admin.nom || '', email: admin.email || '',
    telephone: admin.telephone || '', role: admin.role || 'admin',
    is_active: admin.is_active !== false,
    password: '', password2: '',
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  showPassword.value = false
  showPassword2.value = false
  document.body.style.overflow = 'auto'
}

const saveAdmin = async () => {
  if (!form.value.nom || !form.value.email || !form.value.telephone) {
    toast.error('Champs obligatoires manquants')
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    toast.error('Email invalide')
    return
  }
  if (!editing.value) {
    if (!form.value.password || form.value.password.length < 8) {
      toast.error('Mot de passe : 8 caractères minimum')
      return
    }
    if (form.value.password !== form.value.password2) {
      toast.error('Les mots de passe ne correspondent pas')
      return
    }
  }

  saving.value = true
  try {
    const payload = { ...form.value }
    if (editing.value) {
      delete payload.password
      delete payload.password2
      await adminAPI.updateUser(editing.value.id, payload)
      toast.success('Administrateur modifié')
    } else {
      await adminAPI.createUser(payload)
      toast.success('Administrateur créé')
    }
    closeModal()
    await load()
  } catch (err) {
    const msg =
      err.response?.data?.errors?.email?.[0] ||
      err.response?.data?.error ||
      "Erreur lors de l'enregistrement"
    logger.warn('Save admin error')
    toast.error(msg)
  } finally {
    saving.value = false
  }
}

const toggleStatus = async (admin) => {
  if (admin.id === currentUserId.value) {
    toast.warning('Vous ne pouvez pas modifier votre propre statut')
    return
  }
  const ok = await askConfirm({
    title: 'Changer le statut',
    message: `Voulez-vous vraiment ${admin.is_active ? 'désactiver' : 'activer'} ${admin.nom} ?`,
    dangerous: admin.is_active,
  })
  if (!ok) return
  try {
    await adminAPI.updateUser(admin.id, { is_active: !admin.is_active })
    toast.success(`Compte ${admin.is_active ? 'désactivé' : 'activé'}`)
    await load()
  } catch {
    toast.error('Erreur')
  }
}

const removeAdmin = async (admin) => {
  if (admin.id === currentUserId.value) {
    toast.warning('Vous ne pouvez pas vous supprimer')
    return
  }
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer définitivement ${admin.nom} ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await adminAPI.deleteUser(admin.id)
    toast.success('Administrateur supprimé')
    await load()
  } catch {
    toast.error('Erreur')
  }
}

const handleLogout = async () => {
  await auth.logout()
  router.push('/it-login')
}

onMounted(() => {
  if (!auth.isSuperIT) {
    toast.error('Accès réservé au SuperIT')
    router.push('/dashboard')
    return
  }
  load()
})
</script>

<style scoped>
.admin-users-layout { min-height: 100vh; background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); font-family: 'Inter', system-ui, sans-serif; }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 20px; }
.stat-pill { display: flex; align-items: center; gap: 12px; padding: 14px 18px; background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; border-left: 4px solid #818cf8; }
.stat-pill.green { border-left-color: #10b981; }
.stat-pill.red { border-left-color: #ef4444; }
.stat-pill.gold { border-left-color: #facc15; }
.stat-pill i { font-size: 20px; color: #818cf8; }
.stat-pill.green i { color: #10b981; }
.stat-pill.red i { color: #ef4444; }
.stat-pill.gold i { color: #facc15; }
.stat-value { font-size: 20px; font-weight: 700; color: #fff; line-height: 1; }
.stat-label { font-size: 11.5px; color: #94a3b8; }

.filters-bar { display: flex; gap: 12px; padding: 14px 18px; background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; margin-bottom: 20px; flex-wrap: wrap; align-items: center; }
.search-wrap { flex: 1; min-width: 200px; position: relative; }
.search-wrap i { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 13px; }
.search-wrap input { width: 100%; padding: 10px 14px 10px 40px; border: 1.5px solid rgba(255, 255, 255, 0.1); border-radius: 10px; font-size: 13.5px; background: rgba(255, 255, 255, 0.04); color: #fff; }
.search-wrap input::placeholder { color: #94a3b8; }
.search-wrap input:focus { outline: none; border-color: #818cf8; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15); }
.filter-select { padding: 10px 14px; border: 1.5px solid rgba(255, 255, 255, 0.1); border-radius: 10px; font-size: 13.5px; background: rgba(255, 255, 255, 0.04); color: #fff; cursor: pointer; }
.filter-select option { background: #1e1b4b; }
.result-count { font-size: 12.5px; color: #94a3b8; padding: 6px 14px; background: rgba(255, 255, 255, 0.04); border-radius: 20px; }
.result-count i { color: #818cf8; margin-right: 4px; }

.btn-create { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; border: none; border-radius: 10px; font-size: 13.5px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5); transition: all 0.15s; }
.btn-create:hover { transform: translateY(-1px); }

.loading-block, .empty-block { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 60px 20px; text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid rgba(255, 255, 255, 0.15); border-top-color: #818cf8; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-block p { color: #94a3b8; }
.empty-block i { font-size: 48px; color: #6366f1; margin-bottom: 12px; display: block; }
.empty-block h3 { color: #fff; margin: 0 0 6px; }
.empty-block p { color: #94a3b8; margin: 0 0 16px; }

.users-list { display: flex; flex-direction: column; gap: 12px; }
.user-card { display: flex; align-items: center; gap: 16px; padding: 16px 20px; background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(20px); border: 1.5px solid rgba(255, 255, 255, 0.08); border-radius: 14px; transition: all 0.15s; }
.user-card:hover { border-color: rgba(129, 140, 248, 0.3); transform: translateX(2px); }
.user-card.is-me { border-color: #818cf8; background: rgba(99, 102, 241, 0.08); }
.user-card.online { border-color: rgba(16, 185, 129, 0.3); }

.user-avatar { position: relative; width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(135deg, #64748b, #475569); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 17px; flex-shrink: 0; }
.user-avatar.super { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.online-ring { position: absolute; inset: -3px; border: 2px solid #10b981; border-radius: 50%; animation: ring-pulse 2s infinite; }
@keyframes ring-pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
.status-dot { position: absolute; bottom: 0; right: 0; width: 13px; height: 13px; border-radius: 50%; background: #ef4444; border: 2px solid #1e1b4b; }
.status-dot.active { background: #10b981; }

.user-body { flex: 1; min-width: 0; }
.user-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 6px; }
.user-head h3 { font-size: 15px; font-weight: 700; color: #fff; margin: 0; display: flex; align-items: center; gap: 8px; }
.you-tag { font-size: 10px; background: #6366f1; color: #fff; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.role-badge { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.role-badge.super { background: rgba(250, 204, 21, 0.15); color: #facc15; }
.role-badge.admin { background: rgba(99, 102, 241, 0.15); color: #818cf8; }
.status-badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.online-badge { display: inline-flex; align-items: center; gap: 5px; padding: 3px 10px; background: rgba(16, 185, 129, 0.15); color: #10b981; border-radius: 20px; font-size: 11px; font-weight: 600; }
.online-badge .dot { width: 6px; height: 6px; background: #10b981; border-radius: 50%; animation: pulse-dot 1.5s infinite; }
@keyframes pulse-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.user-meta { display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: 12.5px; color: #94a3b8; }
.user-meta span { display: inline-flex; align-items: center; gap: 6px; }
.user-meta i { color: #64748b; font-size: 12px; }

.user-actions { display: flex; gap: 8px; flex-shrink: 0; }
.btn-icon { width: 36px; height: 36px; border-radius: 9px; border: 1.5px solid rgba(255, 255, 255, 0.1); background: rgba(255, 255, 255, 0.04); color: #94a3b8; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 13px; transition: all 0.15s; }
.btn-icon:hover:not(:disabled) { background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.2); color: #fff; transform: translateY(-1px); }
.btn-icon.success { color: #10b981; border-color: rgba(16, 185, 129, 0.3); }
.btn-icon.danger { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }
.btn-icon.danger:hover:not(:disabled) { background: rgba(239, 68, 68, 0.15); }
.btn-icon:disabled { opacity: 0.3; cursor: not-allowed; }

.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px; }
.modal-box { background: #1e1b4b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; width: 100%; max-width: 600px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
.modal-title { display: flex; align-items: center; gap: 12px; }
.modal-title i { font-size: 20px; color: #818cf8; }
.modal-title h2 { font-size: 17px; color: #fff; margin: 0; }
.close-btn { width: 34px; height: 34px; border-radius: 50%; border: none; background: none; color: #94a3b8; cursor: pointer; }
.close-btn:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }

.modal-form { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12.5px; font-weight: 600; color: #cbd5e1; }
.form-group input, .form-group select { padding: 10px 14px; border: 1.5px solid rgba(255, 255, 255, 0.1); border-radius: 9px; font-size: 13.5px; background: rgba(255, 255, 255, 0.04); color: #fff; }
.form-group input::placeholder { color: #94a3b8; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: #818cf8; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15); }
.form-group select option { background: #1e1b4b; }

.input-password { position: relative; }
.input-password input { width: 100%; padding-right: 40px; }
.input-password button { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; color: #94a3b8; cursor: pointer; }
.input-password button:hover { color: #818cf8; }

.checkbox-wrap { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #cbd5e1; cursor: pointer; }
.checkbox-wrap input { width: 16px; height: 16px; accent-color: #6366f1; }

.modal-actions { display: flex; justify-content: flex-end; gap: 10px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08); }

.btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 9px; font-size: 13.5px; font-weight: 600; border: none; cursor: pointer; transition: all 0.15s; }
.btn-primary { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; }
.btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .user-card { flex-wrap: wrap; }
  .user-actions { width: 100%; justify-content: flex-end; margin-top: 8px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>
