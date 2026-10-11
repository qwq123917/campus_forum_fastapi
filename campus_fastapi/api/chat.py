"""聊天相关路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.dependencies import get_current_user_id
from campus_fastapi.core.responses import success
from campus_fastapi.infrastructure.database import get_db
from campus_fastapi.schemas.chat import CreateConversationRequest, SendMessageRequest
from campus_fastapi.services import chat_service

router = APIRouter(prefix="/api/chat", tags=["聊天"])


# ========== 会话列表 ==========
@router.get("/conversations", summary="获取会话列表")
async def get_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户的会话列表"""
    data = await chat_service.get_conversations(db, user_id, page, page_size)
    return success(data=data)


# ========== 创建/获取会话 ==========
@router.post("/conversations", summary="创建或获取会话")
async def create_conversation(
    req: CreateConversationRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """与指定用户创建会话（如已存在则返回已有会话）"""
    data = await chat_service.create_conversation(db, user_id, req)
    return success(data=data)


# ========== 获取会话消息 ==========
@router.get("/conversations/{conversation_id}/messages", summary="获取会话消息")
async def get_messages(
    conversation_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取会话中的消息列表"""
    data = await chat_service.get_messages(db, conversation_id, user_id, page, page_size)
    return success(data=data)


# ========== 发送消息 ==========
@router.post("/conversations/{conversation_id}/messages", summary="发送消息")
async def send_message(
    conversation_id: int,
    req: SendMessageRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """在会话中发送消息"""
    data = await chat_service.send_message(db, conversation_id, user_id, req)
    return success(data=data)