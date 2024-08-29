from typing import Optional, List
from . import base
from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from .order_item import Items
    
class Orders(base.BaseWithIdNumber):
    quantity: int
    total: Decimal
    status: bool
    user_id: UUID
    items: List[Items]

class OrderCreate(BaseModel):
    status: bool
    user_id: UUID