from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database.database import get_db
from sqlalchemy.orm.session import Session
from database.models import User
from database.hashing import Hash
from auth.oauth2 import create_access_token


router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def create_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password")
    
    access_token = create_access_token(data={'username': user.username})
    return {
        'access_token': access_token,
        'token_type':'bearer',
        'user_id':user.id,
        'username':user.username
    }
