from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from app.models.tables import User
from app.schemas.user import TokenData, UserCreate, Users, UserUpdate
from ..utils import helper, auth, constants

router = APIRouter(prefix="/categories", tags=["Category"])

@router.get("/", response_model=List[Users])
def get_users(db: Session = Depends(get_db), 
              userData: TokenData = Depends(auth.get_current_user),
              page_index: int = Query(1, ge=1),
              page_size: int = Query(10, le=100)):
    if userData.role == constants.ROLE_ADMIN:
        query = db.query(User)
    elif userData.role == constants.ROLE_STAFF:
        query = db.query(User).filter(User.role == constants.ROLE_CUSTOMER)
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
def get_user_by_own_id(db: Session= Depends(get_db),
                   userData: TokenData = Depends(auth.get_current_user)):
    user = db.query(User).filter(User.id == userData.id).first()
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

@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(user: UserUpdate, db: Session = Depends(get_db),
                userData: TokenData = Depends(auth.get_current_user)):
    if user.password is None:
        user.password = userData.password
    if not user.username is None:
        user.username = userData.username
    db_user = db.query(User).filter(User.id == userData.id).first()
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if str(db_user.id) != userData.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    password_hashed = helper.hash(user.password)
    user.password = password_hashed
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str,
                db : Session = Depends(get_db),
                userData: TokenData = Depends(auth.get_current_user)):
    
    if userData.role == constants.ROLE_CUSTOMER:
        db_user = db.query(User).filter(User.id == userData.id).first()
        
    elif userData.role == constants.ROLE_STAFF:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    
    else:
        db_user = db.query(User).filter(User.id == id).first()    
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    
    return {"detail": "User deleted"}