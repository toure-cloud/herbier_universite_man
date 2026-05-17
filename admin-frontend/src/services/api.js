import axios from 'axios'

// Configuration de l'URL de base
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

// Configuration axios
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API d'authentification
export const authAPI = {
  register: (userData) => api.post('/create-superadmin/', userData),
  login: (credentials) => api.post('/login/', credentials),
  verify2FA: (code) => api.post('/verify-2fa/', { code, email: localStorage.getItem('auth_email') }),
  logout: () => api.post('/logout/'),
  getCurrentUser: () => api.get('/me/'),
}

// API pour les données publiques (depuis l'API publique)
export const publicAPI = {
  getPlantes: () => api.get('/plantes/'),
  getEquipe: () => api.get('/equipe/'),
  getSlides: () => api.get('/slides/'),
  getProjets: () => api.get('/projets/'),
  getDashboard: () => api.get('/dashboard/'),
}

// API pour la synchronisation
export const adminAPI = {
  syncAll: () => api.get('/sync-all/'),
  syncEndpoint: (endpoint) => api.get(`/sync/${endpoint}/`),
  getSyncLogs: () => api.get('/sync-logs/'),
  getStats: () => api.get('/stats/'),
  getDashboard: () => api.get('/dashboard/'),
}

export default { authAPI, publicAPI, adminAPI }
