<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login as loginApi } from '@/api/auth'
import { setSessionId, setUserInfo, isLoggedIn } from '@/utils/storage'
import type { LoginParams } from '@/types'

const router = useRouter()
const route = useRoute()

/** 已登录则跳转首页 */
if (isLoggedIn()) {
  router.replace('/')
}

const loginType = ref<'phone' | 'email'>('phone')
const phone = ref('')
const email = ref('')
const password = ref('')
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

/** 是否可提交 */
const canSubmit = computed(() => {
  if (loginType.value === 'phone') {
    return phone.value.trim().length === 11 && password.value.length >= 6
  }
  return email.value.trim().length > 0 && password.value.length >= 6
})

/** 切换登录方式 */
function switchType(type: 'phone' | 'email') {
  loginType.value = type
}

/** 提交登录 */
async function onSubmit() {
  if (!canSubmit.value) {
    if (loginType.value === 'phone' && phone.value.trim().length !== 11) {
      return showToast('请输入正确的手机号')
    }
    if (password.value.length < 6) {
      return showToast('密码不能少于6位')
    }
    return
  }

  loading.value = true
  try {
    const params: LoginParams = { password: password.value }
    if (loginType.value === 'phone') {
      params.phone = phone.value.trim()
    } else {
      params.email = email.value.trim()
    }
    const res = await loginApi(params)
    setSessionId(res.data.session_id)
    setUserInfo(res.data.user)
    showToast('登录成功')
    const redirect = (route.query.redirect as string) || '/'
    router.replace(redirect)
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}

function goRegister() {
  router.push('/register')
}
</script>

<template>
  <div class="login-page">
    <!-- 头部 -->
    <div class="header">
      <span class="logo">🎓</span>
      <h1 class="app-name">校园论坛</h1>
      <p class="app-desc">登录你的账号</p>
    </div>

    <!-- 登录方式切换 Tab -->
    <div class="tab-bar">
      <div
        :class="['tab-item', loginType === 'phone' ? 'tab-active' : '']"
        @click="switchType('phone')"
      >
        <span>手机号</span>
      </div>
      <div
        :class="['tab-item', loginType === 'email' ? 'tab-active' : '']"
        @click="switchType('email')"
      >
        <span>邮箱</span>
      </div>
    </div>

    <!-- 手机号登录表单 -->
    <div class="form" v-if="loginType === 'phone'">
      <div class="input-group glass-card">
        <span class="input-icon">📱</span>
        <input
          class="input"
          type="tel"
          v-model="phone"
          placeholder="请输入手机号"
          maxlength="11"
        />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">🔒</span>
        <input
          class="input"
          type="password"
          v-model="password"
          placeholder="请输入密码"
          maxlength="20"
        />
      </div>
    </div>

    <!-- 邮箱登录表单 -->
    <div class="form" v-if="loginType === 'email'">
      <div class="input-group glass-card">
        <span class="input-icon">📧</span>
        <input
          class="input"
          type="email"
          v-model="email"
          placeholder="请输入邮箱"
        />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">🔒</span>
        <input
          class="input"
          type="password"
          v-model="password"
          placeholder="请输入密码"
          maxlength="20"
        />
      </div>
    </div>

    <!-- 登录按钮 -->
    <button
      :class="['glass-btn-primary', 'btn-login', { 'btn-disabled': !canSubmit || loading }]"
      @click="onSubmit"
      :disabled="!canSubmit || loading"
    >
      {{ loading ? '登录中...' : '登 录' }}
    </button>

    <!-- 注册入口 -->
    <div class="register-entry">
      <span class="register-text">还没有账号？</span>
      <span class="register-link" @click="goRegister">立即注册</span>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  background: var(--color-bg);
  min-height: 100vh;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
}

/* ========== 头部 ========== */
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80px;
  padding-bottom: 40px;
}

.logo {
  font-size: 48px;
  margin-bottom: 12px;
}

.app-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 4px;
}

.app-desc {
  font-size: 14px;
  color: var(--color-text-dim);
}

/* ========== Tab切换 ========== */
.tab-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--color-glass-border);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 10px 0;
  font-size: 15px;
  color: var(--color-text-dim);
  position: relative;
  cursor: pointer;
  transition: color 0.2s;
}

.tab-active {
  color: var(--color-primary);
  font-weight: 600;
}

.tab-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background: var(--color-primary);
  border-radius: 1.5px;
}

/* ========== 表单 ========== */
.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.input-group {
  display: flex;
  align-items: center;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
}

.input-icon {
  font-size: 18px;
  margin-right: 10px;
  width: 24px;
  text-align: center;
}

.input {
  flex: 1;
  font-size: 15px;
  color: var(--color-text);
  height: 24px;
  border: none;
  outline: none;
  background: transparent;
}

.input::placeholder {
  color: var(--color-text-dim);
}

/* ========== 登录按钮 ========== */
.btn-login {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
  margin-top: 8px;
}

.btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ========== 注册入口 ========== */
.register-entry {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.register-text {
  font-size: 13px;
  color: var(--color-text-dim);
}

.register-link {
  font-size: 13px;
  color: var(--color-primary);
  margin-left: 4px;
  cursor: pointer;
}
</style>