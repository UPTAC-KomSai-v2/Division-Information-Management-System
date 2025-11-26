<template>
  <q-page class="q-pa-md">
    <h3 class="q-px-xl text-primary text-weight-bold" style="font-family: Arial, Helvetica, sans-serif;">Calendar</h3>
    <h6 class="q-px-xl text-black" style="font-family: Arial, Helvetica, sans-serif;">A Quick Glance at Upcoming Events</h6>
    <div class="q-mx-xl q-my-md" style="border: 1px solid var(--q-primary);">
      <q-splitter
        v-model="splitterModel"
      >

        <template v-slot:before>
          <div class="q-pa-md">
            <q-date
              v-model="date"
              :events="events"
              event-color="orange"
              today-btn
              navigation-view="calendar"
              style="max-width: 95vw; max-height: 75vh;"
              class="q-mx-auto"
            />
          </div>
        </template>

        <template v-slot:after>
          <q-tab-panels
            v-model="date"
            animated
            transition-prev="jump-up"
            transition-next="jump-up"
          >
            <q-tab-panel name="2025/11/25">
              <div class="text-h4 q-mb-md">2019/02/01</div>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            </q-tab-panel>

            <q-tab-panel name="2019/02/05">
              <div class="text-h4 q-mb-md">2019/02/05</div>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            </q-tab-panel>

            <q-tab-panel name="2019/02/06">
              <div class="text-h4 q-mb-md">2019/02/06</div>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
              <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            </q-tab-panel>
          </q-tab-panels>
        </template>
      </q-splitter>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    return {
      splitterModel: ref(50),
      date: ref('2019/02/01'),
      events: [ '2025/11/25', '2019/02/05', '2019/02/06' ]
    }
  }
}
</script>