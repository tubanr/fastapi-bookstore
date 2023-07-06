from sqlalchemy.orm import Session
from database.models import Review
from routers.schemas import ReviewBase




def create_review(db: Session, request: ReviewBase, user_id: int):

    new_review = Review(
        user_id = user_id,
        text = request.text,
        book_id = request.book_id)
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_book_reviews(db: Session, book_id: int ):
    return db.query(Review).filter(Review.book_id == book_id).all()


def delete_review_by_id(db: Session, review_id: int, user_id:int):
    db_review = db.query(Review).get(review_id)
    if db_review is not None:
        db.delete(db_review)
        db.commit()
        return True
    return False