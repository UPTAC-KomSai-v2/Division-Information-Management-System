<template>
  <q-page class="q-pa-lg">
    <!-- Page Header -->
    <div class="q-mb-lg">
      <div class="text-h5 text-weight-bold text-primary">User Profile</div>
      <div class="text-subtitle2 text-grey-7">
        View your registered information
      </div>
    </div>

    <div class="row q-col-gutter-lg">

      <!-- LEFT SIDE: Profile Box (view only) -->
      <div class="col-12 col-md-4">
        <div
          class="q-pa-md"
          style="border: 1px solid var(--q-primary); border-radius: 8px;"
        >
          <div class="column items-center">
            <q-avatar size="120px" class="q-mb-md">
              <img :src="form.avatar" alt="Avatar" />
            </q-avatar>

            <div class="text-subtitle1 text-weight-bold q-mt-sm">
              {{ form.name }}
            </div>

            <div class="text-grey-7">
              {{ form.role }}
            </div>

            <div class="text-caption text-grey-6 q-mt-sm text-center">
              Profile details are managed by the system administrator.
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT SIDE: Information Box (view only) -->
      <div class="col-12 col-md-8">
        <div
          class="q-pa-md"
          style="border: 1px solid var(--q-primary); border-radius: 8px;"
        >
          <div class="text-subtitle1 text-weight-bold q-mb-md">
            Personal Information
          </div>

          <div class="q-gutter-md">
            <q-input
              v-model="form.name"
              label="Full Name"
              outlined
              dense
              readonly
              disable
            />

            <q-input
              v-model="form.email"
              label="Email Address"
              outlined
              dense
              type="email"
              readonly
              disable
            />

            <!-- Position is back to read-only text input -->
            <q-input
              v-model="form.position"
              label="Position"
              outlined
              dense
              readonly
              disable
            />

            <!-- Unit/Department is back to read-only text input -->
            <q-input
              v-model="form.unit"
              label="Unit / Department"
              outlined
              dense
              readonly
              disable
            />

            <q-input
              v-model="form.contact"
              label="Contact Number"
              outlined
              dense
              readonly
              disable
            />

            <q-separator class="q-my-md" />

            <div class="text-subtitle1 text-weight-bold q-mb-sm">
              Notification Preferences
            </div>

            <q-toggle
              v-model="form.notifyAnnouncements"
              label="Receive announcement notifications"
              checked-icon="notifications_active"
              unchecked-icon="notifications_off"
              disable
            />

            <q-toggle
              v-model="form.notifyTickets"
              label="Receive ticket status updates"
              checked-icon="mark_email_unread"
              unchecked-icon="mark_email_read"
              disable
            />

            <div class="text-caption text-grey-6 q-mt-md">
              To update your information or notification settings, please contact
              the Division Office or system administrator.
            </div>
          </div>
        </div>
      </div>

    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()

const form = ref({
  avatar: '',
  name: '',
  email: '',
  role: '',
  position: '',
  unit: '',
  contact: '',
  notifyAnnouncements: false,
  notifyTickets: false
})

onMounted(() => {
  // Load from Pinia store if available
  let user = authStore.user

  // Fallback to localStorage
  if (!user) {
    const saved = localStorage.getItem('user')
    if (saved) user = JSON.parse(saved)
  }

  if (!user) return

  // Map Django fields to your form fields
  form.value.avatar =
  user.avatar
    ? (user.avatar.startsWith('http') ? user.avatar : `${import.meta.env.VITE_API_URL}${user.avatar}`)
    : 'https://cdn.quasar.dev/img/boy-avatar.png'
  form.value.unit = user.department ?? 'Not specified'
  form.value.contact = user.phone ?? 'Not provided'
  form.value.name = user.full_name ?? `${user.first_name || ''} ${user.last_name || ''}`.trim()
  form.value.email = user.email
  form.value.role = user.role
  form.value.position = user.position || user.role   // If you have no position field, fallback
  form.value.notifyAnnouncements = user.notifyAnnouncements ?? false
  form.value.notifyTickets = user.notifyTickets ?? false
})
</script>
