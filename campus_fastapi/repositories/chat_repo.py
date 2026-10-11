"""聊天数据访问层"""

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from campus_fastapi.models.chat import ChatConversation, ChatMessage


async def count_conversations(db: AsyncSession, user_id: int) -> int:
    """统计用户会话数量"""
    stmt = select(func.count()).select_from(ChatConversation).where(
        or_(ChatConversation.user1_id == user_id, ChatConversation.user2_id == user_id)
    )
    return (await db.execute(stmt)).scalar() or 0


async def get_conversations(db: AsyncSession, user_id: int,
                            page: int, page_size: int) -> list[ChatConversation]:
    """获取用户会话列表"""
    stmt = (
        select(ChatConversation)
        .where(or_(ChatConversation.user1_id == user_id, ChatConversation.user2_id == user_id))
        .order_by(ChatConversation.last_message_at.desc(), ChatConversation.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def find_conversation(db: AsyncSession, user1_id: int, user2_id: int) -> ChatConversation | None:
    """查找两个用户之间的会话"""
    stmt = select(ChatConversation).where(
        ChatConversation.user1_id == user1_id,
        ChatConversation.user2_id == user2_id,
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def create_conversation(db: AsyncSession, user1_id: int, user2_id: int) -> ChatConversation:
    """创建会话"""
    conv = ChatConversation(user1_id=user1_id, user2_id=user2_id)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


async def get_conversation_by_id(db: AsyncSession, conversation_id: int) -> ChatConversation | None:
    """根据ID获取会话"""
    result = await db.execute(
        select(ChatConversation).where(ChatConversation.id == conversation_id)
    )
    return result.scalar_one_or_none()


async def count_messages(db: AsyncSession, conversation_id: int) -> int:
    """统计会话消息数量"""
    stmt = select(func.count()).select_from(ChatMessage).where(
        ChatMessage.conversation_id == conversation_id
    )
    return (await db.execute(stmt)).scalar() or 0


async def get_messages(db: AsyncSession, conversation_id: int,
                       page: int, page_size: int) -> list[ChatMessage]:
    """获取会话消息列表"""
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_message(db: AsyncSession, conversation_id: int,
                         sender_id: int, receiver_id: int,
                         content: str) -> ChatMessage:
    """创建消息"""
    msg = ChatMessage(
        conversation_id=conversation_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def update_conversation_last_message(db: AsyncSession, conv: ChatConversation,
                                           content: str, now) -> None:
    """更新会话最后消息"""
    conv.last_message = content
    conv.last_message_at = now
    await db.commit()