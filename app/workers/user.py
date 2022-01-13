import logging
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session

from app import crud
from app.models import PasswordReset
from app.utils import repeat_every
from app.main import app
from app.database import SessionLocal
from app.core import settings


logger = logging.getLogger('main')


@app.on_event("startup")
@repeat_every(seconds=settings.REMOVE_UNVERIFIED_INTERVAL)  # 6 hours
def remove_unverified_users() -> None:
    db: Session = SessionLocal()
    db_users = crud.user.get_all_unverified(db)

    removed = 0
    for db_user in db_users:
        if db_user.timestamp + timedelta(seconds=settings.MAX_UNVERIFIED_TIME) < datetime.utcnow():
            crud.user.remove(db, db_user)
            removed += 1

    logger.info(f'Removed {removed} unverified accounts.')


@app.on_event("startup")
@repeat_every(seconds=settings.REMOVE_PASS_RESETS_INTERVAL)
def remove_suspended_password_resets() -> None:
    db: Session = SessionLocal()

    removable = db.query(PasswordReset).filter(
        PasswordReset.suspended == True).all()
    for i in removable:
        db.delete(i)

    db.commit()

    logger.info(f'Cleaned up {len(removable)} suspended password resets.')
