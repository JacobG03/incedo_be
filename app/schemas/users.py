from pydantic import BaseModel
from pydantic.class_validators import validator

from app.core import settings


class UserBase(BaseModel):
    username: str
    avatar_id: int

    @validator('avatar_id')
    def return_avatar_url(cls, v, values, **kwargs):
        return f'{settings.URL}/users/{values["username"]}/avatar'

    class Config:
        orm_mode = True
