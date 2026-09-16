<template>
  <div class="maintenance-layout superit-theme">
    <Sidebar
      :user="auth.user"
      :is-super-it="true"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Maintenance"
        subtitle="Backup, export et outils système"
        icon="fas fa-tools"
      />

      <div class="maintenance-grid">
        <!-- Backup -->
        <section class="tool-card">
          <div class="tool-icon green"><i class="fas fa-download"></i></div>
          <h3>Sauvegarder les données</h3>
          <p>Export complet de toutes les données de l'herbier au format JSON.</p>
          <button class="btn btn-primary" @click="backupAll" :disabled="working">
            <i v-if="working" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-download"></i>
            Télécharger le backup
          </button>
        </section>

        <!-- Restauration -->
        <section class="tool-card">
          <div class="tool-icon orange"><i class="fas fa-upload"></i></div>
          <h3>Restaurer une sauvegarde</h3>
          <p>Importer un fichier JSON pour restaurer les données.</p>
          <input
            type="file"
            ref="fileInput"
            accept=".json"
            @change="restoreBackup"
            hidden
          />
          <button class="btn btn-secondary" @click="$refs.fileInput.click()" :disabled="working">
            <i class="fas fa-upload"></i>
            Choisir un fichier
          </button>
        </section>

        <!-- Export admins CSV -->
        <section class="tool-card">
          <div class="tool-icon blue"><i class="fas fa-file-csv"></i></div>
          <h3>Exporter les administrateurs</h3>
          <p>Télécharger la liste des administrateurs au format CSV.</p>
          <button class="btn btn-secondary" @click="exportAdminsCSV">
            <i class="fas fa-file-csv"></i>
            Exporter en CSV
          </button>
        </section>

        <!-- Export audit CSV -->
        <section class="tool-card">
          <div class="tool-icon purple"><i class="fas fa-history"></i></div>
          <h3>Exporter le journal d'audit</h3>
          <p>Exporter les 1000 dernières actions au format CSV.</p>
          <button class="btn btn-secondary" @click="exportAuditCSV">
            <i class="fas fa-history"></i>
            Exporter l'audit
          </button>
        </section>

        <!-- Vider le cache -->
        <section class="tool-card">
          <div class="tool-icon red"><i class="fas fa-broom"></i></div>
          <h3>Vider les tokens expirés</h3>
          <p>Nettoyer les tokens et OTP expirés en base.</p>
          <button class="btn btn-danger" @click="cleanup" :disabled="working">
            <i class="fas fa-broom"></i>
            Nettoyer
          </button>
        </section>

        <!-- Statistiques serveur -->
        <section class="tool-card">
          <div class="tool-icon indigo"><i class="fas fa-server"></i></div>
          <h3>Informations serveur</h3>
          <p>Vérifier l'état du serveur et des services.</p>
          <button class="btn btn-secondary" @click="checkServer">
            <i class="fas fa-server"></i>
            Vérifier
          </button>
        </section>
      </div>
    </main>

    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { adminApi, adminAPI, authAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const confirm = useConfirm()

const sidebarCollapsed = ref(false)
const working = ref(false)
const fileInput = ref(null)

const backupAll = async () => {
  working.value = true
  try {
    const [plantes, projets, activites, publications, equipe, partenaires] =
      await Promise.all([
        adminApi.get('/plantes/'),
        adminApi.get('/projets/'),
        adminApi.get('/activites/'),
        adminApi.get('/publications/'),
        adminApi.get('/equipe/'),
        adminApi.get('/partenaires/'),
      ])

    const data = {
      exported_at: new Date().toISOString(),
      version: '1.0',
      plantes: plantes.data,
      projets: projets.data,
      activites: activites.data,
      publications: publications.data,
      equipe: equipe.data,
      partenaires: partenaires.data,
    }

    downloadJSON(data, `herbier-backup-${new Date().toISOString().slice(0, 10)}.json`)
    toast.success('Backup téléchargé')
  } catch {
    toast.error('Erreur lors du backup')
  } finally {
    working.value = false
  }
}

const restoreBackup = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  const ok = await confirm({
    title: 'Restaurer',
    message:
      'Cette opération va remplacer les données actuelles. Continuer ?',
    dangerous: true,
    confirmText: 'Restaurer',
  })
  if (!ok) {
    event.target.value = ''
    return
  }

  working.value = true
  try {
    const text = await file.text()
    const data = JSON.parse(text)

    // Exemple : envoyer chaque section à l'API
    const sections = ['plantes', 'projets', 'activites', 'publications', 'equipe', 'partenaires']
    for (const section of sections) {
      if (Array.isArray(data[section])) {
        for (const item of data[section]) {
          try {
            await adminApi.post(`/${section}/`, item)
          } catch {
            // Ignorer les erreurs individuelles
          }
        }
      }
    }

    toast.success('Restauration terminée')
  } catch {
    toast.error('Fichier invalide')
  } finally {
    working.value = false
    event.target.value = ''
  }
}

const exportAdminsCSV = async () => {
  try {
    const { data } = await adminAPI.getUsers()
    const rows = [
      ['ID', 'Nom', 'Email', 'Téléphone', 'Rôle', 'Statut', 'Créé le', 'Dernière connexion'],
      ...data.map((u) => [
        u.id,
        u.nom,
        u.email,
        u.telephone || '',
        u.role === 'it_admin' ? 'SuperIT' : 'Admin',
        u.is_active ? 'Actif' : 'Inactif',
        u.date_joined ? new Date(u.date_joined).toLocaleString('fr-FR') : '',
        u.last_login ? new Date(u.last_login).toLocaleString('fr-FR') : 'Jamais',
      ]),
    ]
    downloadCSV(rows, `admins-${new Date().toISOString().slice(0, 10)}.csv`)
    toast.success('CSV des admins téléchargé')
  } catch {
    toast.error('Erreur lors de l\'export')
  }
}

const exportAuditCSV = async () => {
  try {
    const { data } = await authAPI.getAuditLogs({ limit: 1000 })
    const rows = [
      ['Date', 'Utilisateur', 'Email', 'Action', 'Modèle', 'Objet', 'Détails', 'IP'],
      ...data.map((log) => [
        log.created_at ? new Date(log.created_at).toLocaleString('fr-FR') : '',
        log.user_nom || 'Système',
        log.user_email || '',
        log.action_label || log.action,
        log.model_name || '',
        log.object_repr || '',
        log.details ? JSON.stringify(log.details).slice(0, 200) : '',
        log.ip_address || '',
      ]),
    ]
    downloadCSV(rows, `audit-${new Date().toISOString().slice(0, 10)}.csv`)
    toast.success('CSV de l\'audit téléchargé')
  } catch {
    toast.error('Erreur lors de l\'export')
  }
}

const cleanup = async () => {
  const ok = await confirm({
    title: 'Nettoyer',
    message: 'Supprimer les tokens et OTP expirés ?',
  })
  if (!ok) return

  working.value = true
  try {
    // Appel à un endpoint de nettoyage (à créer côté backend)
    await adminApi.post('/cleanup/', {})
    toast.success('Nettoyage effectué')
  } catch (err) {
    // Fallback : afficher le message d'erreur
    toast.warning('Endpoint /cleanup/ à implémenter côté backend')
  } finally {
    working.value = false
  }
}

const checkServer = async () => {
  try {
    const { data } = await adminApi.get('/')
    toast.success(`Serveur OK — ${data.message || 'API opérationnelle'}`)
  } catch {
    toast.error('Serveur inaccessible')
  }
}

// ============================================
// HELPERS
// ============================================
const downloadJSON = (data, filename) => {
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: 'application/json',
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

const downloadCSV = (rows, filename) => {
  const csvContent = rows
    .map((row) =>
      row
        .map((cell) => {
          const str = String(cell ?? '')
          return str.includes(',') || str.includes('"') || str.includes('\n')
            ? `"${str.replace(/"/g, '""')}"`
            : str
        })
        .join(',')
    )
    .join('\n')

  const blob = new Blob(['\ufeff' + csvContent], {
    type: 'text/csv;charset=utf-8',
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

const handleLogout = async () => {
  await auth.logout()
  router.push('/it-login')
}

onMounted(() => {
  if (!auth.isSuperIT) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
.maintenance-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  font-family: 'Inter', system-ui, sans-serif;
}
.main-content {
  margin-left: 260px;
  padding: 24px 28px 40px;
  transition: margin-left 0.3s ease;
}
.main-content.expanded { margin-left: 76px; }

.maintenance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 18px;
}

.tool-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 24px;
  transition: all 0.15s;
}
.tool-card:hover {
  border-color: rgba(129, 140, 248, 0.4);
  transform: translateY(-3px);
  box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.3);
}

.tool-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 16px;
}
.tool-icon.green { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.tool-icon.orange { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.tool-icon.blue { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.tool-icon.purple { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }
.tool-icon.red { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.tool-icon.indigo { background: rgba(99, 102, 241, 0.15); color: #818cf8; }

.tool-card h3 {
  font-size: 15px;
  color: #fff;
  margin: 0 0 8px;
  font-weight: 700;
}
.tool-card p {
  font-size: 13px;
  color: #94a3b8;
  margin: 0 0 16px;
  line-height: 1.5;
  min-height: 40px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 9px;
  font-size: 13.5px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s;
  width: 100%;
  justify-content: center;
}
.btn-primary {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  box-shadow: 0 4px 12px -4px rgba(16, 185, 129, 0.5);
}
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary {
  background: rgba(99, 102, 241, 0.1);
  border: 1.5px solid rgba(99, 102, 241, 0.3);
  color: #c7d2fe;
}
.btn-secondary:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.2);
  border-color: #818cf8;
}
.btn-secondary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-danger {
  background: rgba(239, 68, 68, 0.15);
  border: 1.5px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}
.btn-danger:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.25);
  border-color: #ef4444;
}
.btn-danger:disabled { opacity: 0.6; cursor: not-allowed; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .maintenance-grid { grid-template-columns: 1fr; }
}
</style>