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

/** 切换主题 */
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme')
  if (current === 'light') {
    document.documentElement.removeAttribute('data-theme')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.setAttribute('data-theme', 'light')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  loadUserProfile()
})
</script>

<template>
  <div class="profile-page">
    <!-- 用户信息区 -->
    <div class="profile-header">
      <div class="header-main">
        <div class="header-left" @click="router.push('/profile/info')">
          <div class="avatar-wrap">
            <div class="avatar">
              <img v-if="avatarUrl" :src="avatarUrl" alt="头像" class="avatar-img" />
              <span v-else class="avatar-text">{{ user?.username?.charAt(0)?.toUpperCase() || '?' }}</span>
            </div>
            <span class="avatar-badge">2</span>
          </div>
          <div class="user-meta">
            <div class="nickname-row">
              <span class="nickname">{{ user?.username || '未设置' }}</span>
              <span class="arrow-icon">›</span>
            </div>

          </div>
        </div>
        <div class="header-right">
          <span class="header-icon" @click="toggleTheme" title="主题">🌙</span>
          <span class="header-icon" title="扫扫">📷</span>
        </div>
      </div>

      <!-- 数据栏 -->
      <div class="data-bar">
        <div class="data-item">
          <span class="data-num">1</span>
          <span class="data-label">发布</span>
        </div>
        <div class="data-item">
          <span class="data-num">14</span>
          <span class="data-label">获赞</span>
        </div>

      </div>
    </div>

    <!-- 会员横幅 -->
    <div class="member-banner">
      <div class="banner-left">
        <span class="banner-title">校园会员</span>
        <span class="banner-divider"></span>
        <span class="banner-subtitle">解锁最新企业真题</span>
      </div>
      <button class="banner-btn">立即开通</button>
    </div>

    <!-- 菜单入口 -->
    <div class="menu-section">
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
    <div class="logout-btn" @click="onLogout">
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

/* ========== 用户信息区 ========== */
.profile-header {
  padding: 16px 16px 0;
  background: linear-gradient(180deg, rgba(29, 155, 240, 0.15) 0%, transparent 100%);
}

.header-main {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 12px 0 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-avatar);
  background: linear-gradient(135deg, #1D9BF0, #0D8BD9);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.15);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-text {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}

.avatar-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: var(--color-primary);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-bg);
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nickname-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nickname {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
}

.arrow-icon {
  font-size: 16px;
  color: var(--color-text-dim);
}



.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--color-glass);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.15s;
  -webkit-tap-highlight-color: transparent;
}

.header-icon:active {
  background: rgba(255, 255, 255, 0.15);
}

/* ========== 数据栏 ========== */
.data-bar {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid var(--color-divider);
}

.data-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.data-num {
  font-size: 17px;
  font-weight: 700;
  color: var(--color-text);
}

.data-label {
  font-size: 12px;
  color: var(--color-text-secondary);
}



/* ========== 会员横幅 ========== */
.member-banner {
  margin: 12px 16px 0;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #1a2a4a 0%, #0f1b33 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.banner-title {
  font-size: 15px;
  font-weight: 700;
  color: #FFD400;
}

.banner-divider {
  width: 1px;
  height: 14px;
  background: rgba(255, 255, 255, 0.25);
}

.banner-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.banner-btn {
  padding: 6px 16px;
  border-radius: var(--radius-btn);
  background: linear-gradient(135deg, #FFD400, #FF8C00);
  color: #1a2a4a;
  font-size: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s;
  -webkit-tap-highlight-color: transparent;
}

.banner-btn:active {
  transform: scale(0.95);
}

/* ========== 菜单区域 ========== */
.menu-section {
  margin: 12px 16px 0;
  border-radius: var(--radius-sm);
  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
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
  margin: 20px 16px 0;
  padding: 14px 0;
  text-align: center;
  font-size: 15px;
  color: var(--color-like);
  cursor: pointer;
  border-radius: var(--radius-sm);
  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  transition: background 0.15s;
}

.logout-btn:active {
  background: var(--color-glass);
}
</style>