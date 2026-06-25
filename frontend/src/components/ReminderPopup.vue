<template>
  <div class="fixed bottom-6 right-6 w-96 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl z-50 overflow-hidden">
    <div class="bg-purple-900/60 px-4 py-2 flex justify-between items-center">
      <span class="text-sm font-medium">⏰ 经验教练 · 每日快问</span>
      <button @click="$emit('close')" class="text-gray-400 hover:text-gray-200">&times;</button>
    </div>
    <div class="p-4 space-y-3">
      <div v-for="(msg, i) in messages" :key="i" class="flex gap-2" :class="msg.role === 'user' ? 'justify-end' : ''">
        <div v-if="msg.role === 'coach'" class="w-6 h-6 rounded-full bg-teal-500 flex items-center justify-center text-xs flex-shrink-0">AI</div>
        <div class="rounded-lg px-3 py-2 text-sm max-w-[80%]" :class="msg.role === 'coach' ? 'bg-gray-800' : 'bg-purple-900/40'">
          {{ msg.content }}
        </div>
        <div v-if="msg.role === 'user'" class="w-6 h-6 rounded-full bg-yellow-500 flex items-center justify-center text-xs flex-shrink-0">我</div>
      </div>
    </div>
    <div class="border-t border-gray-800 p-3 flex gap-2">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="输入回复..."
        class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500"
      />
      <button @click="send" class="px-4 py-2 bg-teal-500 hover:bg-teal-600 rounded-lg text-sm font-medium text-black">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const emit = defineEmits(['close'])
const input = ref('')
const messages = ref([{ role: 'coach', content: '今天主要做了什么？一句话就行 👋' }])

async function send() {
  if (!input.value.trim()) return
  const userMsg = input.value
  messages.value.push({ role: 'user', content: userMsg })
  input.value = ''
  try {
    const { data } = await api.coachChat(userMsg)
    messages.value.push({ role: 'coach', content: data.response })
  } catch {
    messages.value.push({ role: 'coach', content: '抱歉，出错了。请稍后再试。' })
  }
}
</script>
