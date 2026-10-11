<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createPost, getCategoryList } from '@/api/post'
import type { Category, PostCreateParams } from '@/types'

const router = useRouter()

const form = ref<PostCreateParams>({
  title: '',
  content: '',
  category_id: 0,
})
const categories = ref<Category[]>([])
const loading = ref(false)

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

/** 加载分类 */
async function loadCategories() {
  try {
    const res = await getCategoryList()
    categories.value = res.data
    if (categories.value.length > 0) {
      form.value.category_id = categories.value[0].id
    }
  } catch { /* 忽略 */ }
}

/** 提交发帖 */
async function onSubmit() {
  if (!form.value.title.trim()) {
    return showToast('请输入标题')
  }
  if (!form.value.content.trim()) {
    return showToast('请输入内容')
  }
  if (!form.value.category_id) {
    return showToast('请选择分类')
  }

  loading.value = true
  try {
    await createPost(form.value)
    showToast('发布成功')
    router.back()
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <div class="create-page">
    <!-- 顶部栏 -->
    <header class="top-bar glass-card">
      <div class="top-back" @click="router.back()">← 取消</div>
      <span class="top-title">发帖</span>
      <button
        class="glass-btn-primary publish-btn"
        :disabled="loading || !form.title.trim() || !form.content.trim()"
        @click="onSubmit"
      >
        {{ loading ? '发布中...' : '发布' }}
      </button>
    </header>

    <!-- 表单 -->
    <div class="form-area">
      <!-- 分类选择 -->
      <div class="category-bar">
        <div
          v-for="cat in categories"
          :key="cat.id"
          :class="['cat-pill', { active: form.category_id === cat.id }]"
          @click="form.category_id = cat.id"
        >
          {{ cat.name }}
        </div>
      </div>

      <!-- 标题输入 -->
      <div class="input-group glass-card">
        <input
          class="title-input"
          v-model="form.title"
          placeholder="帖子标题"
          maxlength="100"
        />
      </div>

      <!-- 内容输入 -->
      <div class="input-group glass-card content-group">
        <textarea
          class="content-input"
          v-model="form.content"
          placeholder="分享你的想法..."
          rows="8"
          maxlength="5000"
        ></textarea>
        <div class="char-count">{{ form.content.length }}/5000</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.create-page {
  min-height: 100vh;
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
  padding: 10px 16px;
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

.publish-btn {
  padding: 6px 16px;
  font-size: 13px;
}

/* ========== 表单 ========== */
.form-area {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ========== 分类栏 ========== */
.category-bar {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  white-space: nowrap;
  padding-bottom: 4px;
  -webkit-overflow-scrolling: touch;
}

.category-bar::-webkit-scrollbar {
  display: none;
}

.cat-pill {
  flex-shrink: 0;
  padding: 6px 14px;
  border-radius: var(--radius-btn);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  cursor: pointer;
  transition: all 0.2s;
}

.cat-pill.active {
  background: linear-gradient(135deg, #1D9BF0 0%, #0D8BD9 100%);
  color: #fff;
  border-color: transparent;
  font-weight: 600;
}

/* ========== 输入组 ========== */
.input-group {
  padding: 14px 16px;
}

.title-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.4;
}

.title-input::placeholder {
  color: var(--color-text-dim);
}

.content-group {
  display: flex;
  flex-direction: column;
}

.content-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: var(--color-text);
  line-height: 1.6;
  resize: none;
  min-height: 200px;
}

.content-input::placeholder {
  color: var(--color-text-dim);
}

.char-count {
  text-align: right;
  font-size: 12px;
  color: var(--color-text-dim);
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--color-divider);
}
</style>