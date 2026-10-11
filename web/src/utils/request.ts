import axios from 'axios'
import type { ApiResponse } from '@/types'
import { getSessionId, clearAuth } from './storage'
import { showToast } from 'vant'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

/** 请求拦截器：自动附加session_id */
request.interceptors.request.use((config) => {
  const sessionId = getSessionId()
  if (sessionId) {
    config.headers['X-Session-Id'] = sessionId
  }
  return config
})

/** 响应拦截器：统一处理错误 */
request.interceptors.response.use(
  (response) => {
    const res = response.data as ApiResponse
    // 业务错误码非0视为失败
    if (res.code !== 0) {
      showToast(res.message || '请求失败')
      // 未登录或session过期
      if (res.code === 401) {
        clearAuth()
        window.location.href = '/login'
      }
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return response
  },
  (error) => {
    // 网络错误或服务端500
    const msg = error.response?.data?.message || '服务器开小差了~'
    showToast(msg)
    return Promise.reject(error)
  }
)

/** GET请求 */
export function get<T = unknown>(url: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return request.get(url, { params }).then((res) => res.data)
}

/** POST请求 */
export function post<T = unknown>(url: string, data?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return request.post(url, data).then((res) => res.data)
}

/** PUT请求 */
export function put<T = unknown>(url: string, data?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return request.put(url, data).then((res) => res.data)
}

/** DELETE请求 */
export function del<T = unknown>(url: string, params?: Record<string, unknown>): Promise<ApiResponse<T>> {
  return request.delete(url, { params }).then((res) => res.data)
}

export default request