<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <!-- Header -->
    <div class="full-width row wrap items-center">
      <div class="q-mb-lg col-grow">
        <div class="text-h4 text-weight-bold text-primary">Document Upload</div>
        <div class="text-subtitle1 text-grey-8">A page where users can upload and add their documents to the site's repository.</div>
      </div>
    </div>

    <q-card class="no-shadow" style="border: 1px solid var(--q-primary); border-radius: 8px;">
      <div class="q-pa-lg">
        <q-input type="textarea" outlined v-model="desc" label="Event Description" lazy-rules :rules="[ val => val && val.length > 0 || 'Please type something']" autogrow min-height="3rem" />
        <q-select outlined v-model="type" :options="choices" label="Event Type" lazy-rules :rules="[ val => val && val.length > 0 || 'Please select choice']"/>
        <q-input outlined v-model="venue" label="Event Venue" lazy-rules :rules="[ val => val && val.length > 0 || 'Please type something']" />
        <q-uploader url="http://localhost:4444/upload" square flat bordered multiple batch no-thumbnails style="max-width: 300px" />
      </div>
      <div class="row justify-end">
        <q-btn filled class="text-subtitle1 text-right bg-primary text-white q-mx-lg q-mb-lg" label="Submit" @click="$router.push('/app/documents')"/>
      </div>
    </q-card>
  </div>
</template>

<script setup>
</script>