from typing import Optional
from . import base
from pydantic import BaseModel
    
class Menus(base.Base):
    title: str
    description: str
    price: numeric(5,2)
    status: bool

class CategoryCreate(BaseModel):
    title: str
    description: str
    
class CategoryUpdate(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]