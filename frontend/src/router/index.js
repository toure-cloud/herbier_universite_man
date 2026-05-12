import { createRouter, createWebHistory } from 'vue-router'
import Accueil from '../components/Accueil.vue'
import Activites from '../components/Activites.vue'
import Projets from '../components/Projets.vue'
import Contact from '../components/Contact.vue'
import Herbier from '../components/Herbier.vue'

const routes = [
    { path: '/', name: 'Accueil', component: Accueil },
    { path: '/activites', name: 'Activites', component: Activites },
    { path: '/projets', name: 'Projets', component: Projets },
    { path: '/contact', name: 'Contact', component: Contact },
    { path: '/herbier', name: 'Herbier', component: Herbier }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
