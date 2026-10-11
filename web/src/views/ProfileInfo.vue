<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserProfile } from '@/api/auth'
import { getUserInfo, isLoggedIn, setUserInfo } from '@/utils/storage'
import type { UserInfo } from '@/types'

const router = useRouter()
const user = ref<UserInfo | null>(null)

function formatPhone(phone: string | null | undefined) {
  if (!phone) return '-'
  if (phone.length >= 11) {
    return phone.substring(0, 3) + '****' + phone.substring(7)
  }
  return phone
}

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

onMounted(() => {
  loadUserProfile()
})
</script>

<template>
  <div class="sub-page">
    <!-- 顶栏 -->
    <div class="top-bar">
      <span class="back-btn" @click="router.back()">‹</span>
      <span class="top-title">个人信息</span>
      <span class="top-placeholder"></span>
    </div>

    <!-- 信息列表 -->
    <div class="info-section glass-card">
      <div class="info-item">
        <span class="info-label">昵称</span>
        <span class="info-value">{{ user?.nickname || '-' }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">用户名</span>
        <span class="info-value">{{ user?.username || '-' }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">手机号</span>
        <span class="info-value">{{ formatPhone(user?.phone) }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">邮箱</span>
        <span class="info-value">{{ user?.email || '-' }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">角色</span>
        <span class="info-value">
          {{ user?.role_name === 'super_admin' ? '管理员' : '普通用户' }}
        </span>
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

.info-section {
  margin: 12px;
  padding: 0;
  overflow: hidden;
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-divider);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 14px;
  color: var(--color-text-dim);
  width: 70px;
  flex-shrink: 0;
}

.info-value {
  font-size: 14px;
  color: var(--color-text-secondary);
  flex: 1;
  text-align: right;
}
</style>