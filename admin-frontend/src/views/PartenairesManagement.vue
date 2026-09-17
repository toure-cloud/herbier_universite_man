<template>
  <div class="partenaires-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Partenaires"
        :subtitle="auth.isSuperIT
          ? 'Gérez les partenaires de l\'herbier'
          : 'Consultation des partenaires'"
        icon="fas fa-handshake"
        :show-refresh="true"
        :loading="loading"
        @refresh="loadPartenaires"
      />

      <!-- ✅ Bandeau lecture seule pour l'Admin -->
      <div v-if="!auth.isSuperIT" class="readonly-banner">
        <i class="fas fa-lock"></i>
        <div>
          <strong>Mode lecture seule</strong>
          <p>
            La gestion des partenaires est réservée au <strong>Super Administrateur IT</strong>.
          </p>
        </div>
      </div>

      <header class="page-header">
        <div class="header-left">
          <h1><i class="fas fa-handshake"></i> Partenaires</h1>
          <span class="count-badge">{{ partenaires.length }} partenaire(s)</span>
        </div>
        <button
          v-if="auth.isSuperIT"
          class="btn-create it"
          @click="openCreate"
        >
          <i class="fas fa-plus"></i> Ajouter un partenaire
        </button>
      </header>

      <div v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement des partenaires…</p>
      </div>

      <div v-else-if="!partenaires.length" class="empty-block">
        <i class="fas fa-handshake-slash"></i>
        <p>Aucun partenaire pour le moment.</p>
      </div>

      <section v-else class="partenaires-grid">
        <article
          v-for="p in partenaires"
          :key="p.id"
          class="partenaire-card"
          :class="{ inactive: !p.actif }"
        >
          <div class="partenaire-logo">
            <img v-if="p.logo" :src="p.logo" :alt="p.nom" @error="onImageError" />
            <i v-else class="fas fa-building"></i>
          </div>

          <div class="partenaire-body">
            <h3>{{ p.nom }}</h3>
            <p v-if="p.type" class="partenaire-type">{{ p.type }}</p>
            <p v-if="p.description" class="partenaire-desc">{{ p.description }}</p>

            <a
              v-if="p.site_web"
              :href="p.site_web"
              target="_blank"
              rel="noopener"
              class="partenaire-link"
            >
              <i class="fas fa-external-link-alt"></i> Site web
            </a>

            <span class="status-badge" :class="p.actif ? 'active' : 'inactive'">
              {{ p.actif ? 'Actif' : 'Inactif' }}
            </span>
          </div>

          <div v-if="auth.isSuperIT" class="partenaire-actions">
            <button class="btn-icon edit" @click="openEdit(p)" title="Modifier">
              <i class="fas fa-pen"></i>
            </button>
            <button class="btn-icon delete" @click="confirmDelete(p)" title="Supprimer">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <!-- Modale (mêmes pattern que Equipe, adapté) -->
    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal">
        <header class="modal-head">
          <h2>
            <i :class="editing ? 'fas fa-pen' : 'fas fa-plus'"></i>
            {{ editing ? 'Modifier un partenaire' : 'Ajouter un partenaire' }}
          </h2>
          <button class="btn-close" @click="closeModal"><i class="fas fa-times"></i></button>
        </header>

        <form class="modal-body" @submit.prevent="savePartenaire">
          <div class="form-grid">
            <label class="field">
              <span>Nom *</span>
              <input v-model="form.nom" type="text" required />
            </label>

            <label class="field">
              <span>Type</span>
              <input v-model="form.type" type="text" placeholder="Ex : ONG, Université" />
            </label>

            <label class="field full">
              <span>Site web</span>
              <input v-model="form.site_web" type="url" placeholder="https://…" />
            </label>

            <label class="field full">
              <span>Description</span>
              <textarea v-model="form.description" rows="3"></textarea>
            </label>

            <label class="field">
              <span>Ordre d'affichage</span>
              <input v-model.number="form.ordre" type="number" min="0" />
            </label>

            <label class="field checkbox">
              <input v-model="form.actif" type="checkbox" />
              <span>Actif</span>
            </label>

            <label class="field full">
              <span>Logo</span>
              <input type="file" accept="image/*" @change="onFileChange" />
              <small v-if="form.logoFile">Fichier : {{ form.logoFile.name }}</small>
              <small v-else-if="editing && editing.logo">
                Logo actuel : <em>conservé si aucun nouveau n'est choisi</em>
              </small>
            </label>
          </div>

          <footer class="modal-foot">
            <button type="button" class="btn btn-ghost" @click="closeModal">Annuler</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <i v-if="saving" class="fas fa-spinner fa-spin"></i>
              {{ saving ? 'Enregistrement…' : (editing ? 'Mettre à jour' : 'Créer') }}
            </button>
          </footer>
        </form>
      </div>
    </div>

    <div v-if="deleting" class="modal-backdrop" @click.self="cancelDelete">
      <div class="modal small">
        <header class="modal-head">
          <h2><i class="fas fa-exclamation-triangle"></i> Confirmer la suppression</h2>
        </header>
        <div class="modal-body">
          <p>Voulez-vous vraiment supprimer <strong>{{ deleting.nom }}</strong> ?</p>
          <p class="hint">Cette action est irréversible.</p>
        </div>
        <footer class="modal-foot">
          <button class="btn btn-ghost" @click="cancelDelete">Annuler</button>
          <button class="btn btn-danger" :disabled="saving" @click="doDelete">
            <i v-if="saving" class="fas fa-spinner fa-spin"></i> Supprimer
          </button>
        </footer>
      </div>
    </div>

    <Toast />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { partenairesAPI } from '../utils/api'
import { logger } from '../utils/logger'

const auth = useAuthStore()
const router = useRouter()
const toast = useToast()

const sidebarCollapsed = ref(false)
const loading = ref(false)
const saving = ref(false)

const partenaires = ref([])
const showModal = ref(false)
const editing = ref(null)
const deleting = ref(null)

const form = reactive({
  nom: '', type: '', site_web: '', description: '',
  ordre: 0, actif: true, logoFile: null,
})

const loadPartenaires = async () => {
  loading.value = true
  try {
    const { data } = await partenairesAPI.getAll()
    partenaires.value = Array.isArray(data) ? data : (data.results || [])
  } catch {
    logger.warn('Erreur chargement partenaires')
    toast.error('Impossible de charger les partenaires')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  if (!auth.isSuperIT) return
  editing.value = null
  Object.assign(form, { nom: '', type: '', site_web: '', description: '', ordre: 0, actif: true, logoFile: null })
  showModal.value = true
}

const openEdit = (p) => {
  if (!auth.isSuperIT) return
  editing.value = p
  Object.assign(form, {
    nom: p.nom ?? '', type: p.type ?? '', site_web: p.site_web ?? '',
    description: p.description ?? '', ordre: p.ordre ?? 0,
    actif: p.actif ?? true, logoFile: null,
  })
  showModal.value = true
}

const closeModal = () => { showModal.value = false; editing.value = null }

const onFileChange = (e) => { form.logoFile = e.target.files?.[0] || null }
const onImageError = (e) => { e.target.style.display = 'none' }

const savePartenaire = async () => {
  if (!auth.isSuperIT) return
  saving.value = true
  try {
    const payload = {
      nom: form.nom, type: form.type || '', site_web: form.site_web || '',
      description: form.description || '', ordre: form.ordre ?? 0, actif: form.actif,
    }
    if (form.logoFile) payload.logo = form.logoFile

    if (editing.value) {
      await partenairesAPI.update(editing.value.id, payload)
      toast.success('Partenaire mis à jour')
    } else {
      await partenairesAPI.create(payload)
      toast.success('Partenaire ajouté')
    }
    closeModal()
    await loadPartenaires()
  } catch {
    logger.warn('Erreur sauvegarde partenaire')
    toast.error('Erreur lors de l\'enregistrement')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (p) => { if (!auth.isSuperIT) return; deleting.value = p }
const cancelDelete = () => { deleting.value = null }

const doDelete = async () => {
  if (!auth.isSuperIT || !deleting.value) return
  saving.value = true
  try {
    await partenairesAPI.delete(deleting.value.id)
    toast.success('Partenaire supprimé')
    cancelDelete()
    await loadPartenaires()
  } catch {
    logger.warn('Erreur suppression partenaire')
    toast.error('Impossible de supprimer ce partenaire')
  } finally {
    saving.value = false
  }
}

const handleLogout = async () => {
  await auth.logout()
  router.push(auth.isSuperIT ? '/it-login' : '/admin-login')
}

onMounted(() => {
  if (!auth.isAuthenticated) { router.push('/it-login'); return }
  loadPartenaires()
})
</script>

<style scoped>
/* Reprendre exactement les mêmes styles que EquipeManagement.vue,
   en remplaçant .equipe-grid → .partenaires-grid,
   .membre-* → .partenaire-*,
   .membre-photo → .partenaire-logo
*/
.partenaires-layout { min-height: 100vh; background: #f1f5f9; }
.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; }
.main-content.expanded { margin-left: 76px; }

.readonly-banner {
  display: flex; gap: 14px; align-items: flex-start;
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  border-left: 4px solid #f59e0b;
  border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;
  color: #78350f;
}
.readonly-banner i { font-size: 22px; color: #d97706; flex-shrink: 0; margin-top: 2px; }
.readonly-banner strong { font-size: 14px; }
.readonly-banner p { margin: 4px 0 0; font-size: 13px; }

.page-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px;
}
.header-left { display: flex; align-items: baseline; gap: 12px; }
.page-header h1 {
  font-size: 22px; color: #0f172a; margin: 0; font-weight: 700;
  display: flex; align-items: center; gap: 10px;
}
.superit-theme .page-header h1 { color: #e2e8f0; }
.count-badge {
  background: #e2e8f0; color: #475569;
  padding: 4px 10px; border-radius: 12px;
  font-size: 12px; font-weight: 600;
}
.btn-create {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px; border-radius: 10px; border: none;
  background: #10b981; color: #fff; font-weight: 600; font-size: 14px;
  cursor: pointer; transition: all .15s;
}
.btn-create.it { background: #6366f1; }
.btn-create.it:hover { background: #4f46e5; transform: translateY(-1px); }

.partenaires-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.partenaire-card {
  position: relative;
  background: #fff; border-radius: 14px; padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  display: flex; gap: 16px;
  transition: all .15s;
}
.partenaire-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.superit-theme .partenaire-card {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  color: #e2e8f0;
}
.partenaire-card.inactive { opacity: .55; }

.partenaire-logo {
  width: 64px; height: 64px; flex-shrink: 0;
  border-radius: 12px; overflow: hidden;
  background: #f1f5f9; display: flex; align-items: center; justify-content: center;
}
.superit-theme .partenaire-logo { background: rgba(255,255,255,0.08); }
.partenaire-logo img { width: 100%; height: 100%; object-fit: contain; padding: 6px; }
.partenaire-logo i { font-size: 30px; color: #94a3b8; }

.partenaire-body { flex: 1; min-width: 0; }
.partenaire-body h3 { margin: 0 0 2px; font-size: 15.5px; color: #0f172a; }
.superit-theme .partenaire-body h3 { color: #fff; }
.partenaire-type { margin: 0 0 8px; font-size: 12px; color: #6366f1; font-weight: 600; text-transform: uppercase; }
.partenaire-desc { margin: 0 0 8px; font-size: 13px; color: #64748b; line-height: 1.4; }
.superit-theme .partenaire-desc { color: #94a3b8; }
.partenaire-link {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; color: #10b981; text-decoration: none; font-weight: 600;
  margin-bottom: 8px;
}
.partenaire-link:hover { text-decoration: underline; }

.status-badge {
  display: inline-block; padding: 2px 8px; border-radius: 8px;
  font-size: 11px; font-weight: 600;
}
.status-badge.active { background: rgba(16,185,129,0.15); color: #10b981; }
.status-badge.inactive { background: rgba(239,68,68,0.15); color: #ef4444; }

.partenaire-actions {
  position: absolute; top: 12px; right: 12px;
  display: flex; gap: 6px;
}
.btn-icon {
  width: 32px; height: 32px; border-radius: 8px; border: none;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all .15s;
}
.btn-icon.edit { background: #eef2ff; color: #6366f1; }
.btn-icon.edit:hover { background: #e0e7ff; }
.btn-icon.delete { background: #fee2e2; color: #ef4444; }
.btn-icon.delete:hover { background: #fecaca; }

.loading-block, .empty-block {
  background: #fff; border-radius: 14px; padding: 60px 20px; text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.superit-theme .loading-block, .superit-theme .empty-block {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
}
.spinner {
  width: 40px; height: 40px; margin: 0 auto 16px;
  border: 3px solid rgba(0,0,0,0.08); border-top-color: #10b981;
  border-radius: 50%; animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.empty-block i { font-size: 40px; color: #cbd5e1; margin-bottom: 12px; display: block; }
.empty-block p { color: #94a3b8; margin: 0; }

.modal-backdrop {
  position: fixed; inset: 0; background: rgba(15,23,42,0.7);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 20px;
}
.modal {
  background: #fff; border-radius: 16px;
  max-width: 620px; width: 100%; max-height: 90vh; overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.modal.small { max-width: 420px; }
.modal-head {
  padding: 18px 24px; border-bottom: 1px solid #e2e8f0;
  display: flex; justify-content: space-between; align-items: center;
}
.modal-head h2 {
  margin: 0; font-size: 16px; color: #0f172a;
  display: flex; align-items: center; gap: 10px; font-weight: 700;
}
.modal-head h2 i { color: #6366f1; }
.btn-close {
  background: none; border: none; cursor: pointer;
  width: 32px; height: 32px; border-radius: 8px; color: #64748b;
}
.btn-close:hover { background: #f1f5f9; }

.modal-body { padding: 24px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field.full { grid-column: 1 / -1; }
.field span { font-size: 12.5px; font-weight: 600; color: #475569; }
.field input, .field textarea {
  padding: 10px 12px; border-radius: 8px;
  border: 1px solid #cbd5e1; font-size: 14px; font-family: inherit;
}
.field input:focus, .field textarea:focus { outline: none; border-color: #6366f1; }
.field.checkbox { flex-direction: row; align-items: center; gap: 8px; }
.field small { color: #94a3b8; font-size: 11.5px; }

.modal-foot {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 16px 24px; border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}
.btn {
  padding: 10px 18px; border-radius: 8px; border: none;
  font-weight: 600; font-size: 14px; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px;
}
.btn-primary { background: #6366f1; color: #fff; }
.btn-primary:hover { background: #4f46e5; }
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }
.btn-ghost { background: transparent; color: #64748b; }
.btn-ghost:hover { background: #f1f5f9; }
.btn-danger { background: #ef4444; color: #fff; }
.btn-danger:hover { background: #dc2626; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-grid { grid-template-columns: 1fr; }
  .partenaires-grid { grid-template-columns: 1fr; }
}
</style>