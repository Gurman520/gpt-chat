from pydantic import BaseModel
from datetime import datetime

class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationSchema(ConversationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    pass

class MessageSchema(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    formatted_content: str | None = None
    
    class Config:
        from_attributes = True