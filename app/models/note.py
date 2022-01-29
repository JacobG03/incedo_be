from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database.base import Base


class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    body = Column(Text, nullable=False)
    sort_id = Column(Integer, nullable=True)
    favorite = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    section_id = Column(Integer, ForeignKey('section.id'), nullable=True)

    def __repr__(self):
        return f'{self.id}, {self.title}'


class Section(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sort_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('section.id'), nullable=True)
    notes = relationship('Note', backref='section')
    sub_sections = relationship('Section')
    
    def __repr__(self):
        return f'{self.id}, {self.name}'
