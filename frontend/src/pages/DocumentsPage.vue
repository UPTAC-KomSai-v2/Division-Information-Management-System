<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <!-- HEADER -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Document Repository</div>
        <div class="text-subtitle1 text-grey-8">
          Centralized storage for announcements and documents.
        </div>
      </div>

      <!-- Only admin can create announcements -->
      <div class="q-mx-md q-mb-md flex flex-center" v-if="isAdmin">
        <q-btn class="bg-primary text-white" icon="add" @click="openUploadDialog('document')">
          Upload File
        </q-btn>

        <q-btn class="bg-secondary text-white q-ml-sm" icon="campaign" @click="openUploadDialog('announcement')">
          New Announcement
        </q-btn>
      </div>
    </div>

    <!-- UPLOAD DIALOG -->
    <q-dialog v-model="uploadDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section :class="uploadType === 'announcement' ? 'bg-secondary text-white' : 'bg-primary text-white'">
          <div class="text-h6">
            {{ uploadType === 'announcement' ? 'Create Announcement' : 'Upload Document' }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-input class="q-my-sm" v-model="title" label="Title" outlined />
          <q-input
            v-if="uploadType === 'announcement'"
            class="q-my-sm"
            v-model="description"
            label="Description"
            type="textarea"
            outlined
          />
          <q-uploader
            class="q-ma-sm full-width"
            accept="*/*"
            :auto-upload="false"
            :multiple="false"
            :factory="storeFile"
            ref="uploader"
            label="Select File"
            flat
            bordered
            no-thumbnails
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" v-close-popup @click="resetForm" />
          <q-btn flat label="Submit" color="primary" @click="submitFile" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- TABLE -->
    <q-card class="no-shadow" style="border: 1px solid var(--q-primary); border-radius: 8px;">
      <q-tabs v-model="tab" dense class="bg-primary text-white" align="left">
        <q-tab name="documents" label="Documents" />
        <q-tab name="announcements" label="Announcements" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="announcements">
          <q-table title="Announcements" :rows="rows" :columns="columns" row-key="id" :filter="filter" flat>
            <!-- SEARCH -->
            <template v-slot:top-right>
              <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
                <template #append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>

            <!-- TITLE CELL -->
            <template v-slot:body-cell-title="props">
              <q-td clickable @click="openDetails(props.row)" class="cursor-pointer">
                <div class="text-weight-bold">
                  {{ props.row.title }}
                </div>
              </q-td>
            </template>

            <!-- DATE CELL -->
            <template v-slot:body-cell-date="props">
              <q-td>
                {{ formatDate(props.row.created_at) }}
              </q-td>
            </template>

            <!-- ACTIONS CELL -->
            <template v-slot:body-cell-actions="props">
              <q-td>
                <q-btn flat round icon="download" color="primary" @click="downloadFile(props.row)" />

                <q-btn
                  v-if="isAdmin || props.row.type === 'document'"
                  flat round icon="edit" color="green"
                  @click="editFile(props.row)"
                />

                <q-btn
                  v-if="isAdmin"
                  flat round icon="delete" color="red"
                  @click="deleteFile(props.row)"
                />
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>
        <q-tab-panel name="documents">
          <q-table title="Documents" :rows="rows" :columns="columns" row-key="id" :filter="filter" flat>
            <!-- SEARCH -->
            <template v-slot:top-right>
              <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
                <template #append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>

            <!-- TITLE CELL -->
            <template v-slot:body-cell-title="props">
              <q-td clickable @click="openDetails(props.row)" class="cursor-pointer">
                <div class="text-weight-bold">
                  {{ props.row.title }}
                </div>
              </q-td>
            </template>

            <!-- DATE CELL -->
            <template v-slot:body-cell-date="props">
              <q-td>
                {{ formatDate(props.row.created_at) }}
              </q-td>
            </template>

            <!-- ACTIONS CELL -->
            <template v-slot:body-cell-actions="props">
              <q-td>
                <q-btn flat round icon="download" color="primary" @click="downloadFile(props.row)" />

                <q-btn
                  v-if="isAdmin || props.row.type === 'document'"
                  flat round icon="edit" color="green"
                  @click="editFile(props.row)"
                />

                <q-btn
                  v-if="isAdmin"
                  flat round icon="delete" color="red"
                  @click="deleteFile(props.row)"
                />
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>

    <!-- DETAILS DIALOG -->
    <q-dialog v-model="detailsDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ selectedFile.title }}</div>
          <div class="text-caption">
            Uploaded: {{ formatDate(selectedFile.created_at) }}
          </div>
          <div class="q-mt-sm">{{ selectedFile.description }}</div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat icon="download" color="primary" @click="downloadFile(selectedFile)" label="Download" />
          <q-btn flat icon="close" color="secondary" v-close-popup label="Close" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { api } from "boot/axios"

defineProps({ isAdmin: Boolean })

/* --------------------------- TABLE SETUP --------------------------- */
const filter = ref("")
const rows = ref([])

const columns = [
  { name: "title", label: "Title", field: "title", align: "left", sortable: true },
  { name: "date", label: "Date Uploaded", field: "created_at", align: "left", sortable: true },
  { name: "actions", label: "Actions", field: "actions", align: "right" }
]

/* --------------------------- UPLOAD --------------------------- */
const uploadDialog = ref(false)
const uploadType = ref("document") // document | announcement
const title = ref("")
const description = ref("")
const uploader = ref(null)
const selectedFile = ref(null)
const detailsDialog = ref(false)
const tab = ref('announcements')

function openUploadDialog(type) {
  uploadType.value = type
  uploadDialog.value = true
}

function resetForm() {
  title.value = ""
  description.value = ""
  uploader.value?.reset()
}

function storeFile(files) {
  return files
}

async function submitFile() {
  const form = new FormData()

  form.append("title", title.value)
  form.append("file", uploader.value.files[0])

  if (uploadType.value === "announcement") {
    form.append("description", description.value)
    form.append("type", "announcement")
  } else {
    form.append("type", "document")
  }

  try {
    await api.post("/api/files/", form)
    loadFiles()
    uploadDialog.value = false
    resetForm()
  } catch (err) {
    console.error("UPLOAD ERROR:", err)
  }
}

/* --------------------------- DETAILS --------------------------- */
function openDetails(row) {
  selectedFile.value = row
  detailsDialog.value = true
}

/* --------------------------- ACTIONS --------------------------- */
function downloadFile(row) {
  window.open(row.file_url, "_blank")
}

function editFile(row) {
  console.log("Edit:", row)
}

function deleteFile(row) {
  console.log("Delete:", row)
}

/* --------------------------- LOAD --------------------------- */
async function loadFiles() {
  try {
    const res = await api.get("/api/files/")
    rows.value = res.data
  } catch (err) {
    console.error("LOAD ERROR:", err)
  }
}

onMounted(() => loadFiles())

/* --------------------------- HELPERS --------------------------- */
function formatDate(date) {
  return new Date(date).toLocaleDateString()
}
</script>