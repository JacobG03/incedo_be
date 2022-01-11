import os
import logging
from sqlalchemy.orm import Session


from app.database.session import engine
from app.database.base import Base
from app.models import Avatar, Theme
from app.core import settings, default_theme


logger = logging.getLogger('main')


def initialise(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    # Populates first Avatar table (id = 1)
    setDefaultAvatar(db)
    # Populates first Theme table (id = 1) 
    setDefaultTheme(db)
    

def setDefaultAvatar(db: Session) -> None:
    with open(os.path.abspath(settings.AVATAR_PATH), 'rb') as f:
        content = f.read()
        
    db_avatar = Avatar(content=content)
    
    db.add(db_avatar)
    db.commit()
    db.refresh(db_avatar)

    logger.info(f'Default Avatar has been created.\n{db_avatar}')


def setDefaultTheme(db: Session) -> None:
    theme = Theme(**default_theme.dict())
    
    db.add(theme)
    db.commit()
    db.refresh(theme)
    
    logger.info(f'Default Theme has been created.\n{theme}')
    