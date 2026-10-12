<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getConversations } from '@/api/chat'
import { isLoggedIn } from '@/utils/storage'
import type { ChatConversation } from '@/types'

const router = useRouter()

const conversations = ref<ChatConversation[]>([])
const loading = ref(false)
const finished = ref(false)
const page = ref(1)

/** 消息分类 */
const msgCategories = [
  { icon: '🔔', label: '系统通知', badge: true },
  { icon: '👍', label: '赞和收藏', badge: false },
  { icon: '💬', label: '评论和@', badge: false },
  { icon: '👤', label: '新增关注', badge: false },
]

/** 加载会话列表 */
async function loadConversations(reset = false) {
  if (!isLoggedIn()) {
    router.push('/login')
    return
  }
  if (reset) {
    page.value = 1
    conversations.value = []
    finished.value = false
  }
  loading.value = true
  try {
    const res = await getConversations({ page: page.value, page_size: 20 })
    const items = res.data.items
    if (reset) {
      conversations.value = items
    } else {
      conversations.value.push(...items)
    }
    if (items.length < 20) finished.value = true
    page.value++
  } catch {
    finished.value = true
  } finally {
    loading.value = false
  }
}

/** 格式化时间 */
function formatTime(dateStr: string | null) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}小时前`
  return d.toLocaleDateString()
}

/** 获取对方名字 */
function getOtherName(conv: ChatConversation) {
  return `${conv.user1_name} / ${conv.user2_name}`
}

/** 滚动加载 */
function onScroll(e: Event) {
  const el = e.target as HTMLElement
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 100 && !loading.value && !finished.value) {
    loadConversations()
  }
}

onMounted(() => {
  loadConversations(true)
})
</script>

<template>
  <div class="chat-list-page" @scroll="onScroll">
    <!-- 顶部导航栏 -->
    <header class="top-bar">
      <h1 class="top-title">消息</h1>
      <div class="top-actions">
        <span class="top-action-icon" title="搜索">🔍</span>
        <span class="top-action-icon" title="清空">🗑️</span>
      </div>
    </header>

    <!-- 消息分类快捷区 -->
    <div class="category-bar">
      <div
        v-for="cat in msgCategories"
        :key="cat.label"
        class="category-item"
      >
        <div class="category-icon-wrap">
          <span class="category-icon">{{ cat.icon }}</span>
          <span v-if="cat.badge" class="category-badge"></span>
        </div>
        <span class="category-label">{{ cat.label }}</span>
      </div>
    </div>

    <!-- 会话列表 -->
    <div class="conv-list">
      <div
        v-for="conv in conversations"
        :key="conv.id"
        class="conv-card animate-fade-in"
        @click="router.push(`/chat/${conv.id}`)"
      >
        <div class="conv-avatar">
          {{ getOtherName(conv).charAt(0) }}
        </div>
        <div class="conv-info">
          <div class="conv-top">
            <span class="conv-name">{{ getOtherName(conv) }}</span>
            <span class="conv-time">{{ formatTime(conv.last_time) }}</span>
          </div>
          <span class="conv-last-msg">{{ conv.last_message || '暂无消息' }}</span>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <span>加载中...</span>
      </div>
      <div v-if="finished && conversations.length > 0" class="finished-state">
        没有更多会话了
      </div>
      <div v-if="!loading && finished && conversations.length === 0" class="empty-state">
        <span class="empty-icon">💬</span>
        <p>暂无会话</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-list-page {
  min-height: 100vh;
  background: var(--color-bg);
  overflow-y: auto;
}

/* ========== 顶部导航栏 ========== */
.top-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-divider);
}

.top-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.top-action-icon {
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.15s;
  -webkit-tap-highlight-color: transparent;
}

.top-action-icon:active {
  transform: scale(0.9);
}

/* ========== 消息分类快捷区 ========== */
.category-bar {
  display: flex;
  align-items: flex-start;
  justify-content: space-around;
  padding: 16px 8px;
  border-bottom: 1px solid var(--color-divider);
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.category-icon-wrap {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: var(--color-glass);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.category-item:active .category-icon-wrap {
  background: rgba(255, 255, 255, 0.15);
}

.category-icon {
  font-size: 20px;
}

.category-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-like);
}

.category-label {
  font-size: 11px;
  color: var(--color-text-secondary);
}

/* ========== 会话列表 ========== */
.conv-list {
  padding: 0 0 20px;
  display: flex;
  flex-direction: column;
}

.conv-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid var(--color-divider);
}

.conv-card:active {
  background: var(--color-glass);
}

.conv-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-avatar);
  background: linear-gradient(135deg, #1D9BF0, #0D8BD9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.conv-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.conv-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.conv-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-time {
  font-size: 12px;
  color: var(--color-text-dim);
  flex-shrink: 0;
  margin-left: 8px;
}

.conv-last-msg {
  font-size: 13px;
  color: var(--color-text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ========== 状态 ========== */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px;
  color: var(--color-text-dim);
  font-size: 14px;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--color-glass-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.finished-state {
  text-align: center;
  padding: 20px;
  color: var(--color-text-dim);
  font-size: 13px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 20px;
  color: var(--color-text-dim);
  font-size: 14px;
}

.empty-icon {
  font-size: 40px;
}
</style>