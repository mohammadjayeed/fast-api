from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model= schemas.UserCreateResponse )
def create_users(users: schemas.UserCreate, db: Session = Depends(get_db)):

    users.password = utils.hash(users.password)
    new_user = models.User(**users.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model= schemas.UserCreateResponse )
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    

    return user