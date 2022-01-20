import io
import random
from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException, Response, Body
from starlette.responses import StreamingResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud
from app.schemas import _user, _assets
from app.api.deps import get_current_user, get_db, get_verified_user
from app.models import Avatar
from app.core import settings


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


@router.get('/avatar', tags=['Avatar'])
async def Get_Avatar(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_current_user(db, Authorize)
    db_avatar = db.query(Avatar).get(db_user.avatar_id)

    return StreamingResponse(io.BytesIO(db_avatar.content), media_type='image/png')


@router.put('/avatar', tags=['Avatar'])
async def Update_Avatar(
        avatar: UploadFile = File(..., media_type='image/png'),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)

    try:
        binary = await avatar.read()
        image = Image.open(io.BytesIO(binary))
        im_resized = image.resize(
            size=(settings.AVATAR_SIZE, settings.AVATAR_SIZE))
        buf = io.BytesIO()
        im_resized.save(buf, format=image.format)
        byte_im = buf.getvalue()
    except UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    crud.user.update_avatar(db, content=byte_im, db_user=db_user)

    return Response(status_code=status.HTTP_200_OK)


@router.get('/theme', tags=['Theme'], response_model=_assets.Theme)
async def Get_Theme(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):
    
    user_id = Authorize.get_jwt_subject()
    if not user_id:
        themes = crud.theme.get_multi(db)
        return themes[random.randint(0, len(themes) - 1)]

    db_user = get_current_user(db, Authorize)
    db_theme = crud.theme.get(db, model_id=db_user.theme_id)

    return db_theme


@router.put('/theme', tags=['Theme'], response_model=_assets.Theme)
async def Change_Theme(
        id: int = Body(..., embed=True),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_current_user(db, Authorize)

    # Check if theme exists
    db_theme = crud.theme.get(db, model_id=id)
    if not db_theme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Update currently selected theme
    db_user.theme_id = id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_theme
