from . import base
from pydantic import BaseModel, EmailStr

class User(base.Base):
    username: str
    email: EmailStr
    password: str
    role: str
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str