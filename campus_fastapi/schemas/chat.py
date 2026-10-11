from pydantic import BaseModel


class ConversationOut(BaseModel):
    """会话输出"""
    id: int
    user1_id: int
    user2_id: int
    user1_name: str | None = None
    user2_name: str | None = None
    last_message: str | None = None
    last_time: str | None = None

    model_config = {"from_attributes": True}


class CreateConversationRequest(BaseModel):
    """创建会话请求"""
    user_id: int


class MessageOut(BaseModel):
    """消息输出"""
    id: int
    conversation_id: int
    sender_id: int
    sender_name: str | None = None
    content: str
    created_at: str | None = None

    model_config = {"from_attributes": True}


class SendMessageRequest(BaseModel):
    """发送消息请求"""
    content: str