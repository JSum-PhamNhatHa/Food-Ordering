from fastapi import Depends, FastAPI, HTTPException, status
from app.main import app
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, LoginResponse
import utils.helper

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user, please create at least one user then try again!"
        )
    return users

@app.get("/users/{id}", response_model=LoginResponse)
def get_user_by_id(id: str, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user with id {id}!"
        )
    else:
        return user

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):    
    #hash pass
    password_hashed = utils.helper.hash(user.password)
    user.password = password_hashed
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user