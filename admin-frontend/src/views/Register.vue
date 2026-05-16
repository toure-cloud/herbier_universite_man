<template>
  <div class="register">
    <h1>Créer un compte admin</h1>
    <form @submit.prevent="handleRegister">
      <input type="text" v-model="form.nom" placeholder="Nom complet" required>
      <input type="email" v-model="form.email" placeholder="Email" required>
      <input type="tel" v-model="form.telephone" placeholder="Téléphone" required>
      <input type="password" v-model="form.password" placeholder="Mot de passe" required>
      <input type="password" v-model="form.password2" placeholder="Confirmer" required>
      <button type="submit">Créer</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      form: {
        nom: '',
        email: '',
        telephone: '',
        password: '',
        password2: ''
      }
    }
  },
  methods: {
    handleRegister() {
      alert('Fonctionnalité à implémenter')
    }
  }
}
</script>
