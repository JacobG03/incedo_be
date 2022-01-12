import io
from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException, Response, Body
from starlette.responses import StreamingResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_current_user, get_db, get_verified_user
from app.models import Avatar


router = APIRouter()


@router.get('', response_model=schemas.MeOut)
async def Get_Current_User(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    return get_current_user(db, Authorize)


@router.put('', response_model=schemas.MeOut)
async def Update_Current_User(
        updates: schemas.UserUpdate,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize) 
    updated_user = crud.user.update(db, db_obj=db_user, obj_in=updates)

    return updated_user


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

    content = await avatar.read()
    crud.user.update_avatar(db, content=content, db_user=db_user)

    return Response(status_code=status.HTTP_200_OK)


@router.get('/theme', tags=['Theme'], response_model=schemas.Theme)
async def Get_Theme(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_current_user(db, Authorize)
    db_theme = crud.theme.get(db, model_id=db_user.theme_id)

    return db_theme


@router.put('/theme', tags=['Theme'], response_model=schemas.Theme)
async def Change_Theme(
    id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)
    
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
