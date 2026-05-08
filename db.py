import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from model import Base, BookDB, BookCreate, BookUpdate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") [cite: 1]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializar tablas (Solo crea 'books', ignorando dogs/stickers)
Base.metadata.create_all(bind=engine)

class BookRepository:
    @staticmethod
    def create(db: Session, book: BookCreate):
        db_book = BookDB(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def find_all(db: Session):
        return db.query(BookDB).all()

    @staticmethod
    def find_one(db: Session, book_id: int):
        return db.query(BookDB).filter(BookDB.id == book_id).first()

    @staticmethod
    def find_by_author(db: Session, author: str):
        return db.query(BookDB).filter(BookDB.author.ilike(f"%{author}%")).first()

    @staticmethod
    def update(db: Session, book_id: int, book_data: BookUpdate):
        db_query = db.query(BookDB).filter(BookDB.id == book_id)
        db_book = db_query.first()
        if db_book:
            update_data = book_data.dict(exclude_unset=True)
            db_query.update(update_data)
            db.commit()
            db.refresh(db_book)
        return db_book

    @staticmethod
    def delete(db: Session, book_id: int):
        db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
        if db_book:
            db.delete(db_book)
            db.commit()
            return True
        return False