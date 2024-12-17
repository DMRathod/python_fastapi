import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Session, select
from .database import engine

class UPosts(SQLModel, table=True):
    id: Optional[int] | None = Field(default= None, primary_key = True)
    tittle: str
    content: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)

class User(SQLModel, table=True):
    userid: Optional[int] | None = Field(default=None, primary_key=True)
    email: str
    password: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)




def insert_data_in_table(post: UPosts):
    session = Session(engine)
    session.add(post)
    session.commit()
    session.refresh(post)
    session.close()
    print("Data Inserted into the UPost Table")
    return post

def select_all_post():
    with Session(engine) as session:
        posts = session.exec(select(UPosts)).all()
        for post in posts:
            print("post tittle", post.tittle, "post id", post.id)
    return posts

def get_post_by_id(id: int):
    with Session(engine) as session:    
        post = session.get(UPosts, id)
    return post

def update_post_by_id(id: int, upost: UPosts):
    with Session(engine) as session:
        postTobeUpdated = session.exec(select(UPosts).where(UPosts.id == id)).first()
        if postTobeUpdated: 
            upost.id = id
            postTobeUpdated = session.merge(upost)
            session.add(postTobeUpdated)
            session.commit()
            session.refresh(postTobeUpdated)        
    return postTobeUpdated

def delete_post_by_id(id: int):
    with Session(engine) as session:
        upost = session.get(UPosts, id)
        session.delete(upost)
        session.commit()
    return upost

