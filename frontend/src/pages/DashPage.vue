<template>
  <div class="q-pa-lg">
    <!-- Page Header -->
    <div class="q-mb-md">
      <div class="text-h4 text-weight-bold text-primary">Division Information Management System</div>
    </div>

    <!-- Main Container -->
    <div class="row wrap q-my-md" style="border: 1px solid var(--q-primary); border-radius: 8px;">

      <!-- CARD 1 - Support Center -->
      <div class="col-12 col-sm-6 q-pa-sm">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <!-- HEADER BAR -->
          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6 q-mx-sm">Support Center</div>
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

      <!-- CARD 2 - Feed -->
      <div class="col-12 col-sm-6 q-pa-sm">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6 q-mx-sm">Document Repository</div>
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

      <!-- CARD 3 - Calendar + Directory -->
      <div class="col-12 col-sm-6 q-pa-sm">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6 q-mx-sm">Calendar</div>
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
      <div class="col-12 col-sm-6 q-pa-sm">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">

          <div
            class="row items-center justify-between q-pa-sm"
            style="background: var(--q-primary); border-top-left-radius: 8px; border-top-right-radius: 8px;"
          >
            <div class="text-white text-h6 q-mx-sm">Directory</div>
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

    <div class="q-pa-xs" style="border: 1px solid var(--q-primary); border-radius: 8px;">
      <div class="col-12 col-sm-6 q-pa-sm">
        <div style="border: 1px solid var(--q-primary); border-radius: 8px;">
          <div class="row items-center justify-between q-pa-sm" style="background: var(--q-primary); border-radius: 8px;">
            <div class="text-white text-h6 q-mx-sm">Generate Report</div>
          </div>
          <div class="row wrap">
            <div class="col-12 col-md-6 q-pa-md">
              <div class="row q-col-gutter-md q-mb-md">
                <!-- DATE FROM -->
                <div class="col-12 col-sm-6">
                  <q-input dense outlined v-model="dateFrom" label="Date From" readonly>
                    <template #append>
                      <q-icon name="event" class="cursor-pointer" @click="showFromPicker = true" />
                    </template>

                    <q-popup-proxy v-model="showFromPicker" transition-show="scale" transition-hide="scale">
                      <q-date v-model="dateFrom" minimal mask="YYYY-MM-DD" @update:model-value="updateDateFrom"/>
                    </q-popup-proxy>
                  </q-input>
                </div>

                <!-- DATE TO -->
                <div class="col-12 col-sm-6">
                  <q-input dense outlined v-model="dateTo" label="Date To" readonly>
                    <template #append>
                      <q-icon name="event" class="cursor-pointer" @click="showToPicker = true" />
                    </template>

                    <q-popup-proxy v-model="showToPicker" transition-show="scale" transition-hide="scale">
                      <q-date v-model="dateTo" minimal mask="YYYY-MM-DD" @update:model-value="updateDateTo"/>
                    </q-popup-proxy>
                  </q-input>
                </div>
              </div>
              <q-select dense outlined v-model="type" :options="choices" label="Unit" lazy-rules :rules="[ val => val && val.length > 0 || 'Please select choice']"/>
              <q-btn class="bg-primary text-white" icon="text_snippet" @click="$router.push('/app/admin')">Generate Report</q-btn>            
            </div>
            <div class="col-12 col-md-6 q-pa-md">
              <q-card class="no-shadow q-mx-xs q-mt-md q-mb-sm" style="border: 1px solid var(--q-primary); border-radius: 8px;">
                <q-table
                  title="Report Preview"
                  :rows="rows"
                  :columns="columns"
                  row-key="id"
                  :filter="filter"
                  flat
                >
                  <template v-slot:top-right>
                    <q-btn outline class="text-primary q-mx-xs" icon="article" style="font-family: Arial, Helvetica, sans-serif;" @click="$router.push('/app/upload')"> PDF </q-btn>
                    <q-btn outline class="text-primary q-mx-xs" icon="dataset" style="font-family: Arial, Helvetica, sans-serif;" @click="$router.push('/app/upload')"> Excel</q-btn>
                  </template>

                  <template v-slot:body-cell-facultyName="props">
                    <q-td :props="props">
                      <div class="row items-center no-wrap">
                        <div class="text-weight-bold">{{ props.row.facultyName }}</div>
                      </div>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-unit="props">
                    <q-td :props="props">
                      <div class="row items-center no-wrap">
                        <div class="text-weight-bold">{{ props.row.unit }}</div>
                      </div>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-publications="props">
                    <q-td :props="props">
                      <div class="row items-center no-wrap">
                        <div class="text-weight-bold">{{ props.row.publications }}</div>
                      </div>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-serviceHours="props">
                    <q-td :props="props">
                      <div class="row items-center no-wrap">
                        <div class="text-weight-bold">{{ props.row.serviceHours }}</div>
                      </div>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-trainingsAttended="props">
                    <q-td :props="props">
                      <div class="row items-center no-wrap">
                        <div class="text-weight-bold">{{ props.row.trainingsAttended }}</div>
                      </div>
                    </q-td>
                  </template>
                </q-table>
              </q-card>
            </div>
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

const type = ref(null)

const choices = [
  'Meeting',
  'Workshop',
  'Seminar',
  'Maintenance'
]

const filter = ref('')

// 1. Define Table Columns
const columns = [
  {
    name: 'facultyName',
    required: true,
    label: 'Faculty Name',
    align: 'left',
    field: 'facultyName',
    sortable: true
  },
  {
    name: 'unit',
    label: 'Unit',
    align: 'left',
    field: 'unit',
    sortable: true
  },
  {
    name: 'publications',
    label: 'Publications',
    align: 'left',
    field: 'publications',
    sortable: true
  },
  {
    name: 'serviceHours',
    label: 'Service Hours',
    align: 'left',
    field: 'serviceHours',
    sortable: true
  },
  {
    name: 'trainingsAttended',
    label: 'Trainings Attended',
    align: 'left',
    field: 'trainingsAttended',
    sortable: true
  }
]


// 2. Define Dummy Data
const rows = [
  {
    id: 1,
    facultyName: 'John Doe',
    unit: 'Computer Science',
    publications: 5,
    serviceHours: 32,
    trainingsAttended: 3
  },
  {
    id: 2,
    facultyName: 'Sarah Smith',
    unit: 'Mathematics',
    publications: 2,
    serviceHours: 20,
    trainingsAttended: 1
  },
  {
    id: 3,
    facultyName: 'Michael Brown',
    unit: 'Physics',
    publications: 4,
    serviceHours: 15,
    trainingsAttended: 2
  },
  {
    id: 4,
    facultyName: 'Emily White',
    unit: 'Biology',
    publications: 1,
    serviceHours: 10,
    trainingsAttended: 4
  },
  {
    id: 5,
    facultyName: 'David Lee',
    unit: 'Chemistry',
    publications: 3,
    serviceHours: 25,
    trainingsAttended: 2
  }
]


    return {
      selectedDate, events, tickets, documents, people,
      type, choices, filter, columns, rows
    }
  }
}
</script>