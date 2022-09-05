from urllib import response
import pytest
from jose import jwt
from app import schemas
from app.config import settings


 

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello Suseendar!!!, welcome back'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/",json ={"email":"hello@gmail.com","password":"password123"})
    new_user = schemas.Userout(**res.json())
    assert new_user.id ==  1
    assert res.status_code == 200 

def test_login_user(client,test_user):
    res = client.post(
        "/userlogin",data={"username":test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    # print(res.json())
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[
('wrong@email.com','password123',403),
('wrong@email.com','wrongpassword',403),
(None,'password123',422),
('suseendar@gmail.com',None,422)])

def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post("/userlogin",data={"username":email,"password":password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'invalid creds'