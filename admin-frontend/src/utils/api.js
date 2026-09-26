import axios from 'axios'

// ============================================
// CONFIGURATION
// ============================================
// ✅ Détection d'environnement (compatible tunnels de dev)
const isProduction =
  import.meta.env.PROD ||
  (
    window.location.hostname !== 'localhost' &&
    window.location.hostname !== '127.0.0.1' &&
    !window.location.hostname.includes('devtunnels.ms') &&
    !window.location.hostname.includes('trycloudflare.com') &&
    !window.location.hostname.includes('ngrok') &&
    !window.location.hostname.includes('loca.lt')
  )

// ✅ VITE_API_URL en priorité (défini dans .env.development)
const ADMIN_API_URL = import.meta.env.VITE_API_URL || (
  isProduction
    ? 'https://herbier-admin-backend.onrender.com/api'
    : 'http://localhost:8001/api'
)

const PUBLIC_API_URL = import.meta.env.VITE_PUBLIC_API_URL || (
  isProduction
    ? 'https://herbier-backend.onrender.com/api'
    : 'http://localhost:8000/api'
)

// ============================================
// UTILITAIRES
// ============================================
const buildFormData = (data) => {
  const formData = new FormData()
  Object.entries(data || {}).forEach(([key, value]) => {
    if (value === null || value === undefined || value === '') return
    if (key === 'image_preview' || key === 'image_file' || key === '_existing_image') return

    if (value instanceof File) {
      formData.append(key, value, value.name)
    } else if (typeof value === 'boolean') {
      formData.append(key, value ? 'true' : 'false')
    } else if (value instanceof Blob) {
      formData.append(key, value)
    } else if (typeof value === 'object') {
      formData.append(key, JSON.stringify(value))
    } else {
      formData.append(key, value)
    }
  })
  return formData
}

const hasFile = (data) =>
  data && Object.values(data).some((v) => v instanceof File)

const buildRequest = (data) => {
  if (hasFile(data)) {
    return { data: buildFormData(data), headers: { 'Content-Type': 'multipart/form-data' } }
  }
  return { data, headers: {} }
}

const handleAuthError = (error) => {
  if (error.response?.status === 401) {
    console.warn('⚠️ Token expiré ou invalide')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    const path = window.location.pathname
    if (
      path !== '/it-login' &&
      path !== '/admin-login' &&
      path !== '/login' &&
      path !== '/register'
    ) {
      window.location.href = '/it-login'
    }
  }
  if (error.response?.status === 403) {
    console.error('🚫 Accès interdit (403)')
  }
  return Promise.reject(error)
}

// ============================================
// INSTANCES AXIOS
// ============================================
const adminApi = axios.create({
  baseURL: ADMIN_API_URL,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
  withCredentials: false,
  timeout: 90000,
})

adminApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    if (config.data instanceof FormData) delete config.headers['Content-Type']
    return config
  },
  (error) => Promise.reject(error)
)

adminApi.interceptors.response.use(
  (response) => response,
  (error) => handleAuthError(error)
)

const publicApi = axios.create({
  baseURL: PUBLIC_API_URL,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
  withCredentials: false,
  timeout: 30000,
})

publicApi.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('❌ [Public API] Erreur:', error.response?.status)
    return Promise.reject(error)
  }
)

// ============================================
// AUTH API
// ============================================
export const authAPI = {
  register: (data) => adminApi.post('/create-superadmin/', data),
  itLogin: (data) => adminApi.post('/it/login/', data),
  adminLogin: (data) => adminApi.post('/admin/login/', data),
  login: (data) => adminApi.post('/it/login/', data),
  verify2FA: (data) => adminApi.post('/verify-2fa/', data),
  resendCode: (data) => adminApi.post('/resend-code/', data),
  logout: () => {
    const token = localStorage.getItem('access_token')
    return token ? adminApi.post('/logout/') : Promise.resolve()
  },
  me: () => adminApi.get('/me/'),
  getCurrentUser: () => adminApi.get('/me/'),
  forgotPassword: (data) => adminApi.post('/forgot-password/', data),
  resetPassword: (data) => adminApi.post('/reset-password/', data),
  totpSetup: () => adminApi.post('/totp/setup/'),
  totpVerifySetup: (data) => adminApi.post('/totp/verify-setup/', data),
  totpDisable: (data) => adminApi.post('/totp/disable/', data),
}

// ============================================
// PUBLIC API
// ============================================
export const publicAPI = {
  getPartenaires: () => publicApi.get('/partenaires/'),
  getPlantes: () => publicApi.get('/plantes/'),
  getEquipe: () => publicApi.get('/equipe/'),
  getSlides: () => publicApi.get('/slides/'),
  getProjets: () => publicApi.get('/projets/'),
  getActivites: () => publicApi.get('/activites/'),
  getTemoignages: () => publicApi.get('/temoignages/'),
  getPublications: () => publicApi.get('/publications/'),
  getFaqs: () => publicApi.get('/faqs/'),
  getStatistiques: () => publicApi.get('/statistiques/'),
  getMethodologie: () => publicApi.get('/methodologie/'),
  getDashboard: () => publicApi.get('/dashboard/'),
  getHerbierStats: () => publicApi.get('/herbier-stats/'),
  getSearchSuggestions: (query, limit = 10) =>
    publicApi.get(`/search-suggestions/?q=${query}&limit=${limit}`),
}

// ============================================
// ADMIN API (haut niveau)
// ============================================
export const adminAPI = {
  // Utilisateurs
  getUsers: () => adminApi.get('/users/'),
  createUser: (data) => adminApi.post('/users/create/', data),
  updateUser: (id, data) => adminApi.patch(`/users/${id}/`, data),
  deleteUser: (id) => adminApi.delete(`/users/${id}/delete/`),

  // Contenu (GET)
  getPlantes: () => adminApi.get('/plantes/'),
  getEquipe: () => adminApi.get('/equipe/'),
  getSlides: () => adminApi.get('/slides/'),
  getProjets: () => adminApi.get('/projets/'),
  getActivites: () => adminApi.get('/activites/'),
  getPartenaires: () => adminApi.get('/partenaires/'),
  getTemoignages: () => adminApi.get('/temoignages/'),
  getPublications: () => adminApi.get('/publications/'),
  getFaqs: () => adminApi.get('/faqs/'),
  getStatistiques: () => adminApi.get('/statistiques/'),
  getMethodologie: () => adminApi.get('/methodologie/'),

  // Stats & audit
  getAdminStats: () => adminApi.get('/stats/'),
  getAuditLogs: (params = {}) => adminApi.get('/audit/logs/', { params }),

  // CRUD génériques
  createItem: (endpoint, data) => {
    const { data: body, headers } = buildRequest(data)
    return adminApi.post(`/${endpoint}/`, body, { headers })
  },
  updateItem: (endpoint, id, data) => {
    const { data: body, headers } = buildRequest(data)
    return adminApi.put(`/${endpoint}/${id}/`, body, { headers })
  },
  patchItem: (endpoint, id, data) =>
    adminApi.patch(`/${endpoint}/${id}/`, data),
  deleteItem: (endpoint, id) => adminApi.delete(`/${endpoint}/${id}/`),
  createMultiple: (endpoint, data) => adminApi.post(`/${endpoint}/batch/`, data),

  // Sync
  syncAll: () => adminApi.post('/sync-all/', {}),
  syncHerbierData: (data) => adminApi.post('/sync-herbier-data/', data),
}

// ============================================
// APIs PAR RESSOURCE (alias utilisés par les vues)
// ============================================
const makeResourceAPI = (endpoint) => ({
  getAll: () => adminApi.get(`/${endpoint}/`),
  list: () => adminApi.get(`/${endpoint}/`),
  get: (id) => adminApi.get(`/${endpoint}/${id}/`),
  getById: (id) => adminApi.get(`/${endpoint}/${id}/`),
  create: (data) => {
    const { data: body, headers } = buildRequest(data)
    return adminApi.post(`/${endpoint}/`, body, { headers })
  },
  update: (id, data) => {
    const { data: body, headers } = buildRequest(data)
    return adminApi.put(`/${endpoint}/${id}/`, body, { headers })
  },
  patch: (id, data) => adminApi.patch(`/${endpoint}/${id}/`, data),
  delete: (id) => adminApi.delete(`/${endpoint}/${id}/`),
  remove: (id) => adminApi.delete(`/${endpoint}/${id}/`),
})

export const plantesAPI       = makeResourceAPI('plantes')
export const projetsAPI       = makeResourceAPI('projets')
export const activitesAPI     = makeResourceAPI('activites')
export const publicationsAPI  = makeResourceAPI('publications')
export const equipeAPI        = makeResourceAPI('equipe')
export const partenairesAPI   = makeResourceAPI('partenaires')
export const temoignagesAPI   = makeResourceAPI('temoignages')
export const slidesAPI        = makeResourceAPI('slides')
export const faqsAPI          = makeResourceAPI('faqs')
export const statistiquesAPI  = makeResourceAPI('statistiques')
export const methodologieAPI  = makeResourceAPI('methodologie')
export const usersAPI         = makeResourceAPI('users')

// ============================================
// EXPORTS INSTANCES AXIOS
// ============================================
export { adminApi, publicApi }

// ============================================
// EXPORT PAR DÉFAUT
// ============================================
export default {
  authAPI,
  publicAPI,
  adminAPI,
  adminApi,
  publicApi,
  plantesAPI,
  projetsAPI,
  activitesAPI,
  publicationsAPI,
  equipeAPI,
  partenairesAPI,
  temoignagesAPI,
  slidesAPI,
  faqsAPI,
  statistiquesAPI,
  methodologieAPI,
  usersAPI,
}