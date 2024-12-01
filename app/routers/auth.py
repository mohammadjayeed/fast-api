from fastapi import HTTPException, status, APIRouter, Depends, Query
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils
from ..oauth2 import create_access_token
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer




router = APIRouter(

    tags=['authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):


    #   { "username":  , "password": }   OAuth2PasswordRequestForm takes anything email/username 
    # and stores in field called username


    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={'message':'please check your credentials'},)
    

    is_valid = utils.verify(user_credentials.password, user.password)

    if not is_valid:
        
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={'message':'please check your credentials'},)

    token = create_access_token({"email_addr": user.email, "user_id":user.id})
    
    return {"access_token": token, "token_type": "bearer"}

# @router.post('/verify', status_code=status.HTTP_200_OK )
# def verify_me(token: Annotated[str, Depends(oauth2_scheme)]):
#     print('here')
#     verify_token(token)