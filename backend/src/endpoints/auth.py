from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from auth.auth import AuthService
from schemas.user import UserCreate
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/auth",tags=["Auth"])
auth_service = AuthService()

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(user_data, db)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login_user(form_data, db)

@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    return auth_service.logout(current_user.email)
