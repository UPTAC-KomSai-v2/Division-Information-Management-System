<template>
  <q-layout>
    <q-page-container>
      <q-page class="bg-primary flex flex-center full-height">
        <div class="q-pa-xl flex flex-center" style="height: 100vh;">
          <div class="bg-grey-3 q-pa-lg rounded-borders">

            <img
              alt="DIMS logo"
              src="~assets/dims.png"
              class="q-mx-auto block"
              style="width: 75px; height: 75px"
            />

            <p class="text-primary text-center text-weight-bold text-h4">
              DIMS
            </p>
            <p class="text-center text-subtitle1">
              Division Information Management System
            </p>
            <p class="text-center text-weight-light text-subtitle2">
              University of the Philippines Tacloban College
            </p>

            <!-- EMAIL instead of username -->
            <q-input
              class="q-my-xs"
              dense
              outlined
              v-model="email"
              label="Email"
              type="email"
            />

            <q-input
              class="q-my-sm"
              dense
              outlined
              v-model="password"
              type="password"
              label="Password"
            />

            <!-- Error message shown when login fails -->
            <q-banner
              v-if="error"
              class="bg-red-3 text-red-10 q-mt-md"
              rounded
            >
              {{ error }}
            </q-banner>

            <div class="row justify-end">
              <q-btn
                flat
                class="text-caption text-right text-primary q-my-sm"
                label="Forgot Password?"
                @click="$router.push('/forgot-password')"
              />
            </div>

            <q-btn
              class="full-width"
              label="Login"
              color="primary"
              :loading="loading"
              :disable="loading"
              @click="login"
            />
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'
import { useAuthStore } from 'src/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// all refs – NEVER reassign these variables themselves, only .value
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

// must match your Django URL in config/urls.py
const loginUrl = '/api/auth/login/'

const login = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await api.post(loginUrl, {
      email: email.value,        // 🔴 key name MUST be "email"
      password: password.value
    })

    authStore.setAuth({
      access: response.data.access,
      refresh: response.data.refresh,
      user: response.data.user
    })

    localStorage.setItem('access', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)

    if (response.data.user) {
      localStorage.setItem('user', JSON.stringify(response.data.user))
    }

    router.push('/app/dashboard')
  } catch (err) {
    console.error('LOGIN ERROR:', err?.response?.status, err?.response?.data)
    error.value =
      err?.response?.data?.detail || 'Invalid email or password'
  } finally {
    loading.value = false
  }
}

// import { ref } from 'vue'
// import { useRouter } from 'vue-router'
// import { useAuthStore } from 'src/stores/auth'
// // ✅ use the axios instance from boot/axios
// import { api } from 'boot/axios'

// const router = useRouter()
// const auth = useAuthStore()

// const email = ref('')
// const password = ref('')
// const error = ref<String | null>(null)
// const loading = ref(false)

// // Match the URL you used in Django urls.py:
// // path("api/auth/login/", EmailTokenObtainPairView.as_view(), ...)
// const loginUrl = '/api/auth/login/'

// const login = async () => {
//   loading.value = true
//   error.value = null

//   try {
//     const response = await api.post(loginUrl, {
//       // ✅ backend now expects "email", not "username"
//       email: email.value,
//       password: password.value
//     })

//     // Tokens from SimpleJWT
//     localStorage.setItem('access', response.data.access)
//     localStorage.setItem('refresh', response.data.refresh)

//     // Optional: store user info (from our custom serializer)
//     if (response.data.user) {
//       localStorage.setItem('user', JSON.stringify(response.data.user))
//     }

//     // Redirect to dashboard
//     await auth.login(email.value, password.value)
//     await router.push('/app/dashboard')
//   } catch (err) {
//     console.error(err)
//     error.value =
//       err?.response?.data?.detail ||
//       'Invalid email or password'
//   } finally {
//     loading.value = false
//   }
// }

</script>
