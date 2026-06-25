<template>
  <div class="max-w-3xl mx-auto">
    <button @click="$router.back()" class="text-gray-400 hover:text-gray-200 mb-4 inline-block">&larr; 返回</button>
    <h2 class="text-xl font-bold mb-6">✏️ 编辑原始记录</h2>
    <div v-if="record" class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div class="mb-4">
        <label class="text-xs text-gray-500 uppercase mb-2 block">原始内容</label>
        <textarea
          v-model="content"
          class="w-full h-48 bg-gray-800 border border-gray-700 rounded-lg p-4 text-gray-200 focus:outline-none focus:border-purple-500 resize-none"
        ></textarea>
      </div>
      <div class="flex gap-3">
        <button @click="save" :disabled="saving" class="px-6 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg font-medium transition-colors">
          {{ saving ? '保存中...' : '保存并重新加工' }}
        </button>
        <button @click="$router.back()" class="px-6 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg font-medium transition-colors">
          取消
        </button>
      </div>
      <div v-if="saved" class="mt-3 text-sm text-green-400">已保存，AI 正在重新加工经验卡片...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const record = ref(null)
const content = ref('')
const saving = ref(false)
const saved = ref(false)

onMounted(async () => {
  const { data } = await api.getRecord(route.params.id)
  record.value = data
  content.value = data.content
})

async function save() {
  saving.value = true
  try {
    await api.updateRecord(route.params.id, content.value)
    saved.value = true
    setTimeout(() => { saved.value = false }, 3000)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    saving.value = false
  }
}
</script>
