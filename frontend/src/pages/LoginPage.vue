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
            <q-input class="q-my-xs" dense outlined v-model="email" label="Email" lazy-rules :rules="[ val => val || 'Please Enter Email']"/>
            <q-input class="q-my-sm" dense outlined v-model="pass" label="Password" lazy-rules :rules="[ val => val && val.length > 0 || 'Please Enter Password']" />
            <p class="text-right text-weight-light text-caption q-mt-xs" style="cursor: pointer; text-decoration: underline;" @click="$router.push('/forgot-password')">
              Forgot Password? </p>
            <q-btn class="full-width" color="secondary" label="Login" @click="$router.push('/app')"/>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
</script>