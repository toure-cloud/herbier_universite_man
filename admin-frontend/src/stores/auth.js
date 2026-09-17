// src/stores/auth.js
import { defineStore } from 'pinia'
import { authAPI } from '../utils/api'
import { logger } from '../utils/logger'

// ✅ Restaure l'utilisateur depuis localStorage (survit au refresh)
function loadUserFromStorage() {
  try {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // ✅ Restauré depuis localStorage — évite le "menu Admin" au refresh
    user: loadUserFromStorage(),
    accessToken: localStorage.getItem('access_token'),
    email: localStorage.getItem('auth_email') || '',
    initialized: false,
    loading: false,
  }),

  getters: {
    isAuthenticated: (s) => !!s.accessToken && !!s.user,
    // ✅ Tolérant sur la casse pour éviter les surprises backend
    isSuperIT: (s) => {
      const r = (s.user?.role || '').toLowerCase()
      return r === 'it_admin' || r === 'it-admin'
    },
    isAdmin: (s) => (s.user?.role || '').toLowerCase() === 'admin',
    dashboardType: (s) =>
      (s.user?.role || '').toLowerCase() === 'it_admin' ? 'superit' : 'admin',

    getEmail: (s) => s.email,
    getUser: (s) => s.user,

    canManageUsers: (s) => (s.user?.role || '').toLowerCase() === 'it_admin',
    canViewAudit: (s) => (s.user?.role || '').toLowerCase() === 'it_admin',
    canSync: (s) => (s.user?.role || '').toLowerCase() === 'it_admin',
    canCrudContent: (s) =>
      ['it_admin', 'admin'].includes((s.user?.role || '').toLowerCase()),
  },

  actions: {
    setEmail(email) {
      this.email = email
      localStorage.setItem('auth_email', email)
    },

    saveSession(access, user) {
      this.accessToken = access
      this.user = user
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', access) // cohérent avec logout
      localStorage.setItem('user', JSON.stringify(user))
    },

    clearSession() {
      this.accessToken = null
      this.user = null
      this.email = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      localStorage.removeItem('auth_email')
    },

    async loginIT(credentials) {
      return this._login(credentials, 'it')
    },

    async loginAdmin(credentials) {
      return this._login(credentials, 'admin')
    },

    async _login(credentials, type) {
      try {
        // ✅ itLogin / adminLogin existent maintenant dans authAPI
        const fn = type === 'it' ? authAPI.itLogin : authAPI.adminLogin
        const { data } = await fn(credentials)

        if (data.success && data.requires_2fa) {
          this.setEmail(data.email)
          return { success: true, requires2FA: true, email: data.email }
        }
        return { success: false, message: data.error || 'Erreur inconnue' }
      } catch (err) {
        logger.warn(`Login ${type} échoué`)
        return {
          success: false,
          message: err.response?.data?.error || 'Erreur de connexion',
        }
      }
    },

    async verify2FA(code) {
      const email = this.email || localStorage.getItem('auth_email')

      if (!email) {
        return {
          success: false,
          message: 'Email manquant. Reconnectez-vous.',
        }
      }

      try {
        const { data } = await authAPI.verify2FA({ email, code })
        if (data.success) {
          this.saveSession(data.access, data.user)
          return { success: true, user: data.user }
        }
        return { success: false, message: data.error || 'Code invalide' }
      } catch (err) {
        return {
          success: false,
          message: err.response?.data?.error || 'Code invalide',
        }
      }
    },

    async fetchUser() {
      if (!this.accessToken) {
        this.initialized = true
        return null
      }
      try {
        // ✅ authAPI.me() existe maintenant
        const { data } = await authAPI.me()
        this.user = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
        return this.user
      } catch (err) {
        logger.warn('fetchUser échoué')
        this.clearSession()
        return null
      } finally {
        this.initialized = true
      }
    },

    async logout() {
      try {
        if (this.accessToken) await authAPI.logout()
      } catch {
        // silencieux
      } finally {
        this.clearSession()
      }
    },
  },
})