from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()

# Modelo de Base de Datos (SQLAlchemy)
class BookDB(Base):
    __tablename__ = "books"

    # Se eliminaron las etiquetas que causaban el error
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    available = Column(Boolean, nullable=False)
    language = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now())
    img = Column(String, nullable=False)

# Esquemas de Pydantic (Herencia para operaciones)
class BookBase(BaseModel):
    name: str
    author: str
    pages: int
    available: bool
    language: str
    img: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    available: Optional[bool] = None
    language: Optional[str] = None
    img: Optional[str] = None

class BookResponse(BookBase):
    id: int
    created: datetime

    class Config:
        from_attributes = True