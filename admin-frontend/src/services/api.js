import axios from 'axios'

// Configuration des URLs
const ADMIN_API_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8001/api'
const PUBLIC_API_URL = import.meta.env.VITE_PUBLIC_API_URL || 'https://herbier-universite-man.onrender.com/api'

// Service pour l'API publique
export const publicAPI = {
    getPlantes: () => axios.get(`${PUBLIC_API_URL}/plantes/`),
    getEquipe: () => axios.get(`${PUBLIC_API_URL}/equipe/`),
    getPartenaires: () => axios.get(`${PUBLIC_API_URL}/partenaires/`),
    getSlides: () => axios.get(`${PUBLIC_API_URL}/slides/`),
    getProjets: () => axios.get(`${PUBLIC_API_URL}/projets/`),
    getActivites: () => axios.get(`${PUBLIC_API_URL}/activites/`),
    getTemoignages: () => axios.get(`${PUBLIC_API_URL}/temoignages/`),
    getPublications: () => axios.get(`${PUBLIC_API_URL}/publications/`),
    getFAQs: () => axios.get(`${PUBLIC_API_URL}/faqs/`),
    getStatistiques: () => axios.get(`${PUBLIC_API_URL}/statistiques/`),
    getDashboard: () => axios.get(`${PUBLIC_API_URL}/dashboard/`),
}

// Service pour l'API admin
export const adminAPI = {
    syncAll: () => axios.get(`${ADMIN_API_URL}/sync-all/`),
    syncEndpoint: (endpoint) => axios.get(`${ADMIN_API_URL}/sync/${endpoint}/`),
    getSyncLogs: () => axios.get(`${ADMIN_API_URL}/sync-logs/`),
    getStats: () => axios.get(`${ADMIN_API_URL}/stats/`),
    getDashboard: () => axios.get(`${ADMIN_API_URL}/dashboard/`),
}

// Service pour l'authentification
export const authAPI = {
    login: (credentials) => axios.post(`${ADMIN_API_URL}/login/`, credentials),
    register: (userData) => axios.post(`${ADMIN_API_URL}/create-superadmin/`, userData),
    verify2FA: (code) => axios.post(`${ADMIN_API_URL}/verify-2fa/`, code),
    logout: () => axios.post(`${ADMIN_API_URL}/logout/`),
}

export default { publicAPI, adminAPI, authAPI }
