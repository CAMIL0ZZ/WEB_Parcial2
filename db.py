import os
from sqlmodel import Session, create_engine, SQLModel
from fastapi import FastAPI, Depends
from typing import Annotated


engine = create_engine()

def create_all_tables(app: FastAPI):
    if os.getenv("ENV") == "dev":
        SQLModel.metadata.create_all(engine)
    yield


def get_session()->Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

