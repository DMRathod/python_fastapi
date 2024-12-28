from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.crud.posts_crud import *
from app.model import UPostOut
from app.oauth2 import get_current_user

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UPostOut],)
def get_list_of_post(userid: int = Depends(get_current_user))->List[UPostOut]:
    posts = get_all_post()
    return posts

@router.get('/get/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut)
def get_post(id: int, response: Response, user_email: str = Depends(get_current_user)):
    print("user email", user_email)
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    print(list(post))
    return post

@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=UPostOut)
def create_post(post: UPosts, user_email: str = Depends(get_current_user)):
    print(user_email)
    post = insert_data_in_uposts_table(post)
    return post

@router.put('/update/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut)
def update_post(id: int, upost: UPosts, response: Response, user_email: str = Depends(get_current_user)):
    post = update_post_by_id(id, upost)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    print(list(post))
    return post

@router.delete('/delete/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut)
def delete_post(id: int, response: Response, user_email: str = Depends(get_current_user)):
    post = delete_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    return post
