from sqlmodel import create_engine 

POSTGRESS_SQL_DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

engine = create_engine(POSTGRESS_SQL_DATABASE_URL, echo= True)
