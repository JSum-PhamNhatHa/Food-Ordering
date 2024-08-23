from pydantic import BaseModel

class Base(BaseModel):
    id: str
    create_date: str
    update_date: str