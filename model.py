from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Dog(SQLModel, table = True):
    __tablename__ = "dogs"
    id: int
    name: str
    size: str
    dangerous: bool
    sterilized: bool
    breed: str
    created: datetime
    img: str

    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
