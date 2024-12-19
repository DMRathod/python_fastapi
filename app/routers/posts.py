from fastapi import APIRouter, HTTPException, status, Response
from app.crud.posts_crud import *

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK)
def get_list_of_all_post():
    posts = get_all_post()
    return {"ALL UPosts":posts}

@router.post('/newupost', status_code=status.HTTP_201_CREATED)
def create_post(post: UPosts):
    post = insert_data_in_uposts_table(post)
    return {"Created UPost": post.model_dump()}

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_post(id: int, response: Response):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    print(list(post))
    return {f"Post with ID {id}": post}

@router.put('/update/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, upost: UPosts, response: Response):
    post = update_post_by_id(id, upost)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    print(list(post))
    return {"Updated Post": post}

@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int, response: Response):
    post = delete_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist in UPosts")
    return {"Deleted Post": post}
