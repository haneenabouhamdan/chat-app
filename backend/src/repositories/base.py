from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)  # bound to SQLAlchemy base models

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model: Type[T] = model

    def get_by_id(self, db: Session, id: str) -> Optional[T]:
        return db.query(self.model).filter_by(id=id).first()

    def get_all(self, db: Session) -> List[T]:
        return db.query(self.model).all()

    def get_by(self, db: Session, **kwargs) -> Optional[T]:
        return db.query(self.model).filter_by(**kwargs).first()

    def update(self, db: Session, id: str, data: dict) -> Optional[T]:
        obj = self.get_by_id(db, id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: str) -> bool:
        obj = self.get_by_id(db, id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
