<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <div class="q-mb-lg">
      <div class="text-h4 text-weight-bold text-primary">Document Repository</div>
      <div class="text-subtitle1 text-grey-8"> A centralized storage hub for securely organizing, and accessing all institutional documents.</div>
    </div>

    <q-card class="no-shadow" style="border: 1px solid var(--q-primary);">
      <q-table
        title="Documents"
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
            <div class="row items-center no-wrap">
              <div class="text-weight-bold">{{ props.row.name }}</div>
              <div class="text-caption text-grey">{{ props.row.email }}</div>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-access="props">
          <q-td :props="props">
            <q-chip
              dense
              :color="getAccessColor(props.row.access).bg"
              :text-color="getAccessColor(props.row.access).text"
              class="text-weight-bold q-px-sm"
            >
              {{ props.row.access }}
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn flat round color=primary icon="open_in_new" size="sm" class="q-mr-sm" />
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
  { name: 'type', align: 'left', label: 'Type', field: 'type', sortable: true },
  { name: 'access', align: 'left', label: 'Access Status', field: 'access', sortable: true },
  { name: 'actions', align: 'right', label: 'Actions', field: 'actions' }
]

// 2. Define Dummy Data
const rows = [
  {
    id: 1,
    name: 'John Doe',
    type: 'Publication',
    access: 'Restricted'
  },
  {
    id: 2,
    name: 'Sarah Smith',
    type: 'Memos',
    access: 'Public'
  },
  {
    id: 3,
    name: 'Michael Brown',
    type: 'Memos',
    access: 'Public'
  },
  {
    id: 4,
    name: 'Emily White',
    type: 'Awards',
    access: 'Restricted'
  },
  {
    id: 5,
    name: 'David Lee',
    type: 'Publication',
    access: 'Permitted'
  }
]

// 3. Helper for Access Colors
const getAccessColor = (access) => {
  switch (access) {
    case 'Public':
      return { bg: 'green-2', text: 'green-9' }
    case 'Permitted':
      return { bg: 'blue-2', text: 'blue-9' }
    case 'Restricted':
      return { bg: 'red-2', text: 'red-9' }
    default:
      return { bg: 'grey-2', text: 'black' }
  }
}
</script>