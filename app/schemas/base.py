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
    
class PagingModel(BaseModel):
    page_index: int
    page_size: int
    total_page: int
    total_size: int
    page_skip: int