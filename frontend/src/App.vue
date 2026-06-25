<template>
  <AppLayout>
    <router-view />
    <ReminderPopup v-if="store.showReminder" @close="store.showReminder = false" />
  </AppLayout>
</template>

<script setup>
import AppLayout from './components/AppLayout.vue'
import ReminderPopup from './components/ReminderPopup.vue'
import { useAppStore } from './store'
import api from './api'
import { onMounted } from 'vue'

const store = useAppStore()

onMounted(() => {
  setInterval(async () => {
    try {
      const { data } = await api.getReminderStatus()
      if (data.should_remind) store.showReminder = true
    } catch {}
  }, 60000)
})
</script>
