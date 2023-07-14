from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_review
from routers.schemas import ReviewBase, UserAuth, ReviewDisplay
from auth.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/reviews',
    tags=['review']
)


@router.post('') #updated
def create_review(request: ReviewBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    user_id =current_user.id

    return db_review.create_review(db,request, user_id)



@router.get('')
def spesific_book_reviews(book_id: int = None, db:Session = Depends(get_db)):
    return db_review.get_book_reviews(db,book_id)
  


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    success = db_review.delete_review_by_id(db, review_id, current_user)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "review not found" )
    return {"detail": "Review deleted"}



