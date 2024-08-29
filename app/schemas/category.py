from typing import Optional
from . import base
from pydantic import BaseModel
from uuid import UUID
    
class Categories(base.Base):
    title: str
    description: str
    status: bool

class CategoryCreate(BaseModel):
    title: str
    description: str
    status: bool
    user_id: UUID
    
class CategoryUpdate(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]