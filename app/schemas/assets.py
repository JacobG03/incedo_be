from pydantic import BaseModel, EmailStr
from typing import Any, List, Dict, Optional


class Email(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


class Theme(BaseModel):
    id: Optional[int] = None
    name: str
    bg: str
    main: str
    sub: str
    info: str
    text: str
    error: str
    
    class Config:
        orm_mode = True


class ThemeUpdate(BaseModel):
    name: Optional[str] = None
    bg: Optional[str] = None
    main: Optional[str] = None
    sub: Optional[str] = None
    info: Optional[str] = None
    text: Optional[str] = None
    error: Optional[str] = None
