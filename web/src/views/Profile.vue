<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { logout as logoutApi, getUserProfile } from '@/api/auth'
import { getUserInfo, clearAuth, isLoggedIn, setUserInfo } from '@/utils/storage'
import type { UserInfo } from '@/types'

const router = useRouter()

const user = ref<UserInfo | null>(null)

/** 头像地址 */
const avatarUrl = computed(() => {
  if (!user.value?.avatar) return ''
  const avatar = user.value.avatar
  if (avatar.startsWith('http')) return avatar
  return avatar
})

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

/** 加载用户信息 */
async function loadUserProfile() {
  if (!isLoggedIn()) {
    router.replace('/login')
    return
  }
  try {
    const res = await getUserProfile()
    user.value = res.data
    setUserInfo(res.data)
  } catch {
    user.value = getUserInfo<UserInfo>()
  }
}

/** 退出登录 */
async function onLogout() {
  if (!confirm('确定要退出登录吗？')) return
  try {
    await logoutApi()
  } catch { /* 忽略 */ }
  clearAuth()
  showToast('已退出登录')
  router.replace('/login')
}

onMounted(() => {
  loadUserProfile()
})
</script>

<template>
  <div class="profile-page">
    <!-- 头部区域 -->
    <div class="profile-header">
      <div class="avatar-wrap">
        <div class="avatar">
          {{ user?.username?.charAt(0)?.toUpperCase() || '?' }}
        </div>
      </div>
      <h2 class="nickname">{{ user?.username || '未设置' }}</h2>
      <span class="role-tag">
        {{ user?.role_name === 'super_admin' ? '管理员' : '普通用户' }}
      </span>
    </div>

    <!-- 菜单入口 -->
    <div class="menu-section glass-card">
      <div class="menu-item" @click="router.push('/profile/info')">
        <div class="menu-left">
          <span class="menu-icon">👤</span>
          <span class="menu-text">个人信息</span>
        </div>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item" @click="router.push('/profile/func')">
        <div class="menu-left">
          <span class="menu-icon">📋</span>
          <span class="menu-text">功能</span>
        </div>
        <span class="menu-arrow">›</span>
      </div>
      <div class="menu-item" @click="router.push('/profile/settings')">
        <div class="menu-left">
          <span class="menu-icon">⚙️</span>
          <span class="menu-text">设置</span>
        </div>
        <span class="menu-arrow">›</span>
      </div>
    </div>

    <!-- 退出登录 -->
    <div class="logout-btn glass-card" @click="onLogout">
      <span>退出登录</span>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  background: var(--color-bg);
  min-height: 100vh;
  padding-bottom: 30px;
}

/* ========== 头部区域 ========== */
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 0 20px;
  background: linear-gradient(135deg, #1D9BF0 0%, #0D8BD9 100%);
}

.avatar-wrap {
  position: relative;
  margin-bottom: 10px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-avatar);
  border: 3px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

.nickname {
  font-size: 18px;
  color: #fff;
  font-weight: 700;
  margin-bottom: 4px;
}

.role-tag {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 10px;
  border-radius: var(--radius-btn);
}

/* ========== 菜单区域 ========== */
.menu-section {
  margin: 12px 12px 0;
  padding: 0;
  overflow: hidden;
}

.menu-item {
  display: flex;
  flex-direction: row;
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

/* ========== 退出登录 ========== */
.logout-btn {
  margin: 20px 12px 0;
  padding: 14px 0;
  text-align: center;
  font-size: 15px;
  color: var(--color-like);
  cursor: pointer;
  transition: background 0.15s;
}

.logout-btn:active {
  background: var(--color-glass);
}
</style>