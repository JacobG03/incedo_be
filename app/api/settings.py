import io
from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, Body, Depends, File, Request, UploadFile, status, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app import crud

from app.core.config import settings
from app.schemas import _assets, _settings
from app.utils.hashing import verify_password
from .deps import get_current_user, get_db, get_verified_user


router = APIRouter()


@router.put('/username')
async def Update_Username(
        update: _settings.UsernameUpdate,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)

    crud.user.update_username(db, db_user, update)

    return {'message': 'Username updated successfully.'}


@router.put('/email')
async def Update_Email(
        update: _settings.EmailUpdate,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)
    
    crud.user.update_email(db, db_user=db_user, update=update)

    return {'message': 'Email updated successfully.'}


@router.put('/avatar', tags=['Avatar'])
async def Update_Avatar(
        request: Request,
        avatar: UploadFile = File(...),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    if 'content-length' not in request.headers:
        return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
    content_length = int(request.headers['content-length'])
    if content_length > settings.MAX_AVATAR_SIZE:
        return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

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

    db_avatar = crud.user.update_avatar(db, content=byte_im, db_user=db_user)

    return JSONResponse({'avatar_url': f'{settings.URL}/users/{db_user.username}/avatar/{db_avatar.uri}'})


@router.get('/themes')
async def Get_Themes(db: Session = Depends(get_db)):
    return crud.theme.get_multi(db)


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


@router.put('/password')
async def Change_Password(
        updates: _settings.UpdatePassword,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)

    crud.user.new_password(db, db_user=db_user, obj_in=updates)

    return {'message': 'Password updated.'}


class Responses(object):
    username_taken = {
        "loc": [
            "body",
            "username"
        ],
        "msg": "Username is taken."
    }

    email_taken = {
        "loc": [
            "body",
            "email"
        ],
        "msg": "Email is taken."
    }

    invalid_password = {
        "loc": [
            "body",
            "password"
        ],
        "msg": "Invalid password."
    }
