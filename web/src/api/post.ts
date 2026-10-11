import { get, post, del } from '@/utils/request'
import type { Post, PostCreateParams, Comment, CommentCreateParams, Category, PaginatedData } from '@/types'

/** 获取帖子列表 */
export function getPostList(params?: { page?: number; page_size?: number; category_id?: number }) {
  return get<PaginatedData<Post>>('/posts', params as Record<string, unknown>)
}

/** 获取帖子详情 */
export function getPostDetail(id: number) {
  return get<Post>(`/posts/${id}`)
}

/** 创建帖子 */
export function createPost(data: PostCreateParams) {
  return post<Post>('/posts', data as unknown as Record<string, unknown>)
}

/** 删除帖子 */
export function deletePost(id: number) {
  return del<null>(`/posts/${id}`)
}

/** 获取帖子评论 */
export function getComments(postId: number, params?: { page?: number; page_size?: number }) {
  return get<PaginatedData<Comment>>(`/posts/${postId}/comments`, params as Record<string, unknown>)
}

/** 发表评论 */
export function createComment(postId: number, data: CommentCreateParams) {
  return post<Comment>(`/posts/${postId}/comments`, data as unknown as Record<string, unknown>)
}

/** 点赞/取消点赞 */
export function toggleLike(targetId: number, targetType: 'post' | 'comment') {
  return post<null>('/likes', { target_id: targetId, target_type: targetType })
}

/** 获取分类列表 */
export function getCategoryList() {
  return get<Category[]>('/categories')
}