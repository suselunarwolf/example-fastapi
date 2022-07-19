import email
from lib2to3.pgen2 import token
from fastapi import APIRouter,Depends,status,Response,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas,models,utils,ouath2 
from sqlalchemy.orm import Session

router = APIRouter(tags=['login'])

@router.post("/userlogin",response_model=schemas.Token)
def User_log(userlog : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.email == userlog.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid creds")
    if not utils.verify(userlog.password,user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid creds")
    
    jtoken = ouath2.create_token(data = {"user_id": user.id})

    return {"access_token": jtoken,"token_type": "bearer"}
    