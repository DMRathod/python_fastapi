from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.model import UserLogin, Token
from app.crud.users_crud import get_user_by_email
from app.util import *
from app.oauth2 import create_jwt_token

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User Not Found")
    access_token = create_jwt_token(data = {"email": user.email})
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password or Email Id")
    return {"access_token": access_token, "token_type": "bearer"}


