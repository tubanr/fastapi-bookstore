from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import BookBase, BookDisplay
from database.database import get_db
from database import db_book
from typing import List
from database.models import Book
import random
import string
import shutil

router = APIRouter(
    prefix='/books',
    tags=['book']
)



@router.post('')
def create_book(request: BookBase, db: Session = Depends(get_db)):
    return db_book.create_book(db, request)


"""
#To make image folder accessible statically
@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}"""



"""@router.get('', response_model=List[BookDisplay])
def get_all_books(db: Session = Depends(get_db)):
    return db_book.get_all_books(db)"""


# search a book  by title or author or keyword
@router.get('', response_model=List[BookDisplay])
def search_books_by_keyword(title: str = None, author: str = None, keyword: str = None, db: Session = Depends(get_db)):
    return db_book.search_books(db, title, author, keyword)


# Define route to retrieve a single book by its ID
@router.get("/{book_id}", response_model=BookDisplay) 
def Get_specific_book(book_id: int, db: Session = Depends(get_db)):
    book = db_book.get_book(db, book_id)
    if not book:
        # Raise HTTPException with 404 status code
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book



# Define route for updating a book
@router.put('/{book_id}', response_model=BookDisplay)
def update_book(book_id: int, request: BookBase, db: Session = Depends(get_db)):
    book = db_book.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    updated_book = db_book.update_book(db, book, request)
    return updated_book



@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db_book.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {'message': 'book deleted successfully'}





    