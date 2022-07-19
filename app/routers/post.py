from unittest import skip
from fastapi import APIRouter, FastAPI ,status , Response,HTTPException ,Depends
from .. import models,schemas,ouath2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts" ,
    tags=['posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),current_user : int  = Depends(ouath2.get_current_user),
limit: int = 3,skip: int =0,search: Optional[str] = ""):
#    cursor.execute(""" SELECT * FROM posts """)
#    posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print (post_query)

    return post_query

@router.post("/",  status_code = status.HTTP_201_CREATED,response_model=schemas.PostResponce)
def createpost(post : schemas.PostCreate,db: Session = Depends(get_db),current_user : int  = Depends(ouath2.get_current_user) ):
  #  cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """ , (post.title,post.content,post.published))
  #  new_post = cursor.fetchall()
  #  conn.commit()
    print (current_user.email)
    post.dict()
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get("/posts/latest")
#def getlatest():
#    post = my_posts[len(my_posts)-1]
#    return post

@router.get("/{id}")
def get_post(id: int,db: Session = Depends(get_db),current_user : int  = Depends(ouath2.get_current_user),
limit: int = 3 ):
 #   cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
 #   singlepost = cursor.fetchone()
    #singlepost = db.query(models.Post).filter(models.Post.id == id).first()
    singlepost = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not singlepost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with the is { id } is not found")
    return {"post you wanted": singlepost}

@router.delete("/{id}")
def delete_post(id: int,db: Session = Depends(get_db),current_user : int  = Depends(ouath2.get_current_user)):
#    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id))
#    deleted_post = cursor.fetchone()
#    conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #print(post)
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with this {id} is not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"user is not accessible to delete the post")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id : int, post : schemas.PostCreate ,db: Session = Depends(get_db),user_id : int  = Depends(ouath2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RetURNING * """, (post.title,post.content,post.published,(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with this {id} is not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"user is not accessible to update the post")
    
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()