from pydantic import BaseModel
from pydantic.class_validators import validator

from app.core import settings


class UserBase(BaseModel):
    username: str
    avatar_id: int
    theme_id: str

    @validator('avatar_id')
    def return_avatar_url(cls, v, values, **kwargs):
        return f'{settings.URL}/users/{values["username"]}/avatar'
    
    @validator('theme_id')
    def return_theme_url(cls, v, values, **kwargs):
        return f'{settings.URL}/users/{values["username"]}/theme'

    class Config:
        orm_mode = True
