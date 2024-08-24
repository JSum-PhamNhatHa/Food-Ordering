from typing import Optional
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
    role: str
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None