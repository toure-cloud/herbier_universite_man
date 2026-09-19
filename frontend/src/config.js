// src/config.js
const RAW_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')
const API_URL = RAW_URL.endsWith('/api') ? RAW_URL : `${RAW_URL}/api`

export default {
  API_URL,
  API_ENDPOINTS: {
    slides: `${API_URL}/slides/`,
    plantes: `${API_URL}/plantes/`,
    activites: `${API_URL}/activites/`,
    equipe: `${API_URL}/equipe/`,
    projets: `${API_URL}/projets/`,
    temoignages: `${API_URL}/temoignages/`,
    publications: `${API_URL}/publications/`,
    partenaires: `${API_URL}/partenaires/`,   // ✅ ajouté
    faqs: `${API_URL}/faqs/`,
    contact: `${API_URL}/submit-contact/`,
    dashboard: `${API_URL}/dashboard/`,
    activitesData: `${API_URL}/activites-data/`,
    projetsData: `${API_URL}/projets-data/`,
    contactData: `${API_URL}/contact-data/`,
    herbierStats: `${API_URL}/herbier-stats/`,
  }
}