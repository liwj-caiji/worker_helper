<template>
  <aside class="w-52 bg-gray-900 border-r border-gray-800 flex flex-col p-4">
    <h1 class="text-lg font-bold mb-8 text-purple-400">经验工厂</h1>
    <nav class="flex flex-col gap-1 flex-1">
      <router-link to="/" class="nav-item" :class="{ active: $route.name === 'coach' }">
        💬 教练对话
      </router-link>
      <router-link to="/cards" class="nav-item" :class="{ active: $route.name === 'cards' }">
        📋 经验卡片
      </router-link>
      <router-link to="/records" class="nav-item" :class="{ active: $route.name === 'records' }">
        📝 原始记录
      </router-link>
    </nav>
    <div class="border-t border-gray-800 pt-4 flex flex-col gap-2">
      <button @click="$emit('toggleQuickNote')" class="text-sm text-gray-400 hover:text-purple-400 text-left">
        ✏️ 随手记
      </button>
      <router-link to="/settings" class="nav-item text-sm" :class="{ active: $route.name === 'settings' }">
        ⚙️ 设置
      </router-link>
    </div>
  </aside>
</template>

<script setup>
defineEmits(['toggleQuickNote'])
</script>

<style scoped>
@reference "tailwindcss";

.nav-item {
  @apply px-3 py-2 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-gray-200 transition-colors text-sm;
}
.nav-item.active {
  @apply bg-purple-900/40 text-purple-300;
}
</style>
