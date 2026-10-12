<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

function initTheme() {
  const saved = localStorage.getItem('theme')
  if (saved === 'light') {
    document.documentElement.setAttribute('data-theme', 'light')
  } else {
    document.documentElement.removeAttribute('data-theme')
  }
}

onMounted(() => {
  initTheme()
})

const showTabbar = computed(() => {
  return !['/login', '/register'].includes(route.path)
})

const activeTab = computed(() => {
  const path = route.path
  if (path === '/') return 'home'
  if (path.startsWith('/notifications')) return 'notifications'
  if (path.startsWith('/chat')) return 'messages'
  if (path.startsWith('/profile')) return 'profile'
  return 'home'
})

function onTabClick(tab: string) {
  const routes: Record<string, string> = {
    home: '/',
    notifications: '/',
    messages: '/chat',
    profile: '/profile',
  }
  const target = routes[tab] || '/'
  if (route.path !== target) {
    router.push(target)
  }
}
</script>

<template>
  <div class="app-shell">
    <main class="app-main">
      <router-view />
    </main>

    <!-- 底部导航 - 玻璃拟态 -->
    <nav v-if="showTabbar" class="tabbar glass-card">
      <div
        v-for="tab in [
          { key: 'home', icon: '🏠', label: '首页' },
          { key: 'notifications', icon: '🔔', label: '通知' },
          { key: 'messages', icon: '💬', label: '消息' },
          { key: 'profile', icon: '👤', label: '我' },
        ]"
        :key="tab.key"
        :class="['tabbar-item', { active: activeTab === tab.key }]"
        @click="onTabClick(tab.key)"
      >
        <span class="tabbar-icon">{{ tab.icon }}</span>
        <span class="tabbar-label">{{ tab.label }}</span>
      </div>
    </nav>

  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.app-main {
  flex: 1;
  padding-bottom: calc(var(--tabbar-height) + 16px);
}

/* ========== 底部导航 ========== */
.tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--tabbar-height);
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0;
  border-top: 1px solid var(--color-glass-border);
  border-left: none;
  border-right: none;
  border-bottom: none;
  z-index: 100;
}

.tabbar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 4px 12px;
  cursor: pointer;
  transition: transform 0.15s;
  -webkit-tap-highlight-color: transparent;
}

.tabbar-item:active {
  transform: scale(0.9);
}

.tabbar-icon {
  font-size: 20px;
  line-height: 1;
  transition: transform 0.2s;
}

.tabbar-item.active .tabbar-icon {
  transform: scale(1.1);
}

.tabbar-label {
  font-size: 10px;
  color: var(--color-text-dim);
  transition: color 0.2s;
}

.tabbar-item.active .tabbar-label {
  color: var(--color-primary);
  font-weight: 600;
}


</style>