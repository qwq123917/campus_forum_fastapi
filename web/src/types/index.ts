/** 统一响应格式 */
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

/** 用户信息 */
export interface UserInfo {
  id: number
  username: string
  phone: string | null
  email: string | null
  avatar: string | null
  role_id: number
  role_name: string
  created_at: string
}

/** 登录响应 */
export interface LoginData {
  session_id: string
  user: UserInfo
}

/** 注册请求 */
export interface RegisterParams {
  username: string
  password: string
  phone?: string
  email?: string
}

/** 登录请求 */
export interface LoginParams {
  password: string
  phone?: string
  email?: string
}

/** 分类 */
export interface Category {
  id: number
  name: string
  description: string | null
}

/** 帖子 */
export interface Post {
  id: number
  title: string
  content: string
  category_id: number
  category_name: string
  user_id: number
  username: string
  like_count: number
  comment_count: number
  created_at: string
  updated_at: string
}

/** 发帖请求 */
export interface PostCreateParams {
  title: string
  content: string
  category_id: number
}

/** 评论 */
export interface Comment {
  id: number
  post_id: number
  user_id: number
  username: string
  content: string
  parent_id: number | null
  created_at: string
}

/** 评论请求 */
export interface CommentCreateParams {
  content: string
  parent_id?: number
}

/** 点赞 */
export interface Like {
  id: number
  user_id: number
  target_id: number
  target_type: 'post' | 'comment'
  created_at: string
}

/** 聊天会话 */
export interface ChatConversation {
  id: number
  user1_id: number
  user2_id: number
  user1_name: string
  user2_name: string
  last_message: string | null
  last_time: string | null
}

/** 聊天消息 */
export interface ChatMessage {
  id: number
  conversation_id: number
  sender_id: number
  sender_name: string
  content: string
  created_at: string
}

/** 分页参数 */
export interface PaginationParams {
  page?: number
  page_size?: number
}

/** 分页响应 */
export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}