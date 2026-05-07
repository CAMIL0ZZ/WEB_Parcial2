from sqlmodel import Field, SQLModel

from datetime import datetime, timezone


class Dog(SQLModel, table = True):
    __tablename__ = "dogs"

    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Sticker(SQLModel, table = True):
    __tablename__ = "stickers"

    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Book(SQLModel, table = True):
    __tablename__ = "books"

    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))