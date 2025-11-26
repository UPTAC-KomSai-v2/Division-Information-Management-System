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
            <q-input class="q-my-xs" dense outlined v-model="email" label="Email" lazy-rules :rules="[ val => !!val || 'Please Enter Email']"/>
            <q-input class="q-my-sm" dense outlined v-model="pass" label="Password" :type="isPwd ? 'password' : 'text'" lazy-rules :rules="[ val => !!val || 'Please Enter Password']">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
            <div class="row justify-end">
              <q-btn flat class="text-caption text-right text-primary q-my-sm" label="Forgot Password?" @click="$router.push('/forgot-password')"/>
            </div>
            <q-btn class="full-width" color="secondary" label="Login" @click="$router.push('/app')"/>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const pass = ref('')
const isPwd = ref(true)
</script>