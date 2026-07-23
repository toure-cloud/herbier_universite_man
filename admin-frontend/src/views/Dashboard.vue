<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <nav class="sidebar">
      <div class="logo">
        <i class="fas fa-leaf"></i>
        <span>Herbier Admin</span>
      </div>
      <div class="nav-menu">
        <div class="nav-section">
          <div class="nav-section-title">📊 TABLEAU DE BORD</div>
          <router-link to="/dashboard" class="nav-item">
            <i class="fas fa-tachometer-alt"></i> Accueil
          </router-link>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">🌿 CONTENU PRINCIPAL</div>
          <button @click="activeTab = 'plantes'" :class="['nav-item', { active: activeTab === 'plantes' }]">
            <i class="fas fa-leaf"></i> Plantes
          </button>
          <button @click="activeTab = 'equipe'" :class="['nav-item', { active: activeTab === 'equipe' }]">
            <i class="fas fa-users"></i> Équipe
          </button>
          <button @click="activeTab = 'slides'" :class="['nav-item', { active: activeTab === 'slides' }]">
            <i class="fas fa-images"></i> Slides
          </button>
          <button @click="activeTab = 'projets'" :class="['nav-item', { active: activeTab === 'projets' }]">
            <i class="fas fa-project-diagram"></i> Projets
          </button>
          <button @click="activeTab = 'activites'" :class="['nav-item', { active: activeTab === 'activites' }]">
            <i class="fas fa-chart-line"></i> Activités
          </button>
          <button @click="activeTab = 'partenaires'" :class="['nav-item', { active: activeTab === 'partenaires' }]">
            <i class="fas fa-handshake"></i> Partenaires
          </button>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">⚙️ ADMINISTRATION</div>
          
          <!-- ✅ BOUTON ADMINISTRATION IT - REDIRECTION CORRIGÉE -->
          
<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <nav class="sidebar">
      <div class="logo">
        <i class="fas fa-leaf"></i>
        <span>Herbier Admin</span>
      </div>
      <div class="nav-menu">
        <div class="nav-section">
          <div class="nav-section-title">📊 TABLEAU DE BORD</div>
          <router-link to="/dashboard" class="nav-item">
            <i class="fas fa-tachometer-alt"></i> Accueil
          </router-link>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">🌿 CONTENU PRINCIPAL</div>
          <button @click="activeTab = 'plantes'" :class="['nav-item', { active: activeTab === 'plantes' }]">
            <i class="fas fa-leaf"></i> Plantes
          </button>
          <button @click="activeTab = 'equipe'" :class="['nav-item', { active: activeTab === 'equipe' }]">
            <i class="fas fa-users"></i> Équipe
          </button>
          <button @click="activeTab = 'slides'" :class="['nav-item', { active: activeTab === 'slides' }]">
            <i class="fas fa-images"></i> Slides
          </button>
          <button @click="activeTab = 'projets'" :class="['nav-item', { active: activeTab === 'projets' }]">
            <i class="fas fa-project-diagram"></i> Projets
          </button>
          <button @click="activeTab = 'activites'" :class="['nav-item', { active: activeTab === 'activites' }]">
            <i class="fas fa-chart-line"></i> Activités
          </button>
          <button @click="activeTab = 'partenaires'" :class="['nav-item', { active: activeTab === 'partenaires' }]">
            <i class="fas fa-handshake"></i> Partenaires
          </button>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">⚙️ ADMINISTRATION</div>
          
          <!-- ✅ BOUTON ADMINISTRATION IT - CORRIGÉ -->
          <button 
            @click="goToITAdmin" 
            class="nav-item it-admin-btn"
            type="button">
            <i class="fas fa-shield-alt"></i> Administration IT
            <span class="nav-badge">🔒</span>
          </button>

          <div v-if="isSuperAdmin">
            <button @click="openMembresModal" class="nav-item">
              <i class="fas fa-users-cog"></i> Gestion admins
            </button>
          </div>
          <button @click="syncAllData" class="nav-item" :disabled="syncing">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': syncing }"></i>
            {{ syncing ? 'Synchronisation...' : 'Synchroniser' }}
          </button>
          <button @click="logout" class="nav-item logout">
            <i class="fas fa-sign-out-alt"></i> Déconnexion
          </button>
        </div>
      </div>
    </nav>

    <div class="main-content">
      <div class="top-bar">
        <h1>{{ getTabTitle() }}</h1>
        <div class="user-info">
          <div class="user-badge" :class="{ 'super-admin': isSuperAdmin }">
            <i v-if="isSuperAdmin" class="fas fa-shield-alt"></i>
            <span>{{ currentUserRole }}</span>
          </div>
          <span class="user-name">{{ currentUserName }}</span>
          <div class="avatar">{{ (currentUserName || 'A').charAt(0) }}</div>
        </div>
      </div>

      <div class="content">
        <!-- Loading -->
        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <p>Chargement...</p>
        </div>

        <!-- SECTION PLANTES -->
        <div v-show="activeTab === 'plantes'" class="data-section">
          <div class="section-header">
            <h2><i class="fas fa-leaf"></i> Gestion des plantes</h2>
            <button class="btn-add" @click="openAddModal('plante')">
              <i class="fas fa-plus"></i> Nouvelle plante
            </button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr>
                  <th>Image</th>
                  <th>Nom</th>
                  <th>Famille</th>
                  <th>Nom scientifique</th>
                  <th>Statut</th>
                  <th>Actif</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in plantes" :key="item.id">
                  <td>
                    <div class="table-image" @click="openImagePreview(getFullImageUrl(item.image))">
                      <img v-if="getFullImageUrl(item.image)" :src="getFullImageUrl(item.image)" :alt="item.nom" class="thumbnail" @error="handleImageError">
                      <div v-else class="no-image"><i class="fas fa-image"></i></div>
                    </div>
                  </td>
                  <td><strong>{{ item.nom }}</strong></td>
                  <td>{{ item.famille?.nom || item.famille || '-' }}</td>
                  <td><em>{{ item.nom_scientifique || '-' }}</em></td>
                  <td>{{ item.statut_conservation || '-' }}</td>
                  <td>
                    <span class="status-badge" :class="item.actif ? 'active' : 'inactive'">
                      {{ item.actif ? 'Actif' : 'Inactif' }}
                    </span>
                  </td>
                  <td class="actions">
                    <button class="btn-edit" @click="openEditModal('plante', item)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" @click="deleteItem('plante', item.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="!plantes.length">
                  <td colspan="7" class="empty-row">Aucune plante trouvée</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- SECTION EQUIPE -->
        <div v-show="activeTab === 'equipe'" class="data-section">
          <div class="section-header">
            <h2><i class="fas fa-users"></i> Gestion de l'équipe</h2>
            <button class="btn-add" @click="openAddModal('equipe')" v-if="isSuperAdmin">
              <i class="fas fa-plus"></i> Nouveau membre
            </button>
            <span v-else class="permission-badge">🔒 Réservé aux administrateurs</span>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>Photo</th><th>Nom</th><th>Poste</th><th>Email</th><th>Spécialité</th><th>Actif</th><th>Actions</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in equipe" :key="item.id">
                  <td>
                    <div class="table-image" @click="openImagePreview(getFullImageUrl(item.photo || item.image))">
                      <img v-if="getFullImageUrl(item.photo || item.image)" :src="getFullImageUrl(item.photo || item.image)" :alt="item.nom" class="thumbnail" @error="handleImageError">
                      <div v-else class="no-image"><i class="fas fa-user"></i></div>
                    </div>
                  </td>
                  <td><strong>{{ item.nom }}</strong></td>
                  <td>{{ item.poste }}</td>
                  <td>{{ item.email || '-' }}</td>
                  <td>{{ item.specialite || '-' }}</td>
                  <td>
                    <span class="status-badge" :class="item.actif ? 'active' : 'inactive'">
                      {{ item.actif ? 'Actif' : 'Inactif' }}
                    </span>
                  </td>
                  <td class="actions">
                    <button class="btn-edit" @click="openEditModal('equipe', item)" :disabled="!isSuperAdmin">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" @click="deleteItem('equipe', item.id)" :disabled="!isSuperAdmin">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="!equipe.length">
                  <td colspan="7" class="empty-row">Aucun membre trouvé</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- SECTION SLIDES -->
        <div v-show="activeTab === 'slides'" class="data-section">
          <div class="section-header">
            <h2><i class="fas fa-images"></i> Gestion des slides</h2>
            <button class="btn-add" @click="openAddModal('slide')">
              <i class="fas fa-plus"></i> Nouveau slide
            </button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>Image</th><th>Titre</th><th>Texte botanique</th><th>Ordre</th><th>Actif</th><th>Actions</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in slides" :key="item.id">
                  <td>
                    <div class="table-image" @click="openImagePreview(getFullImageUrl(item.image))">
                      <img v-if="getFullImageUrl(item.image)" :src="getFullImageUrl(item.image)" :alt="item.titre" class="thumbnail" @error="handleImageError">
                      <div v-else class="no-image"><i class="fas fa-image"></i></div>
                    </div>
                  </td>
                  <td><strong>{{ item.titre }}</strong></td>
                  <td>{{ truncate(item.texte_botanique, 50) }}</td>
                  <td>{{ item.ordre }}</td>
                  <td>
                    <span class="status-badge" :class="item.actif ? 'active' : 'inactive'">
                      {{ item.actif ? 'Actif' : 'Inactif' }}
                    </span>
                  </td>
                  <td class="actions">
                    <button class="btn-edit" @click="openEditModal('slide', item)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" @click="deleteItem('slide', item.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="!slides.length">
                  <td colspan="6" class="empty-row">Aucun slide trouvé</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- SECTION PROJETS -->
        <div v-show="activeTab === 'projets'" class="data-section">
          <div class="section-header">
            <h2><i class="fas fa-project-diagram"></i> Gestion des projets</h2>
            <button class="btn-add" @click="openAddModal('projet')">
              <i class="fas fa-plus"></i> Nouveau projet
            </button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>Image</th><th>Titre</th><th>Catégorie</th><th>Statut</th><th>Année</th><th>Actions</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in projets" :key="item.id">
                  <td>
                    <div class="table-image" @click="openImagePreview(getFullImageUrl(item.image))">
                      <img v-if="getFullImageUrl(item.image)" :src="getFullImageUrl(item.image)" :alt="item.titre" class="thumbnail" @error="handleImageError">
                      <div v-else class="no-image"><i class="fas fa-image"></i></div>
                    </div>
                  </td>
                  <td><strong>{{ item.titre }}</strong></td>
                  <td>{{ item.categorie }}</td>
                  <td><span class="badge">{{ item.statut }}</span></td>
                  <td>{{ item.annee }}</td>
                  <td class="actions">
                    <button class="btn-edit" @click="openEditModal('projet', item)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" @click="deleteItem('projet', item.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="!projets.length">
                  <td colspan="6" class="empty-row">Aucun projet trouvé</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- SECTION ACTIVITES -->
        <div v-show="activeTab === 'activites'" class="data-section">
          <div class="section-header">
            <h2><i class="fas fa-chart-line"></i> Gestion des activités</h2>
            <button class="btn-add" @click="openAddModal('activite')">
              <i class="fas fa-plus"></i> Nouvelle activité
            </button>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>Image</th><th>Icône</th><th>Titre</th><th>Titre court</th><th>Description</th><th>Ordre</th><th>Actif</th><th>Actions</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in activites" :key="item.id">
                  <td>
                    <div class="table-image" @click="openImagePreview(getFullImageUrl(item.image))">
                      <img v-if="getFullImageUrl(item.image)" :src="getFullImageUrl(item.image)" :alt="item.titre" class="thumbnail" @error="handleImageError">
                      <div v-else class="no-image"><i class="fas fa-image"></i></div>
                    </div>
                  </td>
                  <td><i :class="item.icon" style="font-size:24px"></i></td>
                  <td><strong>{{ item.titre }}</strong></td>
                  <td>{{ item.titre_court }}</td>
                  <td>{{ truncate(item.description_courte, 30) }}</td>
                  <td>{{ item.ordre }}</td>
                  <td>
                    <span class="status-badge" :class="item.actif ? 'active' : 'inactive'">
                      {{ item.actif ? 'Actif' : 'Inactif' }}
                    </span>
                  </td>
                  <td class="actions">
                    <button class="btn-edit" @click="openEditModal('activite', item)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" @click="deleteItem('activite', item.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="!activites.length">
                  <td colspan="8" class="empty-row">Aucune activité trouvée</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- SECTION PARTENAIRES -->
        <div v-show="activeTab === 'partenaires'" class="data-section">
          <div class="section-header">
            <h2><i class="fas fa-handshake"></i> Gestion des partenaires</h2>
            <button class="btn-add" @click="openAddModal('partenaire')" v-if="isSuperAdmin">
              <i class="fas fa-plus"></i> Nouveau partenaire
            </button>
            <span v-else class="permission-badge">🔒 Réservé aux administrateurs</span>
          </div>
          <div class="data-table">
            <table>
              <thead>
                <tr><th>Logo</th><th>Nom</th><th>Description</th><th>Site web</th><th>Type</th><th>Ordre</th><th>Actif</th><th>Actions</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in partenaires" :key="item.id">
                  <td>
                    <div class="table-image" @click="openImagePreview(getFullImageUrl(item.logo || item.image))">
                      <img v-if="getFullImageUrl(item.logo || item.image)" :src="getFullImageUrl(item.logo || item.image)" :alt="item.nom" class="thumbnail" @error="handleImageError">
                      <div v-else class="no-image"><i class="fas fa-building"></i></div>
                    </div>
                  </td>
                  <td><strong>{{ item.nom }}</strong></td>
                  <td>{{ truncate(item.description, 40) }}</td>
                  <td><a v-if="item.site_web" :href="item.site_web" target="_blank"><i class="fas fa-external-link-alt"></i></a><span v-else>-</span></td>
                  <td>{{ item.type || '-' }}</td>
                  <td>{{ item.ordre }}</td>
                  <td>
                    <span class="status-badge" :class="item.actif ? 'active' : 'inactive'">
                      {{ item.actif ? 'Actif' : 'Inactif' }}
                    </span>
                  </td>
                  <td class="actions">
                    <button class="btn-edit" @click="openEditModal('partenaire', item)" :disabled="!isSuperAdmin">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" @click="deleteItem('partenaire', item.id)" :disabled="!isSuperAdmin">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="!partenaires.length">
                  <td colspan="8" class="empty-row">Aucun partenaire trouvé</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- STATS -->
        <div class="stats-section">
          <div class="stats-grid">
            <div class="stat-card">
              <i class="fas fa-leaf"></i>
              <div><h3>{{ plantes.length }}</h3><p>Plantes</p></div>
            </div>
            <div class="stat-card">
              <i class="fas fa-users"></i>
              <div><h3>{{ equipe.length }}</h3><p>Équipe</p></div>
            </div>
            <div class="stat-card">
              <i class="fas fa-images"></i>
              <div><h3>{{ slides.length }}</h3><p>Slides</p></div>
            </div>
            <div class="stat-card">
              <i class="fas fa-project-diagram"></i>
              <div><h3>{{ projets.length }}</h3><p>Projets</p></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL AJOUT/MODIFICATION -->
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ modalTitle }}</h2>
          <button class="close" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveItem">
            <div v-for="(field, key) in currentFields" :key="key" class="form-group">
              <label>{{ field.label }}</label>
              <input v-if="field.type === 'text' || field.type === 'email' || field.type === 'url'" 
                     :type="field.type" v-model="formData[field.name]" class="form-control"
                     :required="field.required">
              <textarea v-else-if="field.type === 'textarea'" 
                        v-model="formData[field.name]" class="form-control" rows="3"></textarea>
              <select v-else-if="field.type === 'select'" 
                      v-model="formData[field.name]" class="form-control">
                <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
              </select>
              <input v-else-if="field.type === 'number'" 
                     type="number" v-model="formData[field.name]" class="form-control">
              <input v-else-if="field.type === 'checkbox'" 
                     type="checkbox" v-model="formData[field.name]" class="form-checkbox">
            </div>
            
            <!-- Upload d'image -->
            <div v-if="modalType === 'plante' || modalType === 'slide' || modalType === 'equipe' || modalType === 'projet' || modalType === 'activite' || modalType === 'partenaire'" class="form-group">
              <label>Image / Logo</label>
              <div class="image-upload-area" 
                   @dragover.prevent @drop.prevent="handleDrop" 
                   @click="triggerFileInput"
                   :class="{ 'has-image': formData.image_preview }">
                <div v-if="formData.image_preview" class="image-preview">
                  <img :src="formData.image_preview" alt="Aperçu">
                  <button type="button" class="remove-image" @click.stop="removeImage">✕</button>
                </div>
                <div v-else class="upload-placeholder">
                  <i class="fas fa-cloud-upload-alt"></i>
                  <p>Cliquez ou déposez une image ici</p>
                  <span class="upload-hint">PNG, JPG, JPEG, WEBP</span>
                </div>
                <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" style="display:none">
              </div>
              <small class="form-help" v-if="formData._existing_image">Image actuelle</small>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-save" :disabled="loading">
                <i v-if="loading" class="fas fa-spinner fa-spin"></i>
                {{ loading ? 'Enregistrement...' : 'Enregistrer' }}
              </button>
              <button type="button" class="btn-cancel" @click="closeModal">Annuler</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- MODAL GESTION ADMINS -->
    <div v-if="showUsersModal" class="modal" @click.self="closeUsersModal">
      <div class="modal-container">
        <div class="modal-header">
          <h2><i class="fas fa-users-cog"></i> Gestion des administrateurs</h2>
          <button class="close" @click="closeUsersModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="add-user-form">
            <h3>Ajouter un administrateur</h3>
            <form @submit.prevent="createUser">
              <div class="form-row">
                <input type="text" v-model="newUser.nom" placeholder="Nom" required>
                <input type="email" v-model="newUser.email" placeholder="Email" required>
              </div>
              <div class="form-row">
                <input type="tel" v-model="newUser.telephone" placeholder="Téléphone" required>
                <select v-model="newUser.role">
                  <option value="admin">Admin</option>
                  <option value="it_admin">IT Admin</option>
                </select>
              </div>
              <div class="form-row">
                <input type="password" v-model="newUser.password" placeholder="Mot de passe" required>
                <input type="password" v-model="newUser.password2" placeholder="Confirmer" required>
              </div>
              <button type="submit" class="btn-add">➕ Ajouter</button>
            </form>
          </div>
          <div class="users-list">
            <h3>Liste des administrateurs</h3>
            <div class="users-table">
              <table>
                <thead>
                  <tr><th>Nom</th><th>Email</th><th>Rôle</th><th>Statut</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  <tr v-for="user in adminUsers" :key="user.id">
                    <td>{{ user.nom }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                      <span :class="'role-badge ' + user.role">
                        {{ user.role === 'it_admin' ? 'IT Admin' : 'Admin' }}
                      </span>
                    </td>
                    <td>
                      <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                        {{ user.is_active ? 'Actif' : 'Inactif' }}
                      </span>
                    </td>
                    <td class="actions">
                      <button @click="toggleUserStatus(user)" class="btn-status">
                        <i :class="user.is_active ? 'fas fa-ban' : 'fas fa-check-circle'"></i>
                      </button>
                      <button @click="deleteUser(user.id)" class="btn-delete">
                        <i class="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="!adminUsers.length">
                    <td colspan="5" class="empty-row">Aucun administrateur</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- IMAGE PREVIEW MODAL -->
    <div v-if="showImagePreview" class="modal image-preview-modal" @click.self="closeImagePreview">
      <div class="image-preview-container" @click.stop>
        <button class="close-preview" @click="closeImagePreview">&times;</button>
        <img :src="previewImage" alt="Aperçu" class="preview-image-full" @error="handleImageError">
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast.show" class="toast" :class="toast.type">
      <i :class="toast.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
      {{ toast.message }}
    </div>
  </div>
</template>

<script>
import { adminAPI, authAPI } from '../services/api'
import { useAuthStore } from '../stores/auth'

const API_BASE_URL = 'http://localhost:8001'

const endpoints = {
  plante: 'plantes',
  equipe: 'equipe',
  slide: 'slides',
  projet: 'projets',
  activite: 'activites',
  partenaire: 'partenaires'
}

export default {
  name: 'Dashboard',
  data() {
    return {
      activeTab: 'plantes',
      loading: false,
      syncing: false,
      plantes: [],
      equipe: [],
      slides: [],
      projets: [],
      activites: [],
      partenaires: [],
      adminUsers: [],
      currentUser: null,
      isSuperAdmin: false,
      isITAdmin: false,
      currentUserName: '',
      currentUserRole: '',
      showModal: false,
      showUsersModal: false,
      showImagePreview: false,
      previewImage: '',
      modalMode: 'add',
      modalType: '',
      modalTitle: '',
      formData: {},
      currentItemId: null,
      toast: { show: false, message: '', type: 'success' },
      newUser: { nom: '', email: '', telephone: '', role: 'admin', password: '', password2: '' },
      fieldsMap: {
        plante: [
          { name: 'nom', label: 'Nom *', type: 'text', required: true },
          { name: 'famille', label: 'Famille', type: 'text' },
          { name: 'nom_scientifique', label: 'Nom scientifique', type: 'text' },
          { name: 'description', label: 'Description', type: 'textarea' },
          { name: 'habitat', label: 'Habitat', type: 'text' },
          { name: 'statut_conservation', label: 'Statut de conservation', type: 'select', options: ['', 'En danger critique', 'En danger', 'Vulnérable', 'Quasi menacé', 'Préoccupation mineure'] },
          { name: 'actif', label: 'Actif', type: 'checkbox' }
        ],
        equipe: [
          { name: 'nom', label: 'Nom *', type: 'text', required: true },
          { name: 'poste', label: 'Poste *', type: 'text', required: true },
          { name: 'email', label: 'Email', type: 'email' },
          { name: 'specialite', label: 'Spécialité', type: 'text' },
          { name: 'photo', label: 'Photo URL', type: 'text' },
          { name: 'ordre', label: 'Ordre', type: 'number' },
          { name: 'actif', label: 'Actif', type: 'checkbox' }
        ],
        slide: [
          { name: 'titre', label: 'Titre *', type: 'text', required: true },
          { name: 'texte_botanique', label: 'Texte botanique *', type: 'textarea', required: true },
          { name: 'ordre', label: 'Ordre', type: 'number' },
          { name: 'actif', label: 'Actif', type: 'checkbox' }
        ],
        projet: [
          { name: 'titre', label: 'Titre *', type: 'text', required: true },
          { name: 'categorie', label: 'Catégorie', type: 'select', options: ['recherche', 'conservation', 'formation', 'developpement'] },
          { name: 'statut', label: 'Statut', type: 'select', options: ['termine', 'encours', 'planifie'] },
          { name: 'annee', label: 'Année', type: 'text' },
          { name: 'lieu', label: 'Lieu', type: 'text' },
          { name: 'description', label: 'Description', type: 'textarea' }
        ],
        activite: [
          { name: 'titre', label: 'Titre *', type: 'text', required: true },
          { name: 'titre_court', label: 'Titre court *', type: 'text', required: true },
          { name: 'description_courte', label: 'Description courte *', type: 'textarea', required: true },
          { name: 'description_longue', label: 'Description longue', type: 'textarea' },
          { name: 'icon', label: 'Icône', type: 'text' },
          { name: 'ordre', label: 'Ordre', type: 'number' },
          { name: 'actif', label: 'Actif', type: 'checkbox' }
        ],
        partenaire: [
          { name: 'nom', label: 'Nom *', type: 'text', required: true },
          { name: 'description', label: 'Description', type: 'textarea' },
          { name: 'logo', label: 'Logo URL', type: 'text' },
          { name: 'site_web', label: 'Site web', type: 'url' },
          { name: 'type', label: 'Type de partenaire', type: 'text' },
          { name: 'ordre', label: 'Ordre', type: 'number' },
          { name: 'actif', label: 'Actif', type: 'checkbox' }
        ]
      }
    }
  },
  computed: {
    currentFields() { return this.fieldsMap[this.modalType] || [] }
  },
  mounted() {
    // ✅ Vérifier l'authentification IT
    const isItAuthenticated = localStorage.getItem('it_admin_authenticated')
    if (isItAuthenticated === 'true') {
      this.isITAdmin = true
      this.isSuperAdmin = true
      this.currentUserRole = 'IT Admin'
      this.currentUserName = 'IT Administrator'
      this.loadAllData()
      this.loadUserData()
    } else {
      this.loadUserData()
      this.loadAllData()
    }
    document.addEventListener('keydown', this.handleEscapeKey)
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscapeKey)
  },
  methods: {
    // ============================================
    // GESTION DES TOUCHES (Escape pour fermer)
    // ============================================
    handleEscapeKey(event) {
      if (event.key === 'Escape') {
        if (this.showModal) this.closeModal()
        if (this.showUsersModal) this.closeUsersModal()
        if (this.showImagePreview) this.closeImagePreview()
      }
    },

    // ============================================
    // CHARGEMENT DES DONNÉES
    // ============================================
    async loadAllData() {
      this.loading = true
      try {
        const [plantes, equipe, slides, projets, activites, partenaires] = await Promise.all([
          adminAPI.getPlantes(),
          adminAPI.getEquipe(),
          adminAPI.getSlides(),
          adminAPI.getProjets(),
          adminAPI.getActivites(),
          adminAPI.getPartenaires()
        ])
        this.plantes = plantes.data || []
        this.equipe = equipe.data || []
        this.slides = slides.data || []
        this.projets = projets.data || []
        this.activites = activites.data || []
        this.partenaires = partenaires.data || []
      } catch (error) {
        console.error('Erreur chargement:', error)
        this.showToast('Erreur lors du chargement des données', 'error')
      } finally {
        this.loading = false
      }
    },

    async loadUserData() {
      const token = localStorage.getItem('access_token')
      if (!token) { this.$router.push('/login'); return }
      try {
        const res = await authAPI.getCurrentUser()
        this.currentUser = res.data
        this.currentUserName = res.data.nom
        this.isSuperAdmin = res.data.role === 'it_admin' || res.data.is_superuser
        this.currentUserRole = this.isSuperAdmin ? 'Super Admin' : 'Admin'
        if (this.isSuperAdmin) {
          const usersRes = await adminAPI.getUsers()
          this.adminUsers = usersRes.data || []
        }
      } catch (error) {
        if (error.response?.status === 401) this.$router.push('/login')
        else this.showToast('Erreur de chargement utilisateur', 'error')
      }
    },

    // ============================================
    // GESTION DES IMAGES
    // ============================================
    getFullImageUrl(imagePath) {
      if (!imagePath) return ''
      
      if (imagePath.startsWith('http://') || 
          imagePath.startsWith('https://') || 
          imagePath.startsWith('data:')) {
        return imagePath
      }
      
      if (imagePath.startsWith('/media/')) {
        return `${API_BASE_URL}${imagePath}`
      }
      
      if (imagePath.startsWith('media/')) {
        return `${API_BASE_URL}/${imagePath}`
      }
      
      if (imagePath.startsWith('uploads/')) {
        return `${API_BASE_URL}/media/${imagePath}`
      }
      
      return imagePath
    },

    handleImageError(event) {
      event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f0f0f0" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="12" fill="%23999" text-anchor="middle" dy=".3em"%3EPas d\'image%3C/text%3E%3C/svg%3E'
      event.target.style.objectFit = 'contain'
      event.target.style.padding = '10px'
    },

    openImagePreview(imageUrl) {
      if (!imageUrl) return
      this.previewImage = imageUrl
      this.showImagePreview = true
      document.body.style.overflow = 'hidden'
    },

    closeImagePreview() {
      this.showImagePreview = false
      this.previewImage = ''
      document.body.style.overflow = 'auto'
    },

    // ============================================
    // GESTION DES MODALS
    // ============================================
    closeModal() {
      this.showModal = false
      this.formData = {}
      this.currentItemId = null
      document.body.style.overflow = 'auto'
    },

    closeUsersModal() {
      this.showUsersModal = false
      document.body.style.overflow = 'auto'
    },

    openAddModal(type) {
      if ((type === 'equipe' || type === 'partenaire') && !this.isSuperAdmin) {
        this.showToast('Vous n\'avez pas les droits pour effectuer cette action', 'error')
        return
      }
      this.modalMode = 'add'
      this.modalType = type
      this.modalTitle = `Ajouter ${this.getTypeLabel(type)}`
      
      this.formData = { 
        actif: true,
        image_preview: null,
        image_file: null,
        _existing_image: null
      }
      this.currentItemId = null
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    openEditModal(type, item) {
      if ((type === 'equipe' || type === 'partenaire') && !this.isSuperAdmin) {
        this.showToast('Vous n\'avez pas les droits pour effectuer cette action', 'error')
        return
      }
      this.modalMode = 'edit'
      this.modalType = type
      this.modalTitle = `Modifier ${item.nom || item.titre || ''}`
      
      let existingImage = ''
      if (type === 'equipe') {
        existingImage = item.photo || item.image || ''
      } else if (type === 'partenaire') {
        existingImage = item.logo || item.image || ''
      } else {
        existingImage = item.image || ''
      }
      
      this.formData = { 
        ...item,
        image_preview: existingImage ? this.getFullImageUrl(existingImage) : null,
        _existing_image: existingImage,
        image_file: null
      }
      
      this.currentItemId = item.id
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },

    // ============================================
    // UPLOAD D'IMAGES
    // ============================================
    triggerFileInput() { 
      this.$refs.fileInput?.click() 
    },

    handleFileSelect(event) {
      const file = event.target.files[0]
      if (!file) return
      
      if (file.size > 5 * 1024 * 1024) {
        this.showToast('L\'image ne doit pas dépasser 5MB', 'error')
        event.target.value = ''
        return
      }
      
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
      if (!validTypes.includes(file.type)) {
        this.showToast('Format d\'image non supporté (JPEG, PNG, GIF, WEBP, SVG)', 'error')
        event.target.value = ''
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        this.formData.image_preview = e.target.result
        this.formData.image_file = file
        this.formData._existing_image = null
      }
      reader.readAsDataURL(file)
    },

    handleDrop(event) {
      const file = event.dataTransfer.files[0]
      if (!file || !file.type.startsWith('image/')) {
        this.showToast('Veuillez déposer une image', 'error')
        return
      }
      
      if (file.size > 5 * 1024 * 1024) {
        this.showToast('L\'image ne doit pas dépasser 5MB', 'error')
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        this.formData.image_preview = e.target.result
        this.formData.image_file = file
        this.formData._existing_image = null
      }
      reader.readAsDataURL(file)
    },

    removeImage() {
      this.formData.image_preview = null
      this.formData.image_file = null
      this.formData._existing_image = null
      
      if (this.modalType === 'equipe') {
        this.formData.photo = null
      } else if (this.modalType === 'partenaire') {
        this.formData.logo = null
      } else {
        this.formData.image = null
      }
    },

    // ============================================
    // CRUD OPERATIONS
    // ============================================
    async saveItem() {
      const endpoint = endpoints[this.modalType]
      
      const requiredFields = this.currentFields.filter(f => f.required)
      for (const field of requiredFields) {
        if (!this.formData[field.name] || this.formData[field.name].trim() === '') {
          this.showToast(`Le champ "${field.label}" est obligatoire`, 'error')
          return
        }
      }
      
      const data = { ...this.formData }
      
      const tempFields = ['image_preview', 'image_file', '_existing_image']
      tempFields.forEach(key => {
        if (data[key] !== undefined) delete data[key]
      })
      
      Object.keys(data).forEach(key => {
        if (data[key] === null || data[key] === undefined || data[key] === '') {
          delete data[key]
        }
      })

      if (this.formData.image_file instanceof File) {
        let imageFieldName = 'image'
        if (this.modalType === 'equipe') imageFieldName = 'photo'
        else if (this.modalType === 'partenaire') imageFieldName = 'logo'
        
        data[imageFieldName] = this.formData.image_file
        
        if (this.modalMode === 'edit') {
          delete data.image
          delete data.photo
          delete data.logo
        }
      } else if (this.modalMode === 'edit' && this.formData._existing_image) {
        let imageFieldName = 'image'
        if (this.modalType === 'equipe') imageFieldName = 'photo'
        else if (this.modalType === 'partenaire') imageFieldName = 'logo'
        data[imageFieldName] = this.formData._existing_image
      }
      
      try {
        this.loading = true
        if (this.modalMode === 'add') {
          await adminAPI.createItem(endpoint, data)
          this.showToast('Ajouté avec succès', 'success')
        } else {
          await adminAPI.updateItem(endpoint, this.currentItemId, data)
          this.showToast('Modifié avec succès', 'success')
        }
        
        this.closeModal()
        await this.loadAllData()
      } catch (error) {
        console.error('❌ Erreur:', error)
        this.showToast('Erreur lors de l\'enregistrement', 'error')
      } finally {
        this.loading = false
      }
    },

    async deleteItem(type, id) {
      if (type === 'equipe' || type === 'partenaire') {
        if (!this.isSuperAdmin) {
          this.showToast('Vous n\'avez pas les droits pour effectuer cette action', 'error')
          return
        }
      }
      if (!confirm('Supprimer définitivement ? Cette action est irréversible.')) return
      const endpoint = endpoints[type]
      try {
        await adminAPI.deleteItem(endpoint, id)
        this.showToast('Supprimé avec succès', 'success')
        await this.loadAllData()
      } catch (error) {
        console.error('Erreur suppression:', error)
        this.showToast('Erreur lors de la suppression', 'error')
      }
    },

    // ============================================
    // GESTION DES UTILISATEURS
    // ============================================
    async createUser() {
      if (this.newUser.password !== this.newUser.password2) {
        this.showToast('Les mots de passe ne correspondent pas', 'error')
        return
      }
      if (this.newUser.password.length < 8) {
        this.showToast('Le mot de passe doit contenir au moins 8 caractères', 'error')
        return
      }
      
      try {
        await adminAPI.createUser(this.newUser)
        this.showToast('Utilisateur créé avec succès', 'success')
        this.newUser = { nom: '', email: '', telephone: '', role: 'admin', password: '', password2: '' }
        const res = await adminAPI.getUsers()
        this.adminUsers = res.data || []
      } catch (error) {
        console.error('Erreur création utilisateur:', error)
        this.showToast('Erreur lors de la création de l\'utilisateur', 'error')
      }
    },

    async toggleUserStatus(user) {
      if (!confirm(`${user.is_active ? 'Désactiver' : 'Activer'} ${user.nom} ?`)) return
      try {
        await adminAPI.toggleUserStatus(user.id, { is_active: !user.is_active })
        this.showToast(`Utilisateur ${user.is_active ? 'désactivé' : 'activé'}`, 'success')
        const res = await adminAPI.getUsers()
        this.adminUsers = res.data || []
      } catch (error) {
        this.showToast('Erreur lors du changement de statut', 'error')
      }
    },

    async deleteUser(id) {
      if (!confirm('Supprimer définitivement cet utilisateur ?')) return
      try {
        await adminAPI.deleteUser(id)
        this.showToast('Utilisateur supprimé', 'success')
        const res = await adminAPI.getUsers()
        this.adminUsers = res.data || []
      } catch (error) {
        this.showToast('Erreur lors de la suppression', 'error')
      }
    },

    // ============================================
    // BOUTON ADMINISTRATION IT - REDIRECTION CORRIGÉE
    // ============================================
    goToITAdmin() {
      // Vérifier si l'utilisateur est déjà Super Admin
      if (this.isSuperAdmin) {
        // Rediriger directement vers la page des administrateurs
        this.$router.push('/administrateurs')
      } else {
        // Sinon, rediriger vers la page de connexion IT
        this.$router.push('/it-login')
      }
    },

    // ============================================
    // AUTRES FONCTIONS
    // ============================================
    async syncAllData() {
      this.syncing = true
      try {
        await adminAPI.syncAll()
        this.showToast('Synchronisation terminée avec succès', 'success')
        await this.loadAllData()
      } catch (error) {
        console.error('Erreur synchronisation:', error)
        this.showToast('Erreur lors de la synchronisation', 'error')
      } finally {
        this.syncing = false
      }
    },

    showToast(message, type = 'success') {
      this.toast = { show: true, message, type }
      setTimeout(() => { this.toast.show = false }, 4000)
    },

    truncate(text, len) { 
      return text?.length > len ? text.substring(0, len) + '...' : text || '' 
    },

    getTabTitle() {
      const titles = { 
        plantes: '🌿 Plantes', 
        equipe: '👥 Équipe', 
        slides: '📸 Slides', 
        projets: '📊 Projets',
        activites: '⚡ Activités',
        partenaires: '🤝 Partenaires'
      }
      return titles[this.activeTab] || 'Tableau de bord'
    },

    getTypeLabel(type) {
      const labels = {
        plante: 'Plante',
        equipe: 'Membre de l\'équipe',
        slide: 'Slide',
        projet: 'Projet',
        activite: 'Activité',
        partenaire: 'Partenaire'
      }
      return labels[type] || type
    },

    openMembresModal() {
      if (!this.isSuperAdmin) {
        this.showToast('Vous n\'avez pas les droits pour accéder à cette section', 'error')
        return
      }
      this.showUsersModal = true
      document.body.style.overflow = 'hidden'
    },

    logout() {
      if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        // ✅ Supprimer également l'authentification IT
        localStorage.removeItem('it_admin_authenticated')
        localStorage.removeItem('it_admin_username')
        localStorage.removeItem('it_admin_login_time')
        localStorage.removeItem('is_super_admin')
        const authStore = useAuthStore()
        authStore.logout()
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.dashboard { display: flex; min-height: 100vh; background: #f5f7fa; }
.sidebar { width: 280px; background: linear-gradient(180deg, #1a472a 0%, #0d3b0f 100%); color: white; position: fixed; height: 100vh; overflow-y: auto; z-index: 100; }
.logo { padding: 30px 20px; font-size: 20px; font-weight: bold; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.logo i { font-size: 28px; color: #FFD700; }
.nav-menu { flex: 1; padding: 20px; display: flex; flex-direction: column; gap: 5px; }
.nav-section { margin-top: 20px; }
.nav-section-title { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); padding: 10px 16px 5px; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; color: rgba(255,255,255,0.8); text-decoration: none; border-radius: 10px; cursor: pointer; background: none; border: none; width: 100%; text-align: left; font-size: 14px; }
.nav-item:hover, .nav-item.active { background: #FFD700; color: #1a472a; }
.logout { margin-top: auto; color: #ff6b6b; }

/* ✅ STYLE BOUTON ADMINISTRATION IT */
.it-admin-btn {
  background: linear-gradient(135deg, rgba(255,215,0,0.12), rgba(255,165,0,0.12));
  border: 1px solid rgba(255,215,0,0.25);
  margin-top: 5px;
  border-radius: 10px;
}

.it-admin-btn:hover {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  color: #1a472a;
}

.it-admin-btn .nav-badge {
  background: #FFD700;
  color: #1a472a;
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 12px;
  margin-left: auto;
}

.main-content { flex: 1; margin-left: 280px; }
.top-bar { background: white; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.top-bar h1 { font-size: 24px; color: #1a472a; margin: 0; }
.user-info { display: flex; align-items: center; gap: 15px; }
.user-badge { background: #e8f5e9; color: #2e7d32; padding: 5px 12px; border-radius: 20px; font-size: 12px; }
.user-badge.super-admin { background: #1a472a; color: #FFD700; }
.avatar { width: 40px; height: 40px; background: linear-gradient(135deg, #32CD32, #228B22); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; }
.content { padding: 30px; }
.loading-container { text-align: center; padding: 60px; }
.spinner { width: 48px; height: 48px; border: 3px solid #e2e8f0; border-top-color: #3498db; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px; }
.btn-add { background: #32CD32; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 8px; }
.btn-add:hover { background: #28a428; }
.btn-add:disabled { opacity: 0.5; cursor: not-allowed; }
.permission-badge { background: #fff3cd; color: #856404; padding: 5px 12px; border-radius: 20px; font-size: 12px; }
.data-section { background: white; border-radius: 20px; padding: 20px; overflow-x: auto; margin-bottom: 30px; }
.data-table { width: 100%; overflow-x: auto; }
.data-table table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; vertical-align: middle; }
.badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; background: #e0e0e0; }
.status-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
.status-badge.active { background: #d4edda; color: #155724; }
.status-badge.inactive { background: #f8d7da; color: #721c24; }
.role-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
.role-badge.it_admin { background: #1a472a; color: #FFD700; }
.role-badge.admin { background: #e3f2fd; color: #1976d2; }
.actions { display: flex; gap: 8px; }
.btn-edit, .btn-delete, .btn-status { background: none; border: none; cursor: pointer; padding: 5px; border-radius: 5px; transition: all 0.2s; }
.btn-edit { color: #2196F3; }
.btn-edit:hover:not(:disabled) { background: #e3f2fd; }
.btn-edit:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-delete { color: #f44336; }
.btn-delete:hover:not(:disabled) { background: #fce4ec; }
.btn-delete:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-status { color: #ff9800; }
.btn-status:hover { background: #fff3e0; }
.empty-row { text-align: center; color: #999; padding: 30px; }

/* Styles pour les images dans les tableaux */
.table-image { width: 50px; height: 50px; cursor: pointer; border-radius: 8px; overflow: hidden; flex-shrink: 0; }
.thumbnail { width: 100%; height: 100%; object-fit: cover; transition: transform 0.2s; }
.thumbnail:hover { transform: scale(1.05); }
.no-image { width: 100%; height: 100%; background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #ccc; font-size: 20px; }

/* Stats */
.stats-section { margin-top: 30px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
.stat-card { background: white; border-radius: 15px; padding: 20px; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.stat-card i { font-size: 30px; color: #32CD32; }
.stat-card h3 { font-size: 24px; margin: 0; color: #1a472a; }
.stat-card p { margin: 0; color: #666; font-size: 12px; }

/* Modal */
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 20px; backdrop-filter: blur(4px); }
.modal-container { background: white; border-radius: 20px; width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; animation: modalSlideIn 0.3s ease; }
@keyframes modalSlideIn { from { transform: translateY(-30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.modal-header { padding: 20px 24px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: white; z-index: 1; border-radius: 20px 20px 0 0; }
.modal-header h2 { margin: 0; font-size: 20px; color: #1a472a; }
.close { background: none; border: none; font-size: 28px; cursor: pointer; color: #999; padding: 0 8px; transition: color 0.3s; }
.close:hover { color: #f44336; transform: rotate(90deg); }
.modal-body { padding: 24px; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; margin-bottom: 6px; font-weight: 500; font-size: 14px; color: #333; }
.form-control { width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; transition: border-color 0.3s; }
.form-control:focus { border-color: #32CD32; outline: none; box-shadow: 0 0 0 3px rgba(50, 205, 50, 0.1); }
.form-checkbox { width: 20px; height: 20px; cursor: pointer; }
.form-help { display: block; color: #888; font-size: 12px; margin-top: 5px; }

/* Upload d'image */
.image-upload-area { border: 2px dashed #ddd; border-radius: 12px; padding: 20px; text-align: center; cursor: pointer; transition: all 0.3s ease; min-height: 150px; display: flex; align-items: center; justify-content: center; }
.image-upload-area:hover { border-color: #32CD32; background: #f8fafc; }
.image-upload-area.has-image { border-color: #32CD32; background: #f8fafc; }
.image-preview { position: relative; width: 100%; max-height: 300px; overflow: hidden; border-radius: 8px; }
.image-preview img { width: 100%; height: auto; max-height: 300px; object-fit: contain; }
.remove-image { position: absolute; top: 10px; right: 10px; width: 30px; height: 30px; background: #e74c3c; color: white; border: none; border-radius: 50%; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; transition: background 0.3s; }
.remove-image:hover { background: #c0392b; }
.upload-placeholder { padding: 20px; }
.upload-placeholder i { font-size: 48px; color: #32CD32; margin-bottom: 10px; }
.upload-hint { display: block; font-size: 12px; color: #999; margin-top: 5px; }

/* Preview d'image plein écran */
.image-preview-modal .image-preview-container { position: relative; max-width: 90vw; max-height: 90vh; }
.image-preview-modal .close-preview { position: absolute; top: -20px; right: -20px; width: 40px; height: 40px; background: rgba(0,0,0,0.7); color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.3s; }
.image-preview-modal .close-preview:hover { background: rgba(0,0,0,0.9); }
.preview-image-full { max-width: 90vw; max-height: 85vh; object-fit: contain; border-radius: 8px; }

.form-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee; }
.btn-save { background: #32CD32; color: white; border: none; padding: 10px 28px; border-radius: 8px; cursor: pointer; font-size: 14px; display: flex; align-items: center; gap: 8px; transition: background 0.3s; }
.btn-save:hover:not(:disabled) { background: #28a428; }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-cancel { background: #f5f5f5; border: 1px solid #ddd; padding: 10px 28px; border-radius: 8px; cursor: pointer; font-size: 14px; transition: background 0.3s; }
.btn-cancel:hover { background: #e8e8e8; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }
.add-user-form { background: #f8f9fa; padding: 20px; border-radius: 15px; margin-bottom: 30px; }
.users-table { overflow-x: auto; }
.users-table table { width: 100%; border-collapse: collapse; }
.users-table th, .users-table td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }

/* Toast */
.toast { position: fixed; bottom: 30px; right: 30px; padding: 14px 24px; border-radius: 12px; z-index: 2000; animation: slideIn 0.3s ease; background: #28a745; color: white; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); font-weight: 500; }
.toast.error { background: #dc3545; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

/* Responsive */
@media (max-width: 768px) { 
  .sidebar { width: 70px; } 
  .logo span, .nav-item span, .nav-section-title { display: none; } 
  .main-content { margin-left: 70px; } 
  .form-row { grid-template-columns: 1fr; }
  .data-table table { font-size: 12px; }
  .data-table th, .data-table td { padding: 8px; }
  .table-image { width: 35px; height: 35px; }
  .top-bar { flex-direction: column; align-items: flex-start; gap: 10px; }
  .section-header { flex-direction: column; align-items: flex-start; }
}
</style>