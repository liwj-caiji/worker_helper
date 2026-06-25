<template>
  <div class="fixed right-0 top-0 h-full w-80 bg-gray-900 border-l border-gray-800 z-50 shadow-2xl p-4">
    <div class="flex justify-between items-center mb-4">
      <h3 class="font-semibold">📝 随手记</h3>
      <button @click="$emit('close')" class="text-gray-500 hover:text-gray-300 text-lg leading-none">&times;</button>
    </div>
    <textarea
      v-model="content"
      placeholder="想到了什么？直接记..."
      class="w-full h-32 bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm text-gray-200 placeholder-gray-500 resize-none focus:outline-none focus:border-purple-500"
    ></textarea>
    <button
      @click="save"
      :disabled="!content.trim() || saving"
      class="mt-3 w-full py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
    >
      {{ saving ? '保存中...' : '保存' }}
    </button>
    <div v-if="saved" class="mt-2 text-xs text-green-400">已保存，AI 正在加工...</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const emit = defineEmits(['close'])
const content = ref('')
const saving = ref(false)
const saved = ref(false)

async function save() {
  if (!content.value.trim()) return
  saving.value = true
  try {
    await api.createRecord(content.value, 'quick_note')
    saved.value = true
    setTimeout(() => { content.value = ''; saved.value = false; emit('close') }, 1500)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    saving.value = false
  }
}
</script>
