<template>
  <div class="verify">
    <h1>Vérification 2FA</h1>
    <p>Entrez le code reçu par email</p>
    <input type="text" v-model="code" placeholder="Code à 6 chiffres" maxlength="6">
    <button @click="handleVerify">Vérifier</button>
  </div>
</template>

<script>
export default {
  name: 'Verify2FA',
  data() {
    return {
      code: ''
    }
  },
  methods: {
    handleVerify() {
      alert('Fonctionnalité à implémenter')
    }
  }
}
</script>
