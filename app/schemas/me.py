from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

from app.core import settings


class UserBase(BaseModel):
    username: str
    email: EmailStr
    
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


class UserCreate(UserBase):
    password: str
    password2: str
    
    @validator('password')
    def validatePasswordLength(cls, v):
        if len(v) > settings.PASSWORD_MAX_LENGTH:
            raise ValueError('Password is too long.')
        elif len(v) < settings.PASSWORD_MIN_LENGTH:
            raise ValueError('Password is too short.')
        return v
    
    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match.')
        return v


class UserInDB(UserBase):
    id: int
    avatar_id: int
    theme_id: int
    hashed_password: str
    salt: str

    class Config:
        orm_mode = True


class MeOut(BaseModel):
    username: str
    avatar_id: int
    theme_id: int
    
    @validator('avatar_id')
    def return_avatar_url(cls, v):
        return f'{settings.URL}/me/avatar'
    
    @validator('theme_id')
    def return_theme_url(cls, v):
        return f'{settings.URL}/me/theme'
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    theme_id: Optional[int] = None


class UserVerifyDB(BaseModel):
    id: int
    user_id: int
    code: int
    verified: bool
    send_time: datetime
    verified_time: datetime
