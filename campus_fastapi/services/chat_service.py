"""聊天业务逻辑层"""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.core.exceptions import BusinessException
from campus_fastapi.core.responses import ResponseCode
from campus_fastapi.repositories import chat_repo, user_repo
from campus_fastapi.schemas.chat import ConversationOut, CreateConversationRequest, MessageOut, SendMessageRequest
from campus_fastapi.schemas.common import PaginatedResponse


async def _build_conversation_out(db: AsyncSession, c) -> dict:
    """构建会话输出"""
    u1_name = await user_repo.get_username(db, c.user1_id)
    u2_name = await user_repo.get_username(db, c.user2_id)
    return ConversationOut(
        id=c.id,
        user1_id=c.user1_id,
        user2_id=c.user2_id,
        user1_name=u1_name,
        user2_name=u2_name,
        last_message=c.last_message,
        last_time=str(c.last_message_at) if c.last_message_at else None,
    ).model_dump()


async def _build_message_out(db: AsyncSession, m) -> dict:
    """构建消息输出"""
    sender_name = await user_repo.get_username(db, m.sender_id)
    return MessageOut(
        id=m.id,
        conversation_id=m.conversation_id,
        sender_id=m.sender_id,
        sender_name=sender_name,
        content=m.content,
        created_at=str(m.created_at) if m.created_at else None,
    ).model_dump()


async def get_conversations(db: AsyncSession, user_id: int,
                            page: int, page_size: int) -> dict:
    """获取当前用户的会话列表"""
    total = await chat_repo.count_conversations(db, user_id)
    conversations = await chat_repo.get_conversations(db, user_id, page, page_size)

    items = []
    for c in conversations:
        items.append(await _build_conversation_out(db, c))

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size).model_dump()


async def create_conversation(db: AsyncSession, user_id: int,
                              req: CreateConversationRequest) -> dict:
    """与指定用户创建会话（如已存在则返回已有会话）"""
    other_id = req.user_id
    if other_id == user_id:
        raise BusinessException(message="不能和自己聊天", code=ResponseCode.PARAM_ERROR)

    # 确保 user1_id < user2_id
    small_id, big_id = min(user_id, other_id), max(user_id, other_id)

    # 查是否已存在
    existing = await chat_repo.find_conversation(db, small_id, big_id)
    if existing:
        return await _build_conversation_out(db, existing)

    # 创建新会话
    conv = await chat_repo.create_conversation(db, small_id, big_id)
    return await _build_conversation_out(db, conv)


async def get_messages(db: AsyncSession, conversation_id: int,
                       user_id: int, page: int, page_size: int) -> dict:
    """获取会话中的消息列表"""
    # 验证会话归属
    conv = await chat_repo.get_conversation_by_id(db, conversation_id)
    if not conv or (conv.user1_id != user_id and conv.user2_id != user_id):
        raise BusinessException(message="会话不存在", code=ResponseCode.NOT_FOUND)

    total = await chat_repo.count_messages(db, conversation_id)
    messages = await chat_repo.get_messages(db, conversation_id, page, page_size)

    items = []
    for m in messages:
        items.append(await _build_message_out(db, m))

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size).model_dump()


async def send_message(db: AsyncSession, conversation_id: int,
                       user_id: int, req: SendMessageRequest) -> dict:
    """在会话中发送消息"""
    # 验证会话归属
    conv = await chat_repo.get_conversation_by_id(db, conversation_id)
    if not conv or (conv.user1_id != user_id and conv.user2_id != user_id):
        raise BusinessException(message="会话不存在", code=ResponseCode.NOT_FOUND)

    # 确定接收者
    receiver_id = conv.user2_id if conv.user1_id == user_id else conv.user1_id

    msg = await chat_repo.create_message(
        db, conversation_id=conversation_id,
        sender_id=user_id, receiver_id=receiver_id, content=req.content,
    )

    # 更新会话最后消息
    await chat_repo.update_conversation_last_message(db, conv, req.content, datetime.now())

    return await _build_message_out(db, msg)