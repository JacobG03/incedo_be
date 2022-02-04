from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional


class Note(BaseModel):
    title: str
    body: Optional[str] = None
    parent_id: Optional[int] = None

    @validator('title')
    def valid_title(cls, v):
        if len(v) < 1:
            raise ValueError('Title is too short.')
        elif len(v) > 100:
            raise ValueError('Title is too long.')
        return v


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    parent_id: Optional[int] = None
    favorite: Optional[bool] = None
    
    class Config:
        orm_mode = True

    @validator('title')
    def valid_title(cls, v):
        if len(v) < 1:
            raise ValueError('Title is too short.')
        elif len(v) > 100:
            raise ValueError('Title is too long.')
        return v


class NoteOut(Note):
    id: int
    timestamp: datetime
    favorite: Optional[bool] = None
    modified: datetime
    
    @validator('timestamp')
    def timestamp_seconds(cls, v: datetime):
        return v.timestamp()
    
    @validator('modified')
    def modified_seconds(cls, v: datetime):
        return v.timestamp()

    class Config:
        orm_mode = True


class NoteDB(NoteOut):
    user_id: int

    class Config:
        orm_mode = True
