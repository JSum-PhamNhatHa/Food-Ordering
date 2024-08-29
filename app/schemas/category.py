from typing import Optional
from . import base
from pydantic import BaseModel
from uuid import UUID
    
class Categories(base.BaseWithIdNumber):
    title: str
    description: str
    status: bool
    user_id: UUID

class CategoryCreate(BaseModel):
    title: str
    description: str
    status: bool
    user_id: UUID
    
class CategoryUpdate(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]