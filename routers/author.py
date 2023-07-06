from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .schemas import AuthorBase, AuthorDisplay
from database.database import get_db
from database import db_author
from typing import List
from database.models import Author


router =  APIRouter(
    prefix='/authors',
    tags=['author']
)

@router.post('',response_model=AuthorDisplay)
def create_author(author: AuthorBase, db: Session = Depends(get_db)):
    return db_author.create_author(db, author)



#Define router to delete author and associated books
@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    success = db_author.delete_author(db, author_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
    return {'message': 'Author deleted successfully'}


#Define router to update author
@router.put("/{author_id}", response_model=AuthorDisplay)
def update_author(author_id: int, author: AuthorBase, db: Session = Depends(get_db)):
    db_author.update_author(db, author_id, author)
    updated_author = db_author.update_author(db, author_id,author)
    if updated_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author