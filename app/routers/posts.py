from typing import List
from fastapi import APIRouter, HTTPException, status, Response
from app.crud.posts_crud import *
from app.model import UPostOut

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UPostOut])
def get_list_of_all_post()->List[UPostOut]:
    posts = get_all_post()
    return posts

@router.post('/newupost', status_code=status.HTTP_201_CREATED, response_model=UPostOut)
def create_post(post: UPosts):
    post = insert_data_in_uposts_table(post)
    return post

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut)
def get_post(id: int, response: Response):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    print(list(post))
    return post

@router.put('/update/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut)
def update_post(id: int, upost: UPosts, response: Response):
    post = update_post_by_id(id, upost)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    print(list(post))
    return post

@router.delete('/delete/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut)
def delete_post(id: int, response: Response):
    post = delete_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    return post
