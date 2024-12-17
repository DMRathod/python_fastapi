from sqlmodel import create_engine, SQLModel, Session

POSTGRESS_SQL_DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

# add echo = true if you like to log create query
engine = create_engine(POSTGRESS_SQL_DATABASE_URL)


def create_database_and_tables():
    SQLModel.metadata.create_all(engine)
    return "Database Connected"

def drop_database_and_tables():
    SQLModel.metadata.drop_all(engine)
    return "Database Disconnected"

def get_session() -> Session: # type: ignore
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

