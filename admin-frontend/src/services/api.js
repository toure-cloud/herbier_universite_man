import axios from 'axios'

// 🏠 LOCAL (développement) - Commenter en production
const API_URL = 'http://localhost:8001/api'

// ☁️ PRODUCTION (Render) - Décommenter pour la production
// const API_URL = 'https://herbier-admin-backend.onrender.com/api'

console.log('🔧 API URL:', API_URL)

const api = axios.create({
  baseURL: API_URL,
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
    console.error('API Error:', error.response?.status, error.response?.data)
    
    // Si token expiré, rediriger vers login
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

// ==================== API D'AUTHENTIFICATION ====================
export const authAPI = {
  // Création de compte
  register: (userData) => api.post('/create-superadmin/', userData),
  
  // Connexion (première étape)
  login: (credentials) => api.post('/login/', credentials),
  
  // Vérification 2FA (deuxième étape)
  verify2FA: (data) => api.post('/verify-2fa/', {
    email: data.email,
    code: data.code
  }),
  
  // Renvoyer le code OTP
  resendCode: (data) => api.post('/resend-code/', {
    email: data.email
  }),
  
  // Déconnexion
  logout: () => api.post('/logout/'),
  
  // Récupérer l'utilisateur courant
  getCurrentUser: () => api.get('/me/'),
}

// ==================== API DES DONNÉES PUBLIQUES ====================
export const publicAPI = {
  // Plantes
  getPlantes: () => api.get('/plantes/'),
  getPlante: (id) => api.get(`/plantes/${id}/`),
  createPlante: (data) => api.post('/plantes/', data),
  updatePlante: (id, data) => api.put(`/plantes/${id}/`, data),
  deletePlante: (id) => api.delete(`/plantes/${id}/`),
  
  // Équipe
  getEquipe: () => api.get('/equipe/'),
  getMembre: (id) => api.get(`/equipe/${id}/`),
  createMembre: (data) => api.post('/equipe/', data),
  updateMembre: (id, data) => api.put(`/equipe/${id}/`, data),
  deleteMembre: (id) => api.delete(`/equipe/${id}/`),
  
  // Slides
  getSlides: () => api.get('/slides/'),
  getSlide: (id) => api.get(`/slides/${id}/`),
  createSlide: (data) => api.post('/slides/', data),
  updateSlide: (id, data) => api.put(`/slides/${id}/`, data),
  deleteSlide: (id) => api.delete(`/slides/${id}/`),
  
  // Projets
  getProjets: () => api.get('/projets/'),
  getProjet: (id) => api.get(`/projets/${id}/`),
  createProjet: (data) => api.post('/projets/', data),
  updateProjet: (id, data) => api.put(`/projets/${id}/`, data),
  deleteProjet: (id) => api.delete(`/projets/${id}/`),
  
  // Activités
  getActivites: () => api.get('/activites/'),
  getActivite: (id) => api.get(`/activites/${id}/`),
  createActivite: (data) => api.post('/activites/', data),
  updateActivite: (id, data) => api.put(`/activites/${id}/`, data),
  deleteActivite: (id) => api.delete(`/activites/${id}/`),
  
  // Témoignages
  getTemoignages: () => api.get('/temoignages/'),
  getTemoignage: (id) => api.get(`/temoignages/${id}/`),
  createTemoignage: (data) => api.post('/temoignages/', data),
  updateTemoignage: (id, data) => api.put(`/temoignages/${id}/`, data),
  deleteTemoignage: (id) => api.delete(`/temoignages/${id}/`),
  
  // Publications
  getPublications: () => api.get('/publications/'),
  getPublication: (id) => api.get(`/publications/${id}/`),
  createPublication: (data) => api.post('/publications/', data),
  updatePublication: (id, data) => api.put(`/publications/${id}/`, data),
  deletePublication: (id) => api.delete(`/publications/${id}/`),
  
  // FAQs
  getFAQs: () => api.get('/faqs/'),
  getFAQ: (id) => api.get(`/faqs/${id}/`),
  createFAQ: (data) => api.post('/faqs/', data),
  updateFAQ: (id, data) => api.put(`/faqs/${id}/`, data),
  deleteFAQ: (id) => api.delete(`/faqs/${id}/`),
  
  // Dashboard
  getDashboard: () => api.get('/dashboard/'),
  
  // Statistiques
  getStats: () => api.get('/statistiques/'),
}

// ==================== API D'ADMINISTRATION ====================
export const adminAPI = {
  // Synchronisation
  syncAll: () => api.get('/sync-all/'),
  syncEndpoint: (endpoint) => api.get(`/sync/${endpoint}/`),
  getSyncLogs: () => api.get('/sync-logs/'),
  
  // Statistiques avancées
  getAdminStats: () => api.get('/stats/'),
  getAdminDashboard: () => api.get('/admin-dashboard/'),
  
  // Gestion des utilisateurs
  getUsers: () => api.get('/superadmins/'),
  getUser: (id) => api.get(`/superadmins/${id}/`),
  createUser: (data) => api.post('/superadmins/', data),
  updateUser: (id, data) => api.put(`/superadmins/${id}/`, data),
  deleteUser: (id) => api.delete(`/superadmins/${id}/`),
  
  // Logs
  getLogs: () => api.get('/logs/'),
}

// Export par défaut
export default { authAPI, publicAPI, adminAPI }
