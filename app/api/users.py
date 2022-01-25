import io
from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.models import Avatar
from app.schemas import _users, _assets
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


@router.get('/{username}', response_model=_users.UserBase)
async def Get_User(
        username: str,
        db: Session = Depends(get_db)):

    db_user = crud.user.get_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_user


@router.get('/{username}/avatar/{uri}', tags=['Avatar'])
async def Get_User_Avatar(
        username: str,
        uri: str,
        db: Session = Depends(get_db)):

    db_user = crud.user.get_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db_avatar = db.query(Avatar).get(db_user.avatar_id)

    return StreamingResponse(io.BytesIO(db_avatar.content), media_type='image/png')


@router.get('/{username}/theme', response_model=_assets.Theme, tags=['Theme'])
async def Get_User_Theme(
        username: str,
        db: Session = Depends(get_db)):

    db_user = crud.user.get_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db_theme = crud.theme.get(db, model_id=db_user.theme_id)

    return db_theme
