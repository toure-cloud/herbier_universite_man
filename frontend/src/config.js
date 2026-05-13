// Configuration de l'API
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  API_URL,
  API_ENDPOINTS: {
    slides: `${API_URL}/api/slides/`,
    plantes: `${API_URL}/api/plantes/`,
    activites: `${API_URL}/api/activites/`,
    equipe: `${API_URL}/api/equipe/`,
    projets: `${API_URL}/api/projets/`,
    temoignages: `${API_URL}/api/temoignages/`,
    publications: `${API_URL}/api/publications/`,
    faqs: `${API_URL}/api/faqs/`,
    contact: `${API_URL}/api/submit-contact/`,
    dashboard: `${API_URL}/api/dashboard/`,
    activitesData: `${API_URL}/api/activites-data/`,
    projetsData: `${API_URL}/api/projets-data/`,
    contactData: `${API_URL}/api/contact-data/`,
    herbierStats: `${API_URL}/api/herbier-stats/`,
  }
}
