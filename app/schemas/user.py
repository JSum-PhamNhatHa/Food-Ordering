from typing import Optional
from . import base
from pydantic import BaseModel, EmailStr
    
class Users(base.Base):
    username: str
    email: str
    password: str
    role: str
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None