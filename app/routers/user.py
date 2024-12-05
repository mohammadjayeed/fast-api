from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import utils

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.UserCreateResponse )
def create_users(users: schemas.UserCreate, db: Session = Depends(get_db)):

    users.password = utils.hash(users.password)
    new_user = models.User(**users.model_dump())

    if not db.query(models.User).filter(models.User.email==new_user.email).first():

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail={'message':f'user with email {new_user.email} already exists'},)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model= schemas.UserCreateResponse )
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f'id {id} not found'},)
    

    return user