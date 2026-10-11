from sqlalchemy import String, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from campus_fastapi.infrastructure.database import Base


class ChatConversation(Base):
    __tablename__ = "sys_chat_conversation"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="会话ID"
    )
    user1_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="用户1 ID（较小ID）"
    )
    user2_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="用户2 ID（较大ID）"
    )
    last_message: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="最后一条消息内容")
    last_message_at: Mapped[str | None] = mapped_column(DateTime, nullable=True, comment="最后消息时间")
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间"
    )


class ChatMessage(Base):
    __tablename__ = "sys_chat_message"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="消息ID"
    )
    conversation_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_chat_conversation.id"), nullable=False, comment="会话ID"
    )
    sender_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="发送者ID"
    )
    receiver_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sys_user.id"), nullable=False, comment="接收者ID"
    )
    content: Mapped[str] = mapped_column(String(2000), nullable=False, comment="消息内容")
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False, comment="是否已读")
    created_at: Mapped[str] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="创建时间"
    )