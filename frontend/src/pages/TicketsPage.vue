<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <!-- Header -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Services Center</div>
        <div class="text-subtitle1 text-grey-8">
          A dedicated support hub where users can submit tickets, track requests, and receive assistance
        </div>
      </div>

      <div class="q-mx-md q-mb-md flex flex-center justify-center items-center">
        <q-btn class="bg-primary text-white" icon="add"
               style="font-family: Arial, Helvetica, sans-serif;"
               @click="newTicket = true">
          New Ticket
        </q-btn>
      </div>
    </div>

    <!-- CREATE TICKET DIALOG -->
    <q-dialog v-model="newTicket" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Create New Ticket</div>
        </q-card-section>

        <q-card-section>
          <q-input class="q-pa-sm" v-model="tktTitle" label="Title" outlined />
          <q-input class="q-pa-sm" v-model="tktDesc" label="Description" outlined />
          <q-select
            class="q-pa-sm"
            v-model="tktPriority"
            :options="tktPriorities"
            label="Priority"
            outlined
            emit-value
            map-options
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" v-close-popup @click="resetForm" />
          <q-btn flat label="Add" color="primary" @click="submitTicket" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- MAIN LAYOUT -->
    <div class="row q-col-gutter-md wrap" style="min-height: 70vh;">
      
      <!-- LEFT COLUMN: LIST -->
      <div class="col-12 col-sm-9 col-md-4">
        <div class="q-pa-md full-height" style="border: 1px solid var(--q-primary); border-radius: 8px;">
          
          <q-input v-model="search" outlined class="full-width"
                   placeholder="Search tickets..." debounce="300" clearable>
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>

          <!-- LIST -->
          <div v-if="filteredTickets.length">
            <q-list bordered separator class="q-mt-sm">
              <q-item v-for="ticket in filteredTickets" :key="ticket.ticket_id"
                      clickable @click="selectedEvent = ticket">
                <q-item-section>{{ ticket.title }}</q-item-section>
              </q-item>
            </q-list>
          </div>

          <!-- EMPTY -->
          <div v-else class="text-grey-6 text-caption q-mt-sm flex flex-center">
            <q-icon name="info" size="xs" class="q-mr-sm" />
            No ticket records.
          </div>

        </div>
      </div>

      <!-- RIGHT COLUMN: DETAILS -->
      <div class="col-12 col-sm-9 col-md-8">
        <div class="q-pa-md full-height" style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div v-if="selectedEvent">
            <div class="text-h6 text-weight-bold">Ticket ID: {{ selectedEvent.ticket_id }}</div>
            <div class="text-subtitle1 text-weight-bold">Title: {{ selectedEvent.title }}</div>
            <div class="text-body1">Priority: {{ selectedEvent.priority }}</div>
            <div class="text-body1">Status: {{ selectedEvent.status }}</div>
            <div class="text-body1">Created By: {{ selectedEvent.creator }}</div>
            <p class="q-mt-sm">Description: {{ selectedEvent.description }}</p>
          </div>

          <div v-else class="text-grey-6 text-caption">
            Select a ticket to view details.
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'

/* --- FORM FIELDS --- */
const tktTitle = ref('')
const tktDesc = ref('')
const tktPriority = ref('MEDIUM')
const newTicket = ref(false)
const loadingTickets = ref(false)

const tktPriorities = [
  { label: 'Low', value: 'LOW' },
  { label: 'Medium', value: 'MEDIUM' },
  { label: 'High', value: 'HIGH' },
  { label: 'Urgent', value: 'URGENT' }
]

/* --- TICKETS FROM BACKEND --- */
const tickets = ref([])
const selectedEvent = ref(null)
const search = ref('')

/* Load tickets from backend */
async function loadTickets() {
  loadingTickets.value = true
  try {
    const response = await api.get('/api/tickets/')
    const raw = response.data
    tickets.value = Array.isArray(raw) ? raw : Array.isArray(raw?.results) ? raw.results : []
  } catch (err) {
    console.error("Failed to load tickets:", err)
  } finally {
    loadingTickets.value = false
  }
}

onMounted(() => {
  loadTickets()
})

/* --- FILTERED LIST --- */
const filteredTickets = computed(() => {
  if (!search.value) return tickets.value
  return tickets.value.filter(t =>
    (t.title || '').toLowerCase().includes(search.value.toLowerCase()) ||
    (t.ticket_id || '').toLowerCase().includes(search.value.toLowerCase())
  )
})

/* --- CREATE NEW TICKET --- */
async function submitTicket() {
  try {
    await api.post('/api/tickets/', {
      title: tktTitle.value,
      description: tktDesc.value,
      priority: tktPriority.value
    })

    newTicket.value = false
    resetForm()
    await loadTickets()
    // select the newest ticket if available
    if (tickets.value.length) {
      selectedEvent.value = tickets.value[0]
    }

  } catch (err) {
    console.error("Failed to create ticket:", err)
  }
}

function resetForm() {
  tktTitle.value = ''
  tktDesc.value = ''
  tktPriority.value = 'MEDIUM'
}
</script>
