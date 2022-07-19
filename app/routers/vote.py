from fastapi import APIRouter, FastAPI ,status , Response,HTTPException ,Depends
from .. import schemas, ouath2,database,models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes" ,
    tags=['votes']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote,db: Session = Depends(database.get_db),current_user : int  = Depends(ouath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == models.Vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} is not present")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).filter(models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} is already voted on the post{vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote is deleted"}


