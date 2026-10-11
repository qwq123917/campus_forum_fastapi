const SESSION_KEY = 'session_id'
const USER_KEY = 'user_info'

/** 获取session_id */
export function getSessionId(): string | null {
  return localStorage.getItem(SESSION_KEY)
}

/** 设置session_id */
export function setSessionId(sessionId: string): void {
  localStorage.setItem(SESSION_KEY, sessionId)
}

/** 移除session_id */
export function removeSessionId(): void {
  localStorage.removeItem(SESSION_KEY)
}

/** 获取用户信息 */
export function getUserInfo<T>(): T | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as T
  } catch {
    return null
  }
}

/** 设置用户信息 */
export function setUserInfo<T>(user: T): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

/** 移除用户信息 */
export function removeUserInfo(): void {
  localStorage.removeItem(USER_KEY)
}

/** 清除所有登录信息 */
export function clearAuth(): void {
  removeSessionId()
  removeUserInfo()
}

/** 是否已登录 */
export function isLoggedIn(): boolean {
  return !!getSessionId()
}