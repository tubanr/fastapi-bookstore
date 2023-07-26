from sqlalchemy.orm import Session,selectinload
from database.models import Review,User
from routers.schemas import ReviewBase,ReviewDisplay




def create_review(db: Session, request: ReviewBase, user_id: int):
   
    new_review = Review(
        user_id = user_id,
        text = request.text,
        book_id = request.book_id,
       
        )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_book_reviews(db: Session, book_id: int ):
    
    reviews = (
        db.query(Review)
        .join(Review.user)
        .filter(Review.book_id == book_id).options(selectinload(Review.user))
        .all()
    )
    reviews_with_username =[
        ReviewDisplay(
        id=review.id,
        user_id=review.user_id,
        text=review.text,
        book_id=review.book_id,
        username=review.user.username)
        for review in reviews
    ]
    return reviews_with_username

    #  return db.query(Review).filter(Review.book_id == book_id).all()
  


def delete_review_by_id(db: Session, review_id: int, user_id:int):
    db_review = db.query(Review).get(review_id)
    if db_review is not None:
        db.delete(db_review)
        db.commit()
        return True
    return False










 # reviews = db.query(Review).filter(Review.book_id==book_id).all()
    # reviews_with_username = []

    # for review in reviews:
    #     user = db.query(User).get(review.user_id)
    #     username = user.username if user else None

    #     review_display = ReviewDisplay(
    #         id=review.id,
    #         user_id=review.user_id,
    #         text=review.text,
    #         book_id=review.book_id,
    #         username=username)
    #     reviews_with_username.append(review_display)
    #     return reviews_with_username