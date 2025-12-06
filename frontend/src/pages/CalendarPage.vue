<template>
  <div class="q-px-xl q-mx-md q-py-lg">

    <!-- HEADER -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Calendar</div>
        <div class="text-subtitle1 text-grey-8">A Quick Glance at Upcoming Events</div>
      </div>
      <div class="q-ma-xs flex flex-center justify-center items-center" v-if="isAdmin">
        <q-btn class="bg-primary text-white" icon="add" label="Add Event"
               @click="addEvent = true"/>
      </div>
    </div>

    <!-- ADD EVENT DIALOG -->
    <q-dialog v-model="addEvent" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Add Event</div>
        </q-card-section>

        <q-card-section>
          <q-input class="q-pa-sm" v-model="ename" label="Event Name" outlined />

          <div class="q-pa-sm">
            <q-input outlined v-model="dateTime" label="Event Date & Time" readonly>
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer" @click="showPicker = true" />
              </template>

              <q-popup-proxy v-model="showPicker" transition-show="scale" transition-hide="scale">
                <q-date v-model="date" mask="YYYY-MM-DD" landscape
                        @update:model-value="updateDateTime"/>
                <q-time class="q-mt-md" v-model="time" format24h
                        @update:model-value="updateDateTime"/>
                <q-time class="q-mt-md" v-model="endTime" format24h
                        @update:model-value="updateDateTime"/>
              </q-popup-proxy>
            </q-input>
          </div>

          <q-input class="q-pa-sm" v-model="edesc" label="Event Description" outlined />
          <q-input class="q-pa-sm" v-model="evenue" label="Event Venue" outlined />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" v-close-popup @click="resetForm"/>
          <q-btn flat label="Add" color="primary" @click="submitEvent" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- MAIN LAYOUT -->
    <div class="row q-col-gutter-md wrap" style="min-height: 70vh;">

      <!-- LEFT COLUMN (CALENDAR) -->
      <div class="col-12 col-sm-6 col-md-4">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">
          <q-date
            v-model="selectedDate"
            :events="events.map(e => e.date)"
            event-color="orange"
            today-btn
            navigation-view="calendar"
            class="full-width"
          />
        </div>
      </div>

      <!-- MIDDLE COLUMN (LIST FOR SELECTED DATE) -->
      <div class="col-12 col-sm-6 col-md-4">
        <div class="q-pa-md full-height"
             style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div class="text-h6 text-primary text-weight-bold">
            {{ selectedDate }}
          </div>

          <div v-if="filteredEvents.length">
            <q-list bordered separator class="q-mt-sm">
              <q-item
                clickable
                v-for="event in filteredEvents"
                :key="event.id"
                @click="selectedEvent = event"
              >
                <q-item-section>{{ event.title }}</q-item-section>
              </q-item>
            </q-list>
          </div>

          <!-- FALLBACK -->
          <div v-else class="text-grey-6 text-caption q-mt-sm">
            No events for this day.
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN (DETAILS) -->
      <div class="col-12 col-md-4">
        <div class="q-pa-md full-height"
             style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div v-if="selectedEvent">
            <div class="text-h6 text-weight-bold">{{ selectedEvent.title }}</div>
            <div class="text-body1">Venue: {{ selectedEvent.venue }}</div>
            <p class="q-mt-sm">{{ selectedEvent.description }}</p>
          </div>

          <div v-else class="text-grey-6 text-caption">
            Select an event to view details.
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'

defineProps({
  isAdmin: Boolean
})

/* -------------------------
    STATE
-------------------------- */
const selectedDate = ref(new Date().toISOString().slice(0, 10))
const selectedEvent = ref(null)

const events = ref([])

/* -------------------------
    LOAD EVENTS FROM BACKEND
-------------------------- */
async function loadEvents() {
  try {
    const res = await api.get('/api/events/')
    events.value = res.data
  } catch (e) {
    console.error("Failed to load events:", e)
  }
}

onMounted(loadEvents)

/* -------------------------
    FILTER EVENTS BY DATE
-------------------------- */
const filteredEvents = computed(() =>
  events.value.filter(e => e.date === selectedDate.value)
)

/* -------------------------
    ADD EVENT FORM
-------------------------- */
const addEvent = ref(false)
const ename = ref('')
const dateTime = ref('')
const edesc = ref('')
const evenue = ref('')
const endTime = ref('')

const showPicker = ref(false)
const date = ref('')
const time = ref('')

function updateDateTime() {
  if (date.value && time.value) {
    dateTime.value = `${date.value} ${time.value}`
  }
}

async function submitEvent() {
  try {
    await api.post('/api/events/', {
      title: ename.value,
      description: edesc.value,
      date: date.value,
      start_time: time.value,
      end_time: endTime.value,
      venue: evenue.value
    })

    addEvent.value = false
    resetForm()
    loadEvents()

  } catch (e) {
    console.error("Failed to create event:", e)
  }
}

function resetForm() {
  ename.value = ''
  dateTime.value = ''
  edesc.value = ''
  evenue.value = ''
  date.value = ''
  time.value = ''
  endTime.value = ''
}
</script>
