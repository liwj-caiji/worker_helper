import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const showQuickNote = ref(false)
  const showReminder = ref(false)

  function toggleQuickNote() {
    showQuickNote.value = !showQuickNote.value
  }

  return { showQuickNote, showReminder, toggleQuickNote }
})
