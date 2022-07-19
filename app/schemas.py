import string
from tokenize import String
from typing import Optional
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  

class PostCreate(PostBase):
    pass



class UserCreation(BaseModel): 
    email: EmailStr
    password: str


class Userout(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponce(PostBase):    
    id: int
    created_at: datetime
    owner_id: int
    owner: Userout

    class Config:
        orm_mode = True    

class PostOut(BaseModel):
    Post: PostResponce
    votes: int

    class Config:
        orm_mode = True 



class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True   

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)
