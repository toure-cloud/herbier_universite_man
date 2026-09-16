// src/utils/api.js
import axios from 'axios';

const RAW_ADMIN_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8001/api';
const ADMIN_API_URL = RAW_ADMIN_URL.replace(/\/+$/, '').endsWith('/api')
  ? RAW_ADMIN_URL.replace(/\/+$/, '')
  : `${RAW_ADMIN_URL.replace(/\/+$/, '')}/api`;

const RAW_PUBLIC_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const PUBLIC_API_URL = RAW_PUBLIC_URL.replace(/\/+$/, '').endsWith('/api')
  ? RAW_PUBLIC_URL.replace(/\/+$/, '')
  : `${RAW_PUBLIC_URL.replace(/\/+$/, '')}/api`;

// ---------- Admin API ----------
const adminApi = axios.create({
  baseURL: ADMIN_API_URL,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
  withCredentials: false,
  timeout: 90000,
});

adminApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  if (config.data instanceof FormData) delete config.headers['Content-Type'];
  return config;
});

adminApi.interceptors.response.use(
  (res) => res,
  (error) => {
    const status = error.response?.status;
    if (status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/it-login';
      }
    }
    return Promise.reject(error);
  }
);

// ---------- Public API ----------
const publicApi = axios.create({
  baseURL: PUBLIC_API_URL,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
  withCredentials: false,
  timeout: 30000,
});

// ---------- Auth API ----------
export const authAPI = {
  // Login séparé
  itLogin: (data) => adminApi.post('/it/login/', data),
  adminLogin: (data) => adminApi.post('/admin/login/', data),
  // 2FA
  verify2FA: (data) => adminApi.post('/verify-2fa/', data),
  resendCode: (data) => adminApi.post('/resend-code/', data),
  logout: () => adminApi.post('/logout/'),
  me: () => adminApi.get('/me/'),
  // Password reset
  forgotPassword: (data) => adminApi.post('/forgot-password/', data),
  verifyResetCode: (data) => adminApi.post('/verify-reset-code/', data),
  resetPassword: (data) => adminApi.post('/reset-password/', data),
  // Audit
  getAuditLogs: (params) => adminApi.get('/audit/logs/', { params }),
};

// ---------- Admin API (CRUD Users) ----------
export const adminAPI = {
  getUsers: () => adminApi.get('/users/'),
  createUser: (data) => adminApi.post('/users/create/', data),
  updateUser: (id, data) => adminApi.patch(`/users/${id}/`, data),
  deleteUser: (id) => adminApi.delete(`/users/${id}/delete/`),
  toggleUserStatus: (id, data) => adminApi.patch(`/users/${id}/`, data),
  getStats: () => adminApi.get('/stats/'),
  syncAll: () => adminApi.post('/sync-all/', {}),
};

// ---------- CRUD génériques ----------
const makeCrud = (endpoint) => ({
  list: (params) => adminApi.get(`/${endpoint}/`, { params }),
  get: (id) => adminApi.get(`/${endpoint}/${id}/`),
  create: (data) => adminApi.post(`/${endpoint}/`, data),
  update: (id, data) => adminApi.put(`/${endpoint}/${id}/`, data),
  patch: (id, data) => adminApi.patch(`/${endpoint}/${id}/`, data),
  remove: (id) => adminApi.delete(`/${endpoint}/${id}/`),
});

export const plantesAPI = makeCrud('plantes');
export const equipeAPI = makeCrud('equipe');
export const slidesAPI = makeCrud('slides');
export const projetsAPI = makeCrud('projets');
export const activitesAPI = makeCrud('activites');
export const partenairesAPI = makeCrud('partenaires');
export const temoignagesAPI = makeCrud('temoignages');
export const publicationsAPI = makeCrud('publications');
export const faqsAPI = makeCrud('faqs');
export const statistiquesAPI = makeCrud('statistiques');
export const methodologieAPI = makeCrud('methodologie');

export { adminApi, publicApi, ADMIN_API_URL, PUBLIC_API_URL };
export default adminApi;