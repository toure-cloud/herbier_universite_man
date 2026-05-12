<template>
    <div class="contact">
        <!-- Hero Section -->
        <section class="hero-contact">
            <div class="hero-bg"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="hero-badge" data-aos="fade-down">
                    <i class="fas fa-comments"></i>
                    <span>Contactez-nous</span>
                </div>
                <h1 class="hero-title" data-aos="fade-up">
                    Prenons contact<br>ensemble
                </h1>
                <p class="hero-subtitle" data-aos="fade-up" data-aos-delay="200">
                    Notre équipe est à votre écoute pour répondre à vos questions<br>
                    et collaborer sur vos projets
                </p>
            </div>
            <div class="hero-wave">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
                    <path fill="#ffffff" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
                </svg>
            </div>
        </section>

        <!-- Contact Info & Form -->
        <section class="contact-main">
            <div class="container">
                <div class="contact-grid">
                    <!-- Informations de contact -->
                    <div class="contact-info" data-aos="fade-right">
                        <div class="info-card">
                            <div class="info-icon">
                                <i class="fas fa-map-marker-alt"></i>
                            </div>
                            <h3>Notre adresse</h3>
                            <p>Université de Man<br>BP 20, Man<br>Côte d'Ivoire</p>
                            <div class="info-map">
                                <iframe 
                                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15840.427718373565!2d-7.558308!3d7.412513!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xfd88a864cb9b5b1%3A0x7c8a5b9f3c4d2e1a!2sMan%2C%20C%C3%B4te%20d&#39;Ivoire!5e0!3m2!1sfr!2sfr!4v1700000000000!5m2!1sfr!2sfr" 
                                    style="border:0;" 
                                    allowfullscreen="" 
                                    loading="lazy">
                                </iframe>
                            </div>
                        </div>

                        <div class="info-card">
                            <div class="info-icon">
                                <i class="fas fa-phone-alt"></i>
                            </div>
                            <h3>Nos contacts</h3>
                            <div class="contact-methods">
                                <div class="contact-method">
                                    <i class="fas fa-phone"></i>
                                    <div>
                                        <strong>Téléphone</strong>
                                        <p>+225 27 00 00 00</p>
                                    </div>
                                </div>
                                <div class="contact-method">
                                    <i class="fas fa-envelope"></i>
                                    <div>
                                        <strong>Email général</strong>
                                        <p>contact@herbier-man.ci</p>
                                    </div>
                                </div>
                                <div class="contact-method">
                                    <i class="fas fa-envelope-open-text"></i>
                                    <div>
                                        <strong>Recherche & Projets</strong>
                                        <p>recherche@herbier-man.ci</p>
                                    </div>
                                </div>
                                <div class="contact-method">
                                    <i class="fab fa-whatsapp"></i>
                                    <div>
                                        <strong>WhatsApp</strong>
                                        <p>+225 07 00 00 00</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="info-card">
                            <div class="info-icon">
                                <i class="fas fa-clock"></i>
                            </div>
                            <h3>Horaires d'ouverture</h3>
                            <div class="schedule">
                                <div class="schedule-item">
                                    <span>Lundi - Vendredi</span>
                                    <span>08:00 - 18:00</span>
                                </div>
                                <div class="schedule-item">
                                    <span>Samedi</span>
                                    <span>09:00 - 13:00</span>
                                </div>
                                <div class="schedule-item">
                                    <span>Dimanche</span>
                                    <span class="closed">Fermé</span>
                                </div>
                            </div>
                        </div>

                        <div class="info-card social-card">
                            <div class="info-icon">
                                <i class="fas fa-share-alt"></i>
                            </div>
                            <h3>Suivez-nous</h3>
                            <div class="social-links">
                                <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-youtube"></i></a>
                            </div>
                        </div>
                    </div>

                    <!-- Formulaire de contact -->
                    <div class="contact-form-wrapper" data-aos="fade-left">
                        <div class="form-header">
                            <h2>Envoyez-nous un message</h2>
                            <p>Remplissez le formulaire ci-dessous et nous vous répondrons dans les plus brefs délais.</p>
                        </div>
                        
                        <form @submit.prevent="submitForm" class="contact-form">
                            <div class="form-group">
                                <label>
                                    <i class="fas fa-user"></i>
                                    Nom complet *
                                </label>
                                <input 
                                    type="text" 
                                    v-model="form.nom" 
                                    required
                                    placeholder="Votre nom et prénom"
                                    :class="{ 'error': errors.nom }">
                                <span class="error-message" v-if="errors.nom">{{ errors.nom }}</span>
                            </div>

                            <div class="form-row">
                                <div class="form-group">
                                    <label>
                                        <i class="fas fa-envelope"></i>
                                        Email *
                                    </label>
                                    <input 
                                        type="email" 
                                        v-model="form.email" 
                                        required
                                        placeholder="votre@email.com"
                                        :class="{ 'error': errors.email }">
                                    <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
                                </div>

                                <div class="form-group">
                                    <label>
                                        <i class="fas fa-phone"></i>
                                        Téléphone
                                    </label>
                                    <input 
                                        type="tel" 
                                        v-model="form.telephone"
                                        placeholder="+225 XX XX XX XX">
                                </div>
                            </div>

                            <div class="form-group">
                                <label>
                                    <i class="fas fa-tag"></i>
                                    Sujet *
                                </label>
                                <select v-model="form.sujet" required>
                                    <option value="">Sélectionnez un sujet</option>
                                    <option value="information">Demande d'information</option>
                                    <option value="collaboration">Proposition de collaboration</option>
                                    <option value="projet">Soumission de projet</option>
                                    <option value="stage">Demande de stage</option>
                                    <option value="autre">Autre</option>
                                </select>
                            </div>

                            <div class="form-group">
                                <label>
                                    <i class="fas fa-comment"></i>
                                    Message *
                                </label>
                                <textarea 
                                    v-model="form.message" 
                                    required
                                    rows="6"
                                    placeholder="Décrivez votre demande en détail..."
                                    :class="{ 'error': errors.message }"></textarea>
                                <span class="error-message" v-if="errors.message">{{ errors.message }}</span>
                            </div>

                            <div class="form-group checkbox">
                                <label>
                                    <input type="checkbox" v-model="form.consentement" required>
                                    <span>J'accepte que mes données soient traitées pour répondre à ma demande *</span>
                                </label>
                            </div>

                            <button type="submit" class="btn-submit" :disabled="isSubmitting">
                                <span v-if="!isSubmitting">
                                    Envoyer le message
                                    <i class="fas fa-paper-plane"></i>
                                </span>
                                <span v-else>
                                    <i class="fas fa-spinner fa-pulse"></i>
                                    Envoi en cours...
                                </span>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section FAQ -->
        <section class="faq-section">
            <div class="container">
                <div class="section-header" data-aos="fade-up">
                    <span class="section-badge">FAQ</span>
                    <h2 class="section-title">Questions fréquentes</h2>
                    <p class="section-subtitle">Trouvez rapidement des réponses à vos questions</p>
                </div>

                <div class="faq-grid">
                    <div class="faq-item" v-for="(faq, index) in faqs" :key="index" data-aos="fade-up" :data-aos-delay="index * 100">
                        <div class="faq-question" @click="toggleFaq(index)">
                            <h3>{{ faq.question }}</h3>
                            <i :class="faq.open ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
                        </div>
                        <div class="faq-answer" :class="{ 'open': faq.open }">
                            <p>{{ faq.reponse }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-contact">
            <div class="container">
                <div class="cta-content" data-aos="zoom-in">
                    <div class="cta-icon">
                        <i class="fas fa-handshake"></i>
                    </div>
                    <h2>Vous souhaitez collaborer avec nous ?</h2>
                    <p>Rejoignez notre réseau de partenaires et contributeurs</p>
                    <div class="cta-buttons">
                        <a href="#" class="btn-primary" @click.prevent="downloadBrochure">
                            <i class="fas fa-download"></i>
                            Télécharger notre brochure
                        </a>
                        <router-link to="/activites" class="btn-outline">
                            Découvrir nos activités
                            <i class="fas fa-arrow-right"></i>
                        </router-link>
                    </div>
                </div>
            </div>
        </section>

        <!-- Toast Notification -->
        <div class="toast" :class="{ show: showToast }">
            <div class="toast-content">
                <i class="fas fa-check-circle"></i>
                <span>{{ toastMessage }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Contact',
    data() {
        return {
            form: {
                nom: '',
                email: '',
                telephone: '',
                sujet: '',
                message: '',
                consentement: false
            },
            errors: {
                nom: '',
                email: '',
                message: ''
            },
            isSubmitting: false,
            showToast: false,
            toastMessage: '',
            faqs: [
                {
                    question: "Comment puis-je proposer une collaboration ?",
                    reponse: "Vous pouvez nous contacter via le formulaire ci-dessus en sélectionnant 'Proposition de collaboration' dans le sujet. Notre équipe vous répondra sous 48h.",
                    open: false
                },
                {
                    question: "Proposez-vous des stages pour les étudiants ?",
                    reponse: "Oui, nous accueillons des stagiaires en botanique, écologie et sciences de l'environnement. Envoyez-nous votre CV et lettre de motivation.",
                    open: false
                },
                {
                    question: "Comment accéder à votre base de données botanique ?",
                    reponse: "Notre base de données est accessible sur demande pour les chercheurs et les institutions partenaires. Contactez notre équipe recherche.",
                    open: false
                },
                {
                    question: "Proposez-vous des formations sur mesure ?",
                    reponse: "Absolument ! Nous pouvons concevoir des programmes de formation adaptés à vos besoins spécifiques. Contactez-nous pour en discuter.",
                    open: false
                },
                {
                    question: "Quels sont les délais de réponse ?",
                    reponse: "Nous nous engageons à répondre à toutes les demandes sous 48 heures ouvrées.",
                    open: false
                }
            ]
        }
    },
    mounted() {
        this.initAnimations()
    },
    methods: {
        initAnimations() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1'
                        entry.target.style.transform = 'translateY(0)'
                    }
                })
            }, { threshold: 0.1 })
            
            document.querySelectorAll('[data-aos]').forEach(el => {
                el.style.opacity = '0'
                el.style.transform = 'translateY(30px)'
                el.style.transition = 'all 0.6s ease-out'
                observer.observe(el)
            })
        },
        validateForm() {
            let isValid = true
            
            if (!this.form.nom || this.form.nom.length < 2) {
                this.errors.nom = 'Veuillez entrer un nom valide (minimum 2 caractères)'
                isValid = false
            } else {
                this.errors.nom = ''
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            if (!this.form.email || !emailRegex.test(this.form.email)) {
                this.errors.email = 'Veuillez entrer une adresse email valide'
                isValid = false
            } else {
                this.errors.email = ''
            }
            
            if (!this.form.message || this.form.message.length < 10) {
                this.errors.message = 'Veuillez entrer un message d\'au moins 10 caractères'
                isValid = false
            } else {
                this.errors.message = ''
            }
            
            return isValid
        },
        async submitForm() {
            if (!this.validateForm()) {
                this.showNotification('Veuillez corriger les erreurs dans le formulaire', 'error')
                return
            }
            
            this.isSubmitting = true
            
            try {
                // Appel API réel - Décommentez pour utiliser l'API
                // const response = await axios.post('http://localhost:8001/api/submit-contact/', this.form)
                
                // Simulation d'envoi
                await new Promise(resolve => setTimeout(resolve, 1500))
                
                this.form = {
                    nom: '',
                    email: '',
                    telephone: '',
                    sujet: '',
                    message: '',
                    consentement: false
                }
                
                this.showNotification('Votre message a été envoyé avec succès ! Nous vous répondrons rapidement.', 'success')
            } catch (error) {
                this.showNotification('Une erreur est survenue. Veuillez réessayer plus tard.', 'error')
            } finally {
                this.isSubmitting = false
            }
        },
        showNotification(message, type) {
            this.toastMessage = message
            this.showToast = true
            setTimeout(() => {
                this.showToast = false
            }, 5000)
        },
        toggleFaq(index) {
            this.faqs[index].open = !this.faqs[index].open
        },
        downloadBrochure() {
            alert('Téléchargement de la brochure...')
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

.contact {
    overflow-x: hidden;
}

/* Hero Section */
.hero-contact {
    position: relative;
    min-height: 450px;
    background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 50%, #1a2a3a 100%);
    display: flex;
    align-items: center;
    text-align: center;
    color: white;
    padding: 80px 0 120px;
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.03)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,165.3C1248,149,1344,107,1392,85.3L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
    background-repeat: repeat-x;
    background-position: bottom;
    opacity: 0.5;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 50%, rgba(52,152,219,0.1), transparent);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.5rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 1.5rem;
}

.hero-badge i {
    font-size: 1rem;
    color: #3498db;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    line-height: 1.2;
    margin: 1rem 0;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    opacity: 0.9;
}

.hero-wave {
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    line-height: 0;
}

/* Container */
.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Contact Main */
.contact-main {
    padding: 80px 0;
    background: #f5f7fa;
}

.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 3rem;
}

/* Contact Info Cards */
.contact-info {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.info-card {
    background: white;
    border-radius: 20px;
    padding: 1.8rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.info-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 30px -12px rgba(0,0,0,0.1);
}

.info-icon {
    width: 50px;
    height: 50px;
    background: #eef2ff;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}

.info-icon i {
    font-size: 1.5rem;
    color: #3498db;
}

.info-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #1e293b;
    margin-bottom: 1rem;
}

.info-card p {
    font-family: 'Inter', sans-serif;
    color: #64748b;
    line-height: 1.6;
}

.info-map {
    margin-top: 1rem;
}

.info-map iframe {
    width: 100%;
    height: 180px;
    border-radius: 12px;
}

.contact-methods {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.contact-method {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e2e8f0;
}

.contact-method i {
    width: 35px;
    height: 35px;
    background: #eef2ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3498db;
}

.contact-method strong {
    display: block;
    font-size: 0.75rem;
    color: #94a3b8;
    margin-bottom: 0.2rem;
}

.contact-method p {
    font-size: 0.9rem;
    color: #1e293b;
    margin: 0;
}

.schedule {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.schedule-item {
    display: flex;
    justify-content: space-between;
    font-family: 'Inter', sans-serif;
    color: #475569;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #e2e8f0;
}

.schedule-item .closed {
    color: #e74c3c;
    font-weight: 500;
}

.social-card .social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.social-link {
    width: 40px;
    height: 40px;
    background: #f1f5f9;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #64748b;
    transition: all 0.3s ease;
}

.social-link:hover {
    background: #3498db;
    color: white;
    transform: translateY(-3px);
}

/* Form Styles */
.contact-form-wrapper {
    background: white;
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 20px 40px -12px rgba(0,0,0,0.08);
}

.form-header {
    text-align: center;
    margin-bottom: 2rem;
}

.form-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.form-header p {
    font-family: 'Inter', sans-serif;
    color: #64748b;
}

.contact-form .form-group {
    margin-bottom: 1.2rem;
}

.contact-form label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #334155;
    font-weight: 500;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}

.contact-form label i {
    color: #3498db;
}

.contact-form input,
.contact-form select,
.contact-form textarea {
    width: 100%;
    padding: 0.8rem 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s ease;
}

.contact-form input:focus,
.contact-form select:focus,
.contact-form textarea:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
}

.contact-form input.error,
.contact-form textarea.error {
    border-color: #e74c3c;
}

.error-message {
    display: block;
    color: #e74c3c;
    font-size: 0.7rem;
    margin-top: 0.3rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.checkbox label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.checkbox input {
    width: auto;
}

.btn-submit {
    width: 100%;
    padding: 1rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 50px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn-submit:hover:not(:disabled) {
    background: #2980b9;
    transform: translateY(-2px);
    gap: 0.8rem;
}

.btn-submit:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

/* FAQ Section */
.faq-section {
    padding: 80px 0;
    background: white;
}

.section-header {
    text-align: center;
    margin-bottom: 3rem;
}

.section-badge {
    display: inline-block;
    background: #eef2ff;
    color: #3498db;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: 1px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    font-family: 'Inter', sans-serif;
    color: #64748b;
}

.faq-grid {
    max-width: 800px;
    margin: 0 auto;
}

.faq-item {
    background: #f8fafc;
    border-radius: 16px;
    margin-bottom: 1rem;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease;
}

.faq-item:hover {
    border-color: #cbd5e1;
}

.faq-question {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 1.5rem;
    cursor: pointer;
    transition: background 0.2s ease;
}

.faq-question:hover {
    background: #f1f5f9;
}

.faq-question h3 {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
}

.faq-question i {
    color: #3498db;
    transition: transform 0.2s ease;
}

.faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
    padding: 0 1.5rem;
}

.faq-answer.open {
    max-height: 200px;
    padding: 0 1.5rem 1.2rem;
}

.faq-answer p {
    font-family: 'Inter', sans-serif;
    color: #64748b;
    line-height: 1.6;
    margin: 0;
}

/* CTA Section */
.cta-contact {
    padding: 60px 0;
    background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 100%);
    color: white;
}

.cta-content {
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}

.cta-icon {
    width: 70px;
    height: 70px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
}

.cta-icon i {
    font-size: 2rem;
    color: #3498db;
}

.cta-content h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    margin-bottom: 1rem;
}

.cta-content p {
    font-family: 'Inter', sans-serif;
    margin-bottom: 2rem;
    opacity: 0.8;
}

.cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.cta-buttons .btn-primary {
    background: #3498db;
    color: white;
    padding: 0.8rem 1.8rem;
    border-radius: 50px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.cta-buttons .btn-primary:hover {
    background: #2980b9;
    transform: translateY(-2px);
    gap: 0.8rem;
}

.cta-buttons .btn-outline {
    background: transparent;
    color: white;
    border: 2px solid white;
    padding: 0.8rem 1.8rem;
    border-radius: 50px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.cta-buttons .btn-outline:hover {
    background: white;
    color: #1a2a3a;
    transform: translateY(-2px);
    gap: 0.8rem;
}

/* Toast Notification */
.toast {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: #27ae60;
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 50px;
    transform: translateX(400px);
    transition: transform 0.3s ease;
    z-index: 1000;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.toast.show {
    transform: translateX(0);
}

.toast-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Inter', sans-serif;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-subtitle {
        font-size: 0.9rem;
    }
    
    .contact-grid {
        grid-template-columns: 1fr;
    }
    
    .form-row {
        grid-template-columns: 1fr;
    }
    
    .cta-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .toast {
        left: 20px;
        right: 20px;
        transform: translateY(100px);
        text-align: center;
    }
    
    .toast.show {
        transform: translateY(0);
    }
    
    .section-title {
        font-size: 1.5rem;
    }
}

@media (min-width: 769px) and (max-width: 1024px) {
    .contact-grid {
        grid-template-columns: 1fr;
    }
}
</style>
