from typing import Generator
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from app import crud
from app.schemas import _user
from app.database.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Session, Authorize: AuthJWT) -> _user.UserInDB:
    Authorize.jwt_required()
    db_user = crud.user.get(db, Authorize.get_jwt_subject())

    return db_user


def get_verified_user(db: Session, Authorize: AuthJWT) -> _user.UserInDB:
    Authorize.jwt_required()
    db_user = crud.user.get(db, Authorize.get_jwt_subject())

    if not db_user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return db_user
