from fastapi import HTTPException, status
from pydantic import ValidationError
from app.database import get_session
from app.model import  Vote, Votes
from sqlmodel import select

session = next(get_session())

def is_vote_exist(vote: Vote, userid):
    vote_found = session.exec(select(Votes).filter(Votes.post_id == vote.post_id, Votes.user_id == userid)).first()
    return vote_found

def add_vote(vote: Vote, userid):
    vote = Votes(post_id=vote.post_id, user_id=userid)
    session.add(vote)
    session.commit()
    return {"msg":"Added Vote"}

def delete_vote(vote: Vote, userid):
    vote = session.exec(select(Votes).filter(Votes.post_id == vote.post_id, Votes.user_id == userid)).first()
    session.delete(vote)
    session.commit()
    return {"msg":"Deleted Vote"}


