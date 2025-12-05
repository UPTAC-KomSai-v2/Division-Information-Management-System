<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <!-- Header -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Document Repository</div>
        <div class="text-subtitle1 text-grey-8">A centralized storage hub for securely organizing, and accessing all institutional documents.</div>
      </div>
      <div class="q-mx-md q-mb-md flex flex-center justify-center items-center "  v-if="isAdmin"> 
        <q-btn class="bg-primary text-white" icon="add" style="font-family: Arial, Helvetica, sans-serif;" @click="uploadDoc = true"> Upload File</q-btn>
      </div>
    </div>

    <q-dialog v-model="uploadDoc" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Upload Document</div>
        </q-card-section>

        <q-card-section>
          <q-input class="q-pa-sm" v-model="dname" label="File Name" outlined />
          <q-input class="q-pa-sm" v-model="ddesc" label="File Description" outlined/>
          <q-uploader ref="uploaderRef" class="q-ma-sm full-width" url="http://localhost:4444/upload" label="Upload File" square flat bordered multiple batch no-thumbnails @added="onFileAdded" :auto-upload="false"/>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" v-close-popup @click="resetForm" />
          <q-btn flat label="Add" color="primary" @click="submitDocument" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-card class="no-shadow" style="border: 1px solid var(--q-primary); border-radius: 8px;">
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
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const filter = ref('')

defineProps({
  isAdmin: Boolean
})

// 1. Define Table Columns
const columns = [
  { name: 'filename', required: true, label: 'File Name', align: 'left', field: 'filename', sortable: true },
  { name: 'type', align: 'left', label: 'Type', field: 'type', sortable: true },
  { name: 'access', align: 'left', label: 'Access Status', field: 'access', sortable: true },
  { name: 'actions', align: 'right', label: 'Actions', field: 'actions' }
]

const uploadDoc = ref(false)

const dname = ref('')
const ddesc = ref('')
const fileList = ref([])

function onFileAdded(files) {
  fileList.value = files
}

async function submitDocument() {
  const formData = new FormData()
  formData.append('name', dname.value)
  formData.append('description', ddesc.value)

  fileList.value.forEach(file => {
    formData.append('file', file)   // adjust field name based on your Django serializer
  })

  try {
    await api.post('http://localhost:8000/api/documents/', formData, { //replace with link to your backend endpoint
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // Refresh table after upload
    const response = await api.get('http://localhost:8000/api/documents/') //replace with link to your backend endpoint
    rows.value = response.data

    uploadDoc.value = false
    resetForm()

  } catch (err) {
    console.error("Upload failed:", err)
  }
}


function resetForm() {
  dname.value = ''
  ddesc.value = ''
  fileList.value = []
}

// 2. Define Dummy Data
const rows = ref([])

onMounted(() => {
  api.get('http://localhost:8000/api/documents/')
    .then(response => {
      rows.value = response.data
    })
    .catch(err => {
      console.error("Error loading documents:", err)
    })
})

const uploaderRef = ref(null)

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