from sqlalchemy.orm import Session

from routers.schemas import UserBase,UserDisplay

from fastapi import APIRouter, Depends

from database.database import get_db
from database import db_user
from database.hashing import Hash





router = APIRouter(
    prefix='/user',
    tags=['user']

)



@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user2(db, request)


