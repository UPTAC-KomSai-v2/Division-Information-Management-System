<template>
  <div class="q-pa-lg q-ma-lg" style="border: 1px solid var(--q-primary); border-radius: 8px;">
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h6 text-weight-bold text-primary"><q-icon name="filter_alt" size="24px" /><span>Report Filters</span></div>
        <div class="text-subtitle1 text-grey-8">Select criteria for your report</div>
      </div>
    </div>
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
    <q-select dense outlined v-model="type" :options="choices" label="Event Type" lazy-rules :rules="[ val => val && val.length > 0 || 'Please select choice']"/>
    <q-btn class="bg-primary text-white" icon="text_snippet" @click="$router.push('/app/admin')">Generate Report</q-btn>
  </div>
  <q-card class="no-shadow q-ma-lg" style="border: 1px solid var(--q-primary); border-radius: 8px;">
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

        <template v-slot:body-cell-department="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <div class="text-weight-bold">{{ props.row.department }}</div>
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
</template>

<script setup>
import { ref } from 'vue'

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
    name: 'department',
    label: 'Department',
    align: 'left',
    field: 'department',
    sortable: true
  },
  {
    name: 'publications',
    label: 'Publications',
    align: 'right',
    field: 'publications',
    sortable: true
  },
  {
    name: 'serviceHours',
    label: 'Service Hours',
    align: 'right',
    field: 'serviceHours',
    sortable: true
  },
  {
    name: 'trainingsAttended',
    label: 'Trainings Attended',
    align: 'right',
    field: 'trainingsAttended',
    sortable: true
  }
]


// 2. Define Dummy Data
const rows = [
  {
    id: 1,
    facultyName: 'John Doe',
    department: 'Computer Science',
    publications: 5,
    serviceHours: 32,
    trainingsAttended: 3
  },
  {
    id: 2,
    facultyName: 'Sarah Smith',
    department: 'Mathematics',
    publications: 2,
    serviceHours: 20,
    trainingsAttended: 1
  },
  {
    id: 3,
    facultyName: 'Michael Brown',
    department: 'Physics',
    publications: 4,
    serviceHours: 15,
    trainingsAttended: 2
  },
  {
    id: 4,
    facultyName: 'Emily White',
    department: 'Biology',
    publications: 1,
    serviceHours: 10,
    trainingsAttended: 4
  },
  {
    id: 5,
    facultyName: 'David Lee',
    department: 'Chemistry',
    publications: 3,
    serviceHours: 25,
    trainingsAttended: 2
  }
]
</script>