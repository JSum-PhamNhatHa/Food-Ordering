from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from ..schemas.user import TokenData
from . import constants 

oath2_scheme = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, constants.SECRET_KEY, algorithm=constants.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.ALGORITHM])
        id: str = payload.get("user_id")
        role: str = payload.get("role")
        username: str = payload.get("username")
        email: str = payload.get("email")
        password: str = payload.get("password")
    
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id, username=username, email=email, role=role, password=password)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: HTTPAuthorizationCredentials = Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token.credentials, credentials_exception)
    