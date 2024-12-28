import jwt
from datetime import datetime, timedelta, timezone
from app.model import TokenData
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.crud.users_crud import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 


def create_jwt_token(data: dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp": expire.timestamp()})
    token =jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)
    return token

def verify_jwt_token(token: str, credentials_exception):
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except jwt.InvalidTokenError:
        raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_jwt_token(token, credentials_exception)
    return verify_jwt_token(token, credentials_exception)





