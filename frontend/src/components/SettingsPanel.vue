<template>
  <div class="max-w-2xl space-y-8">
    <section class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 class="font-semibold mb-4">🤖 LLM 配置</h3>
      <div class="space-y-4">
        <div>
          <label class="text-sm text-gray-400 block mb-1">模型供应商</label>
          <select v-model="llm.llm_provider" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200">
            <option value="claude">Claude (Anthropic)</option>
            <option value="openai">OpenAI (GPT)</option>
          </select>
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">API Key</label>
          <input v-model="llm.llm_api_key" type="password" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">Base URL (可选)</label>
          <input v-model="llm.llm_base_url" placeholder="留空使用默认" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">模型名称</label>
          <input v-model="llm.llm_model" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <button @click="saveLLM" :disabled="savingLLM" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg text-sm font-medium">
          {{ savingLLM ? '保存中...' : '保存 LLM 配置' }}
        </button>
        <div v-if="llmSaved" class="text-sm text-green-400">配置已保存，LLM 提供者已重置</div>
      </div>
    </section>
    <section class="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 class="font-semibold mb-4">⏰ 提醒设置</h3>
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <input v-model="reminder.reminder_enabled" type="checkbox" class="w-4 h-4" />
          <label class="text-sm text-gray-300">启用每日提醒</label>
        </div>
        <div>
          <label class="text-sm text-gray-400 block mb-1">提醒时间</label>
          <input v-model="reminder.reminder_time" type="time" class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-gray-200" />
        </div>
        <button @click="saveReminder" :disabled="savingReminder" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 rounded-lg text-sm font-medium">
          {{ savingReminder ? '保存中...' : '保存提醒配置' }}
        </button>
        <div v-if="reminderSaved" class="text-sm text-green-400">配置已保存</div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'

const llm = reactive({ llm_provider: 'claude', llm_api_key: '', llm_base_url: '', llm_model: 'claude-sonnet-4-6' })
const reminder = reactive({ reminder_enabled: true, reminder_time: '17:30' })
const savingLLM = ref(false)
const savingReminder = ref(false)
const llmSaved = ref(false)
const reminderSaved = ref(false)

onMounted(async () => {
  try {
    const { data: d } = await api.getLLMSettings()
    Object.assign(llm, d)
  } catch {}
  try {
    const { data: d } = await api.getReminderSettings()
    Object.assign(reminder, d)
  } catch {}
})

async function saveLLM() {
  savingLLM.value = true
  try {
    await api.updateLLMSettings({ ...llm })
    llmSaved.value = true
    setTimeout(() => llmSaved.value = false, 3000)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    savingLLM.value = false
  }
}

async function saveReminder() {
  savingReminder.value = true
  try {
    await api.updateReminderSettings({ ...reminder })
    reminderSaved.value = true
    setTimeout(() => reminderSaved.value = false, 3000)
  } catch (e) {
    alert('保存失败: ' + e.message)
  } finally {
    savingReminder.value = false
  }
}
</script>
