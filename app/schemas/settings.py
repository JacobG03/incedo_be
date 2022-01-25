from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from app.core import settings


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    theme_id: Optional[int] = None


class UsernameUpdate(BaseModel):
    username: str

    @validator('username')
    def validateUsernameLength(cls, v):
        if len(v) < settings.USERNAME_MIN_LENGTH:
            raise ValueError('Username is too short.')
        elif len(v) > settings.USERNAME_MAX_LENGTH:
            raise ValueError('Username is too long.')
        return v


class EmailUpdate(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validateEmailLength(cls, v):
        if len(v) > settings.EMAIL_MAX_LENGTH:
            raise ValueError('Email is too long.')
        return v


class UpdatePassword(BaseModel):
    password: str
    new_password: str
    new_password2: str

    @validator('new_password')
    def validatePasswordLength(cls, v):
        if len(v) > settings.PASSWORD_MAX_LENGTH:
            raise ValueError('Password is too long.')
        elif len(v) < settings.PASSWORD_MIN_LENGTH:
            raise ValueError('Password is too short.')
        return v

    @validator('new_password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match.')
        return v
