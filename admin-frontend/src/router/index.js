// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  // ---------- REDIRECTION PAR DÉFAUT ----------
  { path: '/', redirect: '/it-login' },

  // ---------- AUTHENTIFICATION ----------
  { path: '/it-login', name: 'ITLogin', component: () => import('../views/ITLogin.vue'), meta: { guest: true, role: 'it_admin' } },
  { path: '/admin-login', name: 'AdminLogin', component: () => import('../views/AdminLogin.vue'), meta: { guest: true, role: 'admin' } },
  { path: '/verify-2fa', name: 'Verify2FA', component: () => import('../views/Verify2FA.vue'), meta: { guest: true } },
  { path: '/forgot-password', name: 'ForgotPassword', component: () => import('../views/ForgotPassword.vue'), meta: { guest: true } },

  // ---------- DASHBOARD ----------
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { requiresAuth: true } },

  // ---------- CONTENU : Admin + SuperIT ----------
  { path: '/plantes', name: 'Plantes', component: () => import('../views/PlantesManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin', 'admin'] } },
  { path: '/projets', name: 'Projets', component: () => import('../views/ProjetsManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin', 'admin'] } },
  { path: '/activites', name: 'Activites', component: () => import('../views/ActivitesManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin', 'admin'] } },
  { path: '/publications', name: 'Publications', component: () => import('../views/PublicationsManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin', 'admin'] } },

  // ---------- TÉMOIGNAGES : lecture seule pour Admin ----------
  { path: '/temoignages', name: 'Temoignages', component: () => import('../views/TemoignagesManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin', 'admin'] } },

  // ---------- SUPERIT UNIQUEMENT ----------
  { path: '/equipe', name: 'Equipe', component: () => import('../views/EquipeManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/partenaires', name: 'Partenaires', component: () => import('../views/PartenairesManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/settings', name: 'Settings', component: () => import('../views/Settings.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/administrateurs', name: 'AdminUsers', component: () => import('../views/AdminUsersManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/audit', name: 'AuditLogs', component: () => import('../views/AuditLogs.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/maintenance', name: 'Maintenance', component: () => import('../views/Maintenance.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/herbier-data', name: 'HerbierData', component: () => import('../views/HerbierData.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },
  { path: '/stats', name: 'Stats', component: () => import('../views/StatsManagement.vue'), meta: { requiresAuth: true, roles: ['it_admin'] } },

  // ---------- 404 ----------
  { path: '/:pathMatch(.*)*', redirect: '/it-login' },
  { path: '/messages', name: 'ContactMessages',
  component: () => import('../views/ContactMessages.vue'),
  meta: { requiresAuth: true, roles: ['it_admin'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})


// ============================================
// GUARDS DE SÉCURITÉ
// ============================================
router.beforeEach(async (to, from) => {
  const auth = useAuthStore()

  if (!auth.initialized) {
    await auth.fetchUser()
  }

  // Route publique
  if (to.meta.guest) {
    if (auth.isAuthenticated && to.name !== 'Verify2FA') {
      return { path: '/dashboard' }
    }
    return true
  }

  // Route protégée
  if (to.meta.requiresAuth) {
    if (!auth.isAuthenticated) {
      const expectedRole = to.meta.roles?.[0]
      const loginPath = expectedRole === 'admin' ? '/admin-login' : '/it-login'
      return { path: loginPath, query: { redirect: to.fullPath } }
    }

    // ✅ Vérification stricte du rôle
    if (to.meta.roles && !to.meta.roles.includes(auth.user?.role)) {
      // Redirection sécurisée : un Admin ne peut pas accéder aux pages SuperIT
      return { path: '/dashboard' }
    }
  }

  return true
})

export default router
