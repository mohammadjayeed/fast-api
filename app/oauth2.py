import jwt
from jwt import InvalidTokenError
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import models

load_dotenv(override=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    
    # datetime.now(timezone.utc) including timezone.utc, we avoid ambiguity and potential errors
    # when working with time-sensitive applications
    expire = datetime.now(timezone.utc) + timedelta(minutes=20)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def verify_access_token(token: str , credentials_exception):
    

    try:
        
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get('email_addr')
        id: int = payload.get('user_id')
        

        if email is None or id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email, id=id)
    except InvalidTokenError as e:
        raise credentials_exception
    
    
    return token_data.id
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Crendentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id==token).first()

    return user

    
