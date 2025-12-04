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
  <div class="q-pa-lg q-ma-lg" style="border: 1px solid var(--q-primary); border-radius: 8px;">
  </div>
  <div class="q-pa-lg q-ma-lg" style="border: 1px solid var(--q-primary); border-radius: 8px;">
  </div>
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
</script>
