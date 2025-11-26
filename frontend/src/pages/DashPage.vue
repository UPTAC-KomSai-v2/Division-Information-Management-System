<template>
  <q-page class="q-pa-md">
    <h3 class="q-px-xl text-primary text-weight-bold" style="font-family: Arial, Helvetica, sans-serif;">Welcome to DIMS!</h3>
    <h6 class="q-px-xl text-black" style="font-family: Arial, Helvetica, sans-serif;">The Division Information Management System</h6>
    <div class="q-mx-xl q-my-md" style="border: 1px solid var(--q-primary);">
      <!-- Search Input -->
      <q-input v-model="search" outlined class="full-width" placeholder="Search documents, people, tickets..." debounce="300" clearable >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>
      <div class="q-my-md" style="border: 1px solid var(--q-primary);">

      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, watch } from 'vue'

const search = ref('')

let timer = null
watch(search, val => {
  clearTimeout(timer)
  timer = setTimeout(() => console.log('Searching:', val), 300)
})
</script>
