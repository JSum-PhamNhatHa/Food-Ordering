from fastapi import FastAPI
from .routers import user, auth, category, menu, order, order_item
from .models import tables
from .models.database import engine

tables.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(menu.router)
app.include_router(order.router)
app.include_router(order_item.router)