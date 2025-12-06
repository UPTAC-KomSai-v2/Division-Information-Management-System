<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Division Directory</div>
        <div class="text-subtitle1 text-grey-8">A quick-access directory listing all division staff and contact details</div>
      </div>
    </div>

    <q-card class="no-shadow" style="border: 1px solid var(--q-primary); border-radius: 8px;">
      <q-table
        title="Staff Members"
        :rows="rows"
        :columns="columns"
        row-key="id"
        :filter="filter"
        flat
      >
        <template v-slot:top-right>
          <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="row items-center no-wrap bg-white text-black">
              <q-avatar size="40px" class="q-mr-md" :class="props.row.avatarColor">
                <span class="text-weight-bold">{{ props.row.initials }}</span>
              </q-avatar>
              <div>
                <div class="text-weight-bold">{{ props.row.name }}</div>
                <div class="text-caption text-grey">{{ props.row.email }}</div>
              </div>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-role="props">
          <q-td :props="props">
            {{ getRoleLabel(props.row.role) }}
          </q-td>
        </template>

        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-chip
              dense
              :color="getStatusColor(props.row.status).bg"
              :text-color="getStatusColor(props.row.status).text"
              class="text-weight-bold q-px-sm"
            >
              {{ props.row.status }}
            </q-chip>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const filter = ref('')

 defineProps({
    isAdmin: Boolean
  })

// 1. Define Table Columns
const columns = [
  { name: 'name', required: true, label: 'Name', align: 'left', field: 'name', sortable: true },
  { name: 'role', align: 'left', label: 'Role', field: 'role', sortable: true },
  { name: 'status', align: 'left', label: 'Active Status', field: 'status', sortable: true }
]

// ✔ DEFINE IT HERE — nothing above should close `script`
const getRoleLabel = (role) => {
  switch (role) {
    case "ADMIN": return "Division Admin"
    case "STAFF": return "Staff"
    case "FACULTY": return "Faculty / Stakeholder"
    default: return role
  }
}

// 2. Define Dummy Data
const rows = ref([])

onMounted(() => {
  api.get('/api/users/')   // change to your actual endpoint
    .then(res => rows.value = res.data)
    .catch(err => console.error(err))
})

// 3. Helper for Status Colors
const getStatusColor = (status) => {
  switch (status) {
    case 'ACTIVE':
      return { bg: 'green-2', text: 'green-9' }
    case 'INACTIVE':
      return { bg: 'grey-3', text: 'grey-8' }
    case 'ON LEAVE':
      return { bg: 'orange-2', text: 'orange-9' }
    default:
      return { bg: 'grey-2', text: 'black' }
  }
}
</script>
