import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.model import UserIn
from app.database import create_database_and_tables, drop_database_and_tables, get_session, close_connection, get_override_session, set_test_database
from app.oauth2 import create_jwt_token

@pytest.fixture(scope="module")
def session():
    set_test_database()
    drop_database_and_tables()
    create_database_and_tables()
    try:
        yield get_override_session()
    finally:
        close_connection()

@pytest.fixture(scope="module")
def client(session):
    app.dependency_overrides[get_session] = get_override_session
    yield TestClient(app)

@pytest.fixture(scope="module")
def create_user(client):
    user_data = UserIn(email="user@gmail.com", password="user")
    response = client.post("/users/", json=user_data.model_dump())
    assert response.status_code == 201,  f"Failed to create user: {response.json()}"    
    
@pytest.fixture(scope="module")
def create_valid_login_token():
        token = create_jwt_token(data={"email":"user1@yahoo.com", "userid": 2})
        return token
    



