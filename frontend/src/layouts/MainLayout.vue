<template>
  <q-layout view="hHh LpR fFf">

    <q-header elevated class="bg-white text-primary">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title class="row items-center">
          <q-btn flat no-caps dense class="row items-center" @click="$router.push('/app/dashboard')">
            <img alt="DIMS logo" src="~assets/dims.png" style="width: 40px; height: 40px" />
          </q-btn>
        </q-toolbar-title>

        <q-btn
          dense
          flat
          round
          icon="chat"
          class="q-mr-xs"
          @click="$router.push('/app/messages')"
        >
          <q-badge v-if="unreadCount" color="negative" floating>{{ unreadCount }}</q-badge>
        </q-btn>

        <q-btn-dropdown class="q-mx-xs" dense flat round icon="person" >
          <div class="column items-center q-pa-sm q-ma-sm">
            <q-avatar size="72px">
              <img src="~assets/dims_mini.png">
            </q-avatar>

            <div class="text-subtitle1 q-my-sm"> {{ currentUserName }}</div>
            <q-btn class="full-width q-my-xs" color="primary" label="Profile" @click="$router.push('/app/profile')"/>
            <q-btn class="full-width q-my-xs" color="secondary" label="Logout" @click="logout"/>
          </div>
        </q-btn-dropdown>

      </q-toolbar>
    </q-header>

    <q-drawer class="bg-primary text-white" v-model="leftDrawerOpen" side="left" behavior="desktop" overlay bordered >
      <q-list>
        <q-item-label class="text-accent" header> Quick Links</q-item-label>
        <EssentialLink v-for="link in filteredLinks" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

<q-page-container>
      <router-view :is-admin="isAdmin" :user-role="role" />
    </q-page-container>

  </q-layout>
</template>

<style>
.q-drawer .q-router-link--active {
  background: var(--q-secondary) !important; /* your secondary color */
  border-radius: 6px;
}

/* text + icon color when active */
.q-drawer .q-router-link--active .q-item__label,
.q-drawer .q-router-link--active .q-icon {
  color: var(--q-accent) !important; /* your secondary color */
}

/* optional hover for non-active items */
.q-drawer .q-item:hover:not(.q-router-link--active) {
  color: var(--q-accent) !important; 
}
</style>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'
import EssentialLink from 'components/EssentialLink.vue'

const messages = ref([])
const router = useRouter()

// Normalize role string; fallback to STAFF so basic links remain usable
const role = ref((localStorage.getItem('role') || 'STAFF').toUpperCase())
const isAdmin = computed(() => role.value === 'ADMIN')

const unreadCount = computed(() => messages.value.filter((m) => m.unread).length)

// Link definitions with allowedRoles for simple role-based filtering
const linksList = [
  { title: 'Calendar', icon: 'calendar_today', to: '/app/calendar', allowedRoles: ['ADMIN', 'STAFF', 'FACULTY'] },
  { title: 'Directory', icon: 'contacts', to: '/app/directory', allowedRoles: ['ADMIN', 'STAFF'] },
  { title: 'Documents Repository', icon: 'library_books', to: '/app/documents', allowedRoles: ['ADMIN', 'STAFF', 'FACULTY'] },
  { title: 'Services Center', icon: 'build', to: '/app/services', allowedRoles: ['ADMIN', 'STAFF'] },
]

const filteredLinks = computed(() =>
  linksList.filter((link) => !link.allowedRoles || link.allowedRoles.includes(role.value)),
)

const leftDrawerOpen = ref(false)
const currentUserName = ref('User')

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function deriveDisplayName(payload) {
  if (!payload) return null
  const first = (payload.first_name || '').trim()
  const last = (payload.last_name || '').trim()
  if (first || last) return `${first} ${last}`.trim()
  if (payload.name) return String(payload.name).trim()
  if (payload.username) return String(payload.username).trim()
  const email = (payload.email || '').trim()
  if (email && email.includes('@')) return email.split('@')[0]
  return email || null
}

// read username/role from localStorage when layout loads
onMounted(() => {
  const storedName = localStorage.getItem('username')
  if (storedName) {
    currentUserName.value = storedName
  }
  const storedRole = localStorage.getItem('role')
  if (storedRole) {
    role.value = storedRole.toUpperCase()
  }

  // attempt to refresh user info from backend
  const token = localStorage.getItem('access')
  if (token) {
    api
      .get('/api/auth/me/', { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => {
        const data = res.data || {}
        const displayName = deriveDisplayName(data)
        currentUserName.value = displayName || currentUserName.value
        if (data.role) {
          role.value = String(data.role).toUpperCase()
          localStorage.setItem('role', role.value)
        }
        if (displayName) {
          localStorage.setItem('username', displayName)
        }
      })
      .catch(() => {
        // ignore; fall back to stored values
      })
  }
})

function logout() {
  // clear client auth data
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('username')
  localStorage.removeItem('role')

  router.push('/login')
}
</script>
