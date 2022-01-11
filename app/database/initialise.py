import json
import os
import logging
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app import crud
from app.database.session import engine
from app.database.base import Base
from app.models import Avatar, Theme
from app.core import settings, init_account


logger = logging.getLogger('main')

load_dotenv()

def initialise(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    # Populates first Avatar table (id = 1)
    setDefaultAvatar(db)
    # Populates first Theme table (id = 1)
    setDefaultTheme(db)
    # Create own account
    createFirstAccount(db)


def setDefaultAvatar(db: Session) -> None:
    with open(os.path.abspath(settings.AVATAR_PATH), 'rb') as f:
        content = f.read()

    db_avatar = Avatar(content=content)

    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)

    logger.info(f'Default Avatar has been created.\n{db_avatar}')


def setDefaultTheme(db: Session) -> None:
    with open(os.path.abspath('assets/themes.json'), 'r') as f:
        data = json.load(f)
        for theme in data['themes']:
            db_theme = Theme(**theme)
            db.add(db_theme)

    db.commit()

    logger.info(f'Default Themes have been created.')
    logger.info(f'{len(data["themes"])} themes in total.')


def createFirstAccount(db: Session):
    crud.user.create(db, obj_in=init_account)    
    logger.info(f'First account created.')
