import redis
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.encrypt import verify_password
from repositories.user import UserRepository
from schemas.user import UserCreate, UserLogin


class AuthService:
    def __init__(self):
        self.redis = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
        self.secret = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.token_expiry = timedelta(minutes=15)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.user_repository = UserRepository()

    def authenticate_user(self, db: Session, user_data: UserLogin):
        user = self.user_repository.get_by_email(db, email=user_data.email)
        if not user or not verify_password(user_data.password, user.password):
            return None
        return user

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + self.token_expiry
        to_encode.update({"exp": expire})

        token = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        self.redis.setex(f"token:{to_encode['sub']}", self.token_expiry, token)
        return token

    def logout(self, user_email: str):
        result = self.redis.delete(f"token:{user_email}")
        if result == 1:
            return {"message": "Successfully logged out"}
        raise HTTPException(status_code=400, detail="No active session to log out")

    def register_user(self, user_data: UserCreate, db: Session):
        if self.user_repository.get_by_email(db, email=user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = self.user_repository.create(db, user_data=user_data)
        token = self.create_access_token({"sub": new_user.email})
        return {
            "message": "User registered successfully",
            "access_token": token,
            "user_id": new_user.id,
            "username":new_user.username,
            "token_type": "bearer"
        }

    def login_user(self, form_data: OAuth2PasswordRequestForm, db: Session):
        user = self.authenticate_user(db, UserLogin(email=form_data.username, password=form_data.password))
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
        token = self.create_access_token({"sub": user.email})
        return {"access_token": token,"user_id":user.id,"username":user.username, "token_type": "bearer"}

    def get_current_user(self, token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't authenticate user",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            email = payload.get("sub")
            stored_token = self.redis.get(f"token:{email}")
            if stored_token != token or email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.user_repository.get_by_email(db, email=email)
        if not user:
            raise credentials_exception
        return user
