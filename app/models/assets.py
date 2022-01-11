from sqlalchemy import Column, Integer, LargeBinary, String

from app.database.base import Base


class Avatar(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(LargeBinary)
    
    def __repr__(self):
        return f'{self.id}'


class Theme(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    bg = Column(String, nullable=False)
    main = Column(String, nullable=False)
    sub = Column(String, nullable=False)
    info = Column(String, nullable=False)
    text = Column(String, nullable=False)
    error = Column(String, nullable=False)
    
    def __repr__(self):
      return f'{self.id}, {self.name}'
