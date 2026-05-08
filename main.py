import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from model import Base, BookDB, BookCreate, BookUpdate

# Carga las variables desde el archivo .env
load_dotenv()

# Obtiene la URL de Neon
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crea la tabla 'books' en Neon.
# Nota: Esto ignorará las tablas 'dogs' y 'stickers' de parcial2.db[cite: 32, 34].
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
        # Búsqueda por criterio diferente al ID [Criterio 6]
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