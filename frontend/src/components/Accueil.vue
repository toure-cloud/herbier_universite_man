<template>
    <div class="accueil">
        <div class="hero">
            <div class="slideshow-container">
                <div class="slide fade" v-for="(slide, index) in slides" :key="index" v-show="currentSlide === index">
                    <img :src="getImageUrl(slide.image)" :alt="slide.titre">
                    <div class="text-overlay">
                        <h3>{{ slide.titre }}</h3>
                        <p>{{ slide.texte_botanique }}</p>
                    </div>
                </div>
                
                <button class="prev" @click="changeSlide(-1)">❮</button>
                <button class="next" @click="changeSlide(1)">❯</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Accueil',
    data() {
        return {
            slides: [],
            currentSlide: 0,
            slideInterval: null,
            apiUrl: import.meta.env.VITE_API_URL || 'https://herbier-universite-production.up.railway.app'
        }
    },
    mounted() {
        this.fetchSlides()
    },
    methods: {
        async fetchSlides() {
            try {
                const response = await axios.get(`${this.apiUrl}/api/slides/`)
                this.slides = response.data
                if (this.slides.length > 0) {
                    this.startSlideShow()
                }
            } catch (error) {
                console.error('Erreur chargement slides:', error)
                // Utiliser des slides par défaut
                this.slides = [
                    { titre: "Bienvenue", texte_botanique: "Herbier Université de Man", image: null }
                ]
            }
        },
        getImageUrl(imagePath) {
            if (!imagePath) return 'https://picsum.photos/id/104/1920/600'
            if (imagePath.startsWith('http')) return imagePath
            return `${this.apiUrl}${imagePath}`
        },
        startSlideShow() {
            this.slideInterval = setInterval(() => {
                this.currentSlide = (this.currentSlide + 1) % this.slides.length
            }, 5000)
        },
        stopSlideShow() {
            if (this.slideInterval) clearInterval(this.slideInterval)
        },
        changeSlide(direction) {
            this.currentSlide = (this.currentSlide + direction + this.slides.length) % this.slides.length
            this.stopSlideShow()
            this.startSlideShow()
        }
    },
    beforeUnmount() {
        this.stopSlideShow()
    }
}
</script>
