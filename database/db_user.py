from fastapi import HTTPException, status
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from database.models import User
from database.hashing import Hash




def create_user2(db: Session, request: UserBase):
    new_user = User (
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
        role=request.role

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found")
    return user


