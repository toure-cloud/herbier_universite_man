import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { 
    path: '/login', 
    name: 'Login', 
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
  { 
    path: '/verify-2fa', 
    name: 'Verify2FA', 
    component: () => import('../views/Verify2FA.vue'),
    meta: { requiresAuth: false }
  },
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/herbier-data', 
    name: 'HerbierData', 
    component: () => import('../views/HerbierData.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/settings', 
    name: 'Settings', 
    component: () => import('../views/Settings.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/', 
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard - protection des routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const requiresAuth = to.meta.requiresAuth
  
  if (requiresAuth && !token) {
    // Non authentifié, rediriger vers login
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    // Déjà authentifié, rediriger vers dashboard
    next('/dashboard')
  } else {
    next()
  }
})

export default router
