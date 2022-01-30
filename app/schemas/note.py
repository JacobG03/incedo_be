from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Note(BaseModel):
    title: Optional[str] = None
    body: str
    section_id: Optional[int] = None
    sort_id: Optional[int] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    section_id: Optional[int] = None
    sort_id: Optional[int] = None
    favorite: Optional[bool] = None
    
    class Config:
        orm_mode = True


class NoteOut(Note):
    id: int
    timestamp: datetime
    sort_id: Optional[int] = None
    favorite: Optional[bool] = None

    class Config:
        orm_mode = True


class NoteDB(NoteOut):
    user_id: int

    class Config:
        orm_mode = True
