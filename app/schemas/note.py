from datetime import datetime
from pydantic import BaseModel
from typing import Any, List, Dict, Optional


class Note(BaseModel):
    title: Optional[str] = None
    body: str


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class NoteOut(Note):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class NoteDB(NoteOut):
    user_id: int

    class Config:
        orm_mode = True
