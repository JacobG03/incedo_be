from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator

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
    is_admin: bool
    is_verified: bool
    timestamp: datetime

    class Config:
        orm_mode = True


class MeOut(BaseModel):
    username: str
    is_verified: bool
    avatar_id: str = Field(alias="avatar_url")
    email: str

    @validator('avatar_id')
    def return_avatar_url(cls, v, values, **kwargs):
        return f'{settings.URL}/users/{values["username"]}/avatar'

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserLogin(BaseModel):
    email: str
    password: str


class EmailVerifyDB(BaseModel):
    id: int
    user_id: int
    code: int
    times_generated: int


class ResetPasswords(BaseModel):
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
