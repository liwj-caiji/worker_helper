<template>
  <div>
    <div class="flex gap-3 mb-6 flex-wrap">
      <input
        v-model="search"
        @input="fetch"
        placeholder="搜索卡片..."
        class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500 w-64"
      />
      <select v-model="skillTag" @change="fetch" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200">
        <option value="">全部技能</option>
        <option v-for="tag in allTags" :key="tag" :value="tag">{{ tag }}</option>
      </select>
    </div>
    <div v-if="cards.length === 0" class="text-gray-500 text-center py-12">
      还没有经验卡片。去和教练聊聊，或者记点东西吧~
    </div>
    <div class="grid gap-4 md:grid-cols-2">
      <div
        v-for="card in cards" :key="card.id"
        @click="$router.push(`/cards/${card.id}`)"
        class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-purple-700/50 cursor-pointer transition-colors"
      >
        <div class="flex justify-between items-start mb-3">
          <h3 class="font-semibold text-gray-100">{{ card.title }}</h3>
          <span class="text-xs px-2 py-1 rounded-full" :class="scoreColor(card.quality_score)">
            {{ card.quality_score }}
          </span>
        </div>
        <p class="text-sm text-gray-400 line-clamp-2 mb-3">{{ card.tech_solution }}</p>
        <div class="flex flex-wrap gap-1.5">
          <span v-for="tag in card.skill_tags" :key="tag" class="text-xs bg-gray-800 text-teal-400 px-2 py-0.5 rounded">
            {{ tag }}
          </span>
        </div>
        <div class="text-xs text-gray-600 mt-3">{{ formatDate(card.created_at) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const cards = ref([])
const search = ref('')
const skillTag = ref('')
const allTags = ref([])

function scoreColor(s) {
  if (s >= 80) return 'bg-green-900/60 text-green-400'
  if (s >= 60) return 'bg-yellow-900/60 text-yellow-400'
  return 'bg-red-900/60 text-red-400'
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('zh-CN')
}

async function fetch() {
  const { data } = await api.listCards({ search: search.value, skill_tag: skillTag.value || undefined })
  cards.value = data
  allTags.value = [...new Set(data.flatMap(c => c.skill_tags))]
}

onMounted(fetch)
</script>
