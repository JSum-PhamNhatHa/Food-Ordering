from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from app.models.tables import User
from app.schemas.user import TokenData, UserCreate, Users
from ..utils import helper, auth

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/", response_model=List[Users])
def get_users(db: Session = Depends(get_db), 
              userData: TokenData = Depends(auth.get_current_user),
              page_index: int = Query(1, ge=1),
              page_size: int = Query(10, le=100)):
    if userData.role == "admin":
        query = db.query(User)
    elif userData.role == "staff":
        query = db.query(User).filter(User.role == "cust")
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission!"
        )

    total_size = query.count()
    total_page = (total_size + page_size - 1) // page_size

    if page_index > total_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page index out of range!"
        )

    page_skip = (page_index - 1) * page_size
    users = query.offset(page_skip).limit(page_size).all()
    return users

@router.get("/{id}", response_model=Users)
def get_user_by_id(db: Session= Depends(get_db),
                   userData: TokenData = Depends(auth.get_current_user)):
    # print(db.query(User).filter(userData.id == id).first())
    user = db.query(User).filter(str(userData.id) == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user with id {id}!" 
        )
    else:
        return user

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    password_hashed = helper.hash(user.password)
    user.password = password_hashed
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user