import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://herbier-admin-backend.onrender.com',
        changeOrigin: true,
        secure: false
      }
    }
  },
  // ✅ Important pour les variables d'environnement
  define: {
    'import.meta.env.VITE_ADMIN_API_URL': JSON.stringify(process.env.VITE_ADMIN_API_URL),
    'import.meta.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL)
  }
})
