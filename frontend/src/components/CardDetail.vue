<template>
  <div class="max-w-3xl mx-auto">
    <button @click="$router.back()" class="text-gray-400 hover:text-gray-200 mb-4 inline-block">&larr; 返回</button>
    <div v-if="card" class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div class="flex justify-between items-start mb-6">
        <h2 class="text-xl font-bold">{{ card.title }}</h2>
        <span class="text-sm px-3 py-1 rounded-full bg-green-900/60 text-green-400">{{ card.quality_score }} 分</span>
      </div>
      <div class="space-y-4">
        <div>
          <label class="text-xs text-gray-500 uppercase">背景</label>
          <p class="text-gray-200 mt-1">{{ card.background }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">技术方案</label>
          <p class="text-gray-200 mt-1">{{ card.tech_solution }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">量化成果</label>
          <p class="text-teal-400 mt-1 font-medium">{{ card.quantifiable_result }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">反思</label>
          <p class="text-gray-200 mt-1">{{ card.reflection || '暂无' }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase">技能标签</label>
          <div class="flex flex-wrap gap-1.5 mt-1">
            <span v-for="tag in card.skill_tags" :key="tag" class="text-xs bg-gray-800 text-teal-400 px-2 py-0.5 rounded">{{ tag }}</span>
          </div>
        </div>
      </div>
      <div class="mt-6 pt-4 border-t border-gray-800 flex gap-3">
        <router-link v-if="card.source_record_id" :to="`/records/${card.source_record_id}/edit`" class="text-sm text-purple-400 hover:text-purple-300">
          查看原始记录 &rarr;
        </router-link>
        <span class="text-xs text-gray-600">{{ formatDate(card.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const card = ref(null)

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN')
}

onMounted(async () => {
  const { data } = await api.getCard(route.params.id)
  card.value = data
})
</script>
