import { defineStore } from 'pinia'
import axios from 'axios'

const ADMIN_API_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8001'


console.log('🔗 [Auth Store] ADMIN_API_URL:', ADMIN_API_URL)

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    email: localStorage.getItem('auth_email') || ''
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    getUser: (state) => state.user,
    getEmail: (state) => state.email
  },
  
  actions: {
    setEmail(email) {
      this.email = email
      localStorage.setItem('auth_email', email)
    },
    
    async register(userData) {
      try {
        const response = await axios.post(`${API_URL}/create-superadmin/`, userData, {
          headers: { 'Content-Type': 'application/json' }
        })
        if (response.data.success) {
          this.setEmail(response.data.email)
          return { success: true, message: response.data.message }
        }
        return { success: false, message: 'Erreur inconnue' }
      } catch (error) {
        let errorMessage = 'Erreur lors de l\'inscription'
        if (error.response?.data?.error) {
          errorMessage = error.response.data.error
        } else if (error.response?.data?.email) {
          errorMessage = error.response.data.email[0]
        } else if (error.response?.data?.telephone) {
          errorMessage = error.response.data.telephone[0]
        }
        return { success: false, message: errorMessage }
      }
    },
    
    async login(credentials) {
      try {
        const response = await axios.post(`${API_URL}/login/`, credentials)
        if (response.data.success && response.data.requires_2fa) {
          this.setEmail(response.data.email)
          return { success: true, requires2FA: true, message: response.data.message }
        }
        return { success: false, message: 'Email ou mot de passe incorrect' }
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Erreur de connexion' }
      }
    },
    
    async verify2FA(code) {
      try {
        const response = await axios.post(`${API_URL}/verify-2fa/`, {
          email: this.email,
          code: code
        })
        
        if (response.data.success) {
          this.accessToken = response.data.access
          this.refreshToken = response.data.refresh
          this.user = response.data.user
          
          localStorage.setItem('access_token', this.accessToken)
          localStorage.setItem('refresh_token', this.refreshToken)
          
          // Configurer axios pour inclure le token dans toutes les requêtes
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
          
          return { success: true }
        }
        return { success: false, message: response.data.error || 'Code invalide' }
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Code invalide' }
      }
    },
    
    async logout() {
      try {
        if (this.refreshToken) {
          await axios.post(`${API_URL}/logout/`, { refresh: this.refreshToken })
        }
      } catch (error) {
        console.error('Erreur lors de la déconnexion', error)
      } finally {
        this.accessToken = null
        this.refreshToken = null
        this.user = null
        this.email = ''
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('auth_email')
        delete axios.defaults.headers.common['Authorization']
      }
    },
    
    async fetchUser() {
      if (!this.accessToken) {
        return null
      }
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
      
      try {
        const response = await axios.get(`${API_URL}/me/`)
        this.user = response.data
        return this.user
      } catch (error) {
        // Token invalide ou expiré
        if (error.response?.status === 401) {
          await this.logout()
        }
        throw error
      }
    },
    
    // Vérifier si le token est encore valide
    async checkAuth() {
      if (!this.accessToken) {
        return false
      }
      
      try {
        await this.fetchUser()
        return true
      } catch (error) {
        return false
      }
    }
  }
})
