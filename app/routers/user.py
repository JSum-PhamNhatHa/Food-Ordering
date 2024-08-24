from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from ..models.database import get_db
from app.models.user import User
from app.schemas.user import TokenData, UserCreate, LoginResponse
from ..utils import helper, oath2

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user, please create at least one user then try again!"
        )
    return users

@router.get("/{id}", response_model=LoginResponse)
def get_user_by_id(id: str, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user with id {id}!"
        )
    else:
        return user

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
                # userData: TokenData = Depends(oath2.get_current_user)):
    # if userData.role is "admin":        
    #     #hash pass
    #     password_hashed = helper.hash(user.password)
    #     user.password = password_hashed
    #     new_user = User(**user.dict())
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)
    #     return new_user
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="User do not have permission!"
    #     )
    password_hashed = helper.hash(user.password)
    user.password = password_hashed
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user