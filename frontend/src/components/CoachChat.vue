<template>
  <div class="max-w-3xl mx-auto flex flex-col h-[calc(100vh-8rem)]">
    <div class="mb-4">
      <h2 class="text-xl font-bold">💬 教练对话</h2>
      <p class="text-gray-500 text-sm mt-1">AI 教练会引导你回顾工作，你只需要自然回答</p>
    </div>
    <div class="flex-1 overflow-y-auto space-y-3 mb-4" ref="chatContainer">
      <div v-for="(msg, i) in messages" :key="i" class="flex gap-3" :class="msg.role === 'user' ? 'justify-end' : ''">
        <div v-if="msg.role === 'coach'" class="w-8 h-8 rounded-full bg-teal-500 flex items-center justify-center text-sm flex-shrink-0">AI</div>
        <div class="rounded-lg px-4 py-2.5 max-w-[75%]" :class="msg.role === 'coach' ? 'bg-gray-800 text-gray-200' : 'bg-purple-900/40 text-gray-100'">
          {{ msg.content }}
        </div>
        <div v-if="msg.role === 'user'" class="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center text-sm flex-shrink-0">我</div>
      </div>
      <div v-if="loading" class="flex gap-3">
        <div class="w-8 h-8 rounded-full bg-teal-500 flex items-center justify-center text-sm">AI</div>
        <div class="bg-gray-800 rounded-lg px-4 py-2.5 text-gray-400">思考中...</div>
      </div>
    </div>
    <div class="flex gap-2">
      <input
        v-model="input"
        @keyup.enter="send"
        :disabled="loading"
        placeholder="描述你今天的工作..."
        class="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-purple-500"
      />
      <button @click="send" :disabled="loading || !input.trim()" class="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg font-medium transition-colors">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import api from '../api'

const input = ref('')
const messages = ref([{ role: 'coach', content: '你好！我是你的经验教练 🎯 今天做了什么工作？简单说说就行~' }])
const loading = ref(false)
const chatContainer = ref(null)

async function send() {
  if (!input.value.trim() || loading.value) return
  const userMsg = input.value
  messages.value.push({ role: 'user', content: userMsg })
  input.value = ''
  loading.value = true
  await nextTick()
  scrollBottom()
  try {
    const { data } = await api.coachChat(userMsg)
    messages.value.push({ role: 'coach', content: data.response })
  } catch {
    messages.value.push({ role: 'coach', content: '抱歉，出了点问题。请稍后再试。' })
  } finally {
    loading.value = false
    await nextTick()
    scrollBottom()
  }
}

function scrollBottom() {
  if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
}
</script>
