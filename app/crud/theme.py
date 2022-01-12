from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Theme
from app import schemas


class CRUDTheme(CRUDBase[Theme, schemas.Theme, schemas.ThemeUpdate]):
    def get_by_name(self, db: Session, name: str) -> schemas.Theme:
        return db.query(self.model).filter(Theme.name == name).first()


theme = CRUDTheme(Theme)
