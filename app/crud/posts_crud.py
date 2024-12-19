from app.database import get_session
from app.model import UPosts
from sqlmodel import select

session = next(get_session())

def insert_data_in_uposts_table(post: UPosts):
    session.add(post)
    session.commit()
    session.refresh(post)
    session.close()
    return post

def get_all_post():    
        posts = session.exec(select(UPosts)).all()
        return posts

def get_post_by_id(id: int):
        post = session.get(UPosts, id)
        return post

def update_post_by_id(id: int, upost: UPosts):
    postTobeUpdated = session.exec(select(UPosts).where(UPosts.id == id)).first()
    if postTobeUpdated: 
        upost.id = id
        postTobeUpdated = session.merge(upost)
        session.add(postTobeUpdated)
        session.commit()
        session.refresh(postTobeUpdated)        
    return postTobeUpdated

def delete_post_by_id(id: int):
    upost = session.get(UPosts, id)
    if upost:
        session.delete(upost)
        session.commit()
    return upost

