from sqlmodel import create_engine, SQLModel, Session
from .config import settings

POSTGRESS_SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name1}"

# add echo = true if you like to log create query
# engine = create_engine(POSTGRESS_SQL_DATABASE_URL, echo = True)
engine = create_engine(f"{settings.database_string}", echo = True)


def create_database_and_tables():
    print(POSTGRESS_SQL_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    return "Database Connected"

def close_connection():
    engine.dispose()
    return "Database Disconnected"

def drop_database_and_tables():
    SQLModel.metadata.drop_all(engine)
    return "Database Droped"

def get_session() -> Session: # type: ignore
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

