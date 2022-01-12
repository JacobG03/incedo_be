import json
import os
import logging
from PIL import Image
from io import BytesIO
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app import crud
from app.database.session import engine
from app.database.base import Base
from app.models import Avatar, Theme
from app.core import settings, first_account


logger = logging.getLogger('main')

load_dotenv()

def initialise(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    # Populates first Avatar table (id = 1)
    setDefaultAvatar(db)
    # Populates first Theme table (id = 1)
    setDefaultThemes(db)
    # Create own account
    createFirstAccount(db)


def setDefaultAvatar(db: Session) -> None:
    with BytesIO() as output:
        with Image.open(os.path.abspath(settings.AVATAR_PATH)) as img:
            resized = img.resize(size=(settings.AVATAR_SIZE, settings.AVATAR_SIZE))
            resized.save(output, 'png')
        data = output.getvalue()
    
    db_avatar = Avatar(content=data)

    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)

    logger.info(f'Default Avatar has been created.')


def setDefaultThemes(db: Session) -> None:
    with open(os.path.abspath('assets/themes.json'), 'r') as f:
        data = json.load(f)
        for theme in data['themes']:
            db_theme = Theme(**theme)
            db.add(db_theme)

    db.commit()

    logger.info(f'Default Themes have been created.')


def createFirstAccount(db: Session) -> None:
    crud.user.create(db, obj_in=first_account)    
    logger.info(f'First account created.')
