<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <!-- Header -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Calendar</div>
        <div class="text-subtitle1 text-grey-8">A Quick Glance at Upcoming Events</div>
      </div>
      <div class="q-ma-xs flex flex-center justify-center items-center" v-if="isAdmin"> 
        <q-btn class="bg-primary text-white" icon="add" style="font-family: Arial, Helvetica, sans-serif;" label="Add Event" @click="addEvent = true"/>
      </div>
    </div>

    <q-dialog v-model="addEvent" persistent>
      <q-card style="min-width: 350px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6 text-primary">Add Event</div>
        </q-card-section>

        <q-card-section>
          <q-input class="q-pa-sm" v-model="ename" label="Event Name" outlined />
          <div class="q-pa-sm">
            <q-input outlined v-model="dateTime" label="Event Date & Time" readonly >
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer" @click="showPicker = true" />
              </template>

              <q-popup-proxy v-model="showPicker" transition-show="scale" transition-hide="scale">
                <q-date v-model="date" mask="YYYY-MM-DD" landscape @update:model-value="updateDateTime"/>
                <q-time class="q-mt-md" v-model="time" format24h @update:model-value="updateDateTime"/>
              </q-popup-proxy>
            </q-input>
          </div>
          <q-input class="q-pa-sm" v-model="edesc" label="Event Description" outlined/>
          <q-input class="q-pa-sm" v-model="etype" label="Event Type" outlined />
          <q-input class="q-pa-sm" v-model="evenue" label="Event Venue" outlined />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="secondary" v-close-popup @click="resetForm" />
          <q-btn flat label="Add" color="primary" @click="submitEvent" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Main Responsive Container -->
    <div class="row q-col-gutter-md wrap" style="min-height: 70vh;" >
      <!-- LEFT COLUMN -->
      <div class="col-12 col-sm-6 col-md-4" >
        <div class="full-height" style="border: 1px solid var(--q-primary); border-radius: 8px;">
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

      <!-- MIDDLE COLUMN -->
      <div
        class="col-12 col-sm-6 col-md-4"
      >
        <div
          class="q-pa-md full-height"
          style="border: 1px solid var(--q-primary); border-radius: 8px;"
        >
          <div class="text-h6 text-primary text-weight-bold">
            {{ selectedDate }}
          </div>

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
            No events for this day.
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN -->
      <div
        class="col-12 col-md-4"
      >
        <div
          class="q-pa-md full-height"
          style="border: 1px solid var(--q-primary); border-radius: 8px;"
        >
          <div v-if="selectedEvent">
            <div class="text-h6 text-weight-bold">{{ selectedEvent.title }}</div>
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
import { ref, computed } from 'vue'

  defineProps({
    isAdmin: Boolean
  })

  const selectedDate = ref('2025/11/25')
  const selectedEvent = ref(null)

  const events = [
    { date: '2025/11/25', title: 'Faculty Meeting', description: 'Meeting with department heads.' },
    { date: '2025/11/25', title: 'IT Maintenance', description: 'Scheduled downtime from 2-4PM.' },
    { date: '2019/02/05', title: 'Workshop', description: 'Technical writing workshop.' },
    { date: '2019/02/06', title: 'Seminar', description: 'Campus seminar event.' }
  ]

  const filteredEvents = computed(() => events.filter(e => e.date === selectedDate.value) )

  const addEvent = ref(false)

  const ename = ref('')
  const dateTime = ref('')
  const edesc = ref('')
  const etype = ref('')
  const evenue = ref('')

  const showPicker = ref(false)
  const date = ref('')
  const time = ref('')

  function updateDateTime () {
    if (date.value && time.value) {
      dateTime.value = `${date.value} ${time.value}`
    }
  }

  function submitEvent () {
    console.log('User Added:')
    console.log({
      ename: ename.value,
      dateTime: dateTime.value,
      edesc: edesc.value,
      etype: etype.value,
      evenue: evenue.value
    })

    addEvent.value = false
  }

  function resetForm() {
    ename.value = ''
    dateTime.value = ''
    edesc.value = ''
    etype.value = ''
    evenue.value = ''
  }

</script>
