import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue'), meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue'), meta: { requiresAuth: false } },
  { path: '/forgot-password', name: 'ForgotPassword', component: () => import('../views/ForgotPassword.vue'), meta: { requiresAuth: false } },
  { path: '/verify-2fa', name: 'Verify2FA', component: () => import('../views/Verify2FA.vue'), meta: { requiresAuth: false } },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { requiresAuth: true } },
  { path: '/plantes', name: 'Plantes', component: () => import('../views/PlantesManagement.vue'), meta: { requiresAuth: true } },
  { path: '/projets', name: 'Projets', component: () => import('../views/ProjetsManagement.vue'), meta: { requiresAuth: true } },
  { path: '/activites', name: 'Activites', component: () => import('../views/ActivitesManagement.vue'), meta: { requiresAuth: true } },
  { path: '/equipe', name: 'Equipe', component: () => import('../views/EquipeManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/partenaires', name: 'Partenaires', component: () => import('../views/PartenairesManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/slides', name: 'Slides', component: () => import('../views/SlidesManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/temoignages', name: 'Temoignages', component: () => import('../views/TemoignagesManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/publications', name: 'Publications', component: () => import('../views/PublicationsManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/statistiques', name: 'Statistiques', component: () => import('../views/StatsManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/herbier-data', name: 'HerbierData', component: () => import('../views/HerbierData.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/settings', name: 'Settings', component: () => import('../views/Settings.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/users', name: 'Users', component: () => import('../views/UsersManagement.vue'), meta: { requiresAuth: true, adminOnly: true } }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach(async (to, from) => {
  const token = localStorage.getItem('access_token')
  const hasToken = !!token
  const requiresAuth = to.meta.requiresAuth
  const adminOnly = to.meta.adminOnly
  
  if (requiresAuth && !hasToken) return '/login'
  if ((to.path === '/login' || to.path === '/register' || to.path === '/forgot-password' || to.path === '/verify-2fa') && hasToken) return '/dashboard'
  
  if (hasToken && adminOnly) {
    try {
      const authStore = useAuthStore()
      if (!authStore.user) await authStore.fetchUser()
      if (!authStore.user?.is_superuser) return '/dashboard'
    } catch { return '/login' }
  }
  
  return true
})

export default router
