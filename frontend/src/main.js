import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(Quasar, { /* Quasar options here if needed */ })
app.use(createPinia())
app.use(router)

app.mount('#q-app')
