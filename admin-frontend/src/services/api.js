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

// API pour les données
export const dataAPI = {
  // Plantes
  getPlantes: () => api.get('/plantes/'),
  getPlante: (id) => api.get(`/plantes/${id}/`),
  createPlante: (data) => api.post('/plantes/', data),
  updatePlante: (id, data) => api.put(`/plantes/${id}/`, data),
  deletePlante: (id) => api.delete(`/plantes/${id}/`),
  
  // Équipe
  getEquipe: () => api.get('/equipe/'),
  createEquipe: (data) => api.post('/equipe/', data),
  updateEquipe: (id, data) => api.put(`/equipe/${id}/`, data),
  deleteEquipe: (id) => api.delete(`/equipe/${id}/`),
  
  // Slides
  getSlides: () => api.get('/slides/'),
  createSlide: (data) => api.post('/slides/', data),
  updateSlide: (id, data) => api.put(`/slides/${id}/`, data),
  deleteSlide: (id) => api.delete(`/slides/${id}/`),
  
  // Projets
  getProjets: () => api.get('/projets/'),
  createProjet: (data) => api.post('/projets/', data),
  updateProjet: (id, data) => api.put(`/projets/${id}/`, data),
  deleteProjet: (id) => api.delete(`/projets/${id}/`),
  
  // Activités
  getActivites: () => api.get('/activites/'),
  createActivite: (data) => api.post('/activites/', data),
  updateActivite: (id, data) => api.put(`/activites/${id}/`, data),
  deleteActivite: (id) => api.delete(`/activites/${id}/`),
  
  // Témoignages
  getTemoignages: () => api.get('/temoignages/'),
  createTemoignage: (data) => api.post('/temoignages/', data),
  updateTemoignage: (id, data) => api.put(`/temoignages/${id}/`, data),
  deleteTemoignage: (id) => api.delete(`/temoignages/${id}/`),
  
  // Publications
  getPublications: () => api.get('/publications/'),
  createPublication: (data) => api.post('/publications/', data),
  updatePublication: (id, data) => api.put(`/publications/${id}/`, data),
  deletePublication: (id) => api.delete(`/publications/${id}/`),
  
  // FAQs
  getFAQs: () => api.get('/faqs/'),
  createFAQ: (data) => api.post('/faqs/', data),
  updateFAQ: (id, data) => api.put(`/faqs/${id}/`, data),
  deleteFAQ: (id) => api.delete(`/faqs/${id}/`),
  
  // Statistiques
  getStats: () => api.get('/statistiques/'),
  
  // Dashboard
  getDashboard: () => api.get('/dashboard/'),
  
  // Synchronisation
  syncData: () => api.get('/sync-all/'),
  syncEndpoint: (endpoint) => api.get(`/sync/${endpoint}/`),
  getSyncLogs: () => api.get('/sync-logs/'),
}

export default { authAPI, dataAPI }
