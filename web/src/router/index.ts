import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { isLoggedIn } from '@/utils/storage'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requireAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册', requireAuth: false },
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页', requireAuth: false },
  },
  {
    path: '/post/create',
    name: 'PostCreate',
    component: () => import('@/views/PostCreate.vue'),
    meta: { title: '发帖', requireAuth: true },
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('@/views/PostDetail.vue'),
    meta: { title: '帖子详情', requireAuth: false },
  },
  {
    path: '/chat',
    name: 'ChatList',
    component: () => import('@/views/ChatList.vue'),
    meta: { title: '消息', requireAuth: true },
  },
  {
    path: '/chat/:id',
    name: 'ChatDetail',
    component: () => import('@/views/ChatDetail.vue'),
    meta: { title: '聊天', requireAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '我的', requireAuth: true },
  },
  {
    path: '/profile/info',
    name: 'ProfileInfo',
    component: () => import('@/views/ProfileInfo.vue'),
    meta: { title: '个人信息', requireAuth: true },
  },
  {
    path: '/profile/func',
    name: 'ProfileFunc',
    component: () => import('@/views/ProfileFunc.vue'),
    meta: { title: '功能', requireAuth: true },
  },
  {
    path: '/profile/settings',
    name: 'ProfileSettings',
    component: () => import('@/views/ProfileSettings.vue'),
    meta: { title: '设置', requireAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/** 路由守卫：需要登录的页面跳转到登录页 */
router.beforeEach((to, _from, next) => {
  document.title = (to.meta.title as string) || '校园论坛'
  if (to.meta.requireAuth && !isLoggedIn()) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router