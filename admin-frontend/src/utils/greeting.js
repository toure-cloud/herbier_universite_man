// src/utils/greeting.js

/**
 * Retourne "Bonjour" ou "Bonsoir" selon l'heure.
 * - Bonjour : 00h00 à 12h00
 * - Bonsoir : 12h01 à 23h29
 * (23h30 à 23h59 : Bonsoir également par défaut)
 */
export function getGreeting() {
  const now = new Date()
  const hours = now.getHours()
  const minutes = now.getMinutes()

  // Total minutes depuis minuit
  const totalMinutes = hours * 60 + minutes

  const NOON_MINUTES = 12 * 60        // 12h00 = 720 min
  const EVENING_END = 23 * 60 + 29    // 23h29 = 1409 min

  if (totalMinutes <= NOON_MINUTES) {
    return 'Bonjour'
  }
  if (totalMinutes <= EVENING_END) {
    return 'Bonsoir'
  }
  // Entre 23h30 et 23h59, on garde Bonsoir par défaut
  return 'Bonsoir'
}

/**
 * Retourne la salutation complète avec le prénom
 */
export function getGreetingFor(user) {
  const firstName = (user?.nom || '').split(' ')[0] || ''
  const greeting = getGreeting()
  return `${greeting}, ${firstName}`.trim()
}
