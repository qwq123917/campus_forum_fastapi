import { get, post } from '@/utils/request'
import type { ChatConversation, ChatMessage, PaginatedData } from '@/types'

/** 获取会话列表 */
export function getConversations(params?: { page?: number; page_size?: number }) {
  return get<PaginatedData<ChatConversation>>('/chat/conversations', params as Record<string, unknown>)
}

/** 获取或创建会话（与某用户聊天） */
export function getOrCreateConversation(userId: number) {
  return post<ChatConversation>('/chat/conversations', { user_id: userId })
}

/** 获取会话消息列表 */
export function getMessages(conversationId: number, params?: { page?: number; page_size?: number }) {
  return get<PaginatedData<ChatMessage>>(`/chat/conversations/${conversationId}/messages`, params as Record<string, unknown>)
}

/** 发送消息 */
export function sendMessage(conversationId: number, content: string) {
  return post<ChatMessage>(`/chat/conversations/${conversationId}/messages`, { content })
}