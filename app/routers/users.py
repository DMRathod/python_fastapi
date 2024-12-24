from typing import List
from fastapi import APIRouter, status, HTTPException, Response
from app.crud.users_crud import *
from app.model import UserOut
router = APIRouter()

@router.get("/", status_code=status.HTTP_201_CREATED, response_model=List[UserOut])
def get_users()->List[UserOut]:
    users = get_all_user()
    return users

@router.post('/adduser', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: Users)->UserOut:
    try:    
        user = insert_data_in_users_table(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User NOT Created, Please Check Request {str(e.args)}")

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(id: int, response: Response):
    user = get_post_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user

@router.put('/update/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def update_post(id: int, user: Users, response: Response):
    user = update_user_by_id(id, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def delete_post(id: int, response: Response):
    user = delete_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return user
