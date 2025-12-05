<template>
  <div class="q-px-xl q-mx-md q-py-lg">
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h4 text-weight-bold text-primary">Messages</div>
      <q-btn
        dense
        flat
        color="primary"
        icon="settings"
        label="Settings"
        no-caps
        @click="showSettings = !showSettings"
      />
    </div>

    <div class="row q-col-gutter-md wrap" style="min-height: 70vh;">
      <div class="col-12 col-md-4">
        <q-card class="full-height no-shadow" style="border: 1px solid var(--q-primary); border-radius: 8px;">
          <q-card-section class="q-pb-sm">
            <q-input
              v-model="search"
              outlined
              dense
              debounce="200"
              placeholder="Search"
            >
              <template #prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div class="row items-center justify-end text-primary text-caption q-mb-xs">
              <q-icon name="group" size="16px" class="q-mr-xs" />
              Contacts
            </div>

            <q-expansion-item dense expand-separator icon="star" :caption="`(${starred.length})`" label="Starred" default-opened>
              <q-item v-for="item in filteredStarred" :key="item.id" clickable>
                <q-item-section avatar>
                  <q-avatar :color="item.avatarColor" text-color="black">
                    <span class="text-weight-bold">{{ item.initials }}</span>
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <div class="text-body1 text-weight-bold">{{ item.name }}</div>
                  <div class="text-caption text-grey-7">{{ item.status }}</div>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="chevron_right" />
                </q-item-section>
              </q-item>
            </q-expansion-item>

            <q-expansion-item dense expand-separator icon="groups" :caption="`(${groups.length})`" label="Group">
              <q-item v-for="item in filteredGroups" :key="item.id" clickable>
                <q-item-section avatar>
                  <q-avatar color="grey-3" text-color="grey-9">
                    <q-icon name="groups" />
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <div class="text-body1 text-weight-bold">{{ item.name }}</div>
                  <div class="text-caption text-grey-7">{{ item.status }}</div>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="chevron_right" />
                </q-item-section>
              </q-item>
            </q-expansion-item>

            <q-expansion-item dense expand-separator icon="person" :caption="`(${privateChats.length})`" label="Private">
              <q-item v-for="item in filteredPrivate" :key="item.id" clickable>
                <q-item-section avatar>
                  <q-avatar :color="item.avatarColor" text-color="black">
                    <span class="text-weight-bold">{{ item.initials }}</span>
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <div class="text-body1 text-weight-bold">{{ item.name }}</div>
                  <div class="text-caption text-grey-7">{{ item.status }}</div>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="chevron_right" />
                </q-item-section>
              </q-item>
            </q-expansion-item>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-8">
        <q-card class="full-height column no-shadow" style="border: 1px solid var(--q-primary); border-radius: 8px;">
          <template v-if="showSettings">
            <q-card-section class="text-h6 text-weight-bold text-primary">Settings</q-card-section>
            <q-separator />
            <q-card-section>
              <div class="text-subtitle2 text-weight-bold q-mb-sm">Privacy</div>
              <div class="text-body2 text-grey-8 q-mb-sm">You can restrict who can message you</div>
              <q-option-group
                v-model="privacy"
                type="radio"
                color="primary"
                :options="[
                  { label: 'My contacts only', value: 'contacts' },
                  { label: 'My contacts and anyone in my courses', value: 'extended' }
                ]"
              />
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="text-subtitle2 text-weight-bold q-mb-sm">Notification preferences</div>
              <div class="row items-center q-mb-sm">
                <q-toggle v-model="notify.email" color="primary" label="Email" />
              </div>
              <div class="row items-center">
                <q-toggle v-model="notify.mobile" color="primary" label="Mobile" />
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="text-subtitle2 text-weight-bold q-mb-sm">General</div>
              <q-toggle v-model="useEnterToSend" color="primary" label="Use enter to send" />
            </q-card-section>
          </template>
          <template v-else>
            <div class="column flex-center full-height text-grey-6 text-subtitle1">
              Select a conversation to start messaging.
            </div>
          </template>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const search = ref('')
const showSettings = ref(false)
const privacy = ref('extended')
const notify = ref({
  email: true,
  mobile: true
})
const useEnterToSend = ref(true)

const starred = [
  { id: 1, name: 'Vall James Luceres', status: 'online', initials: 'VL', avatarColor: 'bg-grey-3 text-grey-9' }
]

const groups = [
  { id: 2, name: 'Division Leads', status: 'last message 3h ago' },
  { id: 3, name: 'Operations Team', status: 'last message yesterday' },
  { id: 4, name: 'IT Support', status: 'last message Mon' },
  { id: 5, name: 'Campus Coordinators', status: 'last message Fri' }
]

const privateChats = [
  { id: 6, name: 'John Doe', status: 'online', initials: 'JD', avatarColor: 'bg-red-2 text-red-10' },
  { id: 7, name: 'Sarah Smith', status: 'away', initials: 'SS', avatarColor: 'bg-orange-2 text-orange-10' },
  { id: 8, name: 'Emily White', status: 'offline', initials: 'EW', avatarColor: 'bg-blue-2 text-blue-10' },
  { id: 9, name: 'Michael Brown', status: 'offline', initials: 'MB', avatarColor: 'bg-grey-3 text-grey-8' }
]

const filterItems = (items) => {
  const term = search.value.toLowerCase().trim()
  if (!term) return items
  return items.filter((i) => i.name.toLowerCase().includes(term))
}

const filteredStarred = computed(() => filterItems(starred))
const filteredGroups = computed(() => filterItems(groups))
const filteredPrivate = computed(() => filterItems(privateChats))
</script>
