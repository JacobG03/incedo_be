from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database.base import Base


class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    body = Column(Text, nullable=True)
    favorite = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    parent_id = Column(Integer, ForeignKey('section.id'), nullable=True)
    modified = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.title}'


class Section(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    favorite = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('section.id'), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    notes = relationship('Note', backref='section', cascade="all, delete-orphan")
    sub_sections = relationship('Section', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'{self.id}, {self.name}'
