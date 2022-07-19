from fastapi import APIRouter, FastAPI ,status , Response,HTTPException ,Depends
from .. import models,schemas,ouath2
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts" ,
    tags=['posts']
)

@router.get("/",response_model=List[schemas.PostResponce])
def get_post(db: Session = Depends(get_db)):
#    cursor.execute(""" SELECT * FROM posts """)
#    posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/",  status_code = status.HTTP_201_CREATED,response_model=schemas.PostResponce)
def createpost(post : schemas.PostCreate,db: Session = Depends(get_db),user_id : int  = Depends(ouath2.get_current_user) ):
  #  cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """ , (post.title,post.content,post.published))
  #  new_post = cursor.fetchall()
  #  conn.commit()
    post.dict()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#@router.get("/posts/latest")
#def getlatest():
#    post = my_posts[len(my_posts)-1]
#    return post

@router.get("/{id}")
def get_post(id: int,db: Session = Depends(get_db) ):
 #   cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
 #   singlepost = cursor.fetchone()
    singlepost = db.query(models.Post).filter(models.Post.id == id).first()
    if not singlepost:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with the is { id } is not found")
    return {"post you wanted": singlepost}

@router.delete("/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):
#    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id))
#    deleted_post = cursor.fetchone()
#    conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with this {id} is not found")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id : int, post : schemas.PostCreate ,db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RetURNING * """, (post.title,post.content,post.published,(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with this {id} is not found")
    
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()