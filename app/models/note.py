from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime

from app.database.base import Base


class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.title}'
