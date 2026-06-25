<template>
  <div>
    <div class="flex gap-3 mb-6">
      <select v-model="sourceType" @change="fetch" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200">
        <option value="">全部来源</option>
        <option value="chat">教练对话</option>
        <option value="quick_note">随手记</option>
      </select>
      <select v-model="processStatus" @change="fetch" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200">
        <option value="">全部状态</option>
        <option value="pending">待加工</option>
        <option value="processed">已加工</option>
      </select>
    </div>
    <div v-if="records.length === 0" class="text-gray-500 text-center py-12">
      还没有原始记录。
    </div>
    <div class="space-y-3">
      <div
        v-for="record in records" :key="record.id"
        class="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors"
      >
        <div class="flex justify-between items-start mb-2">
          <div class="flex gap-2 items-center">
            <span class="text-xs px-2 py-0.5 rounded" :class="record.source_type === 'chat' ? 'bg-blue-900/60 text-blue-400' : 'bg-purple-900/60 text-purple-400'">
              {{ record.source_type === 'chat' ? '对话' : '快记' }}
            </span>
            <span class="text-xs px-2 py-0.5 rounded" :class="record.process_status === 'processed' ? 'bg-green-900/60 text-green-400' : 'bg-yellow-900/60 text-yellow-400'">
              {{ record.process_status === 'processed' ? '已加工' : '待加工' }}
            </span>
          </div>
          <span class="text-xs text-gray-600">{{ formatDate(record.recorded_at) }}</span>
        </div>
        <p class="text-sm text-gray-300 line-clamp-2">{{ record.content }}</p>
        <div class="mt-3">
          <router-link :to="`/records/${record.id}/edit`" class="text-xs text-purple-400 hover:text-purple-300">编辑</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const records = ref([])
const sourceType = ref('')
const processStatus = ref('')

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN')
}

async function fetch() {
  const params = {}
  if (sourceType.value) params.source_type = sourceType.value
  if (processStatus.value) params.process_status = processStatus.value
  const { data } = await api.listRecords(params)
  records.value = data
}

onMounted(fetch)
</script>
