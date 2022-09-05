from operator import ne
from pyexpat import model
from turtle import title
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext import declarative_base
from app import models
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db ,Base
from app.ouath2 import create_token
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





#client = TestClient(app)
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
  

@pytest.fixture
def test_user(client):
    user_data = {"email":"suseendarannair@gmail.com",
                "password":"password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 200
   # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_token({"user_id": test_user['id']})
    

@pytest.fixture
def authorize_client(client,token,test_user):
    client.headers = {
        **client.headers,
        "Authorizaton": f"Bearer {token}"
    }
    print (test_user['id'])
    return client



# @pytest.fixture
# def test_posts(test_user,session):
#     post_data = [{ "title":"first title",
#                     "content": "first_comment",
#                     "onwer_id": test_user['id'] }]
                     
# #                   {"title":"2nd title",
# #                   "content":"2nd content",
# #                   "owner_id":test_user['id']
# #                   },
# #                   {"title":"3rd title",}
# #                   "content":"3rd content",
# #                   "owner_id":test_user['id']
#     session.add_all([models.Post(title="firsttitle",content="first_content",owner_id=test_user["id"])])   
#     session.commit() 
#     posts = session.query(models.post).all()
#     return posts