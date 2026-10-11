<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPostDetail, getComments, createComment, toggleLike, deletePost } from '@/api/post'
import { isLoggedIn, getUserInfo } from '@/utils/storage'
import type { Post, Comment } from '@/types'
import type { UserInfo } from '@/types'

const route = useRoute()
const router = useRouter()
const postId = Number(route.params.id)

const post = ref<Post | null>(null)
const comments = ref<Comment[]>([])
const commentContent = ref('')
const loading = ref(false)
const commentLoading = ref(false)
const commentFinished = ref(false)
const commentPage = ref(1)
const liked = ref(false)

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

/** 加载帖子详情 */
async function loadPost() {
  try {
    const res = await getPostDetail(postId)
    post.value = res.data
  } catch {
    showToast('帖子不存在')
    router.back()
  }
}

/** 加载评论 */
async function loadComments(reset = false) {
  if (reset) {
    commentPage.value = 1
    comments.value = []
    commentFinished.value = false
  }
  commentLoading.value = true
  try {
    const res = await getComments(postId, { page: commentPage.value, page_size: 20 })
    const items = res.data.items
    if (reset) {
      comments.value = items
    } else {
      comments.value.push(...items)
    }
    if (items.length < 20) commentFinished.value = true
    commentPage.value++
  } catch {
    commentFinished.value = true
  } finally {
    commentLoading.value = false
  }
}

/** 点赞帖子 */
async function onLikePost() {
  if (!isLoggedIn()) return router.push('/login')
  try {
    await toggleLike(postId, 'post')
    liked.value = !liked.value
    if (post.value) {
      post.value.like_count += liked.value ? 1 : -1
    }
  } catch { /* 忽略 */ }
}

/** 发表评论 */
async function onComment() {
  if (!isLoggedIn()) return router.push('/login')
  if (!commentContent.value.trim()) return showToast('请输入评论内容')
  try {
    await createComment(postId, { content: commentContent.value.trim() })
    commentContent.value = ''
    showToast('评论成功')
    loadComments(true)
  } catch { /* 忽略 */ }
}

/** 删除帖子 */
async function onDeletePost() {
  if (!confirm('确定要删除这篇帖子吗？')) return
  try {
    await deletePost(postId)
    showToast('删除成功')
    router.back()
  } catch { /* 忽略 */ }
}

/** 格式化时间 */
function formatTime(dateStr: string) {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}小时前`
  const days = Math.floor(hours / 24)
  if (days < 30) return `${days}天前`
  return d.toLocaleDateString()
}

/** 是否是帖子作者 */
function isAuthor() {
  const user = getUserInfo<UserInfo>()
  return user && post.value && user.id === post.value.user_id
}

/** 滚动加载评论 */
function onScroll(e: Event) {
  const el = e.target as HTMLElement
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 100 && !commentLoading.value && !commentFinished.value) {
    loadComments()
  }
}

onMounted(() => {
  loadPost()
  loadComments(true)
})
</script>

<template>
  <div class="detail-page" v-if="post" @scroll="onScroll">
    <!-- 顶部栏 -->
    <header class="top-bar glass-card">
      <div class="top-back" @click="router.back()">← 返回</div>
      <span class="top-title">帖子详情</span>
      <div v-if="isAuthor()" class="top-action" @click="onDeletePost">删除</div>
      <div v-else class="top-action"></div>
    </header>

    <!-- 帖子内容 -->
    <div class="post-detail glass-card animate-fade-in">
      <div class="post-header">
        <div class="post-avatar">
          {{ post.username?.charAt(0)?.toUpperCase() || '?' }}
        </div>
        <div class="post-meta">
          <span class="post-username">{{ post.username || '匿名' }}</span>
          <span class="post-time">{{ formatTime(post.created_at) }}</span>
        </div>
        <span v-if="post.category_name" class="post-category">{{ post.category_name }}</span>
      </div>

      <h2 class="post-title">{{ post.title }}</h2>
      <div class="post-body">{{ post.content }}</div>

      <!-- 操作栏 -->
      <div class="post-actions">
        <div class="action-btn" @click="onLikePost">
          <span :class="['action-icon', { 'animate-heart': liked }]">
            {{ liked ? '❤️' : '🤍' }}
          </span>
          <span class="action-count">{{ post.like_count }}</span>
        </div>
        <div class="action-btn">
          <span class="action-icon">💬</span>
          <span class="action-count">{{ post.comment_count }}</span>
        </div>
        <div class="action-btn">
          <span class="action-icon">🔗</span>
        </div>
      </div>
    </div>

    <!-- 评论区 -->
    <div class="comment-section">
      <div class="section-header">
        <span class="section-title">评论 ({{ comments.length }})</span>
      </div>

      <div v-for="comment in comments" :key="comment.id" class="comment-card glass-card animate-fade-in">
        <div class="comment-header">
          <div class="comment-avatar">
            {{ comment.username?.charAt(0)?.toUpperCase() || '?' }}
          </div>
          <div class="comment-meta">
            <span class="comment-username">{{ comment.username || '匿名' }}</span>
            <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
          </div>
        </div>
        <div class="comment-body">{{ comment.content }}</div>
      </div>

      <div v-if="commentLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <span>加载中...</span>
      </div>
      <div v-if="commentFinished && comments.length > 0" class="finished-state">
        没有更多评论了
      </div>
      <div v-if="!commentLoading && commentFinished && comments.length === 0" class="empty-comments">
        还没有评论，来说点什么吧
      </div>
    </div>

    <!-- 评论输入框 -->
    <div v-if="isLoggedIn()" class="comment-input-bar glass-card">
      <input
        class="glass-input comment-input"
        v-model="commentContent"
        placeholder="写评论..."
        @keyup.enter="onComment"
      />
      <button class="glass-btn-primary send-btn" @click="onComment" :disabled="!commentContent.trim()">
        发送
      </button>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: var(--color-bg);
  overflow-y: auto;
  padding-bottom: 80px;
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
  color: var(--color-like);
  cursor: pointer;
  font-size: 14px;
  min-width: 48px;
  text-align: right;
}

/* ========== 帖子详情 ========== */
.post-detail {
  margin: 12px;
  padding: 16px;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.post-avatar {
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

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.post-username {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text);
}

.post-time {
  font-size: 12px;
  color: var(--color-text-dim);
}

.post-category {
  padding: 2px 8px;
  border-radius: var(--radius-btn);
  font-size: 11px;
  color: var(--color-primary);
  background: rgba(29, 155, 240, 0.15);
  border: 1px solid rgba(29, 155, 240, 0.25);
}

.post-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 10px;
  line-height: 1.4;
}

.post-body {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  white-space: pre-wrap;
  margin-bottom: 14px;
}

/* ========== 操作栏 ========== */
.post-actions {
  display: flex;
  gap: 32px;
  padding-top: 12px;
  border-top: 1px solid var(--color-divider);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: transform 0.15s;
}

.action-btn:active {
  transform: scale(0.9);
}

.action-icon {
  font-size: 18px;
}

.action-count {
  font-size: 13px;
  color: var(--color-text-dim);
}

/* ========== 评论区 ========== */
.comment-section {
  padding: 0 12px;
}

.section-header {
  padding: 16px 4px 8px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.comment-card {
  padding: 12px 14px;
  margin-bottom: 8px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-avatar);
  background: linear-gradient(135deg, #8B98A5, #536471);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.comment-meta {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.comment-username {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.comment-time {
  font-size: 11px;
  color: var(--color-text-dim);
}

.comment-body {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  padding-left: 40px;
}

/* ========== 评论输入栏 ========== */
.comment-input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 0;
  border-bottom: none;
  border-left: none;
  border-right: none;
  border-top: 1px solid var(--color-glass-border);
  z-index: 50;
}

.comment-input {
  flex: 1;
  border-radius: var(--radius-input);
  padding: 8px 14px;
  font-size: 14px;
}

.send-btn {
  padding: 8px 16px;
  font-size: 13px;
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

.finished-state, .empty-comments {
  text-align: center;
  padding: 20px;
  color: var(--color-text-dim);
  font-size: 13px;
}
</style>