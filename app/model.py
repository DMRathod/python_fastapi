import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Session, select
from .database import engine

class UPosts(SQLModel, table=True):
    id: Optional[int] | None = Field(default= None, primary_key = True)
    tittle: str
    content: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)

class Users(SQLModel, table=True):
    userid: Optional[int] | None = Field(default=None, primary_key=True)
    email: str
    password: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)