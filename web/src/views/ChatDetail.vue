<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMessages, sendMessage } from '@/api/chat'
import { getUserInfo } from '@/utils/storage'
import type { ChatMessage } from '@/types'
import type { UserInfo } from '@/types'

const route = useRoute()
const router = useRouter()
const conversationId = Number(route.params.id)

const messages = ref<ChatMessage[]>([])
const inputContent = ref('')
const loading = ref(false)
const sending = ref(false)
const page = ref(1)
const finished = ref(false)

const currentUser = getUserInfo<UserInfo>()

/** 自定义 toast */
function showToast(msg: string) {
  const el = document.createElement('div')
  el.textContent = msg
  Object.assign(el.style, {
    position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
    background: 'rgba(0,0,0,0.7)', color: '#fff', padding: '8px 16px',
    borderRadius: '4px', fontSize: '14px', zIndex: '9999', pointerEvents: 'none'
  })
  document.body.appendChild(el)
  setTimeout(() => el.remove(), 1500)
}

/** 加载消息 */
async function loadMessages(reset = false) {
  if (reset) {
    page.value = 1
    messages.value = []
    finished.value = false
  }
  loading.value = true
  try {
    const res = await getMessages(conversationId, { page: page.value, page_size: 30 })
    const items = res.data.items
    if (reset) {
      messages.value = items
    } else {
      messages.value.push(...items)
    }
    if (items.length < 30) finished.value = true
    page.value++
    await nextTick()
    scrollToBottom()
  } catch {
    finished.value = true
  } finally {
    loading.value = false
  }
}

/** 发送消息 */
async function onSend() {
  const content = inputContent.value.trim()
  if (!content) return
  sending.value = true
  try {
    await sendMessage(conversationId, content)
    inputContent.value = ''
    loadMessages(true)
  } catch {
    showToast('发送失败')
  } finally {
    sending.value = false
  }
}

/** 滚动到底部 */
function scrollToBottom() {
  const container = document.querySelector('.message-list')
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}

/** 是否是自己发的 */
function isSelf(senderId: number) {
  return currentUser && currentUser.id === senderId
}

/** 格式化时间 */
function formatTime(dateStr: string) {
  const d = new Date(dateStr)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  loadMessages(true)
})
</script>

<template>
  <div class="chat-detail-page">
    <!-- 顶部栏 -->
    <header class="top-bar glass-card">
      <div class="top-back" @click="router.back()">← 返回</div>
      <span class="top-title">聊天</span>
      <div class="top-action"></div>
    </header>

    <!-- 消息列表 -->
    <div class="message-list">
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['message-row', isSelf(msg.sender_id) ? 'self' : 'other']"
      >
        <!-- 对方消息 - 左对齐 -->
        <template v-if="!isSelf(msg.sender_id)">
          <div class="msg-avatar">
            {{ msg.sender_name?.charAt(0)?.toUpperCase() || '?' }}
          </div>
          <div class="msg-content">
            <div class="msg-name">{{ msg.sender_name }}</div>
            <div class="msg-bubble glass-card other-bubble">
              {{ msg.content }}
            </div>
            <div class="msg-time">{{ formatTime(msg.created_at) }}</div>
          </div>
        </template>

        <!-- 自己消息 - 右对齐 -->
        <template v-else>
          <div class="msg-content self-content">
            <div class="msg-time">{{ formatTime(msg.created_at) }}</div>
            <div class="msg-bubble self-bubble">
              {{ msg.content }}
            </div>
          </div>
          <div class="msg-avatar self-avatar">
            {{ currentUser?.username?.charAt(0)?.toUpperCase() || '我' }}
          </div>
        </template>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
      </div>
    </div>

    <!-- 输入栏 -->
    <div class="chat-input-bar glass-card">
      <input
        class="glass-input msg-input"
        v-model="inputContent"
        placeholder="输入消息..."
        @keyup.enter="onSend"
      />
      <button
        class="glass-btn-primary send-btn"
        :disabled="!inputContent.trim() || sending"
        @click="onSend"
      >
        {{ sending ? '...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-detail-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--color-bg);
}

/* ========== 顶部栏 ========== */
.top-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: none;
  border-bottom: 1px solid var(--color-glass-border);
  flex-shrink: 0;
}

.top-back {
  color: var(--color-primary);
  cursor: pointer;
  font-size: 14px;
  min-width: 48px;
}

.top-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.top-action {
  min-width: 48px;
}

/* ========== 消息列表 ========== */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.message-row.self {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-avatar);
  background: linear-gradient(135deg, #8B98A5, #536471);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.self-avatar {
  background: linear-gradient(135deg, #1D9BF0, #0D8BD9);
}

.msg-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-width: 72%;
}

.self-content {
  align-items: flex-end;
}

.msg-name {
  font-size: 12px;
  color: var(--color-text-dim);
  padding-left: 4px;
}

.msg-bubble {
  padding: 10px 14px;
  font-size: 15px;
  line-height: 1.5;
  word-break: break-word;
}

.other-bubble {
  border-radius: 18px 18px 18px 4px;
}

.self-bubble {
  background: linear-gradient(135deg, #1D9BF0 0%, #0D8BD9 100%);
  border: none;
  border-radius: 18px 18px 4px 18px;
  color: #fff;
}

.msg-time {
  font-size: 11px;
  color: var(--color-text-dim);
  padding: 0 4px;
}

/* ========== 输入栏 ========== */
.chat-input-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 0;
  border-bottom: none;
  border-left: none;
  border-right: none;
  border-top: 1px solid var(--color-glass-border);
  flex-shrink: 0;
}

.msg-input {
  flex: 1;
  border-radius: var(--radius-input);
  padding: 10px 14px;
  font-size: 14px;
}

.send-btn {
  padding: 10px 16px;
  font-size: 13px;
  white-space: nowrap;
}

/* ========== 加载状态 ========== */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
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
</style>