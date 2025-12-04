<template>
  <q-layout view="hHh LpR fFf">

    <q-header elevated class="bg-white text-primary">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title class="row items-center">
          <q-btn flat no-caps dense class="row items-center" @click="$router.push('/app/dashboard')">
            <img class="q-mr-sm" alt="DIMS logo" src="~assets/dims.png" style="width: 40px; height: 40px" />
            Division Information <br/> Management System
          </q-btn>
        </q-toolbar-title>

        <q-btn-dropdown class="q-mx-xs" dense flat round icon="person" >
          <div class="column items-center q-pa-sm q-ma-sm">
            <q-avatar size="72px">
              <img src="~assets/dims_mini.png">
            </q-avatar>

<<<<<<< HEAD
            <div class="text-subtitle1 q-my-sm"> {{ currentUserName }}</div>
=======
            <div class="text-subtitle1 q-my-sm">John Doe</div>
            <q-toggle v-model="activeStatus" label="Active Status" />
>>>>>>> main
            <q-btn class="full-width q-my-xs" color="primary" label="Profile" @click="$router.push('/login')"/>
            <q-btn class="full-width q-my-xs" color="secondary" label="Logout" @click="logout" />
          </div>
        </q-btn-dropdown>

      </q-toolbar>
    </q-header>

    <q-drawer class="bg-primary text-white" v-model="leftDrawerOpen" side="left" behavior="desktop" overlay bordered >
      <q-list>
        <q-item-label class="text-accent" header> Quick Links</q-item-label>
        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
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
  background: var(--q-primary-lighten2) !important;
}
</style>


<script setup>
<<<<<<< HEAD
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import EssentialLink from 'components/EssentialLink.vue'

const router = useRouter()

const linksList = [
   {
    title: 'Calendar',
    icon: 'calendar_today',
    to: '/app/calendar',
  },
  {
    title: 'Directory',
    icon: 'contacts',
    to: '/app/directory',
  },
  {
    title: 'Documents Repository',
    icon: 'library_books',
    to: '/app/documents',
  },
  {
    title: 'Services Center',
    icon: 'build',
    to: '/app/services',
  },
=======
import { ref, computed } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const userRole = ref('admin') // replace with auth logic

const baseLinks = [
  {title: 'Calendar', icon: 'calendar_today', to: '/app/calendar'},
  {title: 'Directory', icon: 'contacts', to: '/app/directory'},
  {title: 'Documents Repository', icon: 'library_books', to: '/app/documents'},
  {title: 'Services Center', icon: 'build', to: '/app/services',},
>>>>>>> main
]

const linksList = computed(() => {
  const links = [...baseLinks]

  if (userRole.value === 'admin') {
    links.push({
      title: 'Admin Panel',
      icon: 'admin_panel_settings',
      to: '/app/admin'
    })
  }

  return links
})

const leftDrawerOpen = ref(false)
<<<<<<< HEAD
const currentUserName = ref('User') // default fallback
=======
const activeStatus = ref(false)
>>>>>>> main

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

// read username from localStorage when layout loads
onMounted(() => {
  const storedName = localStorage.getItem('username')
  if (storedName) {
    currentUserName.value = storedName
  }
})

function logout () {
  // clear client auth data
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('username')

  router.push('/login')
}
</script>
