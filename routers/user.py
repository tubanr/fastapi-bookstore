from sqlalchemy.orm import Session

from routers.schemas import UserBase,UserDisplay

from fastapi import APIRouter, Depends

from database.database import get_db
from database import db_user
from database.hashing import Hash




router = APIRouter(
    prefix='/signup',
    tags=['user']

)



@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user2(db, request)



@router.get("/{user_id}", response_model=UserDisplay)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db_user.get_user_by_id(db, user_id)
    return user


