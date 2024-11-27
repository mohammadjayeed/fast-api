from fastapi import HTTPException, status, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils
from .oauth import create_access_token, verify_token
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(

    tags=['authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK )
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={'message':'please check your credentials'},)
    

    is_valid = utils.verify(user_credentials.password, user.password)

    if is_valid:
        token = create_access_token({"email": user.email, "id":user.id})
        print(token)
        return {"message":"logged in"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={'message':'please check your credentials'},)

@router.post('/verify', status_code=status.HTTP_200_OK )
def verify_me(token: Annotated[str, Depends(oauth2_scheme)]):
    print('here')
    verify_token(token)