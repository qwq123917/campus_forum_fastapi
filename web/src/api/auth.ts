import { post } from '@/utils/request'
import type { LoginData, LoginParams, RegisterParams, UserInfo } from '@/types'

/** 用户注册 */
export function register(data: RegisterParams) {
  return post<null>('/auth/register', data as unknown as Record<string, unknown>)
}

/** 用户登录 */
export function login(data: LoginParams) {
  return post<LoginData>('/auth/login', data as unknown as Record<string, unknown>)
}

/** 用户登出 */
export function logout() {
  return post<null>('/auth/logout')
}

/** 获取当前用户信息 */
export function getUserProfile() {
  return post<UserInfo>('/auth/profile')
}