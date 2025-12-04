<template>
  <q-layout>
    <q-page-container>
      <q-page class="bg-primary flex flex-center full-height">
        <div class="q-pa-xl flex flex-center" style="height: 100vh;">
          <div class="bg-grey-3 q-pa-lg rounded-borders">
            <img alt="DIMS logo" src="~assets/dims.png" class="q-mx-auto block" style="width: 75px; height: 75px" />
            <p class="text-primary text-center text-weight-bold text-h4">DIMS</p>
            <p class="text-center text-subtitle1">Division Information Management System</p>
            <p class="text-center text-weight-light text-subtitle2">University of the Philippines Tacloban College</p>
            <p class="text-center text-weight-light text-subtitle2">Please contact System Administrator at example@email.com</p>
            <q-btn class="full-width" color="secondary" label="Confirm" @click="$router.push('/login')"/>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
</script>