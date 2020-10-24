from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    img_url = Column(String, unique=False, nullable=True,)
    writer_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship('Writer', back_populates='posts')

class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=False, nullable=False,)
    url = Column(String, unique=True, nullable=False)
    posts = relationship('Post', back_populates='writer')


print('ok')