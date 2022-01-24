from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from app.core import settings


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    theme_id: Optional[int] = None

    @validator('username')
    def validateUsernameLength(cls, v):
        if len(v) < settings.USERNAME_MIN_LENGTH:
            raise ValueError('Username is too short.')
        elif len(v) > settings.USERNAME_MAX_LENGTH:
            raise ValueError('Username is too long.')
        return v

    @validator('email')
    def validateEmailLength(cls, v):
        if len(v) > settings.EMAIL_MAX_LENGTH:
            raise ValueError('Email is too long.')
        return v


class UsernameUpdate(BaseModel):
    username: str


class EmailUpdate(BaseModel):
    email: EmailStr
    password: str
