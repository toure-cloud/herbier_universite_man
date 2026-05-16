import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  { path: '/verify-2fa', name: 'Verify2FA', component: () => import('../views/Verify2FA.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/herbier-data', name: 'HerbierData', component: () => import('../views/HerbierData.vue') },
  { path: '/settings', name: 'Settings', component: () => import('../views/Settings.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
