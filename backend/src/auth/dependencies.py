from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from .auth import AuthService

auth_service = AuthService()

def get_current_user(token: str = Depends(auth_service.oauth2_scheme), db: Session = Depends(get_db)):
    return auth_service.get_current_user(token, db)
