from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class Message(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    content: str

class MessageCreate(Message):
    receiver_id: UUID
    content: str

class MessageOut(Message):
    id: UUID
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)