<template>
  <div class="q-px-xl q-mx-md q-py-lg">

    <!-- Header -->
    <div class="q-mb-lg">
      <div class="text-h4 text-weight-bold text-primary">Calendar</div>
      <div class="text-subtitle1 text-grey-8">A Quick Glance at Upcoming Events</div>
    </div>

    <!-- Main Responsive Container -->
    <div class="row q-col-gutter-md wrap" style="min-height: 70vh;" >
      <!-- LEFT COLUMN -->
      <div class="col-12 col-sm-6 col-md-4" >
        <div class="q-pa-md full-height">
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


<script>
import { ref, computed } from 'vue'

export default {
  setup () {
    const selectedDate = ref('2025/11/25')
    const selectedEvent = ref(null)

    const events = [
      { date: '2025/11/25', title: 'Faculty Meeting', description: 'Meeting with department heads.' },
      { date: '2025/11/25', title: 'IT Maintenance', description: 'Scheduled downtime from 2-4PM.' },
      { date: '2019/02/05', title: 'Workshop', description: 'Technical writing workshop.' },
      { date: '2019/02/06', title: 'Seminar', description: 'Campus seminar event.' }
    ]

    const filteredEvents = computed(() =>
      events.filter(e => e.date === selectedDate.value)
    )

    return {
      selectedDate,
      selectedEvent,
      events,
      filteredEvents
    }
  }
}
</script>
