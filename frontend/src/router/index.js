import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'coach', component: () => import('../views/CoachView.vue') },
  { path: '/cards', name: 'cards', component: () => import('../views/CardsView.vue') },
  { path: '/cards/:id', name: 'card-detail', component: () => import('../views/CardDetailView.vue') },
  { path: '/records', name: 'records', component: () => import('../views/RecordsView.vue') },
  { path: '/records/:id/edit', name: 'record-edit', component: () => import('../views/RecordEditView.vue') },
  { path: '/settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
]

export default createRouter({ history: createWebHistory(), routes })
