import random
from fastapi import APIRouter, Depends, status, Response
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud
from app.schemas import _user, _assets
from app.api.deps import get_current_user, get_db


router = APIRouter()


@router.get('', response_model=_user.MeOut)
async def Get_Current_User(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    return get_current_user(db, Authorize)


@router.delete('')
async def Delete_Account(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_current_user(db, Authorize)
    crud.user.remove(db, db_user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/theme', tags=['Theme'], response_model=_assets.Theme)
async def Get_Theme(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    Authorize.jwt_optional()
    user_id = Authorize.get_jwt_subject()
    if not user_id:
        themes = crud.theme.get_multi(db)
        return themes[random.randint(0, len(themes) - 1)]

    db_user = get_current_user(db, Authorize)
    db_theme = crud.theme.get(db, model_id=db_user.theme_id)

    return db_theme
