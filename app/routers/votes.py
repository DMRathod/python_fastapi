from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.crud.votes_crud import *
from app.model import Vote, TokenData
from app.oauth2 import get_current_user

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, current_user:TokenData = Depends(get_current_user)):
    vote_found = is_vote_exist(vote, current_user.id)
    print(vote.dir.value == "UPVOTE")
    if(vote.dir.value == "UPVOTE"):
        if vote_found: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has Already voted on Post with id {vote.post_id}")
        add_vote(vote, current_user.id)
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Us~er {current_user.id} has not voted on Post with id {vote.post_id}")
        delete_vote(vote, current_user.id)

