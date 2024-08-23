import time
from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='PersonalFinanceTracker',
#                                 user='postgres', password='123456789', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as err:
#         print("Connecting to database failed, error: ", err)
#         time.sleep(2)

# @app.get("/")
# def get_users(db:Session = Depends(get_db)):
#     users = db.query(models.Temp).all()
#     return {"data": users}

# @app.post("/sql")
# def get_test(post: models.Temp, db:Session = Depends(get_db)):
#     new_post = models.Temp(title=post.title, content=post.content, pulished=post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(n)
#     return {"status": "success"}

# @app.post("/create-user", status_code=status.HTTP_201_CREATED)
# def create_users(user: User, db:Session = Depends(get_db)):
#     # cursor.execute("""INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s)
#     #                RETURNING *""",
#     #                new_user.username, new_user.email, new_user.password_hash, "user")
#     # new = cursor.fetchone()    
#     # conn.commit()
#     new_user = models.User(username=new_user.username, )
#     new_user = db.add()
    
#     return {"data": new}