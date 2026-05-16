import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

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
        const response = await axios.post(`${API_URL}/create-superadmin/`, userData)
        if (response.data.success) {
          this.setEmail(response.data.email)
          return { success: true, message: response.data.message }
        }
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Erreur lors de l\'inscription' }
      }
    },
    
    async login(credentials) {
      try {
        const response = await axios.post(`${API_URL}/login/`, credentials)
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
          
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
          
          return { success: true }
        }
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Code invalide' }
      }
    },
    
    async logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      this.email = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('auth_email')
      delete axios.defaults.headers.common['Authorization']
    },
    
    async fetchUser() {
      if (this.accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        try {
          const response = await axios.get(`${API_URL}/me/`)
          this.user = response.data
        } catch (error) {
          await this.logout()
        }
      }
    }
  }
})
