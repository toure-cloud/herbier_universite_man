// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

import '@fortawesome/fontawesome-free/css/all.css'

import { logger } from './utils/logger'

const app = createApp(App)
const pinia = createPinia()

logger.log('Admin frontend démarré')

app.use(pinia)
app.use(router)
app.mount('#app')