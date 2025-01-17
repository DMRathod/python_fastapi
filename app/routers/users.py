from typing import List
from fastapi import APIRouter, status, HTTPException, Response, Depends
from app.crud.users_crud import *
from app.model import UserOut, UserIn
from app.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/", status_code=status.HTTP_201_CREATED, response_model=List[UserOut], responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def get_list_of_users(session: Session = Depends(get_session))->List[UserOut]:
    users = get_all_user(session)
    return users

@router.get('/by-id/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def get_user_with_id(id: int, response: Response, session: Session = Depends(get_session)):
    user = get_user_by_id(id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user

@router.get('/by-email/{email}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def get_user_with_email(email: str, response: Response, session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {email} does not exist in Users")
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut, responses={
        500: {"description": "Internal server error"}
    })
def create_user(user: UserIn, session: Session = Depends(get_session))->UserOut:
    try: 
        user = Users(email=user.email, password=user.password)   
        user = insert_data_in_users_table(user, session)       
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Validation Error {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error {str(e.args)}") 
    return user

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def update_user(id: int, user: UserIn, response: Response, session: Session = Depends(get_session)):
    user = Users(email=user.email, password=user.password)   
    user = update_user_by_id(id, user, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def delete_user(id: int, response: Response, session: Session = Depends(get_session)):
    user = delete_user_by_id(id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user
