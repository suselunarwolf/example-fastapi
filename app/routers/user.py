from fastapi import FastAPI ,status , Response,HTTPException ,Depends , APIRouter
from .. import models,schemas,utils
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",response_model=schemas.Userout)
def usercreate(user : schemas.UserCreation,db: Session = Depends(get_db)):
  #  cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """ , (post.title,post.content,post.published))
  #  new_post = cursor.fetchall()
  #  conn.commit()
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.Userout)
def get_user(id: int,db: Session = Depends(get_db)):

    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with the is { id } is not found")

    return users
    