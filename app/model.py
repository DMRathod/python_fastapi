import datetime
import bcrypt
from pydantic import EmailStr, field_validator
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
    email: EmailStr = Field(sa_column_kwargs={"unique": True})
    password: str
    create_dtm: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)

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