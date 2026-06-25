<template>
  <div class="flex h-screen bg-gray-950 text-gray-100">
    <SideNav @toggle-quick-note="store.toggleQuickNote()" />
    <div class="flex-1 flex flex-col overflow-hidden">
      <QuickNotePanel v-if="store.showQuickNote" @close="store.showQuickNote = false" />
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import SideNav from './SideNav.vue'
import QuickNotePanel from './QuickNotePanel.vue'
import { useAppStore } from '../store'

const store = useAppStore()
</script>
