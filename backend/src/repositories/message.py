import uuid
from typing import List
from sqlalchemy.orm import Session
from models.message import Message
from schemas.message import MessageCreate
from .base import BaseRepository

class MessageRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__(Message)

    def create(self, db: Session, message_data: MessageCreate) -> Message:
        message = self.model(**message_data.model_dump())
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_all_for_user(self, db: Session, user_id: uuid.UUID) -> List[Message]:
        return db.query(self.model).filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id)
        ).order_by(Message.timestamp.desc()).all()
