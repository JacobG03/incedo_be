import io
from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException, Response
from starlette.responses import StreamingResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db
from app.models import Avatar


router = APIRouter()


@router.get('', response_model=schemas.MeOut)
async def Get_Current_User(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    # get user
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = crud.user.get(db, user_id)

    return user


@router.put('', response_model=schemas.MeOut)
async def Update_Current_User(
        updates: schemas.UserUpdate,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()

    user_id = Authorize.get_jwt_subject()
    db_user = crud.user.get(db, user_id)
    updated_user = crud.user.update(db, db_obj=db_user, obj_in=updates)

    return updated_user


@router.get('/avatar', tags=['Avatar'])
async def Get_Avatar(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()):
        
    Authorize.jwt_required()
    db_user = crud.user.get(db, Authorize.get_jwt_subject())
    db_avatar = db.query(Avatar).get(db_user.avatar_id)
    
    return StreamingResponse(io.BytesIO(db_avatar.content), media_type='image/png')


@router.put('/avatar', tags=['Avatar'])
async def Update_Avatar(
        avatar: UploadFile = File(..., media_type='image/png'),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()
    db_user = crud.user.get(db, Authorize.get_jwt_subject())
    
    content = await avatar.read()
    crud.user.update_avatar(db, content=content, user_in=db_user)

    return Response(status_code=status.HTTP_200_OK)


@router.get('/theme', tags=['Theme'], response_model=schemas.Theme)
async def Get_Theme(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    db_user = crud.user.get(db, Authorize.get_jwt_subject())
    db_theme = crud.theme.get(db, model_id=db_user.theme_id)
    
    return db_theme

