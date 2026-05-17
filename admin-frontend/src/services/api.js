import axios from 'axios'

// URL de base - CORRECTE avec /api
const API_URL = 'https://herbier-admin-backend.onrender.com/api'

console.log('🔧 API URL:', API_URL)

const api = axios.create({
  baseURL: API_URL,  // Important : pas de /api supplémentaire
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (userData) => api.post('/create-superadmin/', userData),
  login: (credentials) => api.post('/login/', credentials),
  verify2FA: (code) => api.post('/verify-2fa/', { code, email: localStorage.getItem('auth_email') }),
  logout: () => api.post('/logout/'),
  getCurrentUser: () => api.get('/me/'),
}

export const publicAPI = {
  getPlantes: () => api.get('/plantes/'),
  getEquipe: () => api.get('/equipe/'),
  getSlides: () => api.get('/slides/'),
  getProjets: () => api.get('/projets/'),
  getDashboard: () => api.get('/dashboard/'),
}

export const adminAPI = {
  syncAll: () => api.get('/sync-all/'),
  syncEndpoint: (endpoint) => api.get(`/sync/${endpoint}/`),
  getSyncLogs: () => api.get('/sync-logs/'),
  getStats: () => api.get('/stats/'),
  getDashboard: () => api.get('/dashboard/'),
}

export default { authAPI, publicAPI, adminAPI }
