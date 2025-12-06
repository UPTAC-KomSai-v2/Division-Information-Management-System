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

      <!-- Upload documents: all users; announcements: admin only -->
      <div class="q-mx-md q-mb-md flex flex-center">
        <q-btn class="bg-primary text-white q-ma-sm" icon="add" @click="openUploadDialog('document')">
          Upload File
        </q-btn>

        <q-btn
          v-if="isAdmin"
          class="bg-secondary text-white q-ma-sm"
          icon="campaign"
          @click="openUploadDialog('announcement')"
        >
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
            class="q-my-sm"
            v-model="description"
            label="Description"
            type="textarea"
            outlined
            autogrow
            maxlength="500"
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
          <q-table title="Announcements" :rows="memos" :columns="columns" row-key="id" :filter="filterMemos" flat>
            <!-- SEARCH -->
            <template v-slot:top-right>
              <q-input borderless dense debounce="300" v-model="filterMemos" placeholder="Search">
                <template #append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>

            <!-- TITLE CELL -->
            <template v-slot:body-cell-title="props">
              <q-td clickable @click="openDetails(props.row)" class="cursor-pointer">
                <div class="text-weight-bold">
                  {{ props.row.name || props.row.title }}
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-description="props">
              <q-td>
                <div class="ellipsis">{{ props.row.description }}</div>
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
              <q-td class="text-center">
                <q-btn
                  flat
                  round
                  icon="download"
                  color="primary"
                  :disable="!props.row.file_url"
                  @click="downloadFile(props.row)"
                />

                <q-btn
                  v-if="isAdmin"
                  flat round icon="edit" color="green"
                  @click="editMemo(props.row)"
                />

                <q-btn
                  v-if="isAdmin"
                  flat round icon="delete" color="red"
                  @click="deleteMemo(props.row)"
                />
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>
        <q-tab-panel name="documents">
          <q-table title="Documents" :rows="documents" :columns="columns" row-key="id" :filter="filterDocuments" flat>
            <!-- SEARCH -->
            <template v-slot:top-right>
              <q-input borderless dense debounce="300" v-model="filterDocuments" placeholder="Search">
                <template #append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>

            <!-- TITLE CELL -->
            <template v-slot:body-cell-title="props">
              <q-td clickable @click="openDetails(props.row)" class="cursor-pointer">
                <div class="text-weight-bold">
                  {{ props.row.name || props.row.title }}
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-description="props">
              <q-td>
                <div class="ellipsis">{{ props.row.description }}</div>
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
              <q-td class="text-center">
                <q-btn
                  flat
                  round
                  icon="download"
                  color="primary"
                  :disable="!props.row.file_url"
                  @click="downloadFile(props.row)"
                />

                <q-btn
                  v-if="isAdmin"
                  flat round icon="edit" color="green"
                  @click="editDocument(props.row)"
                />

                <q-btn
                  v-if="isAdmin"
                  flat round icon="delete" color="red"
                  @click="deleteDocument(props.row)"
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
const filterDocuments = ref("")
const filterMemos = ref("")
const documents = ref([])
const memos = ref([])

const columns = [
  { name: "title", label: "Title", field: "name", align: "left", sortable: true },
  { name: "description", label: "Description", field: "description", align: "left" },
  { name: "date", label: "Date Uploaded", field: "created_at", align: "left", sortable: true },
  { name: "actions", label: "Actions", field: "actions", align: "center", headerClasses: 'text-center' }
]

/* --------------------------- UPLOAD --------------------------- */
const uploadDialog = ref(false)
const uploadType = ref("document") // document | announcement
const title = ref("")
const description = ref("")
const uploader = ref(null)
const selectedFile = ref(null)
const detailsDialog = ref(false)
const tab = ref('documents')

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
  try {
    if (uploadType.value === "announcement") {
      const form = new FormData()
      const fileEntry = uploader.value?.files?.[0]
      const nativeFile = fileEntry?.__nativeFile || fileEntry
      form.append("title", title.value)
      form.append("description", description.value)
      if (nativeFile) {
        form.append("file", nativeFile, nativeFile.name)
      }
      await api.post("/api/memos/", form)
      await loadMemos()
    } else {
      const form = new FormData()
      const fileEntry = uploader.value?.files?.[0]
      const nativeFile = fileEntry?.__nativeFile || fileEntry
      if (!nativeFile) {
        console.error("UPLOAD ERROR: No file selected")
        return
      }
      form.append("name", title.value)
      form.append("file", nativeFile, nativeFile.name)
      if (description.value) {
        form.append("description", description.value)
      }

      await api.post("/api/documents/", form)
      await loadDocuments()
    }
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
  if (!row?.file_url) {
    // no attachment available for this item
    return
  }
  window.open(row.file_url, "_blank")
}

/* --------------------------- LOAD --------------------------- */
async function loadDocuments() {
  try {
    const res = await api.get("/api/documents/")
    const raw = res.data
    documents.value = Array.isArray(raw) ? raw : Array.isArray(raw?.results) ? raw.results : []
  } catch (err) {
    console.error("LOAD DOCUMENTS ERROR:", err)
  }
}

async function loadMemos() {
  try {
    const res = await api.get("/api/memos/")
    const raw = res.data
    memos.value = Array.isArray(raw) ? raw : Array.isArray(raw?.results) ? raw.results : []
  } catch (err) {
    console.error("LOAD MEMOS ERROR:", err)
  }
}

onMounted(() => {
  loadDocuments()
  loadMemos()
})

/* --------------------------- HELPERS --------------------------- */
function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

/* --------------------------- EDIT/DELETE HELPERS --------------------------- */
async function deleteDocument(row) {
  if (!row?.id) return
  try {
    await api.delete(`/api/documents/${row.id}/`)
    await loadDocuments()
  } catch (err) {
    console.error("DELETE DOCUMENT ERROR:", err)
  }
}

async function deleteMemo(row) {
  if (!row?.id) return
  try {
    await api.delete(`/api/memos/${row.id}/`)
    await loadMemos()
  } catch (err) {
    console.error("DELETE MEMO ERROR:", err)
  }
}

async function editDocument(row) {
  if (!row?.id) return
  const newTitle = window.prompt("Edit title:", row.name || row.title || "")
  if (newTitle === null) return
  const newDesc = window.prompt("Edit description:", row.description || "")
  if (newDesc === null) return
  try {
    await api.patch(`/api/documents/${row.id}/`, {
      name: newTitle || row.name,
      description: newDesc,
    })
    await loadDocuments()
  } catch (err) {
    console.error("EDIT DOCUMENT ERROR:", err)
  }
}

async function editMemo(row) {
  if (!row?.id) return
  const newTitle = window.prompt("Edit title:", row.title || "")
  if (newTitle === null) return
  const newDesc = window.prompt("Edit description:", row.description || "")
  if (newDesc === null) return
  try {
    await api.patch(`/api/memos/${row.id}/`, {
      title: newTitle || row.title,
      description: newDesc,
    })
    await loadMemos()
  } catch (err) {
    console.error("EDIT MEMO ERROR:", err)
  }
}
</script>
