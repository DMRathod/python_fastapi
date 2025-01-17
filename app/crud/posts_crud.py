from app.database import get_session
from app.model import UPosts, Votes, Users
from sqlmodel import select, func 
from sqlalchemy.orm import joinedload

session = next(get_session())

def insert_data_in_uposts_table(post: UPosts, session):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_all_post(limit, skip, search, session):    
        posts = session.exec(select(UPosts).filter(UPosts.title.contains(search)).limit(limit).offset(skip)).all()
        return posts

def get_all_post_with_count(limit, skip, search, session):    
        posts = session.exec(select(UPosts, func.count(Votes.post_id).label("vote_count")).join(Votes, UPosts.id == Votes.post_id, isouter=True).group_by(UPosts.id).filter(UPosts.title.contains(search)).limit(limit).offset(skip)).all()
        posts_with_counts = [{"UPosts": post, "vote": vote_count} for post, vote_count in posts]
        return posts_with_counts

def get_post_by_id(id: int, session):
        post = session.get(UPosts, id)
        return post

def update_post_by_id(id: int, upost: UPosts, session):
    postTobeUpdated = session.exec(select(UPosts).where(UPosts.id == id)).first()
    if postTobeUpdated: 
        upost.id = id
        postTobeUpdated = session.merge(upost)
        session.add(postTobeUpdated)
        session.commit()
        session.refresh(postTobeUpdated)        
    return postTobeUpdated

def delete_post_by_id(id: int, session):
    upost = session.exec(select(UPosts).join(Users).where(UPosts.id == id).options(joinedload(UPosts.owner))).first()
    if upost:
        session.delete(upost)
        session.commit()
    return upost

