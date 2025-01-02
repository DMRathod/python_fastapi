import datetime
import bcrypt
from pydantic import EmailStr, field_validator
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlmodel import Field, SQLModel, Relationship
from .database import engine
from enum import Enum

class Users(SQLModel, table=True):
    userid: Optional[int] | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(sa_column_kwargs={"unique": True})
    password: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)
    posts: list["UPosts"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    votes: list["Votes"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade":"all, delete-orphan"})


    @field_validator("email", mode="before")
    def validate_email_domain(cls, value):
        allowed_domains = ["gmail.com", "yahoo.com"] 
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise ValueError(f"Invalid email domain: {domain}. Allowed domains: {', '.join(allowed_domains)}")
        return value
    
    @field_validator("password", mode = "before")
    def password_hash(cls, password):
        if password:
            hashedpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashedpass.decode('utf-8')
        return password

    def verify_password(self, password: str)->bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class UPosts(SQLModel, table=True):
    id: Optional[int] | None = Field(default= None, primary_key = True)
    tittle: str
    content: str
    userid: int = Field(foreign_key="users.userid", nullable=False) 
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)
    owner: Optional[Users] = Relationship(back_populates="posts")
    votes: list["Votes"] = Relationship(back_populates="post", sa_relationship_kwargs={"cascade":"all, delete-orphan"})

class UserOut(SQLModel):
    userid: int
    email: EmailStr
    create_dtm: datetime.datetime

class UPostOut(SQLModel):
    id: int
    tittle: str
    content: str
    userid: int
    create_dtm: datetime.datetime
    owner: Optional[UserOut] 

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    email: Optional[EmailStr] = None
    id: Optional[int] = None

class Votes(SQLModel, table = True):
    user_id: Optional[int] = Field(default= None, primary_key = True, foreign_key="users.userid")
    post_id: Optional[int] = Field(default= None, primary_key = True, foreign_key="uposts.id")    
    user: Optional[Users] = Relationship(back_populates="votes")
    post: Optional[UPosts] = Relationship(back_populates="votes")

class VoteDirection(str,Enum):
    DOWNVOTE = "DOWNVOTE" # type: ignore
    UPVOTE = "UPVOTE" # type: ignore

class Vote(SQLModel):
    post_id: int
    dir: VoteDirection

class UPostswithCount(SQLModel):
    UPosts: UPosts
    vote: int
