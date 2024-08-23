from fastapi import Depends, FastAPI, status
from app.main import app
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserCreate

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user.User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user