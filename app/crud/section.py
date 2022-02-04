from typing import List, Optional
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models.note import Section, Note
from app.schemas import _section, _user


class CRUDSection(CRUDBase[Section, _section.Section, _section.SectionUpdate]):
    def create(self, db: Session, db_user: _user.UserInDB, section_in: _section.Section) -> _section.SectionDB:
        if section_in.parent_id != None:
            try:
                self.get(db, db_user, section_in.parent_id)
            except HTTPException:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[{
                        'loc': [
                            'body',
                            'parent_id'
                        ],
                        'msg': 'Parent does not exist.'
                    }])

        section_db = Section(**section_in.dict())
        db.add(section_db)
        db.commit()
        db.refresh(section_db)

        return section_db

    def get(self, db: Session, db_user: _user.UserInDB, section_id: int)\
        -> Optional[_section.SectionDB]:
        db_section = db.query(self.model).filter_by(
            user_id = db_user.id,
            id = section_id).one_or_none()
        if not db_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return db_section

    def get_multi(self, db: Session, db_user: _user.UserInDB, reverse: bool = False, skip: int = 0,\
        limit: int = 100) -> List[_section.SectionDB]:
        if reverse:
            db_sections = db.query(self.model).filter(
                self.model.user_id == db_user.id).order_by(self.model.id.desc()).limit(limit)
            db_sections = db_sections[skip::1]
        else:
            db_sections = db.query(self.model).filter(
                self.model.user_id == db_user.id).offset(skip).limit(limit).all()

        return db_sections

    def remove(self, db: Session, db_user: _user.UserInDB, db_section: _section.SectionDB ) -> None:
        if db_section.user_id != db_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db.delete(db_section)
        db.commit()

        return
    
    def update(self, db: Session, db_user: _user.UserInDB, section_id: int, section_in: _section.SectionUpdate) -> _section.SectionDB:
        db_section = self.get(db, db_user, section_id)
        if section_in.parent_id:
            if section_in.parent_id == db_section.id:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[{
                        'loc': [
                            'body',
                            'parent_id'
                        ],
                        'msg': 'Parent cannot == this section.'
                    }]
                )
            try:
                self.get(db, db_user, section_in.parent_id)
            except HTTPException:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[{
                        'loc': [
                            'body',
                            'parent_id'
                        ],
                        'msg': 'Parent does not exist.'
                    }]
                )
        # Validate stuff if needed -> test
        
        obj_data = jsonable_encoder(section_in)
        update_data = section_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_section, field, update_data[field])

        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        
        return db_section


section = CRUDSection(Section)
