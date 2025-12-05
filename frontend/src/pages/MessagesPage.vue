<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container class="fit">
      <q-page class="column fit messages-root">
        <div class="messages-row row no-wrap fit">
          <q-dialog v-model="newChatDialog" persistent>
            <q-card style="min-width: 360px; max-width: 480px">
              <q-card-section class="row items-center q-gutter-sm">
                <div class="text-h6">Start a new chat</div>
                <q-space />
                <q-btn flat round dense icon="close" v-close-popup />
              </q-card-section>

              <q-card-section>
                <q-input
                  v-model="newChatSearch"
                  dense
                  outlined
                  placeholder="Search all users"
                  clearable
                >
                  <template #prepend>
                    <q-icon name="search" />
                  </template>
                </q-input>
              </q-card-section>

              <q-separator />

              <q-card-section style="max-height: 360px; padding-top: 0">
                <q-scroll-area style="height: 360px">
                  <q-list separator>
                    <q-item
                      v-for="user in filteredNewChat"
                      :key="user.id"
                      clickable
                      @click="selectNewChat(user)"
                    >
                      <q-item-section avatar>
                        <q-avatar color="grey-4" text-color="grey-9">
                          <q-icon name="person" />
                        </q-avatar>
                      </q-item-section>
                      <q-item-section>
                        <div class="text-body1 text-weight-bold">{{ user.name }}</div>
                        <div class="text-caption text-grey-7">{{ user.email }}</div>
                      </q-item-section>
                    </q-item>

                    <div v-if="!filteredNewChat.length" class="q-pa-md text-grey-7 text-center">
                      No users found
                    </div>
                  </q-list>
                </q-scroll-area>
              </q-card-section>
            </q-card>
          </q-dialog>

          <!-- LEFT SIDEBAR -->
          <div class="col-4 col-md-3 bg-grey-2 column left-pane">
            <div class="q-pa-sm pane-controls">
              <div class="row items-center q-gutter-sm no-wrap">
                <q-input
                  ref="searchInput"
                  v-model="search"
                  dense
                  filled
                  placeholder="Search"
                  class="col"
                  clearable
                >
                  <template #prepend>
                    <q-icon name="search" />
                  </template>
                </q-input>

                <q-btn flat round dense icon="settings" color="grey-8" @click="toggleSettings" />
              </div>

            </div>

            <q-scroll-area class="contacts-list">
              <div class="column">
                <div class="q-pa-sm">
                  <q-btn
                    color="primary"
                    outline
                    icon="add"
                    label="Create New Chat"
                    unelevated
                    class="full-width"
                    @click="startNewChat"
                  />
                </div>

                <div v-for="item in filteredPrivate" :key="item.id">
                  <q-item
                    clickable
                    @click="selectContact(item)"
                    :class="['contact-item', { 'bg-grey-3': selectedContact && selectedContact.id === item.id }]"
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
                </div>
              </div>
            </q-scroll-area>
          </div>

          <!-- RIGHT PANEL -->
          <div class="col-8 col-md-9 conversation-panel">
            <!-- HEADER -->
            <div class="row items-center q-pa-md q-gutter-md header-bar">
              <q-avatar size="56px">
                <q-icon name="person" size="40px" />
              </q-avatar>

              <div class="column contact-header">
                <div class="row items-center q-gutter-xs">
                  <div class="text-h6 text-weight-bold contact-name">
                    {{ selectedContact?.name || 'Select a chat' }}
                  </div>
                </div>
                <div v-if="selectedContact" class="text-caption text-grey-7">
                  {{ selectedContact?.status || 'Offline' }}
                </div>
              </div>

              <q-space />

              <q-btn v-if="selectedContact" flat round dense icon="more_vert">
                <q-menu auto-close>
                  <q-list separator>
                    <q-item clickable @click="changeNickname">
                      <q-item-section>Change nickname</q-item-section>
                    </q-item>
                    <q-item clickable @click="removeNickname">
                      <q-item-section>Remove nickname</q-item-section>
                    </q-item>
                    <q-item clickable @click="deleteContact">
                      <q-item-section>Delete chat</q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </div>

            <!-- SETTINGS MODE -->
            <div
              v-if="showSettings"
              class="conversation-body column q-pa-lg"
              style="background: #f7f9fb"
            >
              <div class="text-h6 text-weight-bold q-mb-md">Settings</div>

              <div class="column q-gutter-md">
                <div class="column">
                  <div class="text-subtitle1 text-weight-bold">Messaging</div>
                  <div class="text-body2 text-grey-7">
                    Choose how you send and view messages.
                  </div>
                  <div class="q-mt-sm">
                    <q-toggle
                      v-model="enterToSend"
                      color="primary"
                      label="Send on Enter (Shift+Enter for newline)"
                    />
                  </div>
                </div>

                <q-separator />

                <div class="column">
                  <div class="text-subtitle1 text-weight-bold">Contacts</div>
                  <div class="text-body2 text-grey-7">
                    Start a conversation with anyone in your directory.
                  </div>
                  <div class="q-mt-sm">
                    <q-btn color="primary" outline icon="add" label="Create New Chat" @click="startNewChat" />
                  </div>
                </div>
              </div>
            </div>

            <!-- CHAT VIEW -->
            <template v-else>
              <div class="conversation-body">
                <!-- ⭐ SCROLL AREA FIXED HERE ⭐ -->
                <q-scroll-area ref="scrollArea" class="message-scroll fit">
                  <div class="q-pa-sm column message-list">
                    <template v-if="visibleMessages.length">
                      <div
                        v-for="msg in visibleMessages"
                        :key="msg.id"
                        class="message-item q-pa-md q-mb-md"
                        :class="msg.senderId === currentUserId ? 'msg-self' : 'msg-other'"
                      >
                        <div class="text-subtitle2 text-weight-bold">
                          {{ msg.senderId === currentUserId ? 'You' : msg.senderName }}
                        </div>

                        <div class="q-mt-sm text-body1">{{ msg.text }}</div>
                      </div>
                    </template>

                    <template v-else>
                      <div class="column flex-center text-center text-grey-8 empty-state">
                        <div class="text-body1 text-weight-bold">
                          {{ selectedContact ? emptyState.title : 'No chat selected' }}
                        </div>
                        <div class="text-body2 text-grey-7 q-mt-xs">
                          {{ selectedContact ? emptyState.subtitle : 'Choose a contact from the left' }}
                        </div>
                      </div>
                    </template>
                  </div>
                </q-scroll-area>
              </div>

              <!-- INPUT BAR -->
              <div class="row items-center q-pa-md q-gutter-sm input-bar">
                <q-input
                  v-model="draftMessage"
                  filled
                  type="textarea"
                  autogrow
                  class="col"
                  placeholder="Write a message"
                  @keydown.enter="handleEnterKey"
                />
                <q-btn flat round dense icon="mood" />
                <q-btn flat round dense icon="send" color="primary" @click="sendMessage" />
              </div>
            </template>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick, onBeforeUnmount } from 'vue'

const search = ref('')
const searchInput = ref(null)
const newChatDialog = ref(false)
const newChatSearch = ref('')
const enterToSend = ref(true)
const draftMessage = ref('')
const messages = ref([])
const showSettings = ref(false)
const directory = ref([])
const selectedContact = ref(null)
const socket = ref(null)
const apiBase = 'http://127.0.0.1:8000/api'
const wsBase = 'ws://127.0.0.1:8000'
const currentUserId = ref(null)
const chattedIdsKey = 'chatted_contact_ids_v3'
const chattedIdsStore = ref({})
const nicknamesKey = 'contact_nicknames_v2'
const nicknamesStore = ref({})

const getContactIdFromConversation = (room, senderId) => {
  if (!room || !currentUserId.value) return null
  const [a, b] = `${room}`.split('_').map((n) => Number(n))
  if (Number.isNaN(a) || Number.isNaN(b)) return null
  if (a === currentUserId.value && !Number.isNaN(b)) return b
  if (b === currentUserId.value && !Number.isNaN(a)) return a
  // fallback: infer from sender
  return senderId && senderId !== currentUserId.value ? senderId : null
}

const persistChattedIds = () => {
  try {
    localStorage.setItem(chattedIdsKey, JSON.stringify(chattedIdsStore.value))
  } catch {
    // ignore storage failures
  }
}

const currentNicknames = computed(() => {
  if (!currentUserId.value) return {}
  return nicknamesStore.value[currentUserId.value] || {}
})

const persistNicknames = () => {
  try {
    localStorage.setItem(nicknamesKey, JSON.stringify(nicknamesStore.value))
  } catch {
    // ignore storage failures
  }
}

const isEmailLike = (val) => typeof val === 'string' && val.includes('@')

const deriveBaseName = (contact) => {
  if (!contact) return 'User'
  const { baseName, full_name, name, username, email, id } = contact
  const emailKey = typeof email === 'string' ? email.toLowerCase() : null
  const local = emailKey && emailKey.includes('@') ? emailKey.split('@')[0] : null
  const candidates = [baseName, full_name, name, username, local]
  const nonEmail = candidates.find((c) => c && !isEmailLike(c))
  if (nonEmail) return nonEmail
  if (id) return `User ${id}`
  return 'User'
}

const applyNickname = (id, fallbackName) => {
  if (!id) return fallbackName
  const stored = currentNicknames.value?.[id]
  return stored && stored.trim() ? stored : fallbackName
}

const currentChattedIds = computed(() => {
  if (!currentUserId.value) return new Set()
  return new Set(chattedIdsStore.value[currentUserId.value] || [])
})

const mergeChattedIds = (userId, ids) => {
  if (!userId || !ids) return
  const next = new Set(chattedIdsStore.value[userId] || [])
  ids.forEach((id) => next.add(id))
  chattedIdsStore.value = { ...chattedIdsStore.value, [userId]: Array.from(next) }
}

const addChattedContact = (id) => {
  if (!id || !currentUserId.value) return
  const userId = currentUserId.value
  const current = new Set(chattedIdsStore.value[userId] || [])
  if (current.has(id)) return
  current.add(id)
  chattedIdsStore.value = { ...chattedIdsStore.value, [userId]: Array.from(current) }
  persistChattedIds()
}

const removeChattedContact = (id) => {
  if (!id || !currentUserId.value) return
  const userId = currentUserId.value
  const current = new Set(chattedIdsStore.value[userId] || [])
  if (!current.has(id)) return
  current.delete(id)
  chattedIdsStore.value = { ...chattedIdsStore.value, [userId]: Array.from(current) }
  persistChattedIds()
}

const scrollArea = ref(null)

function toggleSettings() {
  showSettings.value = !showSettings.value
}

function startNewChat() {
  newChatSearch.value = ''
  newChatDialog.value = true
}

function deleteContact() {
  if (!selectedContact.value) return
  const id = selectedContact.value.id
  messages.value = messages.value.filter((m) => m.contactId !== id)
  directory.value = directory.value.filter((d) => d.id !== id)
  removeChattedContact(id)
  selectedContact.value = null
}

function changeNickname() {
  if (!selectedContact.value || !currentUserId.value) return
  const current = selectedContact.value.name || ''
  const input = window.prompt('Enter a nickname for this contact:', current)
  if (input === null) return
  const name = input.trim()
  if (!name) return

  selectedContact.value = { ...selectedContact.value, name }

  const userMap = nicknamesStore.value[currentUserId.value] || {}
  nicknamesStore.value = {
    ...nicknamesStore.value,
    [currentUserId.value]: { ...userMap, [selectedContact.value.id]: name },
  }
  persistNicknames()

  directory.value = directory.value.map((d) =>
    d.id === selectedContact.value.id ? { ...d, name } : d,
  )

  messages.value = messages.value.map((m) =>
    m.contactId === selectedContact.value.id
      ? { ...m, senderName: name }
      : m.senderId === selectedContact.value.id
      ? { ...m, senderName: name }
      : m,
  )
}

function removeNickname() {
  if (!selectedContact.value || !currentUserId.value) return
  const userMap = { ...(nicknamesStore.value[currentUserId.value] || {}) }
  delete userMap[selectedContact.value.id]
  nicknamesStore.value = { ...nicknamesStore.value, [currentUserId.value]: userMap }
  persistNicknames()

  const baseName = deriveBaseName(selectedContact.value)
  selectedContact.value = { ...selectedContact.value, name: baseName }

  directory.value = directory.value.map((d) =>
    d.id === selectedContact.value.id ? { ...d, name: baseName } : d,
  )

  messages.value = messages.value.map((m) =>
    m.contactId === selectedContact.value.id
      ? { ...m, senderName: baseName }
      : m.senderId === selectedContact.value.id
      ? { ...m, senderName: baseName }
      : m,
  )
}

function selectContact(contact) {
  showSettings.value = false
  selectedContact.value = contact
}

function selectNewChat(user) {
  newChatDialog.value = false
  const contact = {
    id: user.id,
    name: applyNickname(user.id, deriveBaseName(user)),
    status: user.status || 'Online',
    email: user.email,
  }
  showSettings.value = false
  selectContact(contact)
  addChattedContact(contact.id)
}

const messageContactIds = computed(() => {
  const ids = new Set()
  messages.value.forEach((m) => {
    if (m.contactId) {
      ids.add(m.contactId)
      return
    }
    const inferred = getContactIdFromConversation(m.room, m.senderId)
    if (inferred) ids.add(inferred)
    if (m.senderId && m.senderId !== currentUserId.value) ids.add(m.senderId)
  })
  return ids
})

const chattedDirectory = computed(() => {
  const ids = new Set([...currentChattedIds.value, ...messageContactIds.value])
  const fromDirectory = directory.value.filter((u) => ids.has(u.id))

  const byId = new Map(fromDirectory.map((u) => [u.id, u]))

  const missing = []
  ids.forEach((id) => {
    if (byId.has(id)) return
    const msg = messages.value.find((m) => m.contactId === id || m.senderId === id)
    const baseName = deriveBaseName({ id, name: msg?.senderName, email: msg?.senderName })
    missing.push({
      id,
      baseName,
      name: applyNickname(id, baseName),
      status: 'Online',
    })
  })

  return [...fromDirectory, ...missing]
})

const filteredPrivate = computed(() => {
  const term = (search.value || '').toLowerCase().trim()
  const baseList = chattedDirectory.value
  if (!term) return baseList
  return baseList.filter((u) => u.name.toLowerCase().includes(term))
})

const filteredNewChat = computed(() => {
  const term = (newChatSearch.value || '').toLowerCase().trim()
  const baseList = directory.value.filter((u) => u.id !== currentUserId.value)
  if (!term) return baseList
  return baseList.filter((u) => u.name.toLowerCase().includes(term))
})

const emptyState = computed(() =>
  selectedContact.value
    ? { title: 'No messages yet', subtitle: 'Start the conversation' }
    : { title: 'No chat selected', subtitle: 'Choose a contact from the left' },
)

const visibleMessages = computed(() =>
  messages.value.filter(
    (m) =>
      selectedContact.value &&
      m.room ===
        `${Math.min(currentUserId.value, selectedContact.value.id)}_${Math.max(
          currentUserId.value,
          selectedContact.value.id,
        )}`,
  ),
)

// ⭐ Scroll function
async function scrollToBottom() {
  await nextTick()
  if (scrollArea.value) {
    const target = scrollArea.value.getScrollTarget()
    target.scrollTo({ top: target.scrollHeight, behavior: 'smooth' })
  }
}

function sendMessage() {
  const text = draftMessage.value.trim()
  if (!selectedContact.value || !text) return
  if (!socket.value || socket.value.readyState !== WebSocket.OPEN) return

  socket.value.send(JSON.stringify({ text }))
  draftMessage.value = ''
  addChattedContact(selectedContact.value.id)

  scrollToBottom()
}

function handleEnterKey(evt) {
  if (!enterToSend.value) return
  if (evt && evt.shiftKey) return
  if (evt) evt.preventDefault()
  sendMessage()
}

function closeSocket() {
  if (socket.value) socket.value.close()
  socket.value = null
}

watch(
  () => selectedContact.value,
  async (contact) => {
    if (!contact || !currentUserId.value) {
      closeSocket()
      return
    }

    const roomKey = `${Math.min(currentUserId.value, contact.id)}_${Math.max(
      currentUserId.value,
      contact.id,
    )}`

    closeSocket()

    const token = localStorage.getItem('access')
    const wsUrl = `${wsBase}/ws/messages/${roomKey}/?token=${token}`

    socket.value = new WebSocket(wsUrl)

    socket.value.onmessage = async (evt) => {
      try {
        const data = JSON.parse(evt.data)

        const contactId = getContactIdFromConversation(data.conversation_id, data.sender_id)
        const displayName = applyNickname(contactId, data.sender_name)

        messages.value.push({
          id: data.id,
          senderId: data.sender_id,
          senderName: displayName,
          text: data.text,
          room: data.conversation_id,
          contactId,
        })

        addChattedContact(contactId)

        await nextTick()
        scrollToBottom()
      } catch {
        //ignore
      }
    }

    await nextTick()
    scrollToBottom()
  },
  { immediate: true },
)

onBeforeUnmount(closeSocket)

onMounted(async () => {
  try {
    const storedNicknames = JSON.parse(localStorage.getItem(nicknamesKey) || '{}')
    if (storedNicknames && typeof storedNicknames === 'object') {
      nicknamesStore.value = storedNicknames
    }
  } catch {
    // ignore malformed storage
  }

  const token = localStorage.getItem('access')

  if (token) {
    const meRes = await fetch(`${apiBase}/auth/me/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    const me = await meRes.json()
    currentUserId.value = me.id
  }

  const usersRes = await fetch(`${apiBase}/users/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  const users = await usersRes.json()
  directory.value = users.map((u) => {
    const baseName = deriveBaseName({ ...u, id: u.id })
    return {
      ...u,
      baseName,
      name: applyNickname(u.id, baseName),
    }
  })

  await nextTick()
  scrollToBottom()
})

watch(
  () => currentUserId.value,
  () => {
    // migrate chatted ids from old keys when user becomes known
    try {
      const stored = JSON.parse(localStorage.getItem(chattedIdsKey) || '{}')
      if (stored && typeof stored === 'object') {
        chattedIdsStore.value = stored
      }

      // migrate legacy map (v2) scoped per user; skip legacy array (v1) to avoid cross-user leakage
      const legacyMap = JSON.parse(localStorage.getItem('chatted_contact_ids_v2') || '{}')
      if (legacyMap && typeof legacyMap === 'object' && currentUserId.value) {
        const legacyIds = legacyMap[currentUserId.value] || []
        if (Array.isArray(legacyIds)) mergeChattedIds(currentUserId.value, legacyIds)
      }

      persistChattedIds()
    } catch {
      // ignore malformed storage
    }
  },
  { immediate: true },
)
</script>

<style scoped>
.messages-root {
  height: 100%;
  min-height: 0;
  overflow: hidden;
}

.messages-row {
  flex: 1;
  min-height: 0;
}

.left-pane {
  display: flex;
  flex-direction: column;
  flex: 0 0 280px;
  max-width: 320px;
  min-width: 240px;
  min-height: 0;
}

.pane-controls {
  flex-shrink: 0;
  border-bottom: 1px solid #e0e3e7;
}

.contact-item {
  border-bottom: 1px solid #e0e3e7;
}

.contact-item:last-child {
  border-bottom: none;
}

.contacts-list {
  flex: 1;
  min-height: 0;
}

.conversation-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.header-bar {
  flex-shrink: 0;
  border-bottom: 1px solid #e0e3e7;
  background: white;
  margin-left: 1px;
}

.contact-header {
  flex: 1;
  min-width: 0;
}

.contact-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-body {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
}

.message-scroll {
  flex: 1;
  min-height: 0;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-item {
  border-radius: 8px;
  padding: 12px;
}

.msg-self {
  background: #e8f5e9;
  align-self: flex-end;
}

.msg-other {
  background: #f5f5f5;
  align-self: flex-start;
}

.input-bar {
  flex-shrink: 0;
  border-top: 1px solid #ddd;
  background: #fafafa;
  margin-left: 1px;
  margin-bottom: 1px;
}
</style>
