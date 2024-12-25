from fastapi import HTTPException, status
from pydantic import ValidationError
from app.database import get_session
from app.model import  Users
from sqlmodel import select

session = next(get_session())


def insert_data_in_users_table(user: Users)->Users:
    try:    
        user_dict = {**user.model_dump()}
        Users.validate_email_domain(user.email)
        user.password = Users.password_hash(user.password)
        session.add(user)
        session.commit()        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"User NOT Created, Please Check Request {str(e.args)}")    
    session.refresh(user)
    return user

def get_all_user()->Users:    
        users = session.exec(select(Users)).all()
        return users

def get_user_by_id(id: int):
        user = session.get(Users, id)
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")        

def get_user_by_email(email: str):
        user = session.exec(select(Users).where(Users.email == email)).first()
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not found in the System")        
        
def update_user_by_id(id: int, user: Users):
    usertobeupdated = session.exec(select(Users).where(Users.userid == id)).first()
    if usertobeupdated: 
        user.userid = id
        usertobeupdated = session.merge(user)
        session.add(usertobeupdated)
        session.commit()
        session.refresh(usertobeupdated)    
    return usertobeupdated

def delete_user_by_id(id: int):
    user = session.get(Users, id)
    if user: 
        session.delete(user)
        session.commit()
    return user

