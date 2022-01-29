from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel
from .note import NoteDB, NoteOut


class Section(BaseModel):
    name: str
    user_id: Optional[int] = None
    parent_id: Optional[int] = None
    sort_id: Optional[int] = None


class SectionUpdate(BaseModel):
    name: Optional[str]
    parent_id: Optional[int] = None
    sort_id: Optional[int] = None


class SectionDB(Section):
    id: int
    notes: List[NoteDB]
    sub_sections: List[SectionDB]

    class Config:
        orm_mode = True


class SectionOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    sort_id: Optional[int] = None

    notes: List[NoteOut]
    sub_sections: List[SectionOut]

    class Config:
        orm_mode = True
        

class SectionRemove(BaseModel):
    notes: Optional[List[int]] = None
    sub_sections: Optional[List[int]] = None


SectionDB.update_forward_refs()
