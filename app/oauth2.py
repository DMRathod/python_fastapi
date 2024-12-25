import jwt
from datetime import datetime, timedelta
from app.model import TokenData
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_jwt_token(data: dict):
    encoded_data = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({"exp": expire})
    token =jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)
    return token

def verify_jwt_token(token: str, credentials_exception):
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("userid")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)

    except jwt.InvalidTokenError:
        raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_jwt_token(token, credentials_exception)





