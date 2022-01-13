from datetime import datetime
import random
import secrets
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from app.database.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    theme_id = Column(Integer, ForeignKey(
        'theme.id'), default=1, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    avatar_id = Column(Integer, ForeignKey('avatar.id'), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.username}'


class EmailVerify(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    code = Column(String, default=random.randint(1000, 9999), nullable=False)
    times_generated = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, user_id: {self.user_id}'


class PasswordReset(Base):
    id = Column(Integer, primary_key=True)
    uri = Column(String, default=secrets.token_urlsafe(256), nullable=False)
    suspended = Column(Boolean, default=False, nullable=False)
    times = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
