import bcrypt
import random
from typing import BinaryIO, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app import schemas
from app.crud.base import CRUDBase
from app.models import User, Avatar, EmailVerify
from app.utils import verify_password, get_password_hash


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        salt = bcrypt.gensalt().decode()
        hashed_password = get_password_hash(obj_in.password + salt)
        
        # Create user's avatar
        default_avatar = db.query(Avatar).get(1)
        avatar = Avatar(content=default_avatar.content)    
        db.add(avatar)
        db.commit()
        db.refresh(avatar)

        # Create user
        db_user = self.model(
            **obj_in.dict(exclude={'password', 'password2'}),
            salt=salt,
            hashed_password=hashed_password,
            avatar_id=avatar.id
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.username == username).one_or_none()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).one_or_none()
    
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password + user.salt, user.hashed_password):
            return None
        return user
    
    def update_avatar(self, db: Session, content: BinaryIO, user_in: schemas.UserInDB) -> None:
        db_avatar = db.query(Avatar).get(user_in.avatar_id)
        db_avatar.content = content
        
        db.add(db_avatar)
        db.commit()
        db.refresh(db_avatar)
        
        return True
    
    def generate_code(self, db: Session, user_id: int) -> schemas.EmailVerifyDB:
        db_ver = db.query(EmailVerify).filter(EmailVerify.user_id == user_id).first()
        if not db_ver:
            db_ver = EmailVerify(user_id=user_id)
            db.add(db_ver)
            db.commit()
            db.refresh(db_ver)
        
        db_ver.times_generated += 1
        db_ver.code = random.randint(1000, 9999)
        
        db.add(db_ver)
        db.commit()
        db.refresh(db_ver)
        
        return db_ver
    
    def verify_code(self, db: Session, code: str, user_id: int) -> bool:
        db_ver = db.query(EmailVerify).filter(EmailVerify.user_id == user_id).first()
        if not db_ver:
            return False
        if db_ver.code != code:
            return False

        db_user = self.get(db, model_id=user_id)
        db_user.is_verified = True
        db.add(db_user)
        
        db.delete(db_ver)
        db.commit()
        
        return True

user = CRUDUser(User)
