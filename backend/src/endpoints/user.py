from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from schemas.user import UserCreate, UserOut
from database import get_db
from repositories.user import UserRepository
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"],dependencies=[Depends(get_current_user)])
user_repo = UserRepository()

@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return user_repo.get_all(db)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserOut)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if user_repo.get_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return user_repo.create(db, user_data)
