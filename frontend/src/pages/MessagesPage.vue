<template>
  <q-page class="column fit">
    <div class="messages-page column fit">
      <div class="messages-row row no-wrap fit">
        <!-- Left column -->
        <div class="col-4 col-md-3 bg-grey-2 column left-pane">
          <div class="q-pa-sm pane-controls">
            <div class="row items-center q-gutter-sm no-wrap">
              <q-input
                v-model="search"
                dense
                filled
                placeholder="Search"
                class="col"
                clearable
                hide-bottom-space
              >
                <template #prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
              <q-btn flat round dense icon="settings" color="grey-8" @click="toggleSettings" />
            </div>
          </div>

          <div class="column contacts-list">
            <q-expansion-item
              dense
              expand-separator
              switch-toggle-side
              expand-icon="keyboard_arrow_right"
              expanded-icon="keyboard_arrow_down"
              :caption="`(${filteredStarred.length})`"
              label="Starred"
              default-opened
            >
              <q-item
                v-for="item in filteredStarred"
                :key="item.id"
                clickable
                @click="selectStarredContact(item)"
                :class="{ 'bg-grey-3': selectedContact && selectedContact.id === item.id }"
              >
                <q-item-section avatar>
                  <q-avatar color="warning" text-color="white">
                    <q-icon name="star" />
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <div class="text-body2 text-weight-bold">{{ item.name }}</div>
                  <div class="text-caption text-grey-7 ellipsis">{{ item.status || '' }}</div>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="chevron_right" />
                </q-item-section>
              </q-item>
            </q-expansion-item>

            <q-expansion-item
              dense
              expand-separator
              switch-toggle-side
              expand-icon="keyboard_arrow_right"
              expanded-icon="keyboard_arrow_down"
              :caption="`(${filteredPrivate.length})`"
              label="Private"
            >
              <q-item
                v-for="item in filteredPrivate"
                :key="item.id"
                clickable
                @click="selectContact(item)"
              >
                <q-item-section avatar>
                  <q-avatar color="grey-4" text-color="grey-9">
                    <q-icon name="person" />
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <div class="text-body1 text-weight-bold">{{ item.name }}</div>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="chevron_right" />
                </q-item-section>
              </q-item>
            </q-expansion-item>
          </div>
        </div>

        <!-- Right column -->
        <div class="col-8 col-md-9 conversation-panel">
          <div class="row items-center q-pa-md q-gutter-md" style="flex-shrink: 0">
            <q-avatar size="56px">
              <q-icon name="person" size="40px" />
            </q-avatar>
            <div class="column">
              <div class="row items-center q-gutter-xs">
                <div class="text-h6 text-weight-bold">{{ selectedContact?.name }}</div>
                <q-icon v-if="isStarredContact" name="star" color="primary" size="16px" />
              </div>
              <div class="text-caption text-grey-7">{{ selectedContact?.status || 'Online' }}</div>
            </div>
            <q-space />
            <q-btn flat round dense icon="more_vert">
              <q-menu auto-close>
                <q-list separator>
                  <q-item clickable :disable="!selectedContact" @click="toggleStarContact">
                    <q-item-section>{{
                      isStarredContact ? 'Unstar contact' : 'Star contact'
                    }}</q-item-section>
                    <q-item-section side>
                      <q-icon :name="isStarredContact ? 'star' : 'star_border'" />
                    </q-item-section>
                  </q-item>
                  <q-item
                    clickable
                    :disable="!selectedContact || selectedContact.id === 'self'"
                    @click="deleteContact"
                  >
                    <q-item-section>Delete contact</q-item-section>
                    <q-item-section side>
                      <q-icon name="delete" />
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </div>

          <div
            v-if="showSettings"
            class="conversation-body column q-pa-lg"
            style="background: #f7f9fb"
          >
            <div class="text-h6 text-weight-bold q-mb-lg">Settings</div>

            <div class="q-mb-xl">
              <div class="text-subtitle1 text-weight-bold q-mb-sm">Privacy</div>
              <div class="text-body2 text-grey-8 q-mb-sm">You can restrict who can message you</div>
              <q-option-group
                v-model="privacyOption"
                type="radio"
                :options="[
                  { label: 'My contacts only', value: 'contacts_only' },
                  { label: 'My contacts and anyone in the app', value: 'contacts_courses' },
                ]"
              />
            </div>

            <div>
              <div class="text-subtitle1 text-weight-bold q-mb-sm">General</div>
              <div class="row items-center q-gutter-xs">
                <q-toggle v-model="useEnterToSend" color="primary" />
                <span class="text-body2">Use enter to send</span>
              </div>
            </div>
          </div>

          <template v-else>
            <div class="conversation-body column q-pa-lg" style="background: #f7f9fb">
              <div v-if="visibleMessages.length" class="column message-list">
                <div
                  v-for="msg in visibleMessages"
                  :key="msg.id"
                  class="message-item q-pa-md q-mb-md bg-white"
                >
                  <div class="row items-start no-wrap">
                    <div class="col">
                      <div class="text-subtitle2 text-weight-bold">
                        {{ msg.senderName }}
                      </div>
                      <div class="q-mt-sm text-body1">
                        {{ msg.text }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="column flex-center text-center text-grey-8 q-mt-xl">
                <div class="text-body1 text-weight-bold">{{ emptyState.title }}</div>
                <div class="text-body2 text-grey-7 q-mt-xs">
                  {{ emptyState.subtitle }}
                </div>
              </div>
            </div>

            <div
              class="row items-center q-pa-md q-gutter-sm"
              style="border-top: 1px solid #e0e3e7; background: #f5f5f5; flex-shrink: 0"
            >
              <q-input v-model="draftMessage" filled class="col" placeholder="Write a message..." />
              <q-btn flat round dense icon="mood" />
              <q-btn flat round dense icon="send" color="primary" />
            </div>
          </template>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const search = ref('')
const draftMessage = ref('')
const currentUserName = ref('You')
const messages = ref([])
const starred = ref([])
const showSettings = ref(false)
const privacyOption = ref('contacts_groups')
const useEnterToSend = ref(true)
const directory = ref([
  { id: 6, name: 'John Doe', status: 'Offline' },
  { id: 7, name: 'Sarah Smith', status: 'Online' },
  { id: 8, name: 'Emily White', status: 'Offline' },
  { id: 9, name: 'Michael Brown', status: 'Online' },
])
const selectedContact = ref(null)

const filterItems = (items) => {
  const term = search.value.toLowerCase().trim()
  if (!term) return items
  return items.filter((i) => i.name.toLowerCase().includes(term))
}

const filteredStarred = computed(() => filterItems(starred.value))
const privateChats = computed(() => {
  const seen = new Map()
  messages.value.forEach((msg) => {
    if (!msg.contactId || msg.contactId === 'self') return
    if (!seen.has(msg.contactId)) {
      const fromDir = directory.value.find((u) => u.id === msg.contactId)
      seen.set(msg.contactId, {
        id: msg.contactId,
        name: fromDir?.name || msg.senderName || 'Unknown',
        status: fromDir?.status || 'Online',
      })
    }
  })
  return Array.from(seen.values())
})
const filteredPrivate = computed(() => filterItems(privateChats.value))

const visibleMessages = computed(() =>
  messages.value.filter((msg) => msg.contactId === selectedContact.value?.id),
)

const isSelf = computed(
  () =>
    selectedContact.value?.id === 'self' || selectedContact.value?.name === currentUserName.value,
)

const isStarredContact = computed(
  () => !!starred.value.find((c) => c.id === selectedContact.value?.id),
)

const emptyState = computed(() =>
  isSelf.value
    ? {
        title: 'Personal space',
        subtitle: 'Save draft messages, links, notes etc. to access later.',
      }
    : {
        title: 'No messages yet',
        subtitle: 'Send a message to start the conversation.',
      },
)

const setCurrentUserAsStarred = () => {
  const storedName = localStorage.getItem('username')
  currentUserName.value = storedName && storedName.trim() ? storedName : 'You'
  selectedContact.value = {
    id: 'self',
    name: currentUserName.value,
    status: 'Online',
  }
  const selfEntry = starred.value.find((c) => c.id === 'self')
  if (!selfEntry) {
    starred.value = [
      {
        id: 'self',
        name: currentUserName.value,
        status: 'Online',
      },
      ...starred.value,
    ]
  } else {
    // ensure display name stays in sync
    selfEntry.name = currentUserName.value
    selfEntry.status = 'Online'
  }
  messages.value = []
}

const selectContact = (contact) => {
  selectedContact.value = contact
}

const selectStarredContact = (contact) => {
  if (contact.id === 'self') {
    selectedContact.value = {
      id: 'self',
      name: currentUserName.value,
      status: 'Online',
    }
    return
  }
  const fromPrivate = privateChats.value.find((c) => c.id === contact.id)
  selectedContact.value = fromPrivate || contact
}

const toggleStarContact = () => {
  if (!selectedContact.value) return
  const exists = starred.value.find((c) => c.id === selectedContact.value.id)
  if (exists) {
    starred.value = starred.value.filter((c) => c.id !== selectedContact.value.id)
  } else {
    starred.value = [...starred.value, { ...selectedContact.value }]
  }
}

const deleteContact = () => {
  if (!selectedContact.value || selectedContact.value.id === 'self') return
  const id = selectedContact.value.id
  starred.value = starred.value.filter((c) => c.id !== id)
  messages.value = messages.value.filter((m) => m.contactId !== id)
  selectedContact.value = null
}

const toggleSettings = () => {
  showSettings.value = !showSettings.value
}


onMounted(() => {
  setCurrentUserAsStarred()
})
</script>

<style scoped>
.messages-page {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.messages-row {
  flex: 1;
  min-height: 0;
}

.conversation-panel {
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.conversation-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.left-pane {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.pane-controls {
  flex-shrink: 0;
  border-bottom: 1px solid #e0e3e7;
}

.contacts-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}
</style>
