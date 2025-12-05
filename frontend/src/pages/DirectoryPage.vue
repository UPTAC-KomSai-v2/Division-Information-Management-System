<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Division Directory</div>
        <div class="text-subtitle1 text-grey-8">A quick-access directory listing all division staff and contact details</div>
      </div>
      <div class="q-mx-md q-mb-md flex flex-center justify-center items-center"  v-if="isAdmin"> 
        <q-btn class="bg-primary text-white" icon="add" style="font-family: Arial, Helvetica, sans-serif;" @click="addUserDialog = true" label="Add User"/>
      </div>
    </div>

    <q-dialog v-model="addUserDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6 ">Add User</div>
        </q-card-section>

        <q-card-section>
          <q-input class="q-pa-sm" v-model="fname" label="First Name" outlined />
          <q-input class="q-pa-sm" v-model="lname" label="Last Name" outlined />
          <q-input class="q-pa-sm" v-model="email" label="Email" outlined />
          <q-select class="q-pa-sm" outlined v-model="role" :options="roles" label="Role"/>
          <q-select class="q-pa-sm" outlined v-model="dept" :options="depts" label="Department"/>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" v-close-popup @click="resetForm" />
          <q-btn flat label="Add" color="primary" @click="submitUser" />
        </q-card-actions>
      </q-card>
    </q-dialog>

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
            <q-btn flat round color=primary icon="message" size="sm" class="q-mr-sm" />
            <q-btn flat round color=primary icon="edit_square" size="sm" class="q-mr-sm" v-if="isAdmin"/>
            <q-btn flat round color=primary icon="delete" size="sm" class="q-mr-sm" v-if="isAdmin"/>
          </q-td>
        </template>

      </q-table>
    </q-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const roles = [ 'Division Admin', 'Staff', 'Faculty']
const depts = [ 'Computer Science', 'Applied Mathematics', 'Biology', 'MS Environmental Science' ]

const filter = ref('')

 defineProps({
    isAdmin: Boolean
  })

// 1. Define Table Columns
const columns = [
  { name: 'name', required: true, label: 'Name', align: 'left', field: 'name', sortable: true },
  { name: 'role', align: 'left', label: 'Role', field: 'role', sortable: true },
  { name: 'status', align: 'left', label: 'Active Status', field: 'status', sortable: true },
  { name: 'actions', align: 'right', label: 'Actions', field: 'actions' }
]

// 2. Define Dummy Data
const rows = ref([])

onMounted(() => {
  api.get('http://localhost:8000/api/directory/')   // change to your actual endpoint
    .then(res => rows.value = res.data)
    .catch(err => console.error(err))
})


const addUserDialog = ref(false)

const fname = ref('')
const lname = ref('')
const email = ref('')
const role = ref('')
const dept = ref('')

async function submitUser() {
  try {
    const payload = {
      fname: fname.value,
      lname: lname.value,
      email: email.value,
      role: role.value,
      dept: dept.value
    }

    await api.post("http://localhost:8000/api/directory/", payload)

    // refresh the table
    const res = await api.get("http://localhost:8000/api/directory/")
    rows.value = res.data

    addUserDialog.value = false
    resetForm()

  } catch (err) {
    console.error("Failed to add user:", err)
  }
}


function resetForm() {
  fname.value = ''
  lname.value = ''
  email.value = ''
  role.value = ''
  dept.value = ''
}

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