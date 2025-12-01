<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <div class="q-mb-lg">
      <div class="text-h4 text-weight-bold text-primary">Division Directory</div>
      <div class="text-subtitle1 text-grey-8">
        Manage employee access, update roles, and view current status of all division staff members.
      </div>
    </div>

    <q-card class="no-shadow" style="border: 1px solid var(--q-primary);">
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
          
          <q-btn
            color= primary
            icon="add"
            label="Add User"
            class="q-ml-md"
            unelevated
            no-caps
          />
        </template>

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
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

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn flat round color="grey-7" icon="edit" size="sm" class="q-mr-sm" />
            <q-btn flat round color="red-10" icon="delete" size="sm" />
          </q-td>
        </template>

      </q-table>
    </q-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const filter = ref('')

// 1. Define Table Columns
const columns = [
  { name: 'name', required: true, label: 'Name', align: 'left', field: 'name', sortable: true },
  { name: 'role', align: 'left', label: 'Role', field: 'role', sortable: true },
  { name: 'status', align: 'left', label: 'Active Status', field: 'status', sortable: true },
  { name: 'actions', align: 'right', label: 'Actions', field: 'actions' }
]

// 2. Define Dummy Data
const rows = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@division.gov',
    initials: 'JD',
    avatarColor: 'bg-red-2 text-red-10',
    role: 'Administrator',
    status: 'Active'
  },
  {
    id: 2,
    name: 'Sarah Smith',
    email: 's.smith@division.gov',
    initials: 'SS',
    avatarColor: 'bg-orange-2 text-orange-10',
    role: 'Project Manager',
    status: 'Active'
  },
  {
    id: 3,
    name: 'Michael Brown',
    email: 'm.brown@division.gov',
    initials: 'MB',
    avatarColor: 'bg-grey-3 text-grey-8',
    role: 'Field Officer',
    status: 'Inactive'
  },
  {
    id: 4,
    name: 'Emily White',
    email: 'e.white@division.gov',
    initials: 'EW',
    avatarColor: 'bg-blue-2 text-blue-10',
    role: 'Analyst',
    status: 'On Leave'
  },
  {
    id: 5,
    name: 'David Lee',
    email: 'd.lee@division.gov',
    initials: 'DL',
    avatarColor: 'bg-green-2 text-green-10',
    role: 'Viewer',
    status: 'Active'
  }
]

// 3. Helper for Status Colors
const getStatusColor = (status) => {
  switch (status) {
    case 'Active':
      return { bg: 'green-2', text: 'green-9' }
    case 'Inactive':
      return { bg: 'grey-3', text: 'grey-8' }
    case 'On Leave':
      return { bg: 'orange-2', text: 'orange-9' }
    default:
      return { bg: 'grey-2', text: 'black' }
  }
}
</script>