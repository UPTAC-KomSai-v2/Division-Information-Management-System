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
    link: 'https://quasar.dev',
  },
  {
    title: 'Upload Resources',
    icon: 'upload',
    link: 'https://github.com/quasarframework',
  },
  {
    title: 'Calendar',
    icon: 'calendar_today',
    link: 'https://chat.quasar.dev',
  },
  {
    title: 'Services',
    icon: 'build',
    link: 'https://forum.quasar.dev',
  },
  {
    title: 'Feed',
    icon: 'web_stories',
    link: 'https://twitter.quasar.dev',
  },
  {
    title: 'Analytics',
    icon: 'analytics',
    link: 'https://facebook.quasar.dev',
  },
  {
    title: 'Search',
    icon: 'search',
    link: 'https://awesome.quasar.dev',
  },
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
