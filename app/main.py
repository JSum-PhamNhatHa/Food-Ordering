from fastapi import FastAPI
from .routers import user, auth, category
from .models import tables
from .models.database import engine

tables.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)