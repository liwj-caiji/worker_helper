import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export default {
  // Records
  createRecord(content, sourceType = 'quick_note') {
    return api.post('/records', { content, source_type: sourceType })
  },
  listRecords(params) {
    return api.get('/records', { params })
  },
  getRecord(id) {
    return api.get(`/records/${id}`)
  },
  updateRecord(id, content) {
    return api.put(`/records/${id}`, { content })
  },
  deleteRecord(id) {
    return api.delete(`/records/${id}`)
  },

  // Cards
  listCards(params) {
    return api.get('/cards', { params })
  },
  getCard(id) {
    return api.get(`/cards/${id}`)
  },
  updateCard(id, data) {
    return api.put(`/cards/${id}`, data)
  },

  // Coach
  coachChat(content, history = []) {
    return api.post('/coach/chat', { content, history })
  },

  // Settings
  getLLMSettings() {
    return api.get('/settings/llm')
  },
  updateLLMSettings(data) {
    return api.put('/settings/llm', data)
  },
  getReminderSettings() {
    return api.get('/settings/reminder')
  },
  updateReminderSettings(data) {
    return api.put('/settings/reminder', data)
  },
  getReminderStatus() {
    return api.get('/settings/reminder/status')
  },
}
