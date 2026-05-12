import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Accueil from './components/Accueil.vue'
import Herbier from './components/Herbier.vue'
import Activites from './components/Activites.vue'
import Projets from './components/Projets.vue'
import Contact from './components/Contact.vue'

const routes = [
    { path: '/', component: Accueil },
    { path: '/herbier', component: Herbier },
    { path: '/activites', component: Activites },
    { path: '/projets', component: Projets },
    { path: '/contact', component: Contact }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
