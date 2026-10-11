<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPostList, getCategoryList, toggleLike } from '@/api/post'
import { isLoggedIn } from '@/utils/storage'
import type { Post, Category } from '@/types'

const router = useRouter()

const posts = ref<Post[]>([])
const categories = ref<Category[]>([])
const activeCategory = ref<number>(0)
const loading = ref(false)
const finished = ref(false)
const page = ref(1)
const pageSize = 10

/** 加载分类 */
async function loadCategories() {
  try {
    const res = await getCategoryList()
    categories.value = res.data
  } catch { /* 忽略 */ }
}

/** 加载帖子列表 */
async function loadPosts(reset = false) {
  if (reset) {
    page.value = 1
    posts.value = []
    finished.value = false
  }
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize }
    if (activeCategory.value !== 0) {
      params.category_id = activeCategory.value
    }
    const res = await getPostList(params)
    const items = res.data.items
    if (reset) {
      posts.value = items
    } else {
      posts.value.push(...items)
    }
    if (items.length < pageSize) finished.value = true
    page.value++
  } catch {
    finished.value = true
  } finally {
    loading.value = false
  }
}

/** 切换分类 */
function onCategoryChange(id: number) {
  activeCategory.value = id
  loadPosts(true)
}

/** 点赞 */
async function onLike(post: Post, e: Event) {
  e.stopPropagation()
  if (!isLoggedIn()) {
    router.push('/login')
    return
  }
  try {
    await toggleLike(post.id, 'post')
    post.like_count++
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

/** 滚动加载 */
function onScroll(e: Event) {
  const el = e.target as HTMLElement
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 200 && !loading.value && !finished.value) {
    loadPosts()
  }
}

onMounted(() => {
  loadCategories()
  loadPosts(true)
})
</script>

<template>
  <div class="home-page" @scroll="onScroll">
    <!-- 分类标签 - 胶囊样式 -->
    <div class="category-bar">
      <div
        :class="['cat-pill', { active: activeCategory === 0 }]"
        @click="onCategoryChange(0)"
      >
        全部
      </div>
      <div
        v-for="cat in categories"
        :key="cat.id"
        :class="['cat-pill', { active: activeCategory === cat.id }]"
        @click="onCategoryChange(cat.id)"
      >
        {{ cat.name }}
      </div>
    </div>

    <!-- 帖子信息流 -->
    <div class="feed">
      <div
        v-for="post in posts"
        :key="post.id"
        class="post-card glass-card animate-fade-in"
        @click="router.push(`/post/${post.id}`)"
      >
        <!-- 帖子头部 -->
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

        <!-- 帖子标题 -->
        <h3 class="post-title">{{ post.title }}</h3>

        <!-- 帖子内容预览 -->
        <p class="post-preview">{{ post.content }}</p>

        <!-- 操作栏 -->
        <div class="post-actions">
          <div class="action-btn" @click="(e) => onLike(post, e)">
            <span class="action-icon">💬</span>
            <span class="action-count">{{ post.comment_count }}</span>
          </div>
          <div class="action-btn" @click="(e) => onLike(post, e)">
            <span class="action-icon">❤️</span>
            <span class="action-count">{{ post.like_count }}</span>
          </div>
          <div class="action-btn">
            <span class="action-icon">🔗</span>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <span>加载中...</span>
      </div>
      <div v-if="finished && posts.length > 0" class="finished-state">
        没有更多帖子了
      </div>
      <div v-if="!loading && finished && posts.length === 0" class="empty-state glass-card">
        <span class="empty-icon">📝</span>
        <p>还没有帖子，快来发第一篇吧！</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: var(--color-bg);
  overflow-y: auto;
}

/* ========== 分类栏 ========== */
.category-bar {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}

.category-bar::-webkit-scrollbar {
  display: none;
}

.cat-pill {
  flex-shrink: 0;
  padding: 6px 16px;
  border-radius: var(--radius-btn);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  cursor: pointer;
  transition: all 0.2s;
}

.cat-pill:hover {
  background: rgba(255, 255, 255, 0.12);
}

.cat-pill.active {
  background: linear-gradient(135deg, #1D9BF0 0%, #0D8BD9 100%);
  color: #fff;
  border-color: transparent;
  font-weight: 600;
}

/* ========== 信息流 ========== */
.feed {
  padding: 0 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ========== 帖子卡片 ========== */
.post-card {
  padding: 14px 16px;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}

.post-card:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.22);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.post-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-avatar);
  background: linear-gradient(135deg, #1D9BF0, #0D8BD9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 1px;
  flex: 1;
  min-width: 0;
}

.post-username {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-time {
  font-size: 12px;
  color: var(--color-text-dim);
}

.post-category {
  flex-shrink: 0;
  padding: 2px 8px;
  border-radius: var(--radius-btn);
  font-size: 11px;
  color: var(--color-primary);
  background: rgba(29, 155, 240, 0.15);
  border: 1px solid rgba(29, 155, 240, 0.25);
}

.post-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 6px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-preview {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 10px;
}

/* ========== 操作栏 ========== */
.post-actions {
  display: flex;
  gap: 24px;
  padding-top: 8px;
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
  font-size: 16px;
}

.action-count {
  font-size: 13px;
  color: var(--color-text-dim);
}

/* ========== 加载状态 ========== */
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