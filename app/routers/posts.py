from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.crud.posts_crud import *
from app.model import UPostOut, TokenData, UPostswithCount, UPostCreate
from app.oauth2 import get_current_user

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UPostOut], responses={
        404: {"description": "Posts not found"},
        500: {"description": "Internal server error"}
    })
def get_list_of_post(current_user:TokenData = Depends(get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = "")->List[UPostOut]:
    posts = get_all_post(limit, skip, search)
    return posts

@router.get('/withcount', status_code=status.HTTP_200_OK, response_model=List[UPostswithCount], responses={
        404: {"description": "Posts not found"},
        500: {"description": "Internal server error"}
    })
def get_list_of_post_with_count(current_user:TokenData = Depends(get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = "")->List[UPostswithCount]:
    posts = get_all_post_with_count(limit, skip, search)
    return posts
  
@router.get('/get/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut, responses={
        404: {"description": "Post not found"},
        500: {"description": "Internal server error"}
    })
def get_post(id: int, response: Response, current_user:TokenData = Depends(get_current_user)):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    if current_user.id != post.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not Authorized to get the post")
    return post

@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=UPostOut, responses={
        500: {"description": "Internal server error"}
    })
def create_post(post: UPostCreate, current_user:TokenData = Depends(get_current_user)):
    post = UPosts(title=post.title, content=post.content)
    post.userid = current_user.id
    post = insert_data_in_uposts_table(post)
    return post

@router.put('/update/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut, responses={
        404: {"description": "Post not found"},
        500: {"description": "Internal server error"}
    })
def update_post(id: int, post: UPostCreate, response: Response, current_user:TokenData = Depends(get_current_user)):
    post = UPosts(title=post.title, content=post.content)
    post = update_post_by_id(id, post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    if current_user.id != post.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not Authorized to get the post")
    return post

@router.delete('/delete/{id}', status_code=status.HTTP_200_OK, response_model=UPostOut, responses={
        404: {"description": "Post not found"},
        500: {"description": "Internal server error"}
    })
def delete_post(id: int, response: Response, current_user:TokenData = Depends(get_current_user)):
    post = delete_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    if current_user.id != post.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not Authorized to get the post")
    return post
