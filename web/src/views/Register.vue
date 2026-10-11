<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { register as registerApi } from '@/api/auth'
import type { RegisterParams } from '@/types'

const router = useRouter()

const registerType = ref<'phone' | 'email'>('phone')
const phone = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
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

/** 切换注册方式 */
function switchType(type: 'phone' | 'email') {
  registerType.value = type
}

/** 校验邮箱格式 */
function isValidEmail(val: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)
}

/** 是否可提交 */
const canSubmit = computed(() => {
  if (!username.value.trim()) return false
  if (password.value.length < 6) return false
  if (password.value !== confirmPassword.value) return false
  if (registerType.value === 'phone') {
    return phone.value.trim().length === 11
  }
  return isValidEmail(email.value.trim())
})

/** 提交注册 */
async function onSubmit() {
  if (registerType.value === 'phone' && phone.value.trim().length !== 11) {
    return showToast('请输入正确的手机号')
  }
  if (registerType.value === 'email' && !isValidEmail(email.value.trim())) {
    return showToast('请输入正确的邮箱')
  }
  if (!username.value.trim()) {
    return showToast('请输入用户名')
  }
  if (password.value.length < 6) {
    return showToast('密码不能少于6位')
  }
  if (password.value !== confirmPassword.value) {
    return showToast('两次输入的密码不一致')
  }

  loading.value = true
  try {
    await registerApi({
      username: username.value.trim(),
      password: password.value,
      phone: registerType.value === 'phone' ? phone.value.trim() : undefined,
      email: registerType.value === 'email' ? email.value.trim() : undefined,
    })
    showToast('注册成功，请登录')
    router.replace('/login')
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}

function goLogin() {
  router.push('/login')
}
</script>

<template>
  <div class="register-page">
    <!-- 头部 -->
    <div class="header">
      <span class="logo">🎓</span>
      <h1 class="title">注册账号</h1>
      <p class="subtitle">创建你的校园论坛账号</p>
    </div>

    <!-- 注册方式切换 Tab -->
    <div class="tab-bar">
      <div
        :class="['tab-item', registerType === 'phone' ? 'tab-active' : '']"
        @click="switchType('phone')"
      >
        <span>手机号</span>
      </div>
      <div
        :class="['tab-item', registerType === 'email' ? 'tab-active' : '']"
        @click="switchType('email')"
      >
        <span>邮箱</span>
      </div>
    </div>

    <!-- 手机号注册表单 -->
    <div class="form" v-if="registerType === 'phone'">
      <div class="input-group glass-card">
        <span class="input-icon">📱</span>
        <input class="input" type="tel" v-model="phone" placeholder="请输入手机号" maxlength="11" />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">👤</span>
        <input class="input" type="text" v-model="username" placeholder="请输入用户名" maxlength="20" />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">🔒</span>
        <input class="input" type="password" v-model="password" placeholder="请输入密码(不少于6位)" maxlength="20" />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">🔒</span>
        <input class="input" type="password" v-model="confirmPassword" placeholder="请确认密码" maxlength="20" />
      </div>
    </div>

    <!-- 邮箱注册表单 -->
    <div class="form" v-if="registerType === 'email'">
      <div class="input-group glass-card">
        <span class="input-icon">📧</span>
        <input class="input" type="email" v-model="email" placeholder="请输入邮箱" />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">👤</span>
        <input class="input" type="text" v-model="username" placeholder="请输入用户名" maxlength="20" />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">🔒</span>
        <input class="input" type="password" v-model="password" placeholder="请输入密码(不少于6位)" maxlength="20" />
      </div>
      <div class="input-group glass-card">
        <span class="input-icon">🔒</span>
        <input class="input" type="password" v-model="confirmPassword" placeholder="请确认密码" maxlength="20" />
      </div>
    </div>

    <!-- 注册按钮 -->
    <button
      :class="['glass-btn-primary', 'btn-register', { 'btn-disabled': !canSubmit || loading }]"
      @click="onSubmit"
      :disabled="!canSubmit || loading"
    >
      {{ loading ? '注册中...' : '注 册' }}
    </button>

    <!-- 返回登录 -->
    <div class="login-entry">
      <span class="login-text">已有账号？</span>
      <span class="login-link" @click="goLogin">返回登录</span>
    </div>
  </div>
</template>

<style scoped>
.register-page {
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
  padding-top: 60px;
  padding-bottom: 30px;
}

.logo {
  font-size: 40px;
  margin-bottom: 8px;
}

.title {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
}

.subtitle {
  font-size: 13px;
  color: var(--color-text-dim);
  margin-top: 4px;
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

/* ========== 注册按钮 ========== */
.btn-register {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
  margin-top: 8px;
}

.btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ========== 返回登录 ========== */
.login-entry {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.login-text {
  font-size: 13px;
  color: var(--color-text-dim);
}

.login-link {
  font-size: 13px;
  color: var(--color-primary);
  margin-left: 4px;
  cursor: pointer;
}
</style>