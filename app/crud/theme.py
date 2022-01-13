from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Theme
from app.schemas import _assets


class CRUDTheme(CRUDBase[Theme, _assets.Theme, _assets.ThemeUpdate]):
    def get_by_name(self, db: Session, name: str) -> _assets.Theme:
        return db.query(self.model).filter(Theme.name == name).first()


theme = CRUDTheme(Theme)
