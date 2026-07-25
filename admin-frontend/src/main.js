import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

// Importer axios configuré
import './utils/axios'

// Font Awesome
import '@fortawesome/fontawesome-free/css/all.css'

const app = createApp(App)
const pinia = createPinia()
// Ajouter ceci pour debug
console.log('🔗 ADMIN_API_URL:', import.meta.env.VITE_ADMIN_API_URL)
console.log('🔗 API_URL:', import.meta.env.VITE_API_URL)

app.use(pinia)
app.use(router)
app.mount('#app')
