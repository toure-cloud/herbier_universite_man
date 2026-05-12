import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:8001/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour ajouter le token à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les réponses d'erreur (token expiré)
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh_token')
      
      if (refreshToken) {
        try {
          const response = await axios.post('http://localhost:8001/api/token/refresh/', {
            refresh: refreshToken
          })
          
          if (response.data.access) {
            localStorage.setItem('access_token', response.data.access)
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`
            return api(originalRequest)
          }
        } catch (refreshError) {
          // Refresh token invalide, déconnexion
          const authStore = useAuthStore()
          await authStore.logout()
          window.location.href = '/login'
        }
      } else {
        // Pas de refresh token, déconnexion
        const authStore = useAuthStore()
        await authStore.logout()
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
