from typing import List
from fastapi import APIRouter, status, HTTPException, Response
from app.crud.users_crud import *
from app.model import UserOut, UserIn

router = APIRouter()

@router.get("/", status_code=status.HTTP_201_CREATED, response_model=List[UserOut], responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def get_list_of_users()->List[UserOut]:
    users = get_all_user()
    return users

@router.get('/by-id/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def get_user_with_id(id: int, response: Response):
    user = get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user

@router.get('/by-email/{email}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def get_user_with_email(email: str, response: Response):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {email} does not exist in Users")
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut, responses={
        500: {"description": "Internal server error"}
    })
def create_user(user: UserIn)->UserOut:
    try: 
        user = Users(email=user.email, password=user.password)   
        user = insert_data_in_users_table(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error {str(e.args)}")        
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error {str(e.detail)}")
    return user

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def update_user(id: int, user: UserIn, response: Response):
    user = Users(email=user.email, password=user.password)   
    user = update_user_by_id(id, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user

@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut, responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    })
def delete_user(id: int, response: Response):
    user = delete_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user
