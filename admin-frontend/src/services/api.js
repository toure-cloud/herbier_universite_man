// api.js
import axios from 'axios'

// === CONFIGURATION ===
// ✅ Détection automatique de l'environnement
const isProduction = import.meta.env.PROD || 
                     window.location.hostname !== 'localhost'

const ADMIN_API_URL = isProduction 
  ? 'https://herbier-admin-backend.onrender.com/api'
  : 'http://localhost:8001'

const API_URL = isProduction 
  ? 'https://herbier-backend.onrender.com/api'
  : 'http://localhost:8000'

console.log('🔗 ADMIN_API_URL:', ADMIN_API_URL)
console.log('🔗 API_URL:', API_URL)



// ============================================
// UTILITAIRES
// ============================================

/**
 * Construit un FormData pour l'upload de fichiers
 */
const buildFormData = (data) => {
  const formData = new FormData()

  Object.entries(data || {}).forEach(([key, value]) => {
    // Ignorer les valeurs vides
    if (value === null || value === undefined || value === '') return
    
    // Ignorer les champs temporaires
    if (key === 'image_preview' || key === 'image_file' || key === '_existing_image') return

    // Gérer les fichiers
    if (value instanceof File) {
      formData.append(key, value, value.name)
    } 
    // Gérer les booléens
    else if (typeof value === 'boolean') {
      formData.append(key, value ? 'true' : 'false')
    } 
    // Gérer les Blobs
    else if (value instanceof Blob) {
      formData.append(key, value)
    } 
    // Gérer les objets (les convertir en JSON)
    else if (typeof value === 'object') {
      formData.append(key, JSON.stringify(value))
    } 
    // Gérer les valeurs simples
    else {
      formData.append(key, value)
    }
  })

  return formData
}

/**
 * Gère les erreurs et redirige vers login si nécessaire
 */
const handleAuthError = (error) => {
  if (error.response?.status === 401) {
    console.warn('⚠️ Token expiré ou invalide')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
      window.location.href = '/login'
    }
  }
  
  if (error.response?.status === 403) {
    console.error('🚫 Accès interdit (403)')
  }
  
  return Promise.reject(error)
}

// ============================================
// ADMIN API (port 8001)
// ============================================
const adminApi = axios.create({
  baseURL: `${ADMIN_API_URL}/api`,
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: false,
  timeout: 90000, // 90 secondes timeout
})

// ✅ Intercepteur de requête - Ajout du token
adminApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Pour les requêtes avec FormData, supprimer le Content-Type pour que axios le définisse automatiquement
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    
    return config
  },
  (error) => {
    console.error('❌ Erreur intercepteur requête:', error)
    return Promise.reject(error)
  }
)

// ✅ Intercepteur de réponse - Gestion des erreurs
adminApi.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    return handleAuthError(error)
  }
)

// ============================================
// PUBLIC API (port 8000)
// ============================================
const publicApi = axios.create({
  baseURL: `${PUBLIC_API_URL}/api`,
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
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
// EXPORTS - AUTHENTIFICATION
// ============================================
export const authAPI = {
  /**
   * Inscription d'un super administrateur
   */
  register: (data) => {
    console.log('📝 Inscription:', data.email)
    return adminApi.post('/create-superadmin/', data)
  },

  /**
   * Connexion d'un administrateur
   */
  login: (data) => {
    console.log('🔐 Login:', data.email)
    return adminApi.post('/login/', data)
  },

  /**
   * Vérification du code 2FA
   */
  verify2FA: (data) => {
    console.log('🔑 Vérification 2FA:', data.email)
    return adminApi.post('/verify-2fa/', data)
  },

  /**
   * Renvoyer un nouveau code 2FA
   */
  resendCode: (data) => {
    console.log('🔄 Renvoi code:', data.email)
    return adminApi.post('/resend-code/', data)
  },

  /**
   * Déconnexion
   */
  logout: () => {
    console.log('🚪 Déconnexion')
    const token = localStorage.getItem('access_token')
    if (token) {
      return adminApi.post('/logout/')
    }
    return Promise.resolve()
  },

  /**
   * Récupérer l'utilisateur courant
   */
  getCurrentUser: () => {
    console.log('👤 Récupération utilisateur courant')
    return adminApi.get('/me/')
  },

  /**
   * Demander la réinitialisation du mot de passe
   */
  forgotPassword: (data) => {
    console.log('🔑 Demande de réinitialisation:', data.email)
    return adminApi.post('/forgot-password/', data)
  },

  /**
   * Réinitialiser le mot de passe
   */
  resetPassword: (data) => {
    console.log('🔑 Réinitialisation du mot de passe')
    return adminApi.post('/reset-password/', data)
  }
}

// ============================================
// EXPORTS - PUBLIC (Lecture seule)
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
  getSearchSuggestions: (query, limit = 10) => publicApi.get(`/search-suggestions/?q=${query}&limit=${limit}`),
}

// ============================================
// EXPORTS - ADMIN (Écriture)
// ============================================
export const adminAPI = {
  // ==================== GESTION DES UTILISATEURS ====================
  getUsers: () => {
    console.log('👥 Récupération des utilisateurs')
    return adminApi.get('/users/')
  },

  createUser: (data) => {
    console.log('👤 Création utilisateur:', data.email)
    return adminApi.post('/users/create/', data)
  },

  updateUser: (id, data) => {
    console.log('✏️ Mise à jour utilisateur:', id)
    return adminApi.put(`/users/${id}/`, data)
  },

  deleteUser: (id) => {
    console.log('🗑️ Suppression utilisateur:', id)
    return adminApi.delete(`/users/${id}/delete/`)
  },

  toggleUserStatus: (id, data) => {
    console.log('🔄 Changement statut utilisateur:', id)
    return adminApi.put(`/users/${id}/toggle-status/`, data)
  },

  // ==================== GESTION DES DONNÉES ====================
  getPlantes: () => {
    console.log('🌿 Récupération des plantes')
    return adminApi.get('/plantes/')
  },

  getEquipe: () => {
    console.log('👥 Récupération de l\'équipe')
    return adminApi.get('/equipe/')
  },

  getSlides: () => {
    console.log('📸 Récupération des slides')
    return adminApi.get('/slides/')
  },

  getProjets: () => {
    console.log('📊 Récupération des projets')
    return adminApi.get('/projets/')
  },

  getActivites: () => {
    console.log('⚡ Récupération des activités')
    return adminApi.get('/activites/')
  },

  getPartenaires: () => {
    console.log('🤝 Récupération des partenaires')
    return adminApi.get('/partenaires/')
  },

  getTemoignages: () => {
    console.log('💬 Récupération des témoignages')
    return adminApi.get('/temoignages/')
  },

  getPublications: () => {
    console.log('📚 Récupération des publications')
    return adminApi.get('/publications/')
  },

  getFaqs: () => {
    console.log('❓ Récupération des FAQs')
    return adminApi.get('/faqs/')
  },

  getStatistiques: () => {
    console.log('📊 Récupération des statistiques')
    return adminApi.get('/statistiques/')
  },

  getMethodologie: () => {
    console.log('📋 Récupération de la méthodologie')
    return adminApi.get('/methodologie/')
  },

  getAdminStats: () => {
    console.log('📊 Récupération statistiques admin')
    return adminApi.get('/stats/')
  },

  // ==================== CRUD GÉNÉRIQUE ====================
  createItem: (endpoint, data) => {
    console.log(`📝 Création ${endpoint}:`, data)
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.error('❌ Pas de token')
      return Promise.reject(new Error('Non authentifié'))
    }

    // Vérifier s'il y a un upload de fichier
    const hasFileUpload = data && Object.values(data).some(value => value instanceof File)
    const requestData = hasFileUpload ? buildFormData(data) : data
    const headers = hasFileUpload ? { 'Content-Type': 'multipart/form-data' } : {}

    return adminApi.post(`/${endpoint}/`, requestData, { headers })
  },

  updateItem: (endpoint, id, data) => {
    console.log(`✏️ Mise à jour ${endpoint} ${id}:`, data)
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.error('❌ Pas de token')
      return Promise.reject(new Error('Non authentifié'))
    }

    const hasFileUpload = data && Object.values(data).some(value => value instanceof File)
    const requestData = hasFileUpload ? buildFormData(data) : data
    const headers = hasFileUpload ? { 'Content-Type': 'multipart/form-data' } : {}

    return adminApi.put(`/${endpoint}/${id}/`, requestData, { headers })
  },

  deleteItem: (endpoint, id) => {
    console.log(`🗑️ Suppression ${endpoint} ${id}`)
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.error('❌ Pas de token')
      return Promise.reject(new Error('Non authentifié'))
    }
    return adminApi.delete(`/${endpoint}/${id}/`)
  },

  createMultiple: (endpoint, data) => {
    console.log(`📦 Création multiple ${endpoint}:`, data.length)
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.error('❌ Pas de token')
      return Promise.reject(new Error('Non authentifié'))
    }
    return adminApi.post(`/${endpoint}/batch/`, data)
  },

  // ==================== SYNCHRONISATION ====================
  syncAll: () => {
    console.log('🔄 Synchronisation complète')
    return adminApi.post('/sync-all/', {})
  },

  syncHerbierData: (data) => {
    console.log('🔄 Synchronisation des données herbier')
    return adminApi.post('/sync-herbier-data/', data)
  }
}

// ============================================
// EXPORT PAR DÉFAUT
// ============================================
export default { authAPI, publicAPI, adminAPI }