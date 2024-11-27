from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils

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
        return {"message":"logged in"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={'message':'please check your credentials'},)