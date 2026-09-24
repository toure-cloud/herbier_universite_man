<template>
  <aside class="sidebar" :class="{ collapsed, superit: reallySuperIT }">
    <div class="sidebar-header">
      <div class="logo">
        <div class="logo-icon" :class="{ it: reallySuperIT }">
          <i :class="reallySuperIT ? 'fas fa-shield-alt' : 'fas fa-leaf'"></i>
        </div>
        <div v-if="!collapsed" class="logo-text">
          <span class="logo-title">{{ reallySuperIT ? 'SuperIT' : 'Herbier Admin' }}</span>
          <span class="logo-subtitle">{{ reallySuperIT ? 'Console système' : 'Université de Man' }}</span>
        </div>
      </div>
      <button class="toggle-btn" @click="$emit('toggle')" aria-label="Basculer">
        <i :class="collapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
      </button>
    </div>

    <nav class="sidebar-nav">
      <template v-for="item in menuItems" :key="item.to">
        <router-link :to="item.to" class="nav-item" active-class="active">
          <i :class="item.icon"></i>
          <span v-if="!collapsed">{{ item.label }}</span>
          <span v-if="item.badge && !collapsed" class="nav-badge">{{ item.badge }}</span>
        </router-link>
      </template>
    </nav>

    <div class="sidebar-footer">
      <div v-if="!collapsed" class="user-info">
        <div class="user-avatar" :class="{ it: reallySuperIT }">{{ initials }}</div>
        <div class="user-details">
          <span class="user-name">{{ user?.nom || 'Utilisateur' }}</span>
          <span class="user-role">{{ reallySuperIT ? 'SuperIT' : 'Administrateur' }}</span>
        </div>
      </div>
      <button class="logout-btn" @click="$emit('logout')">
        <i class="fas fa-sign-out-alt"></i>
        <span v-if="!collapsed">Déconnexion</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: Object,
  isSuperIT: Boolean,
  collapsed: Boolean,
})

defineEmits(['toggle', 'logout'])

// ✅ Calcul robuste : accepte la prop OU le rôle du user
//    Évite un menu réduit si un parent oublie de passer :is-super-it
const reallySuperIT = computed(() => {
  if (props.isSuperIT === true) return true
  const r = (props.user?.role || '').trim().toLowerCase()
  return r === 'it_admin' || r === 'it-admin' || r === 'super_admin' || r === 'superit'
})

const initials = computed(() => {
  if (!props.user?.nom) return '?'
  return props.user.nom.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2)
})

// ============================================================
// ✅ MENU ADAPTÉ AU RÔLE
// ============================================================
const menuItems = computed(() => {
  // ✅ Éléments communs (Admin + SuperIT)
  const common = [
    { to: '/dashboard', label: 'Tableau de bord', icon: 'fas fa-tachometer-alt' },
  ]

  // ✅ Contenu accessible aux DEUX rôles
  const content = [
    { to: '/plantes', label: 'Plantes', icon: 'fas fa-leaf' },
    { to: '/projets', label: 'Projets', icon: 'fas fa-project-diagram' },
    { to: '/activites', label: 'Activités', icon: 'fas fa-chart-line' },
    { to: '/publications', label: 'Publications', icon: 'fas fa-book' },
    { to: '/temoignages', label: 'Témoignages', icon: 'fas fa-comment-dots' },
  ]

  // ✅ Exclusivités SuperIT (jamais visibles pour Admin)
  const superitOnly = [
    { to: '/equipe', label: 'Équipe', icon: 'fas fa-users' },
    { to: '/partenaires', label: 'Partenaires', icon: 'fas fa-handshake' },
    { to: '/administrateurs', label: 'Administrateurs', icon: 'fas fa-users-cog' },
    { to: '/audit', label: "Journal d'audit", icon: 'fas fa-history', badge: 'Live' },
    { to: '/maintenance', label: 'Maintenance', icon: 'fas fa-tools' },
    { to: '/herbier-data', label: 'Données Herbier', icon: 'fas fa-database' },
    { to: '/stats', label: 'Statistiques', icon: 'fas fa-chart-bar' },
    { to: '/messages', label: 'Messages', icon: 'fas fa-envelope', badge: 'Live' },
  ]

  const commonFooter = [
    { to: '/settings', label: 'Paramètres', icon: 'fas fa-cog' },
  ]

  // ✅ Admin Lambda : uniquement commun + contenu
  if (!reallySuperIT.value) {
    return [...common, ...content]
  }

  // ✅ SuperIT : tout
  return [...common, ...content, ...superitOnly, ...commonFooter]
})
</script>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 100;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
}
/* ✅ Thème indigo pour SuperIT */
.sidebar.superit {
  background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
}
.sidebar.collapsed { width: 76px; }

.sidebar-header {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.logo { display: flex; align-items: center; gap: 12px; overflow: hidden; }
.logo-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #10b981, #059669);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
}
/* ✅ Icône indigo pour SuperIT */
.logo-icon.it {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}
.logo-icon i { color: #fff; font-size: 18px; }
.logo-text { display: flex; flex-direction: column; white-space: nowrap; }
.logo-title { font-weight: 700; font-size: 14px; color: #fff; }
.logo-subtitle { font-size: 10px; color: rgba(255, 255, 255, 0.5); }

.toggle-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  border-radius: 6px;
  padding: 4px 8px;
  cursor: pointer;
}
.toggle-btn:hover { background: rgba(255, 255, 255, 0.08); }

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 500;
  transition: all 0.15s;
  white-space: nowrap;
}
.nav-item i { width: 18px; text-align: center; font-size: 15px; }
.nav-item:hover { background: rgba(255, 255, 255, 0.06); color: #fff; }

/* ✅ Émeraude (Admin) */
.nav-item.active {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  font-weight: 600;
  box-shadow: inset 3px 0 0 #10b981;
}

/* ✅ Indigo (SuperIT) */
.sidebar.superit .nav-item.active {
  background: rgba(99, 102, 241, 0.2);
  color: #c7d2fe;
  box-shadow: inset 3px 0 0 #818cf8;
}
.sidebar.superit .nav-item:hover {
  background: rgba(99, 102, 241, 0.12);
  color: #e0e7ff;
}

.nav-badge {
  margin-left: auto;
  font-size: 10px;
  background: #f59e0b;
  color: #1a1a1a;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 700;
  animation: pulse-badge 2s infinite;
}
@keyframes pulse-badge {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 10px;
  overflow: hidden;
}
.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
}
.user-avatar.it { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.user-details { display: flex; flex-direction: column; overflow: hidden; }
.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-role { font-size: 10px; color: rgba(255, 255, 255, 0.5); }

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #f87171;
  cursor: pointer;
  font-weight: 500;
  font-size: 13px;
  transition: all 0.15s;
}
.logout-btn:hover { background: rgba(239, 68, 68, 0.2); color: #fecaca; }
</style>