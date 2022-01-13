import secrets
import bcrypt
import random
from typing import BinaryIO, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.crud.base import CRUDBase
from app.models import User, Avatar, EmailVerify, PasswordReset
from app.schemas import _assets, _user
from app.utils import verify_password, get_password_hash
from app.core import settings


class CRUDUser(CRUDBase[User, _user.UserCreate, _user.UserUpdate]):
    def create(self, db: Session, *, obj_in: _user.UserCreate) -> _user.UserInDB:
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

    def remove(self, db: Session, db_user: _user.UserInDB) -> bool:
        email_verify_obj = db.query(EmailVerify).filter(
            EmailVerify.user_id == db_user.id).first()

        if email_verify_obj:
            db.delete(email_verify_obj)

        avatar = db.query(Avatar).get(db_user.avatar_id)
        db.delete(avatar)

        db.delete(db_user)
        db.commit()

        return True

    def get_by_username(self, db: Session, username: str) -> Optional[_user.UserInDB]:
        return db.query(self.model).filter(self.model.username == username).one_or_none()

    def get_by_email(self, db: Session, email: str) -> Optional[_user.UserInDB]:
        return db.query(self.model).filter(self.model.email == email).one_or_none()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[_user.UserInDB]:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password + user.salt, user.hashed_password):
            return None
        return user

    def update_avatar(self, db: Session, content: BinaryIO, db_user: _user.UserInDB) -> None:
        db_avatar = db.query(Avatar).get(db_user.avatar_id)
        db_avatar.content = content

        db.add(db_avatar)
        db.commit()
        db.refresh(db_avatar)

        return True

    def generate_code(self, db: Session, user_id: int) -> _user.EmailVerifyDB:
        db_ver = db.query(EmailVerify).filter(
            EmailVerify.user_id == user_id).first()
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
        db_ver = db.query(EmailVerify).filter(
            EmailVerify.user_id == user_id).first()
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

    def get_all_unverified(self, db: Session) -> List[_user.UserInDB]:
        return db.query(self.model).filter(self.model.is_verified == False).all()

    def new_password_reset(self, db: Session, db_user: _user.UserInDB) -> PasswordReset:
        db_reset_password = db.query(PasswordReset).filter(
            PasswordReset.user_id == db_user.id).first()

        if not db_reset_password:
            db_reset_password = PasswordReset(user_id=db_user.id)
            db.add(db_reset_password)
            db.commit()
            db.refresh(db_reset_password)

        db_reset_password.times += 1
        if db_reset_password.times >= settings.MAX_PASS_RESET_ATTEMPTS:
            db_reset_password.suspended = True

        db_reset_password.timestamp = datetime.utcnow()
        db_reset_password.uri = secrets.token_urlsafe(256)

        db.add(db_reset_password)
        db.commit()
        db.refresh(db_reset_password)

        return db_reset_password

    def reset_password(self, db: Session, passwords: _user.ResetPasswords, uri: str) -> bool:
        db_reset_password = db.query(PasswordReset).filter(
            PasswordReset.uri == uri).first()
        if not db_reset_password or db_reset_password.suspended:
            return False
        if db_reset_password.timestamp + timedelta(minutes=settings.PASS_RESET_MINUTES) < datetime.utcnow():
            return False

        db_user = db.query(self.model).get(db_reset_password.user_id)
        hashed_password = get_password_hash(passwords.password + db_user.salt)

        db_user.hashed_password = hashed_password

        db.delete(db_reset_password)
        db.add(db_user)
        db.commit()

        return True


user = CRUDUser(User)
