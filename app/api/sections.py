from typing import List, Optional
from fastapi import APIRouter, Body, Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from .deps import get_db, get_verified_user
from app.schemas import _section
from app import crud

router = APIRouter()


@router.post('', response_model=_section.SectionDB)
async def Create_Section(
        section_in: _section.Section,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)
    section_in.user_id = db_user.id

    return crud.section.create(db, db_user, section_in)


@router.get('/{id}', response_model=_section.SectionOut)
async def Get_Section(
        id: int,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)
    db_section = crud.section.get(db, db_user, id)
    return db_section


@router.get('', response_model=List[_section.SectionOut])
async def Get_Sections(
        reverse: Optional[bool] = False,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)

    return crud.section.get_multi(db, db_user, reverse=reverse, skip=skip, limit=limit)


@router.delete('/{section_id}')
async def Delete_Section(
        section_id: int,
        agreed: bool = Body(..., embed=True),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)
    
    if not agreed:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
        
    db_section = crud.section.get(db, db_user, section_id)
    crud.section.remove(db, db_user, db_section)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        