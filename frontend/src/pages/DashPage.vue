<template>
  <div class="q-pa-lg q-ml-md">

    <!-- Page Header -->
    <div class="q-mb-lg">
      <div class="text-h4 text-weight-bold text-primary">Welcome to DIMS</div>
      <div class="text-subtitle1 text-grey-8">Division Information Management System</div>
    </div>

    <!-- Main Container -->
    <div class="row q-col-gutter-md wrap q-pr-md q-pb-md" style="border: 1px solid var(--q-primary); border-radius: 8px;">

      <!-- CARD 1 - Support Center -->
      <div class="col-12 col-sm-6">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <!-- HEADER BAR -->
          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6">Support Center</div>
            <q-btn
              dense flat round icon="open_in_new"
              class="text-white"
              @click="$router.push('/app/services')"
            />
          </div>

          <!-- CONTENT -->
          <div class="q-pa-md">
            <q-list dense>
              <q-item v-for="t in tickets.slice(0,3)" :key="t.id">
                <q-item-section>
                  <div class="text-weight-bold">{{ t.title }}</div>
                  <div class="text-caption text-grey">{{ t.status }}</div>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </div>

      <!-- CARD 2 - File Repository -->
      <div class="col-12 col-sm-6">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6">Document Repository</div>
            <q-btn
              dense flat round icon="open_in_new"
              class="text-white"
              @click="$router.push('/app/documents')"
            />
          </div>

          <div class="q-pa-sm">
            <q-list dense>
              <q-item v-for="d in documents.slice(0,3)" :key="d.id">
                <q-item-section>
                  <div class="text-weight-bold">{{ d.name }}</div>
                  <div class="text-caption text-grey">{{ d.type }} • {{ d.access }}</div>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </div>

      <!-- CARD 3 - Calendar -->
      <div class="col-12 col-sm-6">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6">Calendar</div>
            <q-btn
              dense flat round icon="open_in_new"
              class="text-white"
              @click="$router.push('/app/calendar')"
            />
          </div>

          <div class="q-pa-md full-height">
            <q-date
              v-model="selectedDate"
              :events="events.map(e => e.date)"
              event-color= "var(--q-accent)"
              minimal
              navigation-view="calendar"
              class="full-width"
            />
          </div>

        </div>
      </div>

      <!-- CARD 4 - Directory -->
      <div class="col-12 col-sm-6">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6">Directory</div>
            <q-btn
              dense flat round icon="open_in_new"
              class="text-white"
              @click="$router.push('/app/directory')"
            />
          </div>

          <div class="q-pa-md">
            <q-list dense>
              <q-item v-for="p in people.slice(0,3)" :key="p.id">
                <q-item-section avatar>
                  <q-avatar size="42px" :class="p.avatarColor" class="flex flex-center text-weight-bold"> {{ p.initials }} </q-avatar>
                </q-item-section>

                <q-item-section>
                  <div class="text-weight-bold">{{ p.name }}</div>
                  <div class="text-caption text-grey">{{ p.position }}</div>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    const selectedDate = ref('2025/11/25')

    const events = [
      { date: '2025/11/25', title: 'Faculty Meeting', description: 'Meeting with department heads.' },
      { date: '2025/11/25', title: 'IT Maintenance', description: 'Scheduled downtime from 2-4PM.' },
      { date: '2019/02/05', title: 'Workshop', description: 'Technical writing workshop.' },
      { date: '2019/02/06', title: 'Seminar', description: 'Campus seminar event.' }
    ]

    const tickets = [
      { id: 1, title: 'Printer not working', status: 'Open' },
      { id: 2, title: 'Login error', status: 'In Progress' },
      { id: 3, title: 'Network downtime', status: 'Resolved' }
    ]

    const documents = [
      { id: 1, name: 'Campus Memo 2025', type: 'Memo', access: 'Public' },
      { id: 2, name: 'Award List Q1', type: 'Award', access: 'Permitted' },
      { id: 3, name: 'Research Paper', type: 'Publication', access: 'Restricted' }
    ]

    const people = [
  {
    id: 1,
    name: 'John Doe',
    position: 'Director',
    initials: 'JD',
    avatarColor: 'bg-red-2 text-red-10'
  },
  {
    id: 2,
    name: 'Sarah Smith',
    position: 'IT Specialist',
    initials: 'SS',
    avatarColor: 'bg-orange-2 text-orange-10'
  },
  {
    id: 3,
    name: 'Mark Lee',
    position: 'Staff',
    initials: 'ML',
    avatarColor: 'bg-blue-2 text-blue-10'
  }
]


    return {
      selectedDate,
      events,
      tickets,
      documents,
      people
    }
  }
}
</script>