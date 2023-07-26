from routers.schemas import BookBase, BookDisplay
from sqlalchemy.orm.session import Session
from database.models import Book, Author,Review
from fastapi import status, HTTPException
from sqlalchemy import or_



def create_book(db: Session, request: BookBase):
    new_book = Book(
        title = request.title,
        author_id = request.author_id,
        description = request.description,
        image_url = request.image_url,
        price = request.price,
        category_id = request.category_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

"""def get_all_books(db: Session ):
    books = db.query(Book).all()
    return [BookDisplay.from_orm(book) for book in books]"""


#search books by title or author or keywords
def search_books(db: Session, title: str = None, author: str = None, keyword: str = None, book_id: int = None):
    query = db.query(Book)
  

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    
    if author:
       query = query.join(Book.author).filter(Author.name.ilike(f"%{author}%"))
    
    if keyword:
        query = query.filter(or_(Book.title.ilike(f"%{keyword}%"), Book.description.ilike(f"%{keyword}%")))
    if book_id:
        query = query.filter(Book.id)
    
    matching_books = query.all()
    return [BookDisplay.from_orm(book) for book in matching_books]


# get a single book from database based on the book_id
def get_book(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()
    return book


# update book
def update_book(db: Session, book: Book, request: BookBase) -> Book:
    book.title = request.title
    book.author_id = request.author_id
    book.description = request.description
    book.image_url = request.image_url
    book.price = request.price
    db.commit()
    db.refresh(book)
    return book



def get_book(db: Session, book_id: int) -> Book:
    return db.query(Book).filter(Book.id == book_id).first()



def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).get(book_id)
    if db_book:
        for review in db_book.reviews:
            db.delete(review)
        db.delete(db_book)
        db.commit()
        return True
    return False


