from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase, ModelType
from app.models import Note, Section
from app.schemas import _note, _user
from app.crud.section import section


class CrudNote(CRUDBase[Note, _note.Note, _note.NoteUpdate]):
    def create(self, db: Session, db_user: _user.UserInDB, note_in: _note.Note) -> _note.NoteDB:
        if note_in.section_id:
            section_db = section.get(db, db_user, note_in.section_id)
            if not section_db:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[{
                        'loc': [
                            'body',
                            'section_id'
                        ],
                        'msg': 'Section does not exist.'
                    }]
                )

        db_note = self.model(**note_in.dict(), user_id=db_user.id)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        return db_note

    def get_multi(self, db: Session, db_user=_user.UserInDB, reverse: bool = False, skip: int = 0, limit: int = 100) -> List[ModelType]:
        if reverse:
            db_obj = db.query(self.model).filter(
                self.model.user_id == db_user.id).order_by(self.model.id.desc()).limit(limit)
            db_obj = db_obj[skip::1]
        else:
            db_obj = db.query(self.model).filter(
                self.model.user_id == db_user.id).offset(skip).limit(limit).all()

        return db_obj

    def update(self, db: Session, db_note: _note.NoteDB, note_in: _note.NoteUpdate) -> ModelType:
        if note_in.section_id:
            section_db = section.get(db, note_in.section_id)
            if not section_db:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[{
                        'loc': [
                            'body',
                            'section_id'
                        ],
                        'msg': 'Section does not exist.'
                    }]
                )

        obj_data = jsonable_encoder(note_in)
        if isinstance(note_in, dict):
            update_data = note_in
        else:
            update_data = note_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_note, field, update_data[field])

        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note


note = CrudNote(Note)
