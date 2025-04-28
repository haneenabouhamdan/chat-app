from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session
from core.encrypt import hash_password
from models.user import User
from schemas.user import UserCreate
from .base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: EmailStr) -> Optional[User]:
        return self.get_by(db, email=email)

    def create(self, db: Session, user_data: UserCreate) -> User:
        user = self.model(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
