<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/** 主题切换 */
const isDark = ref(true)

function initTheme() {
  const saved = localStorage.getItem('theme')
  isDark.value = saved !== 'light'
}

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.removeAttribute('data-theme')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.setAttribute('data-theme', 'light')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  initTheme()
})
</script>

<template>
  <div class="sub-page">
    <!-- 顶栏 -->
    <div class="top-bar">
      <span class="back-btn" @click="router.back()">‹</span>
      <span class="top-title">设置</span>
      <span class="top-placeholder"></span>
    </div>

    <!-- 设置列表 -->
    <div class="menu-section glass-card">
      <div class="menu-item" @click="toggleTheme">
        <div class="menu-left">
          <span class="menu-icon">{{ isDark ? '☀️' : '🌙' }}</span>
          <span class="menu-text">{{ isDark ? '浅色模式' : '深色模式' }}</span>
        </div>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item">
        <div class="menu-left">
          <span class="menu-icon">🔒</span>
          <span class="menu-text">修改密码</span>
        </div>
        <span class="menu-arrow">›</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sub-page {
  background: var(--color-bg);
  min-height: 100vh;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--color-glass);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-btn {
  font-size: 24px;
  color: var(--color-text);
  cursor: pointer;
  width: 32px;
  -webkit-tap-highlight-color: transparent;
}

.top-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.top-placeholder {
  width: 32px;
}

.menu-section {
  margin: 12px;
  padding: 0;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-divider);
  cursor: pointer;
  transition: background 0.15s;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:active {
  background: var(--color-glass);
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.menu-icon {
  font-size: 18px;
}

.menu-text {
  font-size: 15px;
  color: var(--color-text);
}

.menu-arrow {
  font-size: 16px;
  color: var(--color-text-dim);
}
</style>