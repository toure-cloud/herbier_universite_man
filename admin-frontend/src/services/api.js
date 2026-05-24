import axios from 'axios'

// 🏠 LOCAL (développement)
const API_URL = 'http://localhost:8001/api'

// ☁️ PRODUCTION (Render) - décommentez pour déployer
// const API_URL = 'https://herbier-admin-backend.onrender.com/api'

console.log('🔧 API URL:', API_URL)

const api = axios.create({
  baseURL: API_URL,
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
  
  // ✅ CORRIGÉ : utilise le téléphone au lieu de l'email
  verify2FA: (data) => api.post('/verify-2fa/', {
    telephone: data.telephone,
    code: data.code
  }),
  
  logout: () => api.post('/logout/'),
  getCurrentUser: () => api.get('/me/'),
  
  // Ajout de la méthode pour renvoyer le code
  resendCode: (data) => api.post('/resend-code/', {
    telephone: data.telephone
  }),
}

export const publicAPI = {
  getPlantes: () => api.get('/plantes/'),
  getEquipe: () => api.get('/equipe/'),
  getSlides: () => api.get('/slides/'),
  getProjets: () => api.get('/projets/'),
  getDashboard: () => api.get('/dashboard/'),
}

export default { authAPI, publicAPI }