from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class Base(BaseModel):
    id: UUID
    create_at: datetime
    update_at: datetime
    
class BaseWithIdNumber(BaseModel):
    id: int
    create_at: datetime
    update_at: datetime