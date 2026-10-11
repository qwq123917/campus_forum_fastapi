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
  // 简单显示两个用户名
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
    <!-- 顶部栏 -->
    <header class="top-bar glass-card">
      <h1 class="top-title">💬 消息</h1>
    </header>

    <!-- 会话列表 -->
    <div class="conv-list">
      <div
        v-for="conv in conversations"
        :key="conv.id"
        class="conv-card glass-card animate-fade-in"
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
      <div v-if="!loading && finished && conversations.length === 0" class="empty-state glass-card">
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

/* ========== 顶部栏 ========== */
.top-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: none;
  border-bottom: 1px solid var(--color-glass-border);
}

.top-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text);
}

/* ========== 会话列表 ========== */
.conv-list {
  padding: 8px 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.conv-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.conv-card:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.22);
}

.conv-card:active {
  transform: scale(0.98);
}

.conv-avatar {
  width: 44px;
  height: 44px;
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