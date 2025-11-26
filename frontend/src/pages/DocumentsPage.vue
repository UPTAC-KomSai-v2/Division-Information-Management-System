<template>
  <q-page class="q-pa-md">
    <h3 class="q-px-xl text-primary text-weight-bold" style="font-family: Arial, Helvetica, sans-serif;">Document Repository</h3>
    <h6 class="q-px-xl text-black" style="font-family: Arial, Helvetica, sans-serif;">Manage your records and search for other documents</h6>
    <div class="q-mx-xl q-my-md">
      <!-- Search Input -->
      <q-input v-model="search" outlined class="full-width" placeholder="Search publications, awards, memos..." debounce="300" clearable >
        <template #prepend>
          <q-icon name="search" />
        </template>
      </q-input>

      <!-- Tabs -->
      <q-tabs v-model="activeTab" dense class="q-mt-md text-primary" align="left" narrow-indicator>
        <q-tab name="all" label="All" />
        <q-tab name="Publications" label="Publications" />
        <q-tab name="Memos" label="Memos" />
        <q-tab name="Awards" label="Awards" />
        <q-tab name="Miscellaneous" label="Miscellaneous" />
      </q-tabs>

      <!-- Results -->
      <div class="q-mt-md">

        <!-- No results found -->
        <div v-if="filteredResults.length === 0" class="text-grey text-center q-pa-md">
          No results found.
        </div>

        <!-- Result Cards -->
        <q-card v-for="item in filteredResults" :key="item.id" class="q-mb-sm result-card cursor-pointer" @click="goTo(item)" >
          <q-card-section>
            <div class="text-h6">{{ item.name }}</div>
            <div class="text-caption text-grey">{{ item.type }}</div>
          </q-card-section>
        </q-card>

      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'

const search = ref('')
const activeTab = ref('all')
const router = useRouter()

// Example mock data to demonstrate behavior
const results = ref([
  { id: 1, name: 'Memo: Budget 2025', type: 'Memos', route: '/memos/1' },
  { id: 2, name: 'John Santos', type: 'Publications', route: '/pubs/2' },
  { id: 3, name: 'Best Award', type: 'Awards', route: '/awards/112' },
  { id: 4, name: 'Faculty Meeting', type: 'Miscellaneous', route: '/misc/4' }
])

// Filtering based on search term + active tab
const filteredResults = computed(() => {
  return results.value.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(search.value.toLowerCase())

    if (!matchesSearch) return false

    if (activeTab.value === 'all') return true
    return item.type === activeTab.value
  })
})

// Debounce search
let timer = null
watch(search, val => {
  clearTimeout(timer)
  timer = setTimeout(() => console.log('Searching:', val), 300)
})

function goTo(item) {
  router.push(item.route)
}
</script>

<style scoped>
.result-card {
  border: 1px solid #ddd;
  transition: 0.2s;
}

.result-card:hover {
  border-color: var(--q-primary);
  transform: scale(1.01);
}
</style>