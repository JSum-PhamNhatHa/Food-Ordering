from . import base
from pydantic import BaseModel, EmailStr
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    
class LoginResponse(base.Base):
    username: str
    email: str
    password: str
    role: str