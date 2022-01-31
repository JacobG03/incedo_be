from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator
from .note import NoteDB


class Section(BaseModel):
    name: str
    user_id: Optional[int] = None
    parent_id: Optional[int] = None
    sort_id: int
    favorite: Optional[bool] = None


class SectionUpdate(BaseModel):
    name: Optional[str]
    parent_id: Optional[int] = None
    sort_id: Optional[int] = None
    favorite: Optional[bool] = None

    class Config:
        orm_mode = True

class SectionDB(Section):
    id: int
    notes: List[NoteDB]
    sub_sections: List[SectionDB]
    timestamp: datetime
    
    @validator('timestamp')
    def timestamp_seconds(cls, v: datetime):
        return v.timestamp()

    class Config:
        orm_mode = True


class SectionOut(BaseModel):
    id: int
    name: str
    favorite: bool
    parent_id: Optional[int] = None
    sort_id: int
    timestamp: datetime
    
    @validator('timestamp')
    def timestamp_seconds(cls, v: datetime):
        return v.timestamp()
    
    class Config:
        orm_mode = True


SectionDB.update_forward_refs()
