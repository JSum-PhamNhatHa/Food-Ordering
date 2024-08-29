from typing import Optional
from . import base
from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
    
class Items(base.BaseWithIdNumber):
    quantity: int
    price: Decimal
    total: Decimal
    menu_id: int
    user_id: UUID
    order_id: int

class ItemCreate(BaseModel):
    menu_id: int
    quantity: int
    price: Decimal
    # total: Decimal
    user_id: UUID
    
class ItemUpdate(BaseModel):
    id: int
    quantity: int