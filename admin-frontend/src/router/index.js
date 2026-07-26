import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue'), meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue'), meta: { requiresAuth: false } },
  { path: '/forgot-password', name: 'ForgotPassword', component: () => import('../views/ForgotPassword.vue'), meta: { requiresAuth: false } },
  { path: '/verify-2fa', name: 'Verify2FA', component: () => import('../views/Verify2FA.vue'), meta: { requiresAuth: false } },
  { path: '/it-login', name: 'ITLogin', component: () => import('../views/ITLogin.vue'), meta: { requiresAuth: false } },
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
  { path: '/administrateurs', name: 'Administrateurs', component: () => import('../views/AdminUsersManagement.vue'), meta: { requiresAuth: true, adminOnly: true } },
  { path: '/users', name: 'Users', component: () => import('../views/UsersManagement.vue'), meta: { requiresAuth: true, adminOnly: true } }
]

const router = createRouter({ 
  history: createWebHistory(), 
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// ✅ Navigation Guard - CORRIGÉE ET AMÉLIORÉE
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token')
  const hasToken = !!token
  const requiresAuth = to.meta.requiresAuth
  const adminOnly = to.meta.adminOnly

  // ✅ Gestion de la page /it-login
  if (to.path === '/it-login') {
    const isItAuthenticated = localStorage.getItem('it_admin_authenticated')
    // Si déjà authentifié IT, vérifier le token
    if (isItAuthenticated === 'true') {
      if (!hasToken) {
        return next('/login')
      }
      return next('/administrateurs')
    }
    // Si non authentifié, laisser accéder à la page de login IT
    return next()
  }

  // ✅ Gestion de la page /administrateurs
  if (to.path === '/administrateurs') {
    const isItAuthenticated = localStorage.getItem('it_admin_authenticated')
    // Vérifier si l'utilisateur est authentifié IT
    if (isItAuthenticated !== 'true') {
      return next('/it-login')
    }
    // Vérifier si l'utilisateur a un token
    if (!hasToken) {
      return next('/login')
    }
    return next()
  }

  // ✅ Si la route nécessite une authentification et qu'il n'y a pas de token
  if (requiresAuth && !hasToken) {
    // Sauvegarder la route demandée pour redirection après login
    if (to.path !== '/login') {
      localStorage.setItem('redirect_after_login', to.fullPath)
    }
    return next('/login')
  }

  // ✅ Vérification des droits adminOnly
  if (hasToken && adminOnly) {
    try {
      const authStore = useAuthStore()
      if (!authStore.user) {
        await authStore.fetchUser()
      }
      const isSuperAdmin = authStore.user?.is_superuser || authStore.user?.role === 'it_admin'
      if (!isSuperAdmin) {
        console.warn('🚫 Accès refusé à', to.path, '- droits insuffisants')
        return next('/dashboard')
      }
    } catch (error) {
      console.error('❌ Erreur vérification droits:', error)
      // Si erreur (token expiré ou invalide), déconnecter
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      localStorage.removeItem('it_admin_authenticated')
      return next('/login')
    }
  }

  // ✅ Si l'utilisateur est connecté et essaie d'accéder aux pages d'auth
  const authPages = ['/login', '/register', '/forgot-password', '/verify-2fa']
  if (authPages.includes(to.path) && hasToken) {
    // Vérifier si l'utilisateur est IT Admin
    if (localStorage.getItem('it_admin_authenticated') === 'true') {
      return next('/administrateurs')
    }
    return next('/dashboard')
  }

  // ✅ Redirection depuis la racine
  if (to.path === '/' && hasToken) {
    return next('/dashboard')
  }

  return next()
})

export default router