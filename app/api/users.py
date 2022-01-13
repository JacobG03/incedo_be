from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.schemas import _users
from app.api.deps import get_db

router = APIRouter()


@router.get('', response_model=List[_users.UserBase])
async def Get_Users(
        reverse: bool = False,
        limit: int = 100,
        skip: int = 0,
        db: Session = Depends(get_db)):

    db_users = crud.user.get_multi(db, reverse=reverse, limit=limit, skip=skip)
    return db_users
