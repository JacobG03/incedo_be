from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase, ModelType
from app.models import Note
from app.schemas import _note, _user


class CrudNote(CRUDBase[Note, _note.Note, _note.NoteUpdate]):
    def create(self, db: Session, db_user: _user.UserInDB, note_in: _note.Note) -> _note.NoteDB:
        db_note = self.model(**note_in.dict(), user_id=db_user.id)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        
        return db_note
      
    def get_multi(self, db: Session, db_user=_user.UserInDB, *, reverse: bool = False, skip: int = 0, limit: int = 100) -> List[ModelType]:
        if reverse:
            db_obj = db.query(self.model).filter(self.model.user_id == db_user.id).order_by(self.model.id.desc()).limit(limit)
            db_obj = db_obj[skip::1]
        else:
            db_obj = db.query(self.model).filter(self.model.user_id == db_user.id).offset(skip).limit(limit).all()
            
        return db_obj

note = CrudNote(Note)
