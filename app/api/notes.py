from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from .deps import get_note_author, get_db, get_verified_user
from app import crud
from app.schemas import _note


router = APIRouter()


@router.get('')
async def Get_Notes(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)

    return crud.note.get_multi(db, db_user=db_user)


@router.get('/{id}', response_model=_note.NoteOut)
async def Get_Note(
        id: int,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    get_note_author(db, Authorize, id)
    db_note = crud.note.get(db, id)

    return db_note


@router.post('', response_model=_note.NoteOut)
async def Create_Note(
        note_in: _note.Note,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_verified_user(db, Authorize)

    return crud.note.create(db, db_user, note_in)


@router.put('/{id}', response_model=_note.NoteOut)
async def Update_Note(
        id: int,
        note_in: _note.NoteUpdate,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    get_note_author(db, Authorize, id)
    db_note = crud.note.get(db, id)

    return crud.note.update(db, db_obj=db_note, obj_in=note_in)


@router.delete('/{id}')
async def Delete_Note(
        id: int,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

  get_note_author(db, Authorize, id)
  crud.note.remove(db, model_id=id)
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)
