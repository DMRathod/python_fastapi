from sqlmodel import create_engine, SQLModel, Session
from .config import settings

POSTGRESS_SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name1}"
TEST_POSTGRESS_SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.test_database_name}"

# add echo = true if you like to log create query
SQL_DATABASE_URL = POSTGRESS_SQL_DATABASE_URL
# engine = create_engine(SQL_DATABASE_URL) #Dev Env
engine = create_engine(f"{settings.database_string}",echo = True)

def set_test_database():
    print("Setting Up test databse")
    global engine
    # engine = create_engine(f"{settings.test_database_string}", echo = True)
    engine = create_engine(TEST_POSTGRESS_SQL_DATABASE_URL)

def get_override_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
    
def create_database_and_tables():
    SQLModel.metadata.create_all(bind=engine)
    print("database Created")
    print("database Created at :", engine.url)
    return "Database Connected"

def close_connection():
    print("Database Closed")
    engine.dispose()
    return "Database Disconnected"

def drop_database_and_tables():
    print("Database Dropped")
    SQLModel.metadata.drop_all(engine)
    return "Database Droped"

def get_session() -> Session: # type: ignore
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
