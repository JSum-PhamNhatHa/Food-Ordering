from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils import oath2
from ..models.database import get_db
from app.schemas.user import UserLogin
from ..utils import helper

router = APIRouter(tags=['Authentication'])

@router.post("/login", status_code=status.HTTP_201_CREATED)
def login(user_credentials: UserLogin = Depends(), db: Session= Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Creadentials"
        )
        
    if not helper.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Creadentials"
        )
        
    access_token = oath2.create_access_token(
        data={"user_id": str(user.id),
              "role": user.role,
              "username": user.username,
              "email": user.email})
    return access_token