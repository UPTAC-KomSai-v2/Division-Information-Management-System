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
        >
          <q-badge v-if="unreadCount" color="negative" floating>{{ unreadCount }}</q-badge>
          <q-menu anchor="bottom right" self="top right">
            <q-list style="min-width: 260px">
              <q-item v-for="msg in messages" :key="msg.id" clickable>
                <q-item-section avatar>
                  <q-avatar :color="msg.avatarColor" text-color="black">
                    <span class="text-weight-bold">{{ msg.initials }}</span>
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <div class="row items-center justify-between">
                    <div class="text-weight-bold">{{ msg.from }}</div>
                    <span class="text-caption text-grey">{{ msg.time }}</span>
                  </div>
                  <div class="text-body2 ellipsis">{{ msg.preview }}</div>
                </q-item-section>
                <q-item-section side>
                  <q-badge v-if="msg.unread" color="secondary" />
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable @click="$router.push('/app/messages')">
                <q-item-section class="text-primary text-weight-bold">View all messages</q-item-section>
                <q-item-section side>
                  <q-icon name="chevron_right" />
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>

        <q-btn-dropdown class="q-mx-xs" dense flat round icon="person" >
          <div class="column items-center q-pa-sm q-ma-sm">
            <q-avatar size="72px">
              <img src="~assets/dims_mini.png">
            </q-avatar>

            <div class="text-subtitle1 q-my-sm"> {{ currentUserName }}</div>
            <q-btn class="full-width q-my-xs" color="primary" label="Profile" @click="$router.push('/app/Profile')"/>
            <q-btn class="full-width q-my-xs" color="secondary" label="Logout" @click="$router.push('/login')"/>
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
  color: var(--q-accent) !important; 
}
</style>


<script setup>
import { ref, computed } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

//const userRole = ref('admin') // replace with auth logic

const messages = ref([
  {
    id: 1,
    from: 'Sarah Smith',
    preview: 'Can you review the updated roster before noon?',
    time: '09:20 AM',
    initials: 'SS',
    avatarColor: 'bg-orange-2 text-orange-10',
    unread: true
  },
  {
    id: 2,
    from: 'Operations Leads',
    preview: 'Reminder: inspection team is on campus Thursday.',
    time: 'Yesterday',
    initials: 'OL',
    avatarColor: 'bg-green-2 text-green-10',
    unread: false
  },
  {
    id: 3,
    from: 'Helpdesk',
    preview: 'Ticket #TCK-004 has been closed.',
    time: 'Mon',
    initials: 'HD',
    avatarColor: 'bg-blue-2 text-blue-10',
    unread: false
  }
])

const unreadCount = computed(() => messages.value.filter(m => m.unread).length)

const linksList = [
  {title: 'Calendar', icon: 'calendar_today', to: '/app/calendar'},
  {title: 'Directory', icon: 'contacts', to: '/app/directory'},
  {title: 'Documents Repository', icon: 'library_books', to: '/app/documents'},
  {title: 'Services Center', icon: 'build', to: '/app/services',},
]

const leftDrawerOpen = ref(false)
const currentUserName = ref('User')

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
