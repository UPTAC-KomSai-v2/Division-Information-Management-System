<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <div class="q-mb-lg">
      <div class="text-h4 text-weight-bold text-primary">Welcome to DIMS</div>
      <div class="text-subtitle1 text-grey-8">Division Information Management System</div>
    </div>
    <div style="border: 1px solid var(--q-primary);">
      <!-- Search Input -->
      <q-input v-model="search" outlined class="full-width" placeholder="Search documents, people, tickets..." debounce="300" clearable >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>
      <div class="q-my-md" style="border: 1px solid var(--q-primary);">

      </div>
    </div>
  </div>
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
