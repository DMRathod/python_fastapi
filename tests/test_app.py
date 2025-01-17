from app.model import UserOut, UserIn, Token, UPostCreate, UPostOut, Vote, UPostswithCount

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to FastAPI, My First Web APP"}

def test_login_user(client, create_user):
    response = client.post("/auth/login", data={"username": "user@gmail.com", "password": "user"}) 
    login_response = Token(**response.json())
    assert response.status_code == 200,  f"Login Failed: {response.json()}"

def test_create_user(client):
    response = client.post("/users/",json=UserIn(email="user1@yahoo.com", password="user1").model_dump())
    UserOut(**response.json())
    assert response.status_code == 201

def test_get_user_by_id(client):
    response = client.get("/users/by-id/1")
    user = UserOut(**response.json())
    assert user.userid == 1
    assert user.email == "user@gmail.com"

def test_get_user_not_exist_by_id(client):
    response = client.get("/users/by-id/9999999999")
    assert response.status_code == 404

def test_get_user_by_email(client):
    response = client.get("/users/by-email/user@gmail.com")
    user = UserOut(**response.json())
    assert user.userid == 1
    assert user.email == "user@gmail.com"

def test_get_user_not_exist_by_email(client):
    response = client.get("/users/by-email/user546745@gmail.com")
    assert response.status_code == 404

def test_create_duplicate_user(client):
    response = client.post("/users/", json=UserIn(email="user@gmail.com", password="test1").model_dump())
    assert response.json() == {'detail': 'Validation Error 406: Failed to Create User : Validation'}
    assert response.status_code == 400

def test_update_user(client):
    response = client.put("/users/1",json=UserIn(email="updateduser@yahoo.com", password="updateduser").model_dump())
    UserOut(**response.json())
    assert response.status_code == 200

def test_update_non_existing_user(client):
    response = client.put("/users/9999999999",json=UserIn(email="updateduser@yahoo.com", password="updateduser").model_dump())
    assert response.status_code == 404

def test_delete_user(client):
    response = client.delete("/users/1")
    UserOut(**response.json())
    assert response.status_code == 200

def test_delete_non_existing_user(client):
    response = client.delete("/users/9999999999")
    assert response.status_code == 404

def test_list_of_users(client):
    client.post("/users/",json=UserIn(email="test100@yahoo.com", password="test").model_dump())
    client.post("/users/",json=UserIn(email="test101@yahoo.com", password="test").model_dump())
    client.post("/users/",json=UserIn(email="test102@yahoo.com", password="test").model_dump())
    client.post("/users/",json=UserIn(email="test103@yahoo.com", password="test").model_dump())
    response = client.get("/users/")
    users = [UserOut(**userdata) for userdata in response.json()]
    assert len(users) == 5

def test_create_post(client, create_valid_login_token):
    response = client.post("/uposts/", json=UPostCreate(title="my test post 1", content="my test content 1").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    UPostOut(**response.json())
    assert response.status_code == 201

def test_get_post(client, create_valid_login_token):
    response = client.get("/uposts/1",  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    UPostOut(**response.json())
    assert response.status_code == 200

def test_get_non_existing_post(client, create_valid_login_token):
    response = client.get("/uposts/9999999999",  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    assert response.status_code == 404    

def test_update_post(client, create_valid_login_token):
    response = client.put("/uposts/1", json=UPostCreate(title="my test updated post 1", content="my test udpated content 1").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    UPostOut(**response.json())
    assert response.status_code == 200

def test_update_non_existing_post(client, create_valid_login_token):
    response = client.put("/uposts/9999999999", json=UPostCreate(title="my test updated post 1", content="my test udpated content 1").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    assert response.status_code == 404

def test_delete_post(client, create_valid_login_token):
    response = client.delete("/uposts/1", headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    assert response.status_code == 200

def test_delete_non_existing_post(client, create_valid_login_token):
    response = client.delete("/uposts/9999999999", headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    assert response.status_code == 404

def test_list_of_posts(client, create_valid_login_token):
    response = client.post("/uposts/", json=UPostCreate(title="my test post 1", content="my test content 1").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    response = client.post("/uposts/", json=UPostCreate(title="my test post 2", content="my test content 2").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    response = client.post("/uposts/", json=UPostCreate(title="my test post 3", content="my test content 3").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    response = client.post("/uposts/", json=UPostCreate(title="my test post 4", content="my test content 4").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    response = client.post("/uposts/", json=UPostCreate(title="my test post 5", content="my test content 5").model_dump(),  headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    response = client.get("/uposts/",  headers={"Authorization": f"Bearer {create_valid_login_token}"})
    post_response = response.json()
    posts = [UPostOut(**post) for post in post_response]
    assert len(posts) == 5

def test_upvote(client, create_valid_login_token):
    response = client.post("/vote/", json= Vote(post_id=5, dir="UPVOTE").model_dump(), headers={"Authorization": f"Bearer {create_valid_login_token}"})
    assert response.json() == {"Message":"Added Vote"}
    assert response.status_code == 201

def test_upvote_already_provided(client, create_valid_login_token):
    response = client.post("/vote/", json= Vote(post_id=5, dir="UPVOTE").model_dump(), headers={"Authorization": f"Bearer {create_valid_login_token}"})
    assert response.json() == {'detail': 'User 2 has Already voted on Post with id 5'}
    assert response.status_code == 409

def test_downvote(client, create_valid_login_token):
    response = client.post("/vote/", json= Vote(post_id=5, dir="DOWNVOTE").model_dump(), headers={"Authorization": f"Bearer {create_valid_login_token}"})
    assert response.json() == {"Message":"Deleted Vote"}
    assert response.status_code == 201

def test_downvote_with_no_upvote(client, create_valid_login_token):
    response = client.post("/vote/", json= Vote(post_id=4, dir="DOWNVOTE").model_dump(), headers={"Authorization": f"Bearer {create_valid_login_token}"})
    assert response.json() == {'detail': 'User 2 has not voted on Post with id 4'}
    assert response.status_code == 404

def test_list_of_posts_with_count(client, create_valid_login_token):
    response = client.get("/uposts/count", headers={"Authorization": f"Bearer {create_valid_login_token}"} )
    posts = [UPostswithCount(**post) for post in response.json()]
    assert len(posts) == 5





