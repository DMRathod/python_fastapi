from fastapi import APIRouter, status, HTTPException, Response
from app.crud.users_crud import *

router = APIRouter()

@router.get("/", status_code=status.HTTP_201_CREATED)
def get_users():
    users = get_all_user()
    return {"Users": users}

@router.post('/adduser', status_code=status.HTTP_201_CREATED)
def create_user(user: Users):
    try:    
        user = insert_data_in_users_table(user)
        return {"Created User": user.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User NOT Created, Please Check Request {str(e.args)}")

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int, response: Response):
    user = get_post_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return {f"User with ID {id}": user}

@router.put('/update/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, user: Users, response: Response):
    user = update_user_by_id(id, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return {"Updated User": user}


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int, response: Response):
    user = delete_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} does not exist in Users")
    return {"Deleted user": user}
