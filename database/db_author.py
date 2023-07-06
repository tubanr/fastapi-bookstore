from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Author
from routers.schemas import AuthorBase
from database.database import get_db


def create_author(db: Session, author: AuthorBase):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = db.query(Author).get(author_id)
    if db_author:  
       
        for book in db_author.books:
            db.delete(book)
        db.delete(db_author)
        db.commit()
        return True
    return False


# update author
def update_author(db: Session, author_id: int, author: AuthorBase):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author:
        for key, value in author.dict(exclude_unset=True).items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author






   
   









