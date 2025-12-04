<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <!-- Header -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Services Center</div>
        <div class="text-subtitle1 text-grey-8"> A dedicated support hub where users can submit tickets, track requests, and receive assistance</div>
      </div>
      <div class="q-mx-md q-mb-md flex flex-center justify-center items-center"> 
        <q-btn class="bg-primary text-white" icon="add" style="font-family: Arial, Helvetica, sans-serif;" @click="newTicket = true"> New Ticket</q-btn>
         <q-dialog v-model="newTicket">
          <q-card style="min-width: 400px; max-width: 600px;">
            <q-card-section>
              <div class="text-h6">Create New Ticket</div>
            </q-card-section>

            <q-card-section>
              <q-input v-model="tktTitle" label="Title" outlined class="full-width" />
              <q-input v-model="tktDesc" label="Description" outlined type="textarea" class="full-width q-mt-md" />
            </q-card-section>

            <q-card-actions align="right">
              <q-btn flat label="Cancel" color="primary" v-close-popup />
              <q-btn flat label="Submit" color="primary" @click="submitTicket" />
            </q-card-actions>
          </q-card>
         </q-dialog>
      </div>
    </div>

    <!-- Main Responsive Container -->
    <div class="row q-col-gutter-md wrap" style="min-height: 70vh;" >
      <!-- MIDDLE COLUMN -->
      <div class="col-12 col-sm-9 col-md-4">
        <div
          class="q-pa-md full-height"
          style="border: 1px solid var(--q-primary); border-radius: 8px;"
        >
          <q-input v-model="search" outlined class="full-width" placeholder="Search current and previous tickets..." debounce="300" clearable >
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>

          <div v-if="filteredEvents.length">
            <q-list bordered separator class="q-mt-sm">
              <q-item
                clickable
                v-for="(event, index) in filteredEvents"
                :key="index"
                @click="selectedEvent = event"
              >
                <q-item-section>{{ event.title }}</q-item-section>
              </q-item>
            </q-list>
          </div>

          <div v-else class="text-grey-6 text-caption q-mt-sm">
            No ticket records.
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN -->
      <div
        class="col-12 col-sm-9 col-md-8"
      >
        <div
          class="q-pa-md full-height"
          style="border: 1px solid var(--q-primary); border-radius: 8px;"
        >
          <div v-if="selectedEvent">
            <div class="text-h6 text-weight-bold">Ticket ID: {{ selectedEvent.id }}</div>
            <div class="text-subtitle1 text-weight-bold">Title: {{ selectedEvent.title }}</div>
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


<script>
import { ref, computed, watch} from 'vue'
const search = ref('')
const tktTitle = ref('')
const tktDesc = ref('')
const newTicket = ref(false)

let timer = null
watch(search, val => {
  clearTimeout(timer)
  timer = setTimeout(() => console.log('Searching:', val), 300)
})

export default {
  setup () {
    const selectedDate = ref('2025/11/25')
    const selectedEvent = ref(null)

    const events = [
      {
        id: 'TCK-001',
        date: '2025/11/25',
        title: 'Faculty Meeting',
        description: 'Meeting with department heads.',
        status: 'Open',
        creator: 'Admin Office'
      },
      {
        id: 'TCK-002',
        date: '2025/11/25',
        title: 'IT Maintenance',
        description: 'Scheduled downtime from 2-4PM.',
        status: 'In Progress',
        creator: 'IT Division'
      },
      {
        id: 'TCK-003',
        date: '2019/02/05',
        title: 'Workshop',
        description: 'Technical writing workshop.',
        status: 'Closed',
        creator: 'Training Division'
      },
      {
        id: 'TCK-004',
        date: '2019/02/06',
        title: 'Seminar',
        description: 'Campus seminar event.',
        status: 'Closed',
        creator: 'HR Department'
      }
    ]

    const filteredEvents = computed(() =>
      events.filter(e => e.date === selectedDate.value)
    )

    return {
      search,
      selectedDate,
      selectedEvent,
      events,
      filteredEvents,
      newTicket,
      tktTitle,
      tktDesc,
    }
  }
}
</script>
