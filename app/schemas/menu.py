from typing import Optional
from . import base
from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
    
class Menus(base.BaseWithIdNumber):
    title: str
    description: str
    price: Decimal
    status: bool
    user_id: UUID
    category_id: int

class MenuCreate(BaseModel):
    title: str
    description: str
    price: Decimal
    status: bool
    user_id: UUID
    category_id: int
    
class MenuUpdate(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]