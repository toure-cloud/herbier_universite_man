import { defineStore } from 'pinia'
import { authAPI } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    email: localStorage.getItem('auth_email') || '',
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    getUser: (state) => state.user,
    getEmail: (state) => state.email,
  },
  
  actions: {
    setEmail(email) {
      this.email = email
      localStorage.setItem('auth_email', email)
    },
    
    async register(userData) {
      try {
        const response = await authAPI.register(userData)
        if (response.data.success) {
          this.setEmail(response.data.email)
          return { success: true, message: response.data.message, email: response.data.email }
        }
      } catch (error) {
        const errors = error.response?.data?.errors || {}
        const errorMessage = Object.values(errors).flat().join(', ') || 'Erreur lors de l\'inscription'
        return { success: false, message: errorMessage }
      }
    },
    
    async login(credentials) {
      try {
        const response = await authAPI.login(credentials)
        if (response.data.success && response.data.requires_2fa) {
          this.setEmail(response.data.email)
          return { success: true, requires2FA: true, message: response.data.message }
        }
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Erreur de connexion' }
      }
    },
    
    async verify2FA(code) {
      try {
        const response = await authAPI.verify2FA(code)
        if (response.data.success) {
          this.accessToken = response.data.access
          this.refreshToken = response.data.refresh
          this.user = response.data.user
          
          localStorage.setItem('access_token', this.accessToken)
          localStorage.setItem('refresh_token', this.refreshToken)
          localStorage.removeItem('auth_email')
          
          return { success: true }
        }
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Code invalide' }
      }
    },
    
    async logout() {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Erreur déconnexion:', error)
      } finally {
        this.accessToken = null
        this.refreshToken = null
        this.user = null
        this.email = ''
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('auth_email')
      }
    },
    
    async fetchUser() {
      if (this.accessToken) {
        try {
          const response = await authAPI.getCurrentUser()
          this.user = response.data
        } catch (error) {
          await this.logout()
        }
      }
    },
  },
})
