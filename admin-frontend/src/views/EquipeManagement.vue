<template>
  <div class="equipe-layout" :class="{ 'superit-theme': auth.isSuperIT }">
    <Sidebar
      :user="auth.user"
      :is-super-it="auth.isSuperIT"
      :collapsed="sidebarCollapsed"
      @toggle="sidebarCollapsed = !sidebarCollapsed"
      @logout="handleLogout"
    />

    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopBar
        title="Équipe"
        :subtitle="auth.isSuperIT
          ? 'Gérez les membres de l\'équipe de l\'herbier'
          : 'Consultation des membres de l\'équipe'"
        icon="fas fa-users"
        :show-refresh="true"
        :loading="loading"
        @refresh="loadEquipe"
      >
        <template #actions>
          <button
            v-if="auth.isSuperIT"
            class="btn-create it"
            @click="openCreate"
          >
            <i class="fas fa-plus"></i> Nouveau membre
          </button>
        </template>
      </TopBar>

      <!-- ✅ Bandeau lecture seule pour l'Admin -->
      <div v-if="!auth.isSuperIT" class="readonly-banner">
        <i class="fas fa-lock"></i>
        <div>
          <strong>Mode lecture seule</strong>
          <p>
            La gestion de l'équipe est réservée au
            <strong>Super Administrateur IT</strong>.
            Vous pouvez consulter les membres, mais pas les modifier.
          </p>
        </div>
      </div>

      <!-- ✅ Filtres -->
      <section class="filters-bar">
        <div class="search-wrap">
          <i class="fas fa-search"></i>
          <input v-model.trim="search" type="text" placeholder="Rechercher un membre…" />
        </div>
        <div class="result-count">
          <i class="fas fa-users"></i> {{ filtered.length }} membre(s)
        </div>
      </section>

      <section v-if="loading" class="loading-block">
        <div class="spinner"></div>
        <p>Chargement…</p>
      </section>

      <section v-else-if="filtered.length === 0" class="empty-block">
        <i class="fas fa-users-slash"></i>
        <h3>Aucun membre</h3>
        <p v-if="auth.isSuperIT">Ajoutez votre premier membre d'équipe</p>
        <p v-else>L'équipe sera bientôt disponible.</p>
        <button
          v-if="auth.isSuperIT"
          class="btn-create it"
          @click="openCreate"
        >
          <i class="fas fa-plus"></i> Nouveau membre
        </button>
      </section>

      <section v-else class="equipe-grid">
        <article
          v-for="membre in filtered"
          :key="membre.id"
          class="membre-card"
          :class="{ inactive: !membre.actif }"
        >
          <div class="membre-photo">
            <img
              v-if="membre.photo"
              :src="membre.photo"
              :alt="membre.nom"
              @error="onImageError"
            />
            <i v-else class="fas fa-user-circle"></i>
          </div>

          <div class="membre-body">
            <h3>{{ membre.nom }}</h3>
            <p class="membre-poste">{{ membre.poste }}</p>

            <ul class="membre-meta">
              <li v-if="membre.specialite">
                <i class="fas fa-star"></i> {{ membre.specialite }}
              </li>
              <li v-if="membre.email">
                <i class="fas fa-envelope"></i> {{ membre.email }}
              </li>
              <li>
                <i class="fas fa-sort-numeric-down"></i> Ordre : {{ membre.ordre ?? 0 }}
              </li>
            </ul>

            <span class="status-badge" :class="membre.actif ? 'active' : 'inactive'">
              {{ membre.actif ? 'Actif' : 'Inactif' }}
            </span>
          </div>

          <!-- ✅ Actions visibles uniquement pour le SuperIT -->
          <div v-if="auth.isSuperIT" class="membre-actions">
            <button class="btn-icon edit" @click="openEdit(membre)" title="Modifier">
              <i class="fas fa-pen"></i>
            </button>
            <button class="btn-icon delete" @click="remove(membre)" title="Supprimer">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </article>
      </section>
    </main>

    <!-- ============ MODALE CRÉATION / ÉDITION ============ -->
    <transition name="fade">
      <div v-if="showModal && auth.isSuperIT" class="modal-overlay" @click.self="closeModal">
        <div class="modal-box">
          <div class="modal-header">
            <div class="modal-title">
              <i :class="editing ? 'fas fa-edit' : 'fas fa-user-plus'"></i>
              <h2>{{ editing ? 'Modifier' : 'Nouveau' }} membre</h2>
            </div>
            <button class="close-btn" @click="closeModal">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <form @submit.prevent="save" class="modal-form">
            <div class="form-row-2">
              <div class="form-group">
                <label>Nom complet *</label>
                <input v-model.trim="form.nom" type="text" required placeholder="Ex : Dr. Kouadio" />
              </div>
              <div class="form-group">
                <label>Poste *</label>
                <input v-model.trim="form.poste" type="text" required placeholder="Ex : Directeur" />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Email</label>
                <input v-model.trim="form.email" type="email" placeholder="email@exemple.ci" />
              </div>
              <div class="form-group">
                <label>Spécialité</label>
                <input v-model.trim="form.specialite" type="text" placeholder="Ex : Botanique" />
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label>Ordre d'affichage</label>
                <input v-model.number="form.ordre" type="number" min="0" />
              </div>
              <div class="form-group checkbox-group">
                <label class="checkbox-wrap">
                  <input type="checkbox" v-model="form.actif" />
                  <span>Membre actif</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <ImageUploader
                v-model="form.photoFile"
                label="Photo"
                icon="fas fa-user-circle"
                :multiple="false"
                :max-size="5"
                :existing-images="form.photoExisting ? [form.photoExisting] : []"
                @files-changed="handlePhotoChange"
              />
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Annuler</button>
              <button type="submit" class="btn btn-primary it" :disabled="saving">
                <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                <i v-else class="fas fa-save"></i>
                {{ saving ? 'Enregistrement…' : 'Enregistrer' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import TopBar from '../components/TopBar.vue'
import Toast from '../components/Toast.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import ImageUploader from '../components/ImageUploader.vue'
import { equipeAPI } from '../utils/api'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'
import { logger } from '../utils/logger'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const askConfirm = useConfirm()

const sidebarCollapsed = ref(false)
const equipe = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)

const form = ref({
  nom: '', poste: '', email: '', specialite: '',
  ordre: 0, actif: true,
  photoFile: null, photoExisting: null,
})

const filtered = computed(() => {
  if (!search.value) return equipe.value
  const q = search.value.toLowerCase()
  return equipe.value.filter(
    (m) => m.nom?.toLowerCase().includes(q)
        || m.poste?.toLowerCase().includes(q)
        || m.specialite?.toLowerCase().includes(q)
  )
})

const onImageError = (e) => { e.target.style.display = 'none' }

const loadEquipe = async () => {
  loading.value = true
  try {
    const { data } = await equipeAPI.list()
    equipe.value = Array.isArray(data) ? data : (data.results || [])
  } catch {
    toast.error('Impossible de charger l\'équipe')
  } finally {
    loading.value = false
  }
}

/* ============================================================
   ACTIONS — toutes protégées par auth.isSuperIT
   ============================================================ */

const openCreate = () => {
  if (!auth.isSuperIT) return
  editing.value = null
  form.value = {
    nom: '', poste: '', email: '', specialite: '',
    ordre: 0, actif: true,
    photoFile: null, photoExisting: null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const openEdit = (membre) => {
  if (!auth.isSuperIT) return
  editing.value = membre
  form.value = {
    nom: membre.nom || '',
    poste: membre.poste || '',
    email: membre.email || '',
    specialite: membre.specialite || '',
    ordre: membre.ordre ?? 0,
    actif: membre.actif !== false,
    photoFile: null,
    photoExisting: membre.photo || null,
  }
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  editing.value = null
  document.body.style.overflow = 'auto'
}

const handlePhotoChange = ({ files, existing }) => {
  form.value.photoFile = files[0] || null
  form.value.photoExisting = existing[0] || null
}

const save = async () => {
  if (!auth.isSuperIT) return
  if (!form.value.nom || !form.value.poste) {
    toast.error('Nom et poste sont obligatoires')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('nom', form.value.nom)
    fd.append('poste', form.value.poste)
    if (form.value.email) fd.append('email', form.value.email)
    if (form.value.specialite) fd.append('specialite', form.value.specialite)
    fd.append('ordre', String(form.value.ordre ?? 0))
    fd.append('actif', form.value.actif ? 'true' : 'false')

    if (form.value.photoFile) fd.append('photo', form.value.photoFile)
    else if (form.value.photoExisting) fd.append('photo', form.value.photoExisting)

    if (editing.value) {
      await equipeAPI.update(editing.value.id, fd)
      toast.success('Membre mis à jour')
    } else {
      await equipeAPI.create(fd)
      toast.success('Membre ajouté')
    }
    closeModal()
    await loadEquipe()
  } catch (err) {
    logger.warn('Save equipe error')
    toast.error(err.response?.data?.error || 'Erreur lors de l\'enregistrement')
  } finally {
    saving.value = false
  }
}

const remove = async (membre) => {
  if (!auth.isSuperIT) return
  const ok = await askConfirm({
    title: 'Supprimer',
    message: `Supprimer « ${membre.nom} » de l'équipe ?`,
    dangerous: true,
    confirmText: 'Supprimer',
  })
  if (!ok) return
  try {
    await equipeAPI.remove(membre.id)
    toast.success('Membre supprimé')
    await loadEquipe()
  } catch {
    toast.error('Erreur lors de la suppression')
  }
}

const handleLogout = async () => {
  await auth.logout()
  router.push(auth.isSuperIT ? '/it-login' : '/admin-login')
}

onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/it-login')
    return
  }
  loadEquipe()
})
</script>

<style scoped>
/* ============================================================
   LAYOUT + THEME
   ============================================================ */
.equipe-layout { min-height: 100vh; background: #f1f5f9; font-family: 'Inter', system-ui, sans-serif; }
.equipe-layout.superit-theme { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.main-content { margin-left: 260px; padding: 24px 28px 40px; transition: margin-left 0.3s ease; }
.main-content.expanded { margin-left: 76px; }

/* ============================================================
   BANDEAU LECTURE SEULE
   ============================================================ */
.readonly-banner {
  display: flex; gap: 14px; align-items: flex-start;
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  border-left: 4px solid #f59e0b;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 20px;
  color: #78350f;
}
.readonly-banner i { font-size: 22px; color: #d97706; flex-shrink: 0; margin-top: 2px; }
.readonly-banner strong { font-size: 14px; display: block; margin-bottom: 2px; }
.readonly-banner p { margin: 0; font-size: 13px; line-height: 1.5; }

/* ============================================================
   BOUTONS
   ============================================================ */
.btn-create {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; color: #fff;
  border: none; border-radius: 10px;
  font-size: 13.5px; font-weight: 600; cursor: pointer;
}
.btn-create.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.5);
}
.btn-create:hover { transform: translateY(-1px); }

/* ============================================================
   FILTRES
   ============================================================ */
.filters-bar {
  display: flex; gap: 12px; padding: 14px 18px;
  background: #fff; border-radius: 12px; margin-bottom: 20px;
  flex-wrap: wrap; align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.superit-theme .filters-bar {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.search-wrap { flex: 1; min-width: 200px; position: relative; }
.search-wrap i {
  position: absolute; left: 14px; top: 50%;
  transform: translateY(-50%); color: #94a3b8; font-size: 13px;
}
.search-wrap input {
  width: 100%; padding: 10px 14px 10px 40px;
  border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 13.5px; font-family: inherit;
  background: #f8fafc; color: #0f172a;
}
.superit-theme .search-wrap input {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.search-wrap input:focus { outline: none; border-color: #6366f1; background: #fff; }
.superit-theme .search-wrap input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); }
.result-count {
  font-size: 12.5px; color: #64748b;
  padding: 6px 14px; background: #f1f5f9; border-radius: 20px;
}
.superit-theme .result-count { color: #94a3b8; background: rgba(255, 255, 255, 0.04); }
.result-count i { color: #6366f1; margin-right: 4px; }
.superit-theme .result-count i { color: #818cf8; }

/* ============================================================
   LOADING / EMPTY
   ============================================================ */
.loading-block, .empty-block {
  background: #fff; border-radius: 12px; padding: 60px 20px; text-align: center;
}
.superit-theme .loading-block, .superit-theme .empty-block {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.spinner {
  width: 40px; height: 40px;
  border: 3px solid #e2e8f0; border-top-color: #6366f1;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
.superit-theme .spinner { border-color: rgba(255, 255, 255, 0.15); border-top-color: #818cf8; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-block i { font-size: 48px; color: #cbd5e1; margin-bottom: 12px; display: block; }
.superit-theme .empty-block i { color: #6366f1; }
.empty-block h3 { color: #0f172a; margin: 0 0 6px; }
.superit-theme .empty-block h3 { color: #fff; }
.empty-block p { color: #64748b; margin: 0 0 16px; }
.superit-theme .empty-block p { color: #94a3b8; }

/* ============================================================
   GRID
   ============================================================ */
.equipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 18px;
}
.membre-card {
  background: #fff; border-radius: 14px; overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.15s;
  display: flex; gap: 16px; padding: 18px;
  position: relative;
}
.superit-theme .membre-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: none;
}
.membre-card:hover { transform: translateY(-3px); box-shadow: 0 12px 30px -8px rgba(0, 0, 0, 0.1); }
.superit-theme .membre-card:hover { border-color: rgba(129, 140, 248, 0.4); }
.membre-card.inactive { opacity: 0.55; }

.membre-photo {
  width: 64px; height: 64px; flex-shrink: 0;
  border-radius: 50%; overflow: hidden;
  background: #f1f5f9;
  display: flex; align-items: center; justify-content: center;
}
.superit-theme .membre-photo { background: rgba(255, 255, 255, 0.08); }
.membre-photo img { width: 100%; height: 100%; object-fit: cover; }
.membre-photo i { font-size: 40px; color: #cbd5e1; }
.superit-theme .membre-photo i { color: #6366f1; }

.membre-body { flex: 1; min-width: 0; }
.membre-body h3 { font-size: 15px; color: #0f172a; margin: 0 0 4px; font-weight: 700; }
.superit-theme .membre-body h3 { color: #fff; }
.membre-poste { font-size: 12.5px; color: #6366f1; margin: 0 0 8px; font-weight: 600; }
.superit-theme .membre-poste { color: #818cf8; }
.membre-meta { list-style: none; padding: 0; margin: 0 0 8px; }
.membre-meta li {
  font-size: 12px; color: #475569;
  display: flex; align-items: center; gap: 6px; margin-bottom: 3px;
}
.superit-theme .membre-meta li { color: #cbd5e1; }
.membre-meta i { width: 14px; color: #94a3b8; font-size: 11px; }

.status-badge {
  padding: 3px 10px; border-radius: 20px;
  font-size: 10.5px; font-weight: 600; display: inline-block;
}
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.inactive { background: #fee2e2; color: #b91c1c; }
.superit-theme .status-badge.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.superit-theme .status-badge.inactive { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.membre-actions {
  position: absolute; top: 12px; right: 12px;
  display: flex; gap: 6px;
}
.btn-icon {
  width: 32px; height: 32px; border-radius: 8px;
  border: 1.5px solid #e2e8f0; background: #fff;
  color: #475569; cursor: pointer; font-size: 12px;
  display: flex; align-items: center; justify-content: center;
}
.superit-theme .btn-icon {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}
.btn-icon:hover { background: #f8fafc; }
.superit-theme .btn-icon:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
.btn-icon.edit:hover { color: #6366f1; border-color: #c7d2fe; }
.btn-icon.delete { color: #ef4444; border-color: #fecaca; }
.superit-theme .btn-icon.delete { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); }
.btn-icon.delete:hover { background: #fee2e2; }

/* ============================================================
   MODALE
   ============================================================ */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000; padding: 20px;
}
.superit-theme .modal-overlay { background: rgba(15, 23, 42, 0.8); }
.modal-box {
  background: #fff; border-radius: 16px;
  width: 100%; max-width: 620px; max-height: 90vh; overflow-y: auto;
}
.superit-theme .modal-box {
  background: #1e1b4b;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px; border-bottom: 1px solid #f1f5f9;
  position: sticky; top: 0; background: #fff;
  border-radius: 16px 16px 0 0; z-index: 1;
}
.superit-theme .modal-header {
  background: #1e1b4b;
  border-bottom-color: rgba(255, 255, 255, 0.08);
}
.modal-title { display: flex; align-items: center; gap: 12px; }
.modal-title i { font-size: 20px; color: #6366f1; }
.modal-title h2 { font-size: 17px; color: #0f172a; margin: 0; }
.superit-theme .modal-title h2 { color: #fff; }
.close-btn {
  width: 34px; height: 34px; border-radius: 50%;
  border: none; background: none; color: #94a3b8; cursor: pointer;
}
.close-btn:hover { background: #f1f5f9; color: #0f172a; }
.superit-theme .close-btn:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }

.modal-form { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12.5px; font-weight: 600; color: #334155; }
.superit-theme .form-group label { color: #cbd5e1; }
.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 9px;
  font-size: 13.5px; font-family: inherit;
  background: #f8fafc; color: #0f172a; resize: vertical;
}
.superit-theme .form-group input,
.superit-theme .form-group select,
.superit-theme .form-group textarea {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.form-group input:focus { outline: none; border-color: #6366f1; background: #fff; }
.superit-theme .form-group input:focus { border-color: #818cf8; background: rgba(255, 255, 255, 0.08); }

.checkbox-wrap { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; cursor: pointer; }
.superit-theme .checkbox-wrap { color: #cbd5e1; }
.checkbox-wrap input { width: 16px; height: 16px; accent-color: #6366f1; }

.modal-actions {
  display: flex; justify-content: flex-end; gap: 10px;
  padding-top: 8px; border-top: 1px solid #f1f5f9;
}
.superit-theme .modal-actions { border-top-color: rgba(255, 255, 255, 0.08); }

.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 9px;
  font-size: 13.5px; font-weight: 600; border: none; cursor: pointer;
}
.btn-primary { background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff; }
.btn-primary:hover:not(:disabled) { transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; }
.superit-theme .btn-secondary { background: rgba(255, 255, 255, 0.06); color: #cbd5e1; }
.btn-secondary:hover { background: #e2e8f0; }
.superit-theme .btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .main-content { margin-left: 76px; padding: 16px; }
  .form-row-2 { grid-template-columns: 1fr; }
}
</style>