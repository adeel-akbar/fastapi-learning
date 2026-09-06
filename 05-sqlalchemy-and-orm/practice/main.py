from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get("/", response_model = list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.execute(select(models.Book)).result.scalars().all()
    return books

@app.post("/", status_code = status.HTTP_201_CREATED, 
          response_model = schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/{book_id}", response_model = schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.execute(select(models.Book).where(models.Book.id == book_id)).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Book with id: {book_id} not found..")
    return book

@app.delete("/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.execute(select(models.Book).where(models.Book.id == book_id)).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                    detail = f"Book with id: {book_id} not found..")
    db.delete(book)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/{book_id}", response_model = schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    the_book = db.execute(select(models.Book).where(models.Book.id == book_id)).scalar_one_or_none()
    if not the_book:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                            detail = f"Book with id: {book_id} not found..")
    for key, value in book.model_dump().items():
        setattr(the_book, key, value)
    db.commit()
    db.refresh(the_book)
    return the_book

# QUESTIONS: Get all books where: published == True
@app.get("/published/{published}", response_model = list[schemas.BookResponse])
def get_published_books(published: bool, db: Session = Depends(get_db)):
    result = db.execute(select(models.Book).where(models.Book.published == published)).scalars().all()
    return result

# QUESTION: Get books by a particular author.
@app.get("/author/{author}", response_model = list[schemas.BookResponse])
def get_books_by_author(author: str, db: Session = Depends(get_db)):
    result = db.execute(select(models.Book).where(models.Book.author == author)).scalars().all()
    return result

# If you have multiple get requests or any other requests FastAPI will execute them in
# an order from top to bottom e.g if you have the get request which accepts id as int 
# then for executing the get request which is at bottom you have to change the url as i did
# /published and the /author or you have to comment out the previous one and restart the 
# connection else FastAPI will expect the first one's rule for execution which is id: int.