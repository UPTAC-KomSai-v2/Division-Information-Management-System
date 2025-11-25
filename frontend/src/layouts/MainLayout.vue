<template>
  <q-layout view="hHh LpR fFf">

    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-icon name="school" class="q-mr-sm"/>
          Division Information Management System
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" overlay bordered >
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Directory',
    icon: 'contacts',
    to: '/app/directory',
  },
  {
    title: 'File Repository',
    icon: 'upload',
    to: '/app/repository',
  },
  {
    title: 'Calendar',
    icon: 'calendar_today',
    to: '/app/calendar',
  },
  {
    title: 'Services',
    icon: 'build',
    to: '/app/services',
  },
  {
    title: 'Settings',
    icon: 'settings',
    to: '/app/settings',
  },
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
